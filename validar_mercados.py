#!/usr/bin/env python3
"""
Valida con partidos REALES los mercados del simulador: ¿lo que promete se cumple?

Para cada partido de 2025/26 y 2026/27 (7 ligas):
  * goles esperados = los que reproducen las cuotas medias del mercado antes del partido (1X2 y +/-2.5)
  * reparto de goles entre mitades = el real de la liga en la temporada anterior
  * corners y tarjetas = fuerzas de equipo calibradas usando solo partidos anteriores
Compara la probabilidad dada con lo que pasó, por tramos (50-60%, 60-75%, 75%+).
"""
import math
from collections import defaultdict

import mercados as M
import simulador_real as S

LIGAS = ["E0", "SP1", "D1", "D2", "I1", "N1", "F1"]
GRID = [x / 10 for x in range(2, 41)]
_POIS = {l: M.pois(l) for l in GRID}


def ajustar(p1, px, pover):
    mejor = None
    for lh in GRID:
        ph = _POIS[lh]
        for la in GRID:
            pa = _POIS[la]
            cdf_a = [sum(pa[:k + 1]) for k in range(len(pa))]
            g = sum(ph[i] * cdf_a[i - 1] for i in range(1, len(ph)))
            e = sum(ph[i] * pa[i] for i in range(len(ph)))
            tot = M.total(ph[:8], pa[:8])
            ov = 1 - tot[0] - tot[1] - tot[2]
            err = (g - p1) ** 2 + (e - px) ** 2 + (ov - pover) ** 2
            if mejor is None or err < mejor[0]:
                mejor = (err, lh, la)
    return mejor[1], mejor[2]


def main():
    cubos = defaultdict(lambda: [0, 0.0, 0])
    for lg in LIGAS:
        for temp, prev in (("2526", "2425"), ("2627", "2526")):
            act, ant = S.cargar(lg, temp, max_horas=24 * 30), S.cargar(lg, prev, max_horas=24 * 30)
            con_ht = [f for f in ant if f["ht"] and f["goles"]]
            s1 = sum(sum(f["ht"]) for f in con_ht) / max(1, sum(sum(f["goles"]) for f in con_ht))
            for i, f in enumerate(act):
                r = f["row"]
                try:
                    inv = [1 / float(r[k]) for k in ("AvgH", "AvgD", "AvgA")]
                    ou = [1 / float(r[k]) for k in ("Avg>2.5", "Avg<2.5")]
                except (KeyError, ValueError, ZeroDivisionError):
                    continue
                p = [x / sum(inv) for x in inv]
                lh, la = ajustar(p[0], p[1], ou[0] / sum(ou))
                P, _ = M.goles(lh, la, s1)
                gh, ga = f["goles"]; hth, hta = f["ht"] if f["ht"] else (None, None)
                reales = {"Ambos marcan: sí": gh > 0 and ga > 0, "Ambos marcan: no": not (gh > 0 and ga > 0),
                          "Local o empate": gh >= ga, "Visitante o empate": ga >= gh,
                          "Local más de 0.5 goles": gh > 0, "Visitante más de 0.5 goles": ga > 0,
                          "Rango 2-3 goles": gh + ga in (2, 3), "Más de 1.5 goles": gh + ga >= 2}
                if hth is not None:
                    s2h, s2a = gh - hth, ga - hta
                    reales.update({
                        "Gol en el 1.er tiempo": hth + hta > 0,
                        "Local gana cualquier mitad": hth > hta or s2h > s2a,
                        "Visitante gana cualquier mitad": hta > hth or s2a > s2h,
                        "Local gana ambas mitades": hth > hta and s2h > s2a,
                        "Local marca en ambas mitades": hth > 0 and s2h > 0,
                        "Visitante marca en ambas mitades": hta > 0 and s2a > 0})
                for k, real in reales.items():
                    pr = P[k]
                    tramo = "75%+" if pr >= 0.75 else "60-75%" if pr >= 0.6 else "50-60%" if pr >= 0.5 else None
                    if tramo:
                        c = cubos[(k, tramo)]; c[0] += 1; c[1] += pr; c[2] += real
                # corners y tarjetas con fuerzas de equipo (solo partidos previos)
                jug = act[:i]
                if sum(1 for x in jug if f["h"] in (x["h"], x["a"])) >= 5 and sum(1 for x in jug if f["a"] in (x["h"], x["a"])) >= 5:
                    L = S.Liga(jug, ant)
                    for s, nombre in (("corners", "corners"), ("amarillas", "tarjetas")):
                        if not f[s] or s not in L.medias:
                            continue
                        h, a, _, _ = L.esperado(s, f["h"], f["a"])
                        E = M.estadistica(nombre, h, a, L.dispersion(s), [], [])
                        rh, ra = f[s]
                        checks = {f"Más {nombre}: local": rh > ra, f"Más {nombre}: visitante": ra > rh}
                        if nombre == "tarjetas":
                            checks["Ambos equipos reciben tarjeta"] = rh > 0 and ra > 0
                        for k, real in checks.items():
                            pr = E[k]
                            tramo = "75%+" if pr >= 0.75 else "60-75%" if pr >= 0.6 else "50-60%" if pr >= 0.5 else None
                            if tramo:
                                c = cubos[(k, tramo)]; c[0] += 1; c[1] += pr; c[2] += real
        print(f"{lg} listo")
    print(f"\n{'mercado':36} {'tramo':>7} {'partidos':>8} {'prometido':>10} {'real':>7} {'desvío':>8}")
    for (k, t), (n, sp, ac) in sorted(cubos.items()):
        if n >= 40:
            print(f"{k:36} {t:>7} {n:8d} {sp / n:10.1%} {ac / n:7.1%} {ac / n - sp / n:+8.1%}")


if __name__ == "__main__":
    main()
