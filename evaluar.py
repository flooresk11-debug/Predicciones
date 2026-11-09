#!/usr/bin/env python3
"""Evalúa el registro de picks: aciertos, calibración (Brier) y rentabilidad.

resultado: G (ganada), P (perdida), MG/MP (media ganada/perdida, hándicap asiático), N (nula), pendiente.
Uso: python3 evaluar.py [registro/picks.csv]
"""
import csv
import sys
from collections import defaultdict


def main(ruta="registro/picks.csv"):
    filas = list(csv.DictReader(open(ruta, encoding="utf-8")))
    resueltas = [f for f in filas if f["resultado"] in ("G", "P", "MG", "MP") and f["prob_dada"]]
    pend = sum(f["resultado"] == "pendiente" for f in filas)
    print(f"Picks: {len(filas)} | resueltos: {len(resueltas)} | pendientes: {pend}\n")
    if not resueltas:
        print("Sin picks resueltos: añade los marcadores en la columna 'resultado'.")
        return
    por = defaultdict(list)
    for f in resueltas:
        por[f["origen"]].append(f)
    for origen, fs in por.items():
        n = len(fs)
        valor = {"G": 1.0, "MG": 0.75, "MP": 0.25, "P": 0.0}
        g = sum(valor[f["resultado"]] for f in fs)
        esperado = sum(float(f["prob_dada"]) for f in fs)
        brier = sum((float(f["prob_dada"]) - valor[f["resultado"]]) ** 2 for f in fs) / n
        con_cuota = [f for f in fs if f["cuota"]]
        pago = lambda f, c: {"G": c - 1, "MG": (c - 1) / 2, "MP": -0.5, "P": -1}[f["resultado"]]
        beneficio = sum(pago(f, float(f["cuota"])) for f in con_cuota)
        print(f"[{origen}] aciertos {g:g}/{n} ({g / n:.0%}) | esperados según mis probabilidades: {esperado:.1f} "
              f"| Brier {brier:.3f} (0 = perfecto, 0.25 = moneda al aire)")
        if con_cuota:
            print(f"    rentabilidad con cuota (1 unidad por pick): {beneficio:+.2f} u en {len(con_cuota)} picks "
                  f"(ROI {beneficio / len(con_cuota):+.0%})")
        if g < esperado - 2 * (sum(float(f['prob_dada']) * (1 - float(f['prob_dada'])) for f in fs)) ** 0.5:
            print("    ⚠️ Aciertos muy por debajo de lo esperado: el modelo está mal calibrado (sobreconfiado).")
        cubos = defaultdict(list)
        for f in fs:
            p = float(f["prob_dada"])
            cubos["<70%" if p < 0.7 else "70-79%" if p < 0.8 else "80%+"].append(valor[f["resultado"]])
        for c, v in sorted(cubos.items()):
            print(f"    tramo {c}: {sum(v):g}/{len(v)} ganados")


if __name__ == "__main__":
    main(*sys.argv[1:])
