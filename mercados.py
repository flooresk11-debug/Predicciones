#!/usr/bin/env python3
"""
Cálculo EXACTO (sin simulación aleatoria) de todos los mercados pedidos, a partir de:
  * goles esperados por equipo (lh, la) y reparto real de goles entre 1.ª y 2.ª mitad de la liga (s1)
  * medias esperadas y dispersión real de corners, tarjetas, remates y remates a puerta por equipo

Mercados: ganador, doble oportunidad, goles totales y por equipo, gol en el 1.er tiempo, rango de goles,
ambos marcan, hándicap asiático, gana cualquier mitad, gana ambas mitades, marca en ambas mitades,
corners / tarjetas / remates / remates a puerta (totales, por equipo y qué equipo tiene más),
ambos equipos reciben tarjeta.
"""
import math

MAXG = 12


def pois(lam, n=MAXG):
    return [math.exp(-lam + k * math.log(lam) - math.lgamma(k + 1)) if lam > 0 else (1.0 if k == 0 else 0.0)
            for k in range(n)]


def nb(media, disp, n=60):
    if disp <= 1.0001:
        return pois(media, n)
    r = media / (disp - 1)
    p = r / (r + media)
    return [math.exp(math.lgamma(k + r) - math.lgamma(r) - math.lgamma(k + 1) + r * math.log(p) + k * math.log(1 - p))
            for k in range(n)]


def resultado(ph, pa):
    """P(local gana), P(empate), P(visitante gana) y distribución de diferencia de goles."""
    dif = {}
    for i, x in enumerate(ph):
        for j, y in enumerate(pa):
            dif[i - j] = dif.get(i - j, 0) + x * y
    g = sum(p for d, p in dif.items() if d > 0)
    e = dif.get(0, 0)
    return g, e, 1 - g - e, dif


def total(ph, pa):
    t = [0.0] * (len(ph) + len(pa))
    for i, x in enumerate(ph):
        for j, y in enumerate(pa):
            t[i + j] += x * y
    return t


def mas_de(dist, linea):
    return sum(p for k, p in enumerate(dist) if k > linea)


def handicap(dif, linea):
    """Hándicap asiático para el LOCAL con línea entera o .5: devuelve (gana, devuelve, pierde)."""
    g = d = 0.0
    for k, p in dif.items():
        v = k + linea
        if v > 0:
            g += p
        elif v == 0:
            d += p
    return g, d, 1 - g - d


def goles(lh, la, s1):
    out = {}
    ph, pa = pois(lh), pois(la)
    g, e, v, dif = resultado(ph, pa)
    tot = total(ph, pa)
    out["Gana local"], out["Empate"], out["Gana visitante"] = g, e, v
    out["Local o empate"], out["Visitante o empate"], out["Local o visitante (sin empate)"] = g + e, v + e, g + v
    for x in (0.5, 1.5, 2.5, 3.5, 4.5):
        out[f"Más de {x} goles"] = mas_de(tot, x)
        out[f"Menos de {x} goles"] = 1 - out[f"Más de {x} goles"]
    for x in (0.5, 1.5, 2.5):
        out[f"Local más de {x} goles"] = mas_de(ph, x)
        out[f"Local menos de {x} goles"] = 1 - out[f"Local más de {x} goles"]
        out[f"Visitante más de {x} goles"] = mas_de(pa, x)
        out[f"Visitante menos de {x} goles"] = 1 - out[f"Visitante más de {x} goles"]
    out["Rango 0-1 goles"] = tot[0] + tot[1]
    out["Rango 2-3 goles"] = tot[2] + tot[3]
    out["Rango 4-5 goles"] = tot[4] + tot[5]
    out["Rango 6+ goles"] = 1 - sum(tot[:6])
    out["Ambos marcan: sí"] = (1 - ph[0]) * (1 - pa[0])
    out["Ambos marcan: no"] = 1 - out["Ambos marcan: sí"]
    # mitades: goles de cada mitad independientes, con el reparto real de la liga
    h1, a1, h2, a2 = pois(lh * s1), pois(la * s1), pois(lh * (1 - s1)), pois(la * (1 - s1))
    g1, e1, v1, _ = resultado(h1, a1)
    g2, e2, v2, _ = resultado(h2, a2)
    out["Gol en el 1.er tiempo"] = 1 - h1[0] * a1[0]
    out["Sin gol en el 1.er tiempo"] = h1[0] * a1[0]
    out["Local gana cualquier mitad"] = 1 - (1 - g1) * (1 - g2)
    out["Visitante gana cualquier mitad"] = 1 - (1 - v1) * (1 - v2)
    out["Local gana ambas mitades"] = g1 * g2
    out["Visitante gana ambas mitades"] = v1 * v2
    out["Local marca en ambas mitades"] = (1 - h1[0]) * (1 - h2[0])
    out["Visitante marca en ambas mitades"] = (1 - a1[0]) * (1 - a2[0])
    ah = {}
    for linea in (-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5):
        ah[linea] = handicap(dif, linea)
    return out, ah


def estadistica(nombre, mh, ma, disp, lineas_total, lineas_eq):
    out = {}
    dh, da = nb(mh, disp), nb(ma, disp)
    tot = total(dh, da)
    for x in lineas_total:
        out[f"{nombre} totales más de {x}"] = mas_de(tot, x)
        out[f"{nombre} totales menos de {x}"] = 1 - out[f"{nombre} totales más de {x}"]
    for x in lineas_eq:
        out[f"{nombre} local más de {x}"] = mas_de(dh, x)
        out[f"{nombre} visitante más de {x}"] = mas_de(da, x)
    g, e, v, _ = resultado(dh, da)
    out[f"Más {nombre}: local"], out[f"Más {nombre}: empate"], out[f"Más {nombre}: visitante"] = g, e, v
    if nombre == "tarjetas":
        out["Ambos equipos reciben tarjeta"] = (1 - dh[0]) * (1 - da[0])
    return out


def cuota_justa_ah(g, d, p):
    """Cuota mínima para no perder a largo plazo en una línea con devolución posible."""
    return 1 + p / g if g > 0 else float("inf")
