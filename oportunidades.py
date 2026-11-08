#!/usr/bin/env python3
"""
Busca automáticamente cuotas de bet365 por encima de su precio justo, sin capturas.

Descarga las cuotas de los próximos partidos de football-data.co.uk (se actualizan martes y viernes),
calcula el precio justo con la MEDIA DEL MERCADO sin margen (la referencia validada en
backtest_bet365.py: con umbral +4% dio CLV +2.2% y ROI +4.1% en 1X2) y lista solo las apuestas
donde bet365 paga al menos un 4% más que ese precio justo.

Para cada oportunidad da la CUOTA MÍNIMA: solo tienes que abrir bet365 y comprobar que pagan eso o más.

Uso:
  python3 oportunidades.py                    # todas las ligas
  python3 oportunidades.py --ligas E0 SP1 I1  # solo esas ligas
  python3 oportunidades.py --registrar        # además añade los picks a registro/picks.csv
"""
import argparse
import csv
import io
import os
import urllib.request
from datetime import date, datetime

URL = "https://www.football-data.co.uk/fixtures.csv"
LIGAS = {"E0": "Premier League", "E1": "Championship", "SP1": "LaLiga", "SP2": "LaLiga 2", "I1": "Serie A",
         "I2": "Serie B", "D1": "Bundesliga", "D2": "2. Bundesliga", "F1": "Ligue 1", "F2": "Ligue 2",
         "N1": "Eredivisie", "P1": "Liga Portugal", "B1": "Bélgica", "T1": "Turquía", "G1": "Grecia",
         "SC0": "Escocia"}
MERCADOS = (("1X2", ("H", "D", "A"), ("Gana local", "Empate", "Gana visitante"), True),
            ("+/-2.5", (">2.5", "<2.5"), ("Más de 2.5 goles", "Menos de 2.5 goles"), False))


def num(r, k):
    try:
        v = float(r.get(k) or "")
        return v if v > 1 else None
    except ValueError:
        return None


def descargar():
    req = urllib.request.Request(URL, headers={"User-Agent": "predicciones-analisis/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return list(csv.DictReader(io.StringIO(resp.read().decode("utf-8-sig", errors="ignore"))))


def analizar(filas, umbral, ligas):
    ops = []
    for r in filas:
        if ligas and r["Div"] not in ligas:
            continue
        try:
            if datetime.strptime(r["Date"], "%d/%m/%Y").date() < date.today():
                continue   # partido ya jugado
        except ValueError:
            pass
        for mercado, sufijos, nombres, validado in MERCADOS:
            avg = [num(r, f"Avg{s}") for s in sufijos]
            b365 = [num(r, f"B365{s}") for s in sufijos]
            if None in avg or None in b365:
                continue
            inv = [1 / x for x in avg]
            justa = [x / sum(inv) for x in inv]
            for nombre, pj, c in zip(nombres, justa, b365):
                ev = pj * c - 1
                if ev >= umbral:
                    ops.append(dict(liga=LIGAS.get(r["Div"], r["Div"]), fecha=r["Date"], hora=r.get("Time", ""),
                                    partido=f"{r['HomeTeam']} - {r['AwayTeam']}", apuesta=nombre, mercado=mercado,
                                    cuota=c, prob=pj, ev=ev, minima=round((1 + umbral) / pj, 2),
                                    validado=validado))
    return sorted(ops, key=lambda o: -o["ev"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--umbral", type=float, default=0.04)
    ap.add_argument("--ligas", nargs="*")
    ap.add_argument("--registrar", action="store_true")
    ap.add_argument("--max-cuota", type=float, default=3.5,
                    help="por defecto se excluyen cuotas altas: aciertan ~15%% y exigen cientos de apuestas")
    ap.add_argument("--incluir-largas", action="store_true", help="incluir cuotas > --max-cuota")
    args = ap.parse_args()
    filas = descargar()
    ops = analizar(filas, args.umbral, set(args.ligas or []))
    if not args.incluir_largas:
        largas = [o for o in ops if o["cuota"] > args.max_cuota]
        ops = [o for o in ops if o["cuota"] <= args.max_cuota]
        if largas:
            print(f"(Ocultas {len(largas)} cuotas largas > {args.max_cuota}: usa --incluir-largas para verlas. "
                  "Además, toda oportunidad debe pasar el filtro de análisis antes de apostarse.)")
    print(f"Partidos con cuotas: {len(filas)} | oportunidades (bet365 >= {args.umbral:+.0%} sobre el precio justo): {len(ops)}\n")
    if not ops:
        print("Hoy no hay ventaja en bet365. No apostar también es ganar.")
        return
    print(f"{'fecha':10} {'liga':14} {'partido':38} {'apuesta':20} {'b365':>5} {'justa':>6} {'ventaja':>8} {'mín.':>5}")
    for o in ops:
        marca = "" if o["validado"] else " *"
        print(f"{o['fecha']:10} {o['liga'][:14]:14} {o['partido'][:38]:38} {o['apuesta'][:20]:20} "
              f"{o['cuota']:5.2f} {1 / o['prob']:6.2f} {o['ev']:+8.1%} {o['minima']:5.2f}{marca}")
    print("\nmín. = cuota mínima en bet365 para que siga habiendo ventaja. Si bet365 paga menos, no apuestes.")
    print("* = mercado +/-2.5: pocas apuestas en el backtest, menos probado que el 1X2.")
    print("Las cuotas del archivo pueden tener horas o días: comprueba siempre la cuota actual en bet365.")
    print("Stake: 1 unidad (1-2% del bankroll) por apuesta, sin combinadas.")
    if args.registrar:
        ruta = os.path.join(os.path.dirname(__file__) or ".", "registro", "picks.csv")
        with open(ruta, "a", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            for o in ops:
                w.writerow([date.today().isoformat(), o["partido"], o["apuesta"], "precio-v3", "medio",
                            f"{o['prob']:.3f}", o["cuota"], "pendiente",
                            f"{o['liga']} {o['fecha']}; ventaja {o['ev']:+.1%}; cuota mínima {o['minima']}"])
        print(f"\nAñadidos {len(ops)} picks a registro/picks.csv")


if __name__ == "__main__":
    main()
