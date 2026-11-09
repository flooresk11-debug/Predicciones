#!/usr/bin/env python3
"""
Auditoría del riesgo MEDIO con partidos reales (2025/26 y 2026/27, 7 ligas):
¿mejora el acierto si, además de la probabilidad del mercado (62-77%), exigimos que los
datos de la temporada de AMBOS equipos lo confirmen (>= 65% de sus partidos previos)?
Se compara también la franja 50-62% (la que más se ha perdido en el registro).
"""
from collections import defaultdict

import mercados as M
import simulador_real as S
import validar_mercados as V

LIGAS = ["E0", "SP1", "D1", "D2", "I1", "N1", "F1"]

# mercado -> (función con el resultado real desde el punto de vista (gf, gc, local?), para el partido)
def eventos(gh, ga):
    return {"Menos de 3.5 goles": gh + ga <= 3, "Más de 1.5 goles": gh + ga >= 2,
            "Menos de 2.5 goles": gh + ga <= 2, "Más de 2.5 goles": gh + ga >= 3,
            "Ambos marcan: sí": gh > 0 and ga > 0, "Ambos marcan: no": not (gh > 0 and ga > 0),
            "Local o empate": gh >= ga, "Visitante o empate": ga >= gh,
            "Local más de 0.5 goles": gh > 0, "Visitante más de 0.5 goles": ga > 0}

def tasa_equipo(previos, eq, k):
    """Frecuencia con la que el evento se dio en los partidos previos del equipo (visto desde ese equipo)."""
    n = s = 0
    for x in previos:
        if eq not in (x["h"], x["a"]) or not x["goles"]:
            continue
        gh, ga = x["goles"]
        loc = x["h"] == eq
        gf, gc = (gh, ga) if loc else (ga, gh)
        # traducir el mercado al punto de vista del equipo
        if k in ("Local o empate", "Visitante o empate"):
            mine = (k == "Local o empate") == (eq == "__LOCAL__")
            ok = gf >= gc
        elif k in ("Local más de 0.5 goles",):
            ok = gf > 0
        elif k in ("Visitante más de 0.5 goles",):
            ok = gf > 0
        else:
            ok = eventos(gh, ga)[k]
        n += 1; s += ok
    return (s / n if n else None), n

def main():
    cubos = defaultdict(lambda: [0, 0.0, 0])
    for lg in LIGAS:
        for temp in ("2526", "2627"):
            act = S.cargar(lg, temp, max_horas=24 * 30)
            for i, f in enumerate(act):
                r = f["row"]
                try:
                    inv = [1 / float(r[k]) for k in ("AvgH", "AvgD", "AvgA")]
                    ou = [1 / float(r[k]) for k in ("Avg>2.5", "Avg<2.5")]
                except (KeyError, ValueError, ZeroDivisionError):
                    continue
                if not f["goles"]:
                    continue
                p = [x / sum(inv) for x in inv]
                lh, la = V.ajustar(p[0], p[1], ou[0] / sum(ou))
                P, _ = M.goles(lh, la, 0.44)
                gh, ga = f["goles"]
                real = eventos(gh, ga)
                prev = act[:i]
                for k, ok in real.items():
                    pr = P[k]
                    if not 0.50 <= pr < 0.77:
                        continue
                    franja = "62-77%" if pr >= 0.62 else "50-62%"
                    # datos: equipo local visto desde el local; visitante desde el visitante
                    if k == "Local o empate":
                        th, nh = tasa_equipo(prev, f["h"], "Local o empate"); ta, na = tasa_equipo(prev, f["a"], "Local o empate")
                        ta = None if ta is None else 1 - ta + _empates(prev, f["a"])  # visitante pierde o empata
                    elif k == "Visitante o empate":
                        ta, na = tasa_equipo(prev, f["a"], "Visitante o empate"); th, nh = tasa_equipo(prev, f["h"], "Visitante o empate")
                        th = None if th is None else 1 - th + _empates(prev, f["h"])
                    elif k == "Local más de 0.5 goles":
                        th, nh = tasa_equipo(prev, f["h"], k); ta, na = _encaja(prev, f["a"])
                    elif k == "Visitante más de 0.5 goles":
                        ta, na = tasa_equipo(prev, f["a"], k); th, nh = _encaja(prev, f["h"])
                    else:
                        th, nh = tasa_equipo(prev, f["h"], k); ta, na = tasa_equipo(prev, f["a"], k)
                    if th is None or ta is None or min(nh, na) < 6:
                        continue
                    datos = "datos confirman (>=65% ambos)" if min(th, ta) >= 0.65 else "datos NO confirman"
                    for clave in ((franja, datos), (franja, "todos"), (franja, k, datos)):
                        c = cubos[clave]; c[0] += 1; c[1] += pr; c[2] += ok
        print(f"{lg} listo")
    print(f"\n{'grupo':75} {'n':>6} {'prometido':>9} {'real':>7}")
    for k, (n, sp, ac) in sorted(cubos.items()):
        if n >= 60:
            print(f"{' | '.join(k):75} {n:6d} {sp / n:9.1%} {ac / n:7.1%}")

def _empates(prev, eq):
    n = e = 0
    for x in prev:
        if eq in (x["h"], x["a"]) and x["goles"]:
            n += 1; e += x["goles"][0] == x["goles"][1]
    return e / n if n else 0

def _encaja(prev, eq):
    n = s = 0
    for x in prev:
        if eq in (x["h"], x["a"]) and x["goles"]:
            gh, ga = x["goles"]; gc = ga if x["h"] == eq else gh
            n += 1; s += gc > 0
    return (s / n if n else None), n

if __name__ == "__main__":
    main()
