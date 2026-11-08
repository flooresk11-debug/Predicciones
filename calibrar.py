#!/usr/bin/env python3
"""
Calibra el simulador_real con datos reales: ajusta parámetros en 2025/26 (entrenamiento)
y los comprueba en 2026/27 (prueba, datos que el ajuste no ha visto).

Parámetros:
  K      partidos "virtuales" de la temporada anterior (cuánto se encoge hacia el pasado)
  alfa   potencia de los factores de equipo (1 = tal cual; <1 = más prudente)
  delta  escala de la dispersión extra (0 = Poisson; 1 = dispersión medida bruta)
Mercados: corners +9.5, amarillas +3.5, tiros a puerta +8.5, goles +2.5 (totales del partido).
"""
import itertools
import json
import os
from collections import defaultdict

import simulador_real as S

LIGAS = ["E0", "SP1", "D1", "D2", "I1", "N1", "F1"]
MERCADOS = (("corners", 9.5), ("amarillas", 3.5), ("tiros_puerta", 8.5), ("goles", 2.5))
GRID_K = (6, 12, 20, 30)
GRID_ALFA = (0.3, 0.5, 0.7, 1.0)
GRID_DELTA = (0.0, 0.25, 0.5, 1.0)


def registros(liga, temp, prev, K):
    S.K_PREVIO = K
    act, ant = S.cargar(liga, temp, max_horas=24 * 30), S.cargar(liga, prev, max_horas=24 * 30)
    out = []
    for i, f in enumerate(act):
        jug = act[:i]
        if sum(1 for x in jug if f["h"] in (x["h"], x["a"])) < 5 or sum(1 for x in jug if f["a"] in (x["h"], x["a"])) < 5:
            continue
        L = S.Liga(jug, ant)
        for s, linea in MERCADOS:
            if not f[s] or s not in L.medias:
                continue
            mh, ma = L.medias[s]
            fl, _ = L.factor(f["h"], f"{s}_favor_L"); cv, _ = L.factor(f["a"], f"{s}_contra_V")
            fv, _ = L.factor(f["a"], f"{s}_favor_V"); cl, _ = L.factor(f["h"], f"{s}_contra_L")
            out.append((s, linea, mh, ma, fl, cv, fv, cl, L.disp[s], sum(f[s]) > linea))
    return out


def evaluar(regs, alfa, delta):
    res = defaultdict(lambda: [0, 0.0, 0])
    for s, linea, mh, ma, fl, cv, fv, cl, disp, real in regs:
        media = mh * (fl * cv) ** alfa + ma * (fv * cl) ** alfa
        d = 1.0 if s == "goles" else 1 + delta * (disp - 1)
        p = S.prob_mas_de(linea, media, d)
        x = res[s]; x[0] += 1; x[1] += (p - real) ** 2; x[2] += real
    skill = {}
    for s, (n, br, ac) in res.items():
        base = (ac / n) * (1 - ac / n)
        skill[s] = 1 - (br / n) / base   # >0 mejora a la frecuencia media
    return skill


def main():
    tren, prueba = defaultdict(list), defaultdict(list)
    for K in GRID_K:
        for lg in LIGAS:
            tren[K] += registros(lg, "2526", "2425", K)
            prueba[K] += registros(lg, "2627", "2526", K)
        print(f"K={K}: {len(tren[K])} registros de entrenamiento, {len(prueba[K])} de prueba")
    mejores = {}
    for s, _ in MERCADOS:
        mejor = None
        for K, alfa, delta in itertools.product(GRID_K, GRID_ALFA, GRID_DELTA):
            sk = evaluar([r for r in tren[K] if r[0] == s], alfa, delta)[s]
            if mejor is None or sk > mejor[0]:
                mejor = (sk, K, alfa, delta)
        sk_tren, K, alfa, delta = mejor
        sk_prueba = evaluar([r for r in prueba[K] if r[0] == s], alfa, delta)[s]
        sk_v1 = evaluar([r for r in prueba[6] if r[0] == s], 1.0, 1.0)[s]
        mejores[s] = dict(K=K, alfa=alfa, delta=delta, skill_entrenamiento=round(sk_tren, 4),
                          skill_prueba=round(sk_prueba, 4), skill_prueba_version_anterior=round(sk_v1, 4))
        print(f"{s:13} K={K:2} alfa={alfa} delta={delta} | mejora vs base: entrenamiento {sk_tren:+.1%}, "
              f"PRUEBA {sk_prueba:+.1%} (versión anterior {sk_v1:+.1%})")
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parametros_calibrados.json")
    json.dump(mejores, open(ruta, "w", encoding="utf-8"), indent=2)
    print(f"\nGuardado en {ruta}")


if __name__ == "__main__":
    main()
