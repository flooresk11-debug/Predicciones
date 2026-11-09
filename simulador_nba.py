#!/usr/bin/env python3
"""
Simulador NBA (partido + jugadores) con datos reales y auditados. Sin dependencias externas.

Entrada: data/<partido>.json con
  - ratings de cada equipo (ritmo, ORtg, DRtg) con su fuente,
  - las escaleras de cuotas de bet365 (spread, total, totales por equipo) tal como salen en la app,
  - props de jugador (puntos, triples, asistencias) con los últimos 5 que muestra bet365,
  - promedios de temporada verificados.

Método:
 1. MERCADO: a cada escalera de bet365 se le quita el margen línea a línea y se ajusta una normal
    (media y desviación). Así sale el reparto real que el mercado espera para el total, el margen y
    los puntos de cada equipo, sin inventar desviaciones.
 2. MODELO DE RATINGS: posesiones = media del ritmo de ambos; puntos = posesiones x media(ORtg propio,
    DRtg rival) / 100. No incluye factor cancha ni back-to-back (el mercado sí): por eso se mezcla
    40% modelo / 60% mercado (regla v2 del proyecto: el mercado está mejor calibrado).
 3. MONTE CARLO (semilla fija): puntos de cada equipo normales correlacionados, con la correlación que
    hace cuadrar a la vez la desviación del total y la del margen del mercado. Empate -> prórroga.
 4. JUGADORES: media = 50% promedio de temporada (si está verificado) + 50% últimos 5 (o solo
    últimos 5 si no hay promedio). Puntos: normal con varianza = max(varianza últimos 5, 2 x media).
    Triples y asistencias: binomial negativa con varianza = max(varianza últimos 5, 1.3 x media).
    Estas varianzas mínimas son SUPUESTOS del modelo (con 5 partidos la varianza muestral es inestable).
 5. Cada selección: probabilidad, cuota justa, cuota bet365, valor esperado y nivel de riesgo
    (bajo >= 75%, medio 50-75%, alto < 50%, como en METODO.md).

Uso: python3 simulador_nba.py data/2026-11-09_lakers_hawks_nba.json --salida informes/xxx.md
"""
import argparse
import json
import math
import random
import statistics as st

N_SIM = 200_000
SEMILLA = 20261109
PESO_MERCADO = 0.6


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def sin_margen(o_mas, o_menos):
    a, b = 1 / o_mas, 1 / o_menos
    return a / (a + b)


def ajustar_normal(puntos):
    """puntos: [(linea, p_mayor)] con p_mayor = P(X > linea). Devuelve (media, sd) por mínimos cuadrados."""
    mejor = None
    lineas = [l for l, _ in puntos]
    for mu10 in range(int(min(lineas) * 10) - 200, int(max(lineas) * 10) + 200, 1):
        mu = mu10 / 10
        for sd10 in range(30, 300, 1):
            sd = sd10 / 10
            err = sum((1 - phi((l - mu) / sd) - p) ** 2 for l, p in puntos)
            if mejor is None or err < mejor[0]:
                mejor = (err, mu, sd)
    return mejor[1], mejor[2], mejor[0]


def escalera(lista, solo_centrales=True):
    """Usa las líneas con ambas cuotas <= 4.0: en las colas el margen distorsiona demasiado."""
    pts = []
    for l, o_mas, o_menos in lista:
        if solo_centrales and (o_mas > 4.0 or o_menos > 4.0):
            continue
        pts.append((l, sin_margen(o_mas, o_menos)))
    return pts


def nb_muestra(rng, media, var):
    """Binomial negativa (mezcla gamma-Poisson). Si var <= media, Poisson."""
    if media <= 0:
        return 0
    if var <= media * 1.0001:
        lam = media
    else:
        k = media ** 2 / (var - media)
        lam = rng.gammavariate(k, media / k)
    # Poisson por inversión (lam pequeño en props)
    L, p, n = math.exp(-lam), 1.0, 0
    if lam > 60:
        return max(0, round(rng.gauss(lam, math.sqrt(lam))))
    while True:
        p *= rng.random()
        if p <= L:
            return n
        n += 1


def riesgo(p):
    return "bajo" if p >= 0.75 else ("medio" if p >= 0.50 else "alto")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datos")
    ap.add_argument("--salida")
    ap.add_argument("--peso-mercado", type=float, default=PESO_MERCADO)
    a = ap.parse_args()
    d = json.load(open(a.datos, encoding="utf-8"))
    b = d["bet365"]
    V, H = d["visitante"], d["local"]
    nV, nH = d["nombres"][V], d["nombres"][H]
    out = []
    w = out.append

    # ---------- 1. mercado ----------
    mu_T, sd_T, e1 = ajustar_normal(escalera(b["total"]))
    # spread: P(LAL cubre con h) = P(D > -h); como "mayor que línea" sobre la variable D usamos línea = -h
    pts_sp = sorted((-h, sin_margen(ol, oa)) for h, ol, oa in b["spread_visitante"] if ol <= 4 and oa <= 4)
    mu_D, sd_D, e2 = ajustar_normal(pts_sp)
    mu_L, sd_L, e3 = ajustar_normal(escalera(b["total_visitante"]))
    if b.get("total_local"):
        mu_A, sd_A, e4 = ajustar_normal(escalera(b["total_local"]))
    else:  # sin escalera del local: se deduce de total y margen
        mu_A, sd_A, e4 = mu_T - mu_L, sd_L, float("nan")

    # ---------- 2. modelo de ratings ----------
    E = d["equipos"]
    poss = (E[V]["ritmo"]["valor"] + E[H]["ritmo"]["valor"]) / 2
    m_L = poss * (E[V]["ortg"]["valor"] + E[H]["drtg"]["valor"]) / 200
    m_A = poss * (E[H]["ortg"]["valor"] + E[V]["drtg"]["valor"]) / 200

    # mercado coherente: medias por equipo desde total y margen (más líquidos), cruzado con totales de equipo
    mk_L = (mu_T + mu_D) / 2 * 0.5 + mu_L * 0.5
    mk_A = (mu_T - mu_D) / 2 * 0.5 + mu_A * 0.5
    pm = a.peso_mercado
    fin_L = pm * mk_L + (1 - pm) * m_L
    fin_A = pm * mk_A + (1 - pm) * m_A

    # correlación que cuadra var(total) y var(margen) del mercado
    sL, sA = sd_L, sd_A
    cov = (sd_T ** 2 - sd_D ** 2) / 4
    rho = max(-0.9, min(0.9, cov / (sL * sA)))

    rng = random.Random(SEMILLA)
    sims = []
    for _ in range(N_SIM):
        z1 = rng.gauss(0, 1)
        z2 = rho * z1 + math.sqrt(1 - rho ** 2) * rng.gauss(0, 1)
        l = round(fin_L + sL * z1)
        at = round(fin_A + sA * z2)
        while l == at:  # prórroga de 5 minutos
            f = 5 / 48
            l += round(rng.gauss(fin_L * f, sL * math.sqrt(f)))
            at += round(rng.gauss(fin_A * f, sA * math.sqrt(f)))
        sims.append((l, at))

    def prob(f):
        return sum(1 for s in sims if f(*s)) / N_SIM

    w(f"# Simulación NBA: {d['partido']} ({d['fecha']})\n")
    w(f"Simulaciones: {N_SIM:,} (semilla {SEMILLA}). Peso del mercado: {pm:.0%}.\n")
    w("## 1. Lo que dice el mercado (bet365 sin margen, normal ajustada)\n")
    w("| Variable | Media | Desv. típica | Error de ajuste |\n|---|---|---|---|")
    w(f"| Total del partido | {mu_T:.1f} | {sd_T:.1f} | {e1:.4f} |")
    w(f"| Margen {nV} − {nH} | {mu_D:+.1f} | {sd_D:.1f} | {e2:.4f} |")
    w(f"| Puntos {nV} | {mu_L:.1f} | {sd_L:.1f} | {e3:.4f} |")
    w(f"| Puntos {nH} | {mu_A:.1f} | {sd_A:.1f} | {e4:.4f} |")
    w("\n## 2. Modelo de ratings (Basketball-Reference)\n")
    w(f"- Posesiones esperadas: {poss:.1f}")
    w(f"- {nV}: {m_L:.1f} pts · {nH}: {m_A:.1f} pts · total {m_L + m_A:.1f} · margen {m_L - m_A:+.1f}")
    w("- No incluye cancha, descansos ni bajas recientes (el mercado sí).")
    w("\n## 3. Mezcla final\n")
    w(f"- {nV} {fin_L:.1f} · {nH} {fin_A:.1f} · total {fin_L + fin_A:.1f} · margen {nV} {fin_L - fin_A:+.1f}")
    w(f"- Correlación entre los puntos de ambos equipos (deducida del mercado): {rho:.2f}\n")

    filas = []

    def sel(mercado, p, cuota, nota=""):
        ev = p * cuota - 1 if cuota else None
        filas.append((mercado, p, cuota, ev, nota))

    p_lal = prob(lambda l, at: l > at)
    sel(f"Ganador: {nV}", p_lal, b["ganador"][V])
    sel(f"Ganador: {nH}", 1 - p_lal, b["ganador"][H])
    for h, ol, oa in b["spread_visitante"]:
        sel(f"Hándicap {nV} {h:+.1f}", prob(lambda l, at, h=h: l + h > at), ol)
        sel(f"Hándicap {nH} {-h:+.1f}", prob(lambda l, at, h=h: at - h > l), oa)
    for t, om, ou in b["total"]:
        po = prob(lambda l, at, t=t: l + at > t)
        sel(f"Total: más de {t}", po, om)
        sel(f"Total: menos de {t}", 1 - po, ou)
    for clave, nombre, idx in (("total_visitante", nV, 0), ("total_local", nH, 1)):
        for t, om, ou in b.get(clave) or []:
            po = prob(lambda l, at, t=t, i=idx: (l, at)[i] > t)
            sel(f"Puntos {nombre}: más de {t}", po, om)
            sel(f"Puntos {nombre}: menos de {t}", 1 - po, ou)

    # ---------- 4. jugadores ----------
    prom = d["promedios_temporada"]
    clave_prom = {"puntos": "pts", "asistencias": "ast", "triples": None}
    jug = []
    rngp = random.Random(SEMILLA + 1)
    w("## 4. Jugadores: media usada por el modelo\n")
    w("| Jugador | Mercado | Últimos 5 | Prom. temporada | Media modelo | Desv. |\n|---|---|---|---|---|---|")
    for mercado in ("puntos", "triples", "asistencias"):
        for nombre, (eq, ult, lineas) in b[mercado].items():
            m5 = st.mean(ult)
            v5 = st.variance(ult)
            k = clave_prom[mercado]
            temp = prom.get(nombre, {}).get(k) if k else None
            media = 0.5 * temp + 0.5 * m5 if temp is not None else m5
            if mercado == "puntos":
                var = max(v5, 2 * media)
                muestras = [rngp.gauss(media, math.sqrt(var)) for _ in range(40_000)]
            else:
                var = max(v5, 1.3 * media)
                muestras = [nb_muestra(rngp, media, var) for _ in range(40_000)]
            w(f"| {nombre} ({eq}) | {mercado} | {' '.join(map(str, ult))} | {temp if temp is not None else '—'} | {media:.1f} | {math.sqrt(var):.1f} |")
            for lin, cuota in lineas.items():
                x = float(lin)
                p = sum(1 for s in muestras if s >= x - (0.5 if mercado == "puntos" else 0)) / len(muestras)
                aciertos = sum(1 for u in ult if u >= x)
                jug.append((f"{nombre} {lin}+ {mercado}", p, cuota, p * cuota - 1, f"últimos 5: {aciertos}/5"))

    w("\n## 5. Todas las selecciones del partido\n")
    w("| Selección | Prob. | Cuota justa | bet365 | Valor | Riesgo |\n|---|---|---|---|---|---|")
    for m, p, c, ev, _ in filas:
        w(f"| {m} | {p:.1%} | {1 / p if p > 0 else float('inf'):.2f} | {c} | {ev:+.1%} | {riesgo(p)} |")
    w("\n## 6. Todas las selecciones de jugadores (si el jugador juega)\n")
    w("| Selección | Prob. | Cuota justa | bet365 | Valor | Últimos 5 | Riesgo |\n|---|---|---|---|---|---|---|")
    for m, p, c, ev, n in jug:
        w(f"| {m} | {p:.1%} | {1 / p if p > 0 else float('inf'):.2f} | {c} | {ev:+.1%} | {n.split(': ')[1]} | {riesgo(p)} |")

    texto = "\n".join(out) + "\n"
    if a.salida:
        open(a.salida, "w", encoding="utf-8").write(texto)
    print(texto)


if __name__ == "__main__":
    main()
