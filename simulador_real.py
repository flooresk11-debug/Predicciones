#!/usr/bin/env python3
"""
Simulador con datos 100% reales y descargados automáticamente (football-data.co.uk).

Qué hace, sin que nadie escriba un solo dato a mano:
  1. Descarga la temporada actual (2026/27) y la anterior de la liga indicada: resultados, tiros, tiros a
     puerta, corners, tarjetas y árbitro de cada partido jugado.
  2. Calcula para cada equipo su fuerza en casa y fuera en cada estadística (a favor y en contra),
     relativa a la media de la liga, con encogimiento hacia la temporada anterior cuando hay pocos partidos.
  3. Ancla los goles al mercado (cuotas medias sin margen de los próximos partidos), porque el backtest
     demostró que el mercado está mejor calibrado que cualquier modelo propio.
  4. Usa la dispersión REAL de cada estadística (medida en la liga) con una binomial negativa, no una Poisson.
  5. Simula el partido y da probabilidad y cuota justa de: 1X2, goles, ambos marcan, tiros a puerta,
     corners y tarjetas (por equipo y totales), y compara con bet365 cuando hay cuota.
  6. --validar: aplica el mismo método a la temporada pasada partido a partido (sin mirar el futuro) y mide
     si sus probabilidades se cumplen. Así sabemos en qué mercados el simulador es fiable y en cuáles no.

Uso:
  python3 simulador_real.py --liga E0 --local "Crystal Palace" --visitante "Liverpool"
  python3 simulador_real.py --liga SP1 --validar
Ligas: E0 Premier, SP1 LaLiga, D1 Bundesliga, D2 2.Bundesliga, I1 Serie A, N1 Eredivisie, F1 Ligue 1
"""
import argparse
import csv
import io
import math
import os
import random
import time
import urllib.request
from collections import defaultdict

BASE = "https://www.football-data.co.uk/mmz4281/{temp}/{liga}.csv"
FIXTURES = "https://www.football-data.co.uk/fixtures.csv"
ACTUAL, ANTERIOR = "2627", "2526"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "historico")
# estadística: (columna local, columna visitante)
STATS = {"goles": ("FTHG", "FTAG"), "tiros": ("HS", "AS"), "tiros_puerta": ("HST", "AST"),
         "corners": ("HC", "AC"), "amarillas": ("HY", "AY")}
K_PREVIO = 6          # partidos "virtuales" de la temporada anterior al encoger (por defecto)
PESO_MERCADO = 1.0    # goles: el backtest mostró que el mercado está mejor calibrado que las estadísticas
_RUTA_PARAM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parametros_calibrados.json")
try:
    import json as _json
    PARAM = _json.load(open(_RUTA_PARAM, encoding="utf-8"))   # generado por calibrar.py con datos reales
except (OSError, ValueError):
    PARAM = {}


def param(s):
    p = PARAM.get(s, {})
    return p.get("K", K_PREVIO), p.get("alfa", 1.0), p.get("delta", 1.0)


def descargar(url, ruta=None, max_horas=6):
    if ruta and os.path.exists(ruta) and time.time() - os.path.getmtime(ruta) < max_horas * 3600:
        return open(ruta, encoding="utf-8-sig", errors="ignore").read()
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "predicciones-analisis/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode("utf-8-sig", errors="ignore")
            if ruta:
                os.makedirs(os.path.dirname(ruta), exist_ok=True)
                open(ruta, "w", encoding="utf-8").write(txt)
            return txt
        except OSError:
            time.sleep(2 ** (i + 1))
    if ruta and os.path.exists(ruta):
        return open(ruta, encoding="utf-8-sig", errors="ignore").read()
    raise SystemExit(f"No se pudo descargar {url}")


def cargar(liga, temp, max_horas=6):
    txt = descargar(BASE.format(temp=temp, liga=liga), os.path.join(CACHE, f"{liga}_{temp}.csv"), max_horas)
    filas = []
    for r in csv.DictReader(io.StringIO(txt)):
        try:
            if r.get("FTHG") == "" or r.get("FTHG") is None:
                continue
            fila = {"h": r["HomeTeam"], "a": r["AwayTeam"], "fecha": r["Date"], "arbitro": r.get("Referee", ""),
                    "row": r}
            for s, (ch, ca) in STATS.items():
                fila[s] = (float(r[ch]), float(r[ca])) if r.get(ch) not in (None, "") and r.get(ca) not in (None, "") else None
            filas.append(fila)
        except (ValueError, KeyError):
            continue
    return filas


# ---------------------------------------------------------------- distribuciones
def nb_pmf(k, media, disp):
    """Binomial negativa con varianza = media * disp (disp >= 1). disp=1 -> Poisson."""
    if media <= 0:
        return 1.0 if k == 0 else 0.0
    if disp <= 1.0001:
        return math.exp(-media + k * math.log(media) - math.lgamma(k + 1))
    r = media / (disp - 1)
    p = r / (r + media)
    return math.exp(math.lgamma(k + r) - math.lgamma(r) - math.lgamma(k + 1) + r * math.log(p) + k * math.log(1 - p))


def prob_mas_de(linea, media, disp):
    return 1 - sum(nb_pmf(k, media, disp) for k in range(int(math.floor(linea)) + 1))


def nb_muestra(rnd, media, disp):
    if disp <= 1.0001:
        lam = media
    else:
        r = media / (disp - 1)
        lam = rnd.gammavariate(r, media / r)
    L, k, p = math.exp(-lam), 0, 1.0
    if lam > 30:
        return max(0, int(round(rnd.gauss(lam, math.sqrt(lam)))))
    while True:
        p *= rnd.random()
        if p <= L:
            return k
        k += 1


# ---------------------------------------------------------------- modelo de fuerzas
class Liga:
    def __init__(self, actual, anterior):
        self.medias, self.disp = {}, {}
        self.eq = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))     # (equipo, clave) -> [suma, n]
        self.prev = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))
        self.arbitros = defaultdict(lambda: [0.0, 0])
        for s in STATS:
            vals = [(f[s][0], f[s][1]) for f in actual + anterior if f[s]]
            if vals:
                mh = sum(v[0] for v in vals) / len(vals)
                ma = sum(v[1] for v in vals) / len(vals)
                self.medias[s] = (mh, ma)
                # dispersión real por equipo-partido (varianza/media), mínimo 1
                var_h = sum((v[0] - mh) ** 2 for v in vals) / len(vals)
                var_a = sum((v[1] - ma) ** 2 for v in vals) / len(vals)
                self.disp[s] = max(1.0, ((var_h / mh if mh else 1) + (var_a / ma if ma else 1)) / 2)
        for fs, dest in ((actual, self.eq), (anterior, self.prev)):
            for f in fs:
                self.sumar(f, dest)
        for f in actual + anterior:
            if f["arbitro"] and f["amarillas"]:
                a = self.arbitros[f["arbitro"]]
                a[0] += sum(f["amarillas"]); a[1] += 1

    def sumar(self, f, dest):
        for s in STATS:
            if not f[s] or s not in self.medias:
                continue
            mh, ma = self.medias[s]
            hv, av = f[s]
            for clave, v, ref in (((f["h"], f"{s}_favor_L"), hv, mh), ((f["h"], f"{s}_contra_L"), av, ma),
                                  ((f["a"], f"{s}_favor_V"), av, ma), ((f["a"], f"{s}_contra_V"), hv, mh)):
                if ref > 0:
                    x = dest[clave[0]][clave[1]]
                    x[0] += v / ref; x[1] += 1

    def factor(self, equipo, clave, K=None):
        K = K_PREVIO if K is None else K
        s, n = self.eq[equipo][clave]
        sp, np_ = self.prev[equipo][clave]
        previo = sp / np_ if np_ else 1.0   # sin temporada anterior (ascendido): media de liga
        return (s + K * previo) / (n + K), n

    def esperado(self, s, local, visit, calibrado=True):
        K, alfa, _ = param(s) if calibrado else (K_PREVIO, 1.0, 1.0)
        mh, ma = self.medias[s]
        fl, nl = self.factor(local, f"{s}_favor_L", K)
        cv, _ = self.factor(visit, f"{s}_contra_V", K)
        fv, nv = self.factor(visit, f"{s}_favor_V", K)
        cl, _ = self.factor(local, f"{s}_contra_L", K)
        return mh * (fl * cv) ** alfa, ma * (fv * cl) ** alfa, nl, nv

    def dispersion(self, s, calibrado=True):
        if s == "goles":
            return 1.0
        _, _, delta = param(s) if calibrado else (0, 0, 1.0)
        return 1 + delta * (self.disp[s] - 1)

    def factor_arbitro(self, nombre):
        if not nombre or nombre not in self.arbitros or "amarillas" not in self.medias:
            return 1.0, 0
        s, n = self.arbitros[nombre]
        media = sum(self.medias["amarillas"])
        return ((s / n) * n + K_PREVIO * media) / (n + K_PREVIO) / media, n


def goles_de_mercado(p1, px, p2, pover):
    mejor = None
    for a in range(10, 351, 5):
        for b in range(10, 351, 5):
            lh, la = a / 100, b / 100
            r = probs_goles(lh, la)
            e = (r["1"] - p1) ** 2 + (r["X"] - px) ** 2 + (r["2"] - p2) ** 2
            if pover is not None:
                e += (r["over25"] - pover) ** 2
            if mejor is None or e < mejor[0]:
                mejor = (e, lh, la)
    return mejor[1], mejor[2]


def probs_goles(lh, la, n=10):
    ph = [nb_pmf(i, lh, 1) for i in range(n)]
    pa = [nb_pmf(j, la, 1) for j in range(n)]
    r = defaultdict(float)
    for i in range(n):
        for j in range(n):
            p = ph[i] * pa[j]
            r["1" if i > j else "X" if i == j else "2"] += p
            r["over15"] += p * (i + j >= 2); r["over25"] += p * (i + j >= 3); r["over35"] += p * (i + j >= 4)
            r["btts"] += p * (i > 0 and j > 0); r["local_marca"] += p * (i > 0); r["visit_marca"] += p * (j > 0)
            r["local_2+"] += p * (i - j >= 2); r["visit_2+"] += p * (j - i >= 2)
    return r


def cuotas_mercado(local, visit):
    txt = descargar(FIXTURES, os.path.join(CACHE, "fixtures.csv"), max_horas=3)
    for r in csv.DictReader(io.StringIO(txt)):
        if r["HomeTeam"] == local and r["AwayTeam"] == visit:
            return r
    return None


def sin_margen(*c):
    try:
        inv = [1 / float(x) for x in c]
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    return [x / sum(inv) for x in inv]


def buscar_equipo(nombre, equipos):
    if nombre in equipos:
        return nombre
    cand = [e for e in equipos if nombre.lower() in e.lower() or e.lower() in nombre.lower()]
    if len(cand) == 1:
        return cand[0]
    raise SystemExit(f"Equipo '{nombre}' no encontrado o ambiguo. Equipos: {', '.join(sorted(equipos))}")


# ---------------------------------------------------------------- informe de un partido
def analizar(liga_cod, local, visit, arbitro, sims):
    act, ant = cargar(liga_cod, ACTUAL), cargar(liga_cod, ANTERIOR)
    equipos = {f["h"] for f in act} | {f["a"] for f in act}
    local, visit = buscar_equipo(local, equipos), buscar_equipo(visit, equipos)
    L = Liga(act, ant)
    print(f"# {local} vs {visit} ({liga_cod}) — datos oficiales football-data.co.uk")
    print(f"Temporada 2026/27: {len(act)} partidos jugados en la liga (último {act[-1]['fecha']}); "
          f"temporada 2025/26 usada como base: {len(ant)} partidos.\n")

    # forma real
    for eq in (local, visit):
        ps = [f for f in act if eq in (f["h"], f["a"])]
        g = e = p = gf = gc = 0
        for f in ps:
            a, b = (f["goles"][0], f["goles"][1]) if f["h"] == eq else (f["goles"][1], f["goles"][0])
            gf += a; gc += b
            g += a > b; e += a == b; p += a < b
        ult = " ".join(("G" if (f["goles"][0] > f["goles"][1]) == (f["h"] == eq) and f["goles"][0] != f["goles"][1]
                        else "E" if f["goles"][0] == f["goles"][1] else "P") for f in ps[-5:])
        print(f"{eq}: {len(ps)} PJ {g}G {e}E {p}P, goles {gf:.0f}:{gc:.0f} | últimos 5 (antiguo->reciente): {ult}")

    # valores esperados por estadística
    esp = {}
    print("\n## Valores esperados (fuerza del equipo x debilidad del rival, condición local/visitante)")
    print(f"{'estadística':14} {local[:16]:>16} {visit[:16]:>16} {'total':>7} {'fiabilidad (prueba real)':>26}")
    for s in STATS:
        if s not in L.medias:
            continue
        h, a, nl, nv = L.esperado(s, local, visit)
        esp[s] = [h, a]
        sk = PARAM.get(s, {}).get("skill_prueba")
        fiab = "sin calibrar" if sk is None else (f"{sk:+.1%} vs media liga" + (" (usar mercado)" if s == "goles" else ""))
        print(f"{s:14} {h:16.2f} {a:16.2f} {h + a:7.2f} {fiab:>26}")
    fa, na = L.factor_arbitro(arbitro)
    if arbitro:
        print(f"\nÁrbitro {arbitro}: {na} partidos en los datos; factor de tarjetas {fa:.2f} (1.00 = media de la liga)"
              if na else f"\nÁrbitro {arbitro}: sin partidos en los datos (o la liga no publica árbitro); factor 1.00")
        esp["amarillas"] = [x * fa for x in esp["amarillas"]]

    # anclaje al mercado
    m = cuotas_mercado(local, visit)
    gh, ga = esp["goles"]
    if m:
        p12 = sin_margen(m.get("AvgH"), m.get("AvgD"), m.get("AvgA"))
        pou = sin_margen(m.get("Avg>2.5"), m.get("Avg<2.5"))
        if p12:
            mh, ma = goles_de_mercado(*p12, pou[0] if pou else None)
            print(f"\nMercado (cuotas medias sin margen): 1 {p12[0]:.1%} X {p12[1]:.1%} 2 {p12[2]:.1%}"
                  + (f" | +2.5 {pou[0]:.1%}" if pou else "") + f" -> goles {mh:.2f}-{ma:.2f}")
            print(f"Estadísticas de la temporada -> goles {gh:.2f}-{ga:.2f}. Mezcla {PESO_MERCADO:.0%} mercado.")
            gh, ga = PESO_MERCADO * mh + (1 - PESO_MERCADO) * gh, PESO_MERCADO * ma + (1 - PESO_MERCADO) * ga
    else:
        print("\nSin cuotas de mercado para este partido: goles solo con estadísticas (más incertidumbre).")
    esp["goles"] = [gh, ga]

    # simulación
    rnd = random.Random(2026)
    cont = defaultdict(int)
    lineas = {"tiros_puerta": [6.5, 7.5, 8.5, 9.5, 10.5], "corners": [7.5, 8.5, 9.5, 10.5, 11.5],
              "amarillas": [2.5, 3.5, 4.5, 5.5], "tiros": [20.5, 22.5, 24.5, 26.5]}
    lineas_eq = {"tiros_puerta": [2.5, 3.5, 4.5, 5.5], "corners": [3.5, 4.5, 5.5, 6.5], "amarillas": [0.5, 1.5, 2.5]}
    for _ in range(sims):
        vals = {}
        for s, (h, a) in esp.items():
            d = L.dispersion(s)
            vals[s] = (nb_muestra(rnd, h, d), nb_muestra(rnd, a, d))
        gl, gv = vals["goles"]
        cont["1"] += gl > gv; cont["X"] += gl == gv; cont["2"] += gl < gv
        cont["over15"] += gl + gv >= 2; cont["over25"] += gl + gv >= 3; cont["over35"] += gl + gv >= 4
        cont["btts"] += gl > 0 and gv > 0
        for s, ls in lineas.items():
            if s in vals:
                for x in ls:
                    cont[(s, "T", x)] += sum(vals[s]) > x
        for s, ls in lineas_eq.items():
            if s in vals:
                for x in ls:
                    cont[(s, "L", x)] += vals[s][0] > x
                    cont[(s, "V", x)] += vals[s][1] > x
    P = {k: v / sims for k, v in cont.items()}

    def fila(nombre, p, cuota_b365=None):
        extra = ""
        if cuota_b365:
            extra = f" | bet365 {float(cuota_b365):.2f} -> ventaja {p * float(cuota_b365) - 1:+.1%}"
        riesgo = "BAJO" if p >= 0.75 else "MEDIO" if p >= 0.5 else "ALTO"
        print(f"  {nombre:34} {p:6.1%}  justa {1 / p if p else 0:6.2f}  [{riesgo}]{extra}")

    print(f"\n## Simulación ({sims:,} partidos, semilla fija)")
    print("Goles esperados finales:", f"{gh:.2f} - {ga:.2f}")
    b = m or {}
    fila(f"Gana {local}", P["1"], b.get("B365H")); fila("Empate", P["X"], b.get("B365D"))
    fila(f"Gana {visit}", P["2"], b.get("B365A"))
    fila(f"{local} o empate", P["1"] + P["X"]); fila(f"{visit} o empate", P["2"] + P["X"])
    fila("Más de 1.5 goles", P["over15"]); fila("Más de 2.5 goles", P["over25"], b.get("B365>2.5"))
    fila("Menos de 2.5 goles", 1 - P["over25"], b.get("B365<2.5")); fila("Menos de 3.5 goles", 1 - P["over35"])
    fila("Ambos marcan: sí", P["btts"]); fila("Ambos marcan: no", 1 - P["btts"])
    nombres = {"tiros_puerta": "tiros a puerta", "corners": "corners", "amarillas": "amarillas", "tiros": "tiros"}
    for s in ("tiros_puerta", "corners", "amarillas", "tiros"):
        if s not in esp:
            continue
        print(f"\n  -- {nombres[s]}: esperados {esp[s][0]:.1f} + {esp[s][1]:.1f} = {sum(esp[s]):.1f} --")
        for x in lineas.get(s, []):
            fila(f"Total más de {x}", P[(s, "T", x)])
        for x in lineas_eq.get(s, []):
            fila(f"{local[:14]} más de {x}", P[(s, "L", x)])
            fila(f"{visit[:14]} más de {x}", P[(s, "V", x)])
    print("\nCuota justa = la mínima que debe pagar bet365 para no perder dinero a la larga.")


# ---------------------------------------------------------------- validación sobre la temporada pasada
def validar(liga_cod):
    """Recorre 2025/26 partido a partido usando solo datos previos (2024/25 como base) y mide calibración."""
    temporadas = {"2526": "2425", "2627": "2526"}
    resultados = defaultdict(lambda: [0, 0.0, 0.0, 0.0])   # mercado -> [n, suma prob, aciertos, brier]
    cubos = defaultdict(lambda: [0, 0.0, 0])
    for temp, prev in temporadas.items():
        act, ant = cargar(liga_cod, temp, max_horas=24 * 30 if temp != ACTUAL else 6), cargar(liga_cod, prev, max_horas=24 * 30)
        for i, f in enumerate(act):
            jug = act[:i]
            nh = sum(1 for x in jug if f["h"] in (x["h"], x["a"]))
            na = sum(1 for x in jug if f["a"] in (x["h"], x["a"]))
            if nh < 5 or na < 5:
                continue
            L = Liga(jug, ant)
            for s, linea in (("corners", 9.5), ("amarillas", 3.5), ("tiros_puerta", 8.5), ("goles", 2.5)):
                if not f[s] or s not in L.medias:
                    continue
                h, a, _, _ = L.esperado(s, f["h"], f["a"])
                d = L.dispersion(s)
                p = prob_mas_de(linea, h + a, d)
                real = sum(f[s]) > linea
                x = resultados[(s, linea)]
                x[0] += 1; x[1] += p; x[2] += real; x[3] += (p - real) ** 2
                for pp, rr in ((p, real), (1 - p, not real)):
                    if pp >= 0.6:
                        c = cubos[(s, "60-70%" if pp < 0.7 else "70-80%" if pp < 0.8 else "80%+")]
                        c[0] += 1; c[1] += pp; c[2] += rr
    print(f"# Validación del simulador en {liga_cod} (temporadas 2025/26 y 2026/27, solo datos previos a cada partido)\n")
    print(f"{'mercado':26} {'partidos':>8} {'prob. media':>11} {'real':>7} {'Brier':>7} {'Brier base':>10}")
    for (s, linea), (n, sp, ac, br) in resultados.items():
        base = ac / n
        brier_base = base * (1 - base)
        print(f"{s + ' más de ' + str(linea):26} {n:8d} {sp / n:11.1%} {ac / n:7.1%} {br / n:7.4f} {brier_base:10.4f}")
    print("\nBrier base = acertar siempre la frecuencia media. Si el simulador no lo mejora, no aporta en ese mercado.\n")
    print(f"{'mercado / tramo':30} {'picks':>6} {'prometido':>10} {'real':>7}")
    for (s, t), (n, sp, ac) in sorted(cubos.items()):
        print(f"{s + ' ' + t:30} {n:6d} {sp / n:10.1%} {ac / n:7.1%}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--liga", required=True)
    ap.add_argument("--local")
    ap.add_argument("--visitante")
    ap.add_argument("--arbitro", default="")
    ap.add_argument("--sims", type=int, default=100_000)
    ap.add_argument("--validar", action="store_true")
    a = ap.parse_args()
    if a.validar:
        validar(a.liga)
    else:
        analizar(a.liga, a.local, a.visitante, a.arbitro, a.sims)


if __name__ == "__main__":
    main()
