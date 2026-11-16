#!/usr/bin/env python3
"""Auditoría del registro de picks: calibración, mercados, cuotas, valor y ROI.

Uso: python3 auditoria.py [registro/picks.csv] [--json calibracion_registro.json]
Escribe calibracion_registro.json con los ajustes por mercado que usa valor.py.
Resultados: G, P, MG, MP, N (nula), pendiente. Solo cuentan G/P para aciertos.
"""
import csv
import json
import sys
from collections import defaultdict

GLOBAL_PRIOR = 30  # partidos "virtuales" que tira hacia el ajuste global (evita sobreajustar con n pequeño)


def categoria(m):
    m = m.lower()
    if "córner" in m or "corner" in m:
        return "córneres"
    if "tarjeta" in m or "amarilla" in m:
        return "tarjetas"
    if "remate" in m or "parada" in m:
        return "remates/paradas"
    if "ambos" in m:
        return "ambos marcan"
    if m.startswith("rango"):
        return "rango de goles"
    if "más de" in m and "marca" not in m:
        return "goles más de"
    if "menos de" in m and "marca" not in m:
        return "goles menos de"
    if "+" in m or "-1" in m or "−" in m or "-2" in m:
        return "hándicap"
    if " o " in m or "doble" in m or "empate no apuesta" in m:
        return "doble oportunidad"
    if m.endswith("marca") or "2 o más goles" in m or "3 o más goles" in m or "gana sin encajar" in m:
        return "equipo marca / sin encajar"
    if m == "empate":
        return "empate"
    if m.startswith("gana") or " gana" in m:
        return "ganador / combinaciones"
    return "otros"


def cargar(ruta):
    filas = []
    with open(ruta, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not r.get("fecha"):
                continue
            filas.append(r)
    return filas


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def resumen(lista, nombre):
    if not lista:
        return None
    g = sum(r["resultado"] == "G" for r in lista)
    esp = sum(f(r["prob_dada"]) for r in lista)
    con = [r for r in lista if f(r.get("cuota"))]
    s = f"{nombre:30} n={len(lista):4}  ganó {g / len(lista):4.0%}  esperado {esp / len(lista):4.0%}"
    if con:
        roi = sum((f(r["cuota"]) - 1) if r["resultado"] == "G" else -1 for r in con) / len(con)
        s += f"  | con cuota: n={len(con):3} ROI {roi:+.0%}"
    print(s)


def main(ruta="registro/picks.csv", salida="calibracion_registro.json"):
    filas = cargar(ruta)
    res = [r for r in filas if r["resultado"] in ("G", "P") and f(r["prob_dada"]) is not None]
    pend = sum(r["resultado"] == "pendiente" for r in filas)
    print(f"Picks: {len(filas)} | resueltos G/P: {len(res)} | pendientes: {pend}")
    con_cuota = [r for r in res if f(r.get("cuota"))]
    print(f"Con cuota vista: {len(con_cuota)} ({len(con_cuota) / max(len(res), 1):.0%}). Sin cuota solo se mide acierto, no dinero.\n")

    print("== Calibración (probabilidad dada frente a lo ocurrido)")
    tramos = [(0, .35), (.35, .5), (.5, .62), (.62, .7), (.7, .78), (.78, .86), (.86, 1.01)]
    for lo, hi in tramos:
        resumen([r for r in res if lo <= f(r["prob_dada"]) < hi], f"prob {lo:.0%}-{min(hi, 1):.0%}")
    gap = sum((r["resultado"] == "G") - f(r["prob_dada"]) for r in res) / max(len(res), 1)
    print(f"Desviación global (ganó - esperado): {gap:+.1%}\n")

    print("== Por tipo de mercado")
    por_cat = defaultdict(list)
    for r in res:
        por_cat[categoria(r["mercado"])].append(r)
    ajustes = {}
    for c, lst in sorted(por_cat.items(), key=lambda kv: -len(kv[1])):
        resumen(lst, c)
        n = len(lst)
        obs = sum(r["resultado"] == "G" for r in lst) / n
        esp = sum(f(r["prob_dada"]) for r in lst) / n
        raw = obs - esp
        # el ajuste por mercado se encoge hacia el global cuando n es pequeño
        aj = (n * raw + GLOBAL_PRIOR * gap) / (n + GLOBAL_PRIOR)
        ajustes[c] = {"n": n, "ajuste": round(aj, 4)}
    print()

    print("== Por cuota vista")
    for lo, hi in [(1, 1.3), (1.3, 1.6), (1.6, 2.1), (2.1, 10)]:
        resumen([r for r in con_cuota if lo <= f(r["cuota"]) < hi], f"cuota {lo}-{hi}")
    print()

    print("== ¿El 'valor' calculado sirve? (valor = prob x cuota - 1, con la prob. dada)")
    for lo, hi, nom in [(-9, 0, "valor <= 0"), (0, .05, "valor 0-5%"), (.05, .10, "valor 5-10%"), (.10, 9, "valor > 10%")]:
        resumen([r for r in con_cuota if lo < f(r["prob_dada"]) * f(r["cuota"]) - 1 <= hi or (lo == -9 and f(r["prob_dada"]) * f(r["cuota"]) - 1 <= 0)] if lo != -9 else
                [r for r in con_cuota if f(r["prob_dada"]) * f(r["cuota"]) - 1 <= 0], nom)
    print()

    print("== Por origen")
    por_o = defaultdict(list)
    for r in res:
        por_o[r["origen"]].append(r)
    for o, lst in sorted(por_o.items(), key=lambda kv: -len(kv[1])):
        resumen(lst, o)
    print()

    print("== Por día")
    por_d = defaultdict(list)
    for r in res:
        por_d[r["fecha"]].append(r)
    for d, lst in sorted(por_d.items()):
        resumen(lst, d)

    # solo las recomendadas (origen analista), la cifra que de verdad importa para el usuario
    rec = [r for r in res if r["origen"] == "analista"]
    print()
    resumen(rec, "RECOMENDADAS (analista)")

    out = {"desviacion_global": round(gap, 4), "n_resueltos": len(res), "n_con_cuota": len(con_cuota),
           "por_mercado": ajustes}
    with open(salida, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"\nAjustes por mercado guardados en {salida}")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    main(*(a[:1] or ["registro/picks.csv"]))
