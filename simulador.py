#!/usr/bin/env python3
"""
Simulador de partidos con auditoría de datos.

Principios:
  * Solo usa datos guardados en data/*.json, cada uno con su fuente y estado.
  * Los datos con estado CONFLICTO o NO_DISPONIBLE no se usan ni se rellenan.
  * Antes de simular, audita que los resultados partido a partido sumen
    exactamente lo que dice la tabla publicada (puntos, G/E/P, goles).
  * Modelo: Poisson independiente + Monte Carlo (semilla fija = reproducible).

Uso:
  python3 simulador.py data/2026-11-08_koln_leverkusen.json
  python3 simulador.py data/... --peso-condicion 0.35 --sims 200000
"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

MAX_GOLES = 10


# ---------------------------------------------------------------- utilidades
def pct(x):
    return f"{100 * x:.1f}%"


def poisson(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def cuota_justa(p):
    return float("inf") if p <= 0 else 1 / p


# ---------------------------------------------------------------- auditoría
def auditar(d):
    hallazgos, ok = [], True
    for equipo, partidos in d["resultados_liga"].items():
        g = sum(p["gf"] > p["gc"] for p in partidos)
        e = sum(p["gf"] == p["gc"] for p in partidos)
        pe = sum(p["gf"] < p["gc"] for p in partidos)
        gf = sum(p["gf"] for p in partidos)
        gc = sum(p["gc"] for p in partidos)
        pts = 3 * g + e
        t = d["tabla_oficial_declarada"][equipo]
        calc = dict(pj=len(partidos), g=g, e=e, p=pe, gf=gf, gc=gc, pts=pts)
        dif = {k: (v, t[k]) for k, v in calc.items() if t[k] != v}
        if dif:
            ok = False
            hallazgos.append(f"FALLO {equipo}: calculado vs tabla -> {dif}")
        else:
            hallazgos.append(
                f"OK  {equipo}: {len(partidos)} PJ, {g}G {e}E {pe}P, {gf}:{gc}, {pts} pts "
                f"= coincide con la tabla publicada")
        estados = {}
        for p in partidos:
            estados[p["estado"]] = estados.get(p["estado"], 0) + 1
        hallazgos.append(f"    estados de los resultados de {equipo}: {estados}")

    for equipo, t in d["tiros"].items():
        if not isinstance(t, dict):
            hallazgos.append(f"NO_DISPONIBLE {equipo}: no se usa")
            continue
        hallazgos.append(
            f"OK  tiros {equipo}: {t['tiros']} tiros / {t['goles']} goles = "
            f"{t['tiros'] / t['goles']:.2f} tiros por gol ({t['tiros'] / t['partidos']:.1f} por partido)")

    for clave, v in d["h2h_resumen"].items():
        if v["estado"] == "CONFLICTO":
            hallazgos.append(f"EXCLUIDO (conflicto entre fuentes) h2h.{clave}: {v.get('nota', '')}")
    return ok, hallazgos


# ---------------------------------------------------------------- estadística descriptiva
def splits(partidos, condicion=None):
    ps = [p for p in partidos if condicion is None or p["condicion"] == condicion]
    n = len(ps)
    if n == 0:
        return None
    gf = sum(p["gf"] for p in ps)
    gc = sum(p["gc"] for p in ps)
    return {
        "pj": n,
        "g": sum(p["gf"] > p["gc"] for p in ps),
        "e": sum(p["gf"] == p["gc"] for p in ps),
        "p": sum(p["gf"] < p["gc"] for p in ps),
        "gf": gf, "gc": gc,
        "gf_pp": gf / n, "gc_pp": gc / n,
        "total_pp": (gf + gc) / n,
        "btts": sum(p["gf"] > 0 and p["gc"] > 0 for p in ps) / n,
        "porteria_cero": sum(p["gc"] == 0 for p in ps) / n,
        "sin_marcar": sum(p["gf"] == 0 for p in ps) / n,
        "over15": sum(p["gf"] + p["gc"] > 1.5 for p in ps) / n,
        "over25": sum(p["gf"] + p["gc"] > 2.5 for p in ps) / n,
        "over35": sum(p["gf"] + p["gc"] > 3.5 for p in ps) / n,
    }


# ---------------------------------------------------------------- modelo
def lambdas(d, peso_condicion):
    loc, vis = d["partido"]["local"], d["partido"]["visitante"]
    L, V = d["resultados_liga"][loc], d["resultados_liga"][vis]
    lt, vt = splits(L), splits(V)
    lc, vc = splits(L, "L"), splits(V, "V")
    # Estimador global: ataque propio vs. defensa rival (temporada completa)
    lam_l_glob = (lt["gf_pp"] + vt["gc_pp"]) / 2
    lam_v_glob = (vt["gf_pp"] + lt["gc_pp"]) / 2
    # Estimador por condición: local en casa vs visitante fuera
    lam_l_cond = (lc["gf_pp"] + vc["gc_pp"]) / 2
    lam_v_cond = (vc["gf_pp"] + lc["gc_pp"]) / 2
    w = peso_condicion
    return (w * lam_l_cond + (1 - w) * lam_l_glob,
            w * lam_v_cond + (1 - w) * lam_v_glob,
            dict(lam_l_glob=lam_l_glob, lam_v_glob=lam_v_glob,
                 lam_l_cond=lam_l_cond, lam_v_cond=lam_v_cond))


def matriz(lam_l, lam_v):
    return [[poisson(i, lam_l) * poisson(j, lam_v) for j in range(MAX_GOLES + 1)]
            for i in range(MAX_GOLES + 1)]


def mercados(m):
    def P(cond):
        return sum(m[i][j] for i in range(len(m)) for j in range(len(m)) if cond(i, j))
    r = {
        "1": P(lambda i, j: i > j), "X": P(lambda i, j: i == j), "2": P(lambda i, j: i < j),
        "BTTS sí": P(lambda i, j: i > 0 and j > 0),
        "Más de 1.5": P(lambda i, j: i + j >= 2), "Más de 2.5": P(lambda i, j: i + j >= 3),
        "Más de 3.5": P(lambda i, j: i + j >= 4),
        "Local portería a cero": P(lambda i, j: j == 0),
        "Visitante portería a cero": P(lambda i, j: i == 0),
        "Local menos de 1.5": P(lambda i, j: i <= 1),
        "Visitante más de 0.5": P(lambda i, j: j >= 1),
        "Visitante más de 1.5": P(lambda i, j: j >= 2),
        "Local pierde por 1": P(lambda i, j: j - i == 1),
        "Local pierde por 2+": P(lambda i, j: j - i >= 2),
        "Visitante gana por 2+": P(lambda i, j: j - i >= 2),
        "Local gana a cero": P(lambda i, j: i > j and j == 0),
        "Visitante gana a cero": P(lambda i, j: j > i and i == 0),
    }
    r["1X"] = r["1"] + r["X"]
    r["X2"] = r["X"] + r["2"]
    r["12"] = r["1"] + r["2"]
    r["BTTS no"] = 1 - r["BTTS sí"]
    r["Menos de 2.5"] = 1 - r["Más de 2.5"]
    r["Menos de 3.5"] = 1 - r["Más de 3.5"]
    marcadores = sorted(((m[i][j], f"{i}-{j}") for i in range(6) for j in range(6)), reverse=True)
    return r, marcadores[:8]


def monte_carlo(lam_l, lam_v, n, semilla=2026):
    rnd = random.Random(semilla)

    def muestra(lam):
        # algoritmo de Knuth
        L, k, p = math.exp(-lam), 0, 1.0
        while True:
            p *= rnd.random()
            if p <= L:
                return k
            k += 1
    c = {"1": 0, "X": 0, "2": 0, "btts": 0, "o25": 0}
    for _ in range(n):
        a, b = muestra(lam_l), muestra(lam_v)
        c["1" if a > b else "X" if a == b else "2"] += 1
        c["btts"] += a > 0 and b > 0
        c["o25"] += a + b > 2
    return {k: v / n for k, v in c.items()}


def ev_handicap_asiatico_local_mas1(r, cuota):
    """AH +1 local: gana si local gana o empata; push si pierde por 1; pierde si por 2+."""
    return (r["1"] + r["X"]) * (cuota - 1) - r["Local pierde por 2+"]


# ---------------------------------------------------------------- informe
def informe(d, args):
    loc, vis = d["partido"]["local"], d["partido"]["visitante"]
    out = []
    w = out.append
    ok, hall = auditar(d)
    w(f"# Simulación auditada: {loc} vs {vis}")
    w(f"{d['partido']['competicion']} · {d['partido']['fecha']} {d['partido']['hora_cet']} CET\n")
    w("## 1. Auditoría de datos")
    w("```")
    w("\n".join(hall))
    w("```")
    w("**Resultado de la auditoría:** " + ("todos los totales cuadran con la tabla publicada."
                                          if ok else "HAY INCONSISTENCIAS: no confiar en la simulación."))
    nd = [k for k, v in d["tiros"].items() if v == "NO_DISPONIBLE"]
    w(f"\nDatos **no disponibles** (no se inventan): {', '.join(nd)}, asistencias, "
      "estadísticas de primer tiempo completas, tabla completa.\n")

    w(f"## 2. Estadísticas reales ({d['partido']['competicion'].split(' - ')[0]})")
    w("| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for eq, cond, etiqueta in [(loc, None, "Total"), (loc, "L", "Local"),
                               (vis, None, "Total"), (vis, "V", "Visitante")]:
        s = splits(d["resultados_liga"][eq], cond)
        w(f"| {eq} | {etiqueta} | {s['pj']} | {s['g']}-{s['e']}-{s['p']} | {s['gf']} | {s['gc']} | "
          f"{s['gf_pp']:.2f} | {s['gc_pp']:.2f} | {s['total_pp']:.2f} | {pct(s['btts'])} | "
          f"{pct(s['porteria_cero'])} | {pct(s['sin_marcar'])} | {pct(s['over25'])} |")

    lam_l, lam_v, det = lambdas(d, args.peso_condicion)
    m = matriz(lam_l, lam_v)
    r, marc = mercados(m)
    mc = monte_carlo(lam_l, lam_v, args.sims)

    w("\n## 3. Modelo")
    w(f"- Goles esperados (global): {loc} {det['lam_l_glob']:.2f} · {vis} {det['lam_v_glob']:.2f}")
    w(f"- Goles esperados (local en casa / visitante fuera): {loc} {det['lam_l_cond']:.2f} · {vis} {det['lam_v_cond']:.2f}")
    w(f"- Peso de la condición local/visitante: {args.peso_condicion:.2f} (muestra pequeña por condición)")
    w(f"- **λ final: {loc} {lam_l:.2f} · {vis} {lam_v:.2f}** (total esperado {lam_l + lam_v:.2f})")
    w(f"- Monte Carlo {args.sims:,} simulaciones (semilla 2026): 1 {pct(mc['1'])} · X {pct(mc['X'])} · "
      f"2 {pct(mc['2'])} · BTTS {pct(mc['btts'])} · +2.5 {pct(mc['o25'])}")

    w("\n## 4. Probabilidades (cálculo exacto Poisson)")
    w("| Mercado | Probabilidad | Cuota justa |")
    w("|---|---|---|")
    for k in ["1", "X", "2", "1X", "X2", "12", "BTTS sí", "BTTS no", "Más de 1.5", "Más de 2.5",
              "Menos de 2.5", "Más de 3.5", "Menos de 3.5", "Local portería a cero",
              "Visitante portería a cero", "Local menos de 1.5", "Visitante más de 0.5",
              "Visitante más de 1.5", "Visitante gana por 2+", "Visitante gana a cero"]:
        w(f"| {k} | {pct(r[k])} | {cuota_justa(r[k]):.2f} |")
    w("\nMarcadores más probables: " + ", ".join(f"{s} ({pct(p)})" for p, s in marc))

    w("\n## 5. Comparación con cuotas publicadas")
    w("| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |")
    w("|---|---|---|---|---|")
    for nombre, q in d["cuotas_publicadas"].items():
        if nombre.startswith("_"):
            continue
        c = q["cuota"]
        if q.get("tipo") == "ah_local_+1":
            w(f"| {nombre} | {c} | {pct(1 / c)} | gana {pct(r['1X'])} / push {pct(r['Local pierde por 1'])} | "
              f"{ev_handicap_asiatico_local_mas1(r, c):+.3f} |")
        else:
            p = r[q["mercado"]]
            w(f"| {nombre} | {c} | {pct(1 / c)} | {pct(p)} | {p * c - 1:+.3f} |")

    w("\n## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)")
    w("| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |")
    w("|---|---|---|---|---|---|---|---|")
    for pw in (0.0, 0.2, 0.35, 0.5, 0.7):
        a, b, _ = lambdas(d, pw)
        rr, _ = mercados(matriz(a, b))
        w(f"| {pw:.2f} | {a:.2f} | {b:.2f} | {pct(rr['1'])} | {pct(rr['X'])} | {pct(rr['2'])} | "
          f"{pct(rr['Más de 2.5'])} | {pct(rr['BTTS sí'])} |")

    w("\n## 7. Limitaciones")
    n_min = min(len(v) for v in d["resultados_liga"].values())
    w(f"- Muestra pequeña ({n_min} partidos de liga por equipo): intervalos de confianza amplios.")
    w("- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.")
    w("- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.")
    return "\n".join(out), ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datos", nargs="?", default="data/2026-11-08_koln_leverkusen.json")
    ap.add_argument("--peso-condicion", type=float, default=0.35)
    ap.add_argument("--sims", type=int, default=200_000)
    ap.add_argument("--salida", default=None)
    args = ap.parse_args()
    d = json.loads(Path(args.datos).read_text(encoding="utf-8"))
    texto, ok = informe(d, args)
    print(texto)
    if args.salida:
        Path(args.salida).write_text(texto + "\n", encoding="utf-8")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
