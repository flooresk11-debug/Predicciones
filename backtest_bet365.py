#!/usr/bin/env python3
"""
¿Qué referencia sirve para encontrar cuotas de bet365 por encima de su precio justo?

Para cada partido histórico (football-data.co.uk), toma el precio justo de una referencia
(cuotas sin margen) y apuesta 1 unidad en bet365 cuando: prob_justa * cuota_bet365 - 1 >= umbral.
Mide rentabilidad (ROI) y CLV contra el cierre de Pinnacle sin margen (la mejor señal de ventaja real).

Referencias probadas: Pinnacle apertura (PS), Betfair Exchange (BFE) y media del mercado (Avg).
Mercados: 1X2 y más/menos 2.5.
"""
import csv
import glob
from collections import defaultdict

REFS = {
    "Pinnacle": (("PSH", "PSD", "PSA"), ("P>2.5", "P<2.5")),
    "Betfair Exchange": (("BFEH", "BFED", "BFEA"), ("BFE>2.5", "BFE<2.5")),
    "Media del mercado": (("AvgH", "AvgD", "AvgA"), ("Avg>2.5", "Avg<2.5")),
}
B365 = (("B365H", "B365D", "B365A"), ("B365>2.5", "B365<2.5"))
CIERRE = (("PSCH", "PSCD", "PSCA"), ("PC>2.5", "PC<2.5"))
UMBRALES = (0.0, 0.02, 0.04, 0.06)


def num(r, k):
    try:
        v = float(r.get(k) or "")
        return v if v > 1 else None
    except ValueError:
        return None


def justas(r, cols):
    c = [num(r, k) for k in cols]
    if None in c:
        return None
    inv = [1 / x for x in c]
    return [x / sum(inv) for x in inv]


def main():
    filas = []
    for f in glob.glob("data/historico/*.csv"):
        for r in csv.DictReader(open(f, encoding="utf-8-sig", errors="ignore")):
            if r.get("FTHG"):
                filas.append(r)
    res = defaultdict(lambda: dict(n=0, ben=0.0, clv=0.0, nclv=0))
    for r in filas:
        hg, ag = int(r["FTHG"]), int(r["FTAG"])
        gana = ([hg > ag, hg == ag, hg < ag], [hg + ag >= 3, hg + ag <= 2])
        for nom, ref in REFS.items():
            for m in (0, 1):
                pj = justas(r, ref[m])
                cierre = justas(r, CIERRE[m])
                if not pj:
                    continue
                for i, k in enumerate(B365[m]):
                    c = num(r, k)
                    if not c:
                        continue
                    ev = pj[i] * c - 1
                    for u in UMBRALES:
                        if ev >= u:
                            x = res[(nom, m, u)]
                            x["n"] += 1
                            x["ben"] += (c - 1) if gana[m][i] else -1
                            if cierre:
                                x["clv"] += c * cierre[i] - 1
                                x["nclv"] += 1
    print("Apostando 1 unidad en bet365 cuando su cuota supera el precio justo de la referencia\n")
    print(f"{'referencia':18} {'mercado':8} {'umbral':>7} {'apuestas':>9} {'beneficio':>10} {'ROI':>7} {'CLV':>7}")
    for nom in REFS:
        for m, et in ((0, "1X2"), (1, "+/-2.5")):
            for u in UMBRALES:
                x = res[(nom, m, u)]
                if x["n"] >= 30:
                    clv = x["clv"] / x["nclv"] if x["nclv"] else float("nan")
                    print(f"{nom:18} {et:8} {u:>+7.0%} {x['n']:9d} {x['ben']:+10.1f} {x['ben'] / x['n']:+7.1%} {clv:+7.1%}")
    print("\nCLV = ventaja de la cuota tomada frente al cierre de Pinnacle sin margen (positivo = ventaja real).")


if __name__ == "__main__":
    main()
