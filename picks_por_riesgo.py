#!/usr/bin/env python3
"""
Picks por nivel de riesgo (bajo / medio / alto) con probabilidades del MERCADO, no del modelo propio.

1. Lee las cuotas medias del mercado (1X2 y +/-2.5) de football-data.co.uk/fixtures.csv y les quita el margen.
2. Busca los goles esperados (local, visitante) que reproducen esas probabilidades (Poisson).
3. Con esos goles calcula todos los mercados: doble oportunidad, cada equipo marca, +/-1.5, +/-3.5, ambos marcan...
4. Da la CUOTA JUSTA de cada uno: si bet365 paga eso o más, la apuesta no tiene desventaja.

El backtest mostró que el mercado está mejor calibrado que mi modelo, así que esta es la base más fiable.

Uso: python3 picks_por_riesgo.py Freiburg Inter Villarreal   (nombre del equipo local tal como aparece en el archivo)
"""
import csv
import io
import math
import sys
import time
import urllib.request

URL = "https://www.football-data.co.uk/fixtures.csv"


def descargar():
    for intento in range(4):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": "predicciones-analisis/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig", errors="ignore"))))
        except OSError:
            time.sleep(2 ** (intento + 1))
    raise SystemExit("No se pudo descargar fixtures.csv")


def pois(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)


def mercados(lh, la):
    r = {}
    m = [[pois(i, lh) * pois(j, la) for j in range(11)] for i in range(11)]
    P = lambda c: sum(m[i][j] for i in range(11) for j in range(11) if c(i, j))
    r["Gana local"] = P(lambda i, j: i > j)
    r["Empate"] = P(lambda i, j: i == j)
    r["Gana visitante"] = P(lambda i, j: i < j)
    r["Local o empate (1X)"] = r["Gana local"] + r["Empate"]
    r["Visitante o empate (X2)"] = r["Gana visitante"] + r["Empate"]
    r["Local marca"] = P(lambda i, j: i > 0)
    r["Visitante marca"] = P(lambda i, j: j > 0)
    r["Más de 1.5 goles"] = P(lambda i, j: i + j >= 2)
    r["Menos de 1.5 goles"] = 1 - r["Más de 1.5 goles"]
    r["Más de 2.5 goles"] = P(lambda i, j: i + j >= 3)
    r["Menos de 2.5 goles"] = 1 - r["Más de 2.5 goles"]
    r["Más de 3.5 goles"] = P(lambda i, j: i + j >= 4)
    r["Menos de 3.5 goles"] = 1 - r["Más de 3.5 goles"]
    r["Menos de 4.5 goles"] = P(lambda i, j: i + j <= 4)
    r["Ambos marcan: sí"] = P(lambda i, j: i > 0 and j > 0)
    r["Ambos marcan: no"] = 1 - r["Ambos marcan: sí"]
    r["Local gana por 2+"] = P(lambda i, j: i - j >= 2)
    r["Visitante gana por 2+"] = P(lambda i, j: j - i >= 2)
    return r


def ajustar(p1, px, p2, pover):
    mejor = None
    for a in range(5, 401, 5):
        for b in range(5, 401, 5):
            lh, la = a / 100, b / 100
            r = mercados(lh, la)
            e = ((r["Gana local"] - p1) ** 2 + (r["Empate"] - px) ** 2 + (r["Gana visitante"] - p2) ** 2
                 + (r["Más de 2.5 goles"] - pover) ** 2)
            if mejor is None or e < mejor[0]:
                mejor = (e, lh, la)
    return mejor[1], mejor[2]


def sin_margen(*c):
    inv = [1 / float(x) for x in c]
    return [x / sum(inv) for x in inv]


def riesgo(p):
    return "BAJO" if p >= 0.75 else "MEDIO" if p >= 0.50 else "ALTO"


def main(locales):
    filas = descargar()
    for r in filas:
        if r["HomeTeam"] not in locales:
            continue
        p1, px, p2 = sin_margen(r["AvgH"], r["AvgD"], r["AvgA"])
        po, _ = sin_margen(r["Avg>2.5"], r["Avg<2.5"])
        lh, la = ajustar(p1, px, p2, po)
        res = mercados(lh, la)
        b365 = {"Gana local": r["B365H"], "Empate": r["B365D"], "Gana visitante": r["B365A"],
                "Más de 2.5 goles": r["B365>2.5"], "Menos de 2.5 goles": r["B365<2.5"]}
        print(f"\n=== {r['HomeTeam']} - {r['AwayTeam']} ({r['Date']} {r['Time']} UK) | goles esperados {lh:.2f} - {la:.2f}")
        print(f"{'mercado':26} {'prob.':>6} {'cuota justa':>11} {'b365':>6} {'ventaja':>8}  riesgo")
        for k, p in sorted(res.items(), key=lambda x: -x[1]):
            c = b365.get(k)
            v = f"{p * float(c) - 1:+8.1%}" if c else " " * 8
            print(f"{k:26} {p:6.1%} {1 / p:11.2f} {c or '':>6} {v}  {riesgo(p)}")


if __name__ == "__main__":
    main(set(sys.argv[1:]) or {"Freiburg", "Inter", "Villarreal"})
