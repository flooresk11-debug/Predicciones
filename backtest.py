#!/usr/bin/env python3
"""
Backtest con datos reales (football-data.co.uk) del método de predicción.

Para cada partido usa SOLO los partidos anteriores de esa temporada (sin mirar el futuro) y compara:
  v1       modelo puro (como el simulador original): promedios del equipo, sin anclaje
  v1+enc   v1 con encogimiento hacia la media de la liga (corrige muestras pequeñas)
  v2       v1+enc con el 1X2 mezclado 60% con el mercado (cuotas de apertura sin margen)
  mercado  solo cuotas de apertura sin margen (referencia)

Mide:
  * Calibración (Brier) y aciertos de los picks "seguros" (prob >= 75%) que yo daba como riesgo bajo.
  * Rentabilidad apostando cuando el valor esperado >= umbral contra la cuota de APERTURA de Bet365,
    y CLV (cuánto mejor fue la cuota tomada que la de cierre de Pinnacle sin margen).

Uso: python3 backtest.py [--umbral 0.05] [--min-partidos 6]
"""
import argparse
import csv
import glob
import math
import os
from collections import defaultdict
from datetime import datetime

MAXG = 10


def pois(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def probs(lh, la):
    ph = [pois(i, lh) for i in range(MAXG + 1)]
    pa = [pois(j, la) for j in range(MAXG + 1)]
    r = defaultdict(float)
    for i in range(MAXG + 1):
        for j in range(MAXG + 1):
            p = ph[i] * pa[j]
            r["1" if i > j else "X" if i == j else "2"] += p
            if i + j >= 2:
                r["o15"] += p
            if i + j >= 3:
                r["o25"] += p
            if i > 0 and j > 0:
                r["btts"] += p
            if i > 0:
                r["local_marca"] += p
            if j > 0:
                r["visit_marca"] += p
    r["u25"] = 1 - r["o25"]
    r["1X"] = r["1"] + r["X"]
    r["X2"] = r["X"] + r["2"]
    return r


def sin_margen(*cuotas):
    try:
        inv = [1 / float(c) for c in cuotas]
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    s = sum(inv)
    return [x / s for x in inv]


def f(row, *cols):
    for c in cols:
        v = row.get(c)
        if v not in (None, ""):
            try:
                return float(v)
            except ValueError:
                pass
    return None


def cargar():
    partidos = []
    for ruta in sorted(glob.glob(os.path.join(os.path.dirname(__file__) or ".", "data/historico/*.csv"))):
        liga, temp = os.path.basename(ruta)[:-4].split("_")
        for row in csv.DictReader(open(ruta, encoding="utf-8-sig", errors="ignore")):
            if not row.get("FTHG"):
                continue
            try:
                fecha = datetime.strptime(row["Date"], "%d/%m/%Y")
            except ValueError:
                fecha = datetime.strptime(row["Date"], "%d/%m/%y")
            partidos.append(dict(liga=liga, temp=temp, fecha=fecha, h=row["HomeTeam"], a=row["AwayTeam"],
                                 hg=int(row["FTHG"]), ag=int(row["FTAG"]), row=row))
    partidos.sort(key=lambda p: (p["liga"], p["temp"], p["fecha"]))
    return partidos


def lambdas(hist, h, a, liga_media, encoger, peso_cond=0.35, k=6):
    """Igual que simulador.lambdas: (ataque propio + defensa rival)/2, mezcla total y local/visitante.
    Con encoger=True, cada promedio se acerca a la media de la liga según el tamaño de la muestra."""
    def tasa(eq, campo, cond=None):
        ps = [x for x in hist[eq] if cond is None or x["cond"] == cond]
        n = len(ps)
        if n == 0:
            return None, 0
        v = sum(x[campo] for x in ps) / n
        if encoger:
            ref = liga_media["L" if cond == "L" else "V" if cond == "V" else "T"][campo if cond else "gf"]
            if cond is None:
                ref = liga_media["T"]["gf"]
            v = (n * v + k * ref) / (n + k)
        return v, n
    gf_h, _ = tasa(h, "gf"); gc_h, _ = tasa(h, "gc")
    gf_a, _ = tasa(a, "gf"); gc_a, _ = tasa(a, "gc")
    gfL, _ = tasa(h, "gf", "L"); gcL, _ = tasa(h, "gc", "L")
    gfV, _ = tasa(a, "gf", "V"); gcV, _ = tasa(a, "gc", "V")
    gfL = gfL if gfL is not None else gf_h; gcL = gcL if gcL is not None else gc_h
    gfV = gfV if gfV is not None else gf_a; gcV = gcV if gcV is not None else gc_a
    lh = (1 - peso_cond) * (gf_h + gc_a) / 2 + peso_cond * (gfL + gcV) / 2
    la = (1 - peso_cond) * (gf_a + gc_h) / 2 + peso_cond * (gfV + gcL) / 2
    return max(lh, 0.05), max(la, 0.05)


def lambdas_tiros(hist, h, a, la_, k=6):
    """Goles esperados a partir de remates a puerta (más estables que los goles en muestras cortas)."""
    if not la_.get("sot"):
        return None
    conv = (la_["hg"] + la_["ag"]) / la_["sot"]
    def media(eq, campo):
        v = [x[campo] for x in hist[eq] if x.get(campo) is not None]
        return sum(v) / len(v) if v else None
    sfh, sch, sfa, sca = media(h, "sf"), media(h, "sc"), media(a, "sf"), media(a, "sc")
    if None in (sfh, sch, sfa, sca):
        return None
    ventaja = (la_["hg"] / max(la_["ag"], 1)) ** 0.5
    lh = conv * (sfh + sca) / 2 * ventaja
    la = conv * (sfa + sch) / 2 / ventaja
    return max(lh, 0.05), max(la, 0.05)


def anclar(lh, la, pm, peso=0.6):
    r = probs(lh, la)
    obj = {k: peso * pm[i] + (1 - peso) * r[k] for i, k in enumerate(("1", "X", "2"))}
    tot = lh + la
    mejor = None
    for i in range(5, 96, 2):
        a = tot * i / 100
        rr = probs(a, tot - a)
        e = sum((rr[k] - obj[k]) ** 2 for k in ("1", "X", "2"))
        if mejor is None or e < mejor[0]:
            mejor = (e, a, tot - a)
    return mejor[1], mejor[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--umbral", type=float, default=0.05)
    ap.add_argument("--min-partidos", type=int, default=6)
    ap.add_argument("--umbral-sharp", type=float, default=0.02,
                    help="ventaja mínima de la mejor cuota frente al precio justo de Pinnacle")
    args = ap.parse_args()
    partidos = cargar()

    hist = defaultdict(list)
    liga_acum = defaultdict(lambda: dict(n=0, hg=0, ag=0))
    clave_prev = None
    seguros = defaultdict(lambda: dict(n=0, g=0, p=0.0))
    brier = defaultdict(lambda: [0.0, 0])
    apuestas = defaultdict(lambda: dict(n=0, ben=0.0, clv=0.0, nclv=0))
    total_eval = 0

    for p in partidos:
        clave = (p["liga"], p["temp"])
        if clave != clave_prev:
            hist = defaultdict(list)
            clave_prev = clave
        la_ = liga_acum[clave]
        h, a, row = p["h"], p["a"], p["row"]
        listo = len(hist[h]) >= args.min_partidos and len(hist[a]) >= args.min_partidos and la_["n"] >= 30
        if listo:
            mh, ma = la_["hg"] / la_["n"], la_["ag"] / la_["n"]
            media = {"T": {"gf": (mh + ma) / 2, "gc": (mh + ma) / 2},
                     "L": {"gf": mh, "gc": ma}, "V": {"gf": ma, "gc": mh}}
            pm = sin_margen(f(row, "B365H"), f(row, "B365D"), f(row, "B365A"))
            pou = sin_margen(f(row, "B365>2.5"), f(row, "B365<2.5"))
            pcl = sin_margen(f(row, "PSCH"), f(row, "PSCD"), f(row, "PSCA"))
            pcl_ou = sin_margen(f(row, "PC>2.5"), f(row, "PC<2.5"))
            if pm and pou:
                total_eval += 1
                l1 = lambdas(hist, h, a, media, encoger=False)
                l2 = lambdas(hist, h, a, media, encoger=True)
                l3 = anclar(*l2, pm)
                modelos = {"v1": probs(*l1), "v1+enc": probs(*l2), "v2": probs(*l3)}
                lt = lambdas_tiros(hist, h, a, la_)
                if lt:
                    modelos["tiros"] = probs(*lt)
                    modelos["tiros+mercado"] = probs(*anclar(*lt, pm))
                modelos["mercado"] = dict(modelos["v2"])
                modelos["mercado"].update({"1": pm[0], "X": pm[1], "2": pm[2], "o25": pou[0], "u25": pou[1]})
                hg, ag = p["hg"], p["ag"]
                real = {"1": hg > ag, "X": hg == ag, "2": hg < ag, "o15": hg + ag >= 2, "o25": hg + ag >= 3,
                        "u25": hg + ag <= 2, "btts": hg > 0 and ag > 0, "local_marca": hg > 0,
                        "visit_marca": ag > 0, "1X": hg >= ag, "X2": ag >= hg}
                cuotas = {"1": f(row, "B365H"), "X": f(row, "B365D"), "2": f(row, "B365A"),
                          "o25": f(row, "B365>2.5"), "u25": f(row, "B365<2.5")}
                justas_cierre = {}
                if pcl:
                    justas_cierre.update({"1": 1 / pcl[0], "X": 1 / pcl[1], "2": 1 / pcl[2]})
                if pcl_ou:
                    justas_cierre.update({"o25": 1 / pcl_ou[0], "u25": 1 / pcl_ou[1]})
                pin = sin_margen(f(row, "PSH"), f(row, "PSD"), f(row, "PSA"))
                pin_ou = sin_margen(f(row, "P>2.5"), f(row, "P<2.5"))
                if pin:
                    mejor = {"1": f(row, "MaxH"), "X": f(row, "MaxD"), "2": f(row, "MaxA")}
                    b365 = {"1": f(row, "B365H"), "X": f(row, "B365D"), "2": f(row, "B365A")}
                    for i, mk in enumerate(("1", "X", "2")):
                        for casa, cq in (("pinnacle->mejor cuota", mejor), ("pinnacle->bet365", b365)):
                            c = cq[mk]
                            if c and pin[i] * c - 1 >= args.umbral_sharp:
                                x = apuestas[(casa, False)]
                                x["n"] += 1; x["ben"] += (c - 1) if real[mk] else -1
                                if mk in justas_cierre:
                                    x["clv"] += c / justas_cierre[mk] - 1; x["nclv"] += 1
                if pin_ou:
                    for i, mk in enumerate(("o25", "u25")):
                        c = f(row, "Max>2.5" if mk == "o25" else "Max<2.5")
                        if c and pin_ou[i] * c - 1 >= args.umbral_sharp:
                            x = apuestas[("pinnacle->mejor cuota", True)]
                            x["n"] += 1; x["ben"] += (c - 1) if real[mk] else -1
                            if mk in justas_cierre:
                                x["clv"] += c / justas_cierre[mk] - 1; x["nclv"] += 1
                for nombre, r in modelos.items():
                    for mk in ("1", "X", "2", "o25"):
                        b = brier[(nombre, mk)]
                        b[0] += (r[mk] - real[mk]) ** 2
                        b[1] += 1
                    # picks "seguros" como los que yo daba (prob >= 75%) en mercados de goles / doble oportunidad
                    for mk in ("o15", "local_marca", "visit_marca", "1X", "X2", "btts", "o25", "u25"):
                        if r[mk] >= 0.75:
                            s = seguros[(nombre, mk)]
                            s["n"] += 1; s["g"] += real[mk]; s["p"] += r[mk]
                    if nombre == "mercado":
                        continue
                    for mk, c in cuotas.items():
                        if not c:
                            continue
                        ev = r[mk] * c - 1
                        if ev >= args.umbral:
                            ap_ = apuestas[(nombre, mk in ("o25", "u25"))]
                            ap_["n"] += 1
                            ap_["ben"] += (c - 1) if real[mk] else -1
                            if mk in justas_cierre:
                                ap_["clv"] += c / justas_cierre[mk] - 1
                                ap_["nclv"] += 1
        # actualizar historia DESPUÉS de evaluar (sin mirar el futuro)
        hst, ast = f(row, "HST"), f(row, "AST")
        hist[h].append(dict(gf=p["hg"], gc=p["ag"], cond="L", sf=hst, sc=ast))
        hist[a].append(dict(gf=p["ag"], gc=p["hg"], cond="V", sf=ast, sc=hst))
        la_["n"] += 1; la_["hg"] += p["hg"]; la_["ag"] += p["ag"]
        if hst is not None and ast is not None:
            la_["sot"] = la_.get("sot", 0) + hst + ast

    print(f"Partidos reales: {len(partidos)} | evaluados (con {args.min_partidos}+ partidos previos y cuotas): {total_eval}\n")
    print("== 1. Calibración (Brier, menor es mejor) ==")
    print(f"{'modelo':10} {'1':>7} {'X':>7} {'2':>7} {'+2.5':>7}")
    for nombre in ("v1", "v1+enc", "v2", "tiros", "tiros+mercado", "mercado"):
        if not brier[(nombre, "1")][1]:
            continue
        vals = [brier[(nombre, mk)][0] / brier[(nombre, mk)][1] for mk in ("1", "X", "2", "o25")]
        print(f"{nombre:10} " + " ".join(f"{v:7.4f}" for v in vals))

    print("\n== 2. Picks 'seguros' (prob. >= 75%): ¿se cumplen? ==")
    etiquetas = {"o15": "Más de 1.5", "local_marca": "Local marca", "visit_marca": "Visitante marca",
                 "1X": "Local o empate", "X2": "Visitante o empate", "btts": "Ambos marcan",
                 "o25": "Más de 2.5", "u25": "Menos de 2.5"}
    print(f"{'modelo':9} {'mercado':20} {'picks':>6} {'acierto real':>13} {'prob. prometida':>16} {'desvío':>8}")
    for nombre in ("v1", "v1+enc", "v2"):
        for mk, et in etiquetas.items():
            s = seguros[(nombre, mk)]
            if s["n"] >= 30:
                real, prom = s["g"] / s["n"], s["p"] / s["n"]
                print(f"{nombre:9} {et:20} {s['n']:6d} {real:12.1%} {prom:15.1%} {real - prom:+8.1%}")

    print(f"\n== 3. Apostando cuando valor esperado >= {args.umbral:+.0%} (cuota apertura Bet365, 1 unidad) ==")
    print(f"{'modelo':9} {'mercado':8} {'apuestas':>9} {'beneficio':>10} {'ROI':>7} {'CLV medio':>10}")
    for nombre in ("v1", "v1+enc", "v2", "tiros", "tiros+mercado", "pinnacle->bet365", "pinnacle->mejor cuota"):
        for es_ou, et in ((False, "1X2"), (True, "+/-2.5")):
            x = apuestas[(nombre, es_ou)]
            if x["n"]:
                clv = x["clv"] / x["nclv"] if x["nclv"] else float("nan")
                print(f"{nombre:9} {et:8} {x['n']:9d} {x['ben']:+10.1f} {x['ben'] / x['n']:+7.1%} {clv:+10.1%}")
    print("\nCLV = cuánto mejor fue la cuota tomada que la de cierre de Pinnacle sin margen. "
          "CLV positivo sostenido es la mejor señal de ventaja real a largo plazo.")


if __name__ == "__main__":
    main()
