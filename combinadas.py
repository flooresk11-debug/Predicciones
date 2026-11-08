#!/usr/bin/env python3
"""
Busca combinadas de 2 favoritos "bien pagados" en bet365, como la ganadora del 8/11
(Villarreal 1.53 + Friburgo 1.61, ambas cuotas por encima de su precio justo).

Regla de cada selección:
  * Favorito con cuota bet365 entre --min y --max (por defecto 1.40-1.75).
  * Precio justo = media del mercado sin margen (referencia validada en backtest_bet365.py).
  * bet365 debe pagar al menos el 98% del precio justo (casi justo o mejor). El "aumento de parlay"
    de bet365, cuando lo hay, suma encima.
Se combinan solo partidos distintos, y se ordenan por valor esperado de la combinada.

Uso: python3 combinadas.py [--min 1.40] [--max 1.75] [--top 5]
"""
import argparse
import csv
import io
import itertools
import time
import urllib.request
from datetime import date, datetime

URL = "https://www.football-data.co.uk/fixtures.csv"


def descargar():
    for i in range(4):
        try:
            req = urllib.request.Request(URL, headers={"User-Agent": "predicciones-analisis/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return list(csv.DictReader(io.StringIO(r.read().decode("utf-8-sig", errors="ignore"))))
        except OSError:
            time.sleep(2 ** (i + 1))
    raise SystemExit("No se pudo descargar fixtures.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", type=float, default=1.40)
    ap.add_argument("--max", type=float, default=1.75)
    ap.add_argument("--precio", type=float, default=0.98, help="bet365 >= este % del precio justo")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()
    legs = []
    for r in descargar():
        try:
            if datetime.strptime(r["Date"], "%d/%m/%Y").date() < date.today():
                continue
            avg = [float(r[k]) for k in ("AvgH", "AvgD", "AvgA")]
            b = [float(r[k]) for k in ("B365H", "B365D", "B365A")]
        except (ValueError, KeyError):
            continue
        inv = [1 / x for x in avg]
        pj = [x / sum(inv) for x in inv]
        for i, eq in ((0, r["HomeTeam"]), (2, r["AwayTeam"])):
            if args.min <= b[i] <= args.max and b[i] * pj[i] >= args.precio:
                legs.append(dict(partido=f"{r['HomeTeam']} - {r['AwayTeam']}", liga=r["Div"], fecha=r["Date"],
                                 hora=r["Time"], equipo=eq, cuota=b[i], p=pj[i], justa=1 / pj[i]))
    print(f"Favoritos bien pagados en bet365 ({args.min}-{args.max}, >= {args.precio:.0%} del precio justo): {len(legs)}")
    for l in sorted(legs, key=lambda x: -x["cuota"] * x["p"]):
        print(f"  {l['fecha']} {l['hora']} {l['liga']:4} {l['partido'][:34]:34} gana {l['equipo'][:16]:16} "
              f"b365 {l['cuota']:.2f} | justa {l['justa']:.2f} | prob {l['p']:.0%}")
    combos = []
    for a, c in itertools.combinations(legs, 2):
        if a["partido"] == c["partido"]:
            continue
        cuota, p = a["cuota"] * c["cuota"], a["p"] * c["p"]
        combos.append((p * cuota - 1, cuota, p, a, c))
    combos.sort(key=lambda x: -x[0])
    print(f"\nMejores combinadas de 2 (sin aumento de parlay; si bet365 lo da, mejor):")
    if not combos:
        print("  Ninguna hoy: no hay dos favoritos bien pagados en partidos distintos.")
    for ev, cuota, p, a, c in combos[:args.top]:
        print(f"  {a['equipo']} ({a['cuota']:.2f}) + {c['equipo']} ({c['cuota']:.2f}) = cuota {cuota:.2f} | "
              f"sale {p:.0%} de las veces | valor {ev:+.1%}")
    print("\nCuota mínima de cada selección = su cuota justa. Si bet365 paga menos, cambia de selección.")


if __name__ == "__main__":
    main()
