#!/usr/bin/env python3
"""Valor de una apuesta con la probabilidad CORREGIDA por lo que ha pasado de verdad (v4).

Uso: python3 valor.py "Menos de 3.5 goles" 0.74 1.40
     python3 valor.py "Gana Francia" 0.46            (sin cuota: da la cuota mínima para entrar)

Qué hace:
1. Corrige la probabilidad con calibracion_registro.json (se regenera con auditoria.py): resta el error medio
   del mercado (encogido hacia el error global si hay pocos datos). Los ajustes positivos se dejan a la
   mitad (no nos fiamos de una mejora con pocos datos).
2. Calcula valor = prob_corregida x cuota - 1.
3. Solo es 'VALOR' si el valor >= 8% (margen para el error del modelo), la cuota >= 1.30 y la prob. >= 40%.
   Con prob < 40% o cuota > 3 el margen exigido sube (más ruido, más varianza).
4. Stake: 1/4 de Kelly con la prob. corregida, máximo 0.5 u (0.25 u si el valor es < 15%).
"""
import json
import os
import sys

from auditoria import categoria

RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibracion_registro.json")
MARGEN_MIN = 0.08


def ajuste_prob(mercado, p):
    try:
        cal = json.load(open(RUTA, encoding="utf-8"))
    except FileNotFoundError:
        return p, 0.0, "sin calibración (ejecuta auditoria.py)"
    cat = categoria(mercado)
    aj = cal["por_mercado"].get(cat, {}).get("ajuste", cal.get("desviacion_global", -0.04))
    if aj > 0:
        aj *= 0.5
    # el error se concentra en probabilidades medias; en los extremos casi no hay margen de error
    aj *= max(0.4, 4 * p * (1 - p))
    return max(0.01, min(0.99, p + aj)), aj, cat


def evaluar(mercado, p, cuota=None):
    pc, aj, cat = ajuste_prob(mercado, p)
    out = {"mercado": mercado, "categoria": cat, "prob_dada": p, "ajuste": round(aj, 3), "prob_corregida": round(pc, 3),
           "cuota_justa_corregida": round(1 / pc, 2)}
    margen = MARGEN_MIN + (0.04 if p < 0.40 or (cuota and cuota > 3) else 0)
    out["entra_desde"] = round((1 + margen) / pc, 2)
    if cuota:
        v = pc * cuota - 1
        out["cuota"] = cuota
        out["valor"] = round(v, 3)
        ok = v >= margen and cuota >= 1.30 and pc >= 0.40
        out["veredicto"] = "VALOR" if ok else "SIN VALOR"
        if cuota < 1.30:
            out["motivo"] = "paga menos de 1.30"
        elif pc < 0.40:
            out["motivo"] = "probabilidad corregida < 40%"
        elif v < margen:
            out["motivo"] = f"valor {v:+.1%} < margen mínimo {margen:.0%}"
        if ok:
            kelly = max(0.0, (pc * cuota - 1) / (cuota - 1))
            stake = min(0.5 if v >= 0.15 else 0.25, round(kelly / 4 * 10, 2))
            out["stake_u"] = max(0.1, stake)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    r = evaluar(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else None)
    for k, v in r.items():
        print(f"{k:24} {v}")
