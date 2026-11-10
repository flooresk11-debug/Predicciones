#!/usr/bin/env python3
"""
Perfil REAL de temporada de los dos equipos y frecuencia de ~50 mercados en sus partidos.

No usa cuotas: solo partidos jugados (football-data.co.uk, temporada actual).
Para cada mercado del partido (visto como LOCAL / VISITANTE) cuenta en cuántos partidos se cumplió:
  * local: sus partidos en casa de la temporada / todos sus partidos / sus últimos 6
  * visitante: sus partidos fuera / todos / últimos 6
("Local marca" en los partidos del visitante = el visitante encajó.)
Luego lista los mercados donde los DOS equipos lo cumplen con frecuencia (candidatos a pick),
de todos los tipos: goles, resultado, mitades, corners, tarjetas y remates a puerta.

Uso: python3 perfil_equipos.py --liga SP2 --local "Las Palmas" --visitante "Eldense" [--temp 2627]
"""
import argparse

import simulador_real as S


def vista(f, equipo, rol):
    """Devuelve el partido orientado para que `equipo` ocupe el `rol` (L o V) del partido a analizar."""
    es_local = f["h"] == equipo
    girar = (rol == "L") != es_local
    v = {}
    for k in ("goles", "ht", "corners", "amarillas", "tiros_puerta"):
        x = f.get(k)
        v[k] = (x[1], x[0]) if (x and girar) else x
    return v


def mercados():
    """(nombre, grupo, función(v) -> bool o None si falta el dato)."""
    G = lambda v: v["goles"]
    def mitad(fn):
        def f(v):
            if not v["ht"]:
                return None
            (h1, a1), (gh, ga) = v["ht"], G(v)
            return fn(h1, a1, gh - h1, ga - a1)
        return f
    def est(nombre, fn):
        return lambda v: None if not v[nombre] else fn(*v[nombre])
    M = [
        ("Gana local", "resultado", lambda v: G(v)[0] > G(v)[1]),
        ("Empate", "resultado", lambda v: G(v)[0] == G(v)[1]),
        ("Gana visitante", "resultado", lambda v: G(v)[0] < G(v)[1]),
        ("Local o empate", "resultado", lambda v: G(v)[0] >= G(v)[1]),
        ("Visitante o empate", "resultado", lambda v: G(v)[0] <= G(v)[1]),
        ("Local o visitante (sin empate)", "resultado", lambda v: G(v)[0] != G(v)[1]),
        ("Local no pierde por 2+ (visit. -1.5)", "hándicap", lambda v: G(v)[1] - G(v)[0] < 2),
        ("Visitante no pierde por 2+ (+1.5)", "hándicap", lambda v: G(v)[0] - G(v)[1] < 2),
        ("Más de 1.5 goles", "goles", lambda v: sum(G(v)) >= 2),
        ("Más de 2.5 goles", "goles", lambda v: sum(G(v)) >= 3),
        ("Menos de 2.5 goles", "goles", lambda v: sum(G(v)) <= 2),
        ("Menos de 3.5 goles", "goles", lambda v: sum(G(v)) <= 3),
        ("Menos de 4.5 goles", "goles", lambda v: sum(G(v)) <= 4),
        ("Ambos marcan: sí", "goles", lambda v: min(G(v)) > 0),
        ("Ambos marcan: no", "goles", lambda v: min(G(v)) == 0),
        ("Local marca", "goles equipo", lambda v: G(v)[0] > 0),
        ("Local marca 2+", "goles equipo", lambda v: G(v)[0] >= 2),
        ("Visitante marca", "goles equipo", lambda v: G(v)[1] > 0),
        ("Visitante marca 2+", "goles equipo", lambda v: G(v)[1] >= 2),
        ("Local menos de 1.5 goles", "goles equipo", lambda v: G(v)[0] <= 1),
        ("Visitante menos de 1.5 goles", "goles equipo", lambda v: G(v)[1] <= 1),
        ("Gol en el 1.er tiempo", "mitades", mitad(lambda h1, a1, h2, a2: h1 + a1 > 0)),
        ("Gol en el 2.º tiempo", "mitades", mitad(lambda h1, a1, h2, a2: h2 + a2 > 0)),
        ("Local gana cualquier mitad", "mitades", mitad(lambda h1, a1, h2, a2: h1 > a1 or h2 > a2)),
        ("Visitante gana cualquier mitad", "mitades", mitad(lambda h1, a1, h2, a2: a1 > h1 or a2 > h2)),
        ("Local marca en ambas mitades", "mitades", mitad(lambda h1, a1, h2, a2: h1 > 0 and h2 > 0)),
        ("Visitante marca en ambas mitades", "mitades", mitad(lambda h1, a1, h2, a2: a1 > 0 and a2 > 0)),
        ("2.º tiempo con más goles", "mitades", mitad(lambda h1, a1, h2, a2: h2 + a2 > h1 + a1)),
    ]
    for x in (7.5, 8.5, 9.5, 10.5):
        M.append((f"Corners más de {x}", "corners", est("corners", lambda h, a, x=x: h + a > x)))
    for x in (10.5, 11.5, 12.5):
        M.append((f"Corners menos de {x}", "corners", est("corners", lambda h, a, x=x: h + a < x)))
    M += [("Más corners: local", "corners", est("corners", lambda h, a: h > a)),
          ("Más corners: visitante", "corners", est("corners", lambda h, a: a > h)),
          ("Corners local más de 3.5", "corners", est("corners", lambda h, a: h > 3.5)),
          ("Corners local más de 4.5", "corners", est("corners", lambda h, a: h > 4.5)),
          ("Corners visitante más de 2.5", "corners", est("corners", lambda h, a: a > 2.5)),
          ("Corners visitante más de 3.5", "corners", est("corners", lambda h, a: a > 3.5))]
    for x in (2.5, 3.5, 4.5, 5.5):
        M.append((f"Tarjetas más de {x}", "tarjetas", est("amarillas", lambda h, a, x=x: h + a > x)))
    M += [("Tarjetas menos de 5.5", "tarjetas", est("amarillas", lambda h, a: h + a < 5.5)),
          ("Ambos reciben tarjeta", "tarjetas", est("amarillas", lambda h, a: h > 0 and a > 0)),
          ("Más tarjetas: local", "tarjetas", est("amarillas", lambda h, a: h > a)),
          ("Más tarjetas: visitante", "tarjetas", est("amarillas", lambda h, a: a > h)),
          ("Local 2+ tarjetas", "tarjetas", est("amarillas", lambda h, a: h >= 2)),
          ("Visitante 2+ tarjetas", "tarjetas", est("amarillas", lambda h, a: a >= 2))]
    for x in (6.5, 7.5, 8.5):
        M.append((f"Remates a puerta más de {x}", "remates a puerta", est("tiros_puerta", lambda h, a, x=x: h + a > x)))
    M += [("Remates a puerta local más de 3.5", "remates a puerta", est("tiros_puerta", lambda h, a: h > 3.5)),
          ("Remates a puerta visitante más de 2.5", "remates a puerta", est("tiros_puerta", lambda h, a: a > 2.5)),
          ("Más remates a puerta: local", "remates a puerta", est("tiros_puerta", lambda h, a: h > a)),
          ("Más remates a puerta: visitante", "remates a puerta", est("tiros_puerta", lambda h, a: a > h))]
    return M


def tasa(partidos, equipo, rol, fn):
    s = n = 0
    for f in partidos:
        r = fn(vista(f, equipo, rol))
        if r is None:
            continue
        n += 1; s += bool(r)
    return (s, n)


def fmt(t):
    s, n = t
    return f"{s:2d}/{n:<2d} {s / n:4.0%}" if n else "   -     "


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--liga", required=True)
    ap.add_argument("--local", required=True)
    ap.add_argument("--visitante", required=True)
    ap.add_argument("--temp", default="2627")
    a = ap.parse_args()
    filas = S.cargar(a.liga, a.temp, max_horas=12)
    equipos = sorted({f["h"] for f in filas} | {f["a"] for f in filas})
    for e in (a.local, a.visitante):
        if e not in equipos:
            raise SystemExit(f"'{e}' no está en {a.liga} {a.temp}. Equipos: {', '.join(equipos)}")
    L, V = a.local, a.visitante
    l_todos = [f for f in filas if L in (f["h"], f["a"])]
    v_todos = [f for f in filas if V in (f["h"], f["a"])]
    l_casa = [f for f in l_todos if f["h"] == L]
    v_fuera = [f for f in v_todos if f["a"] == V]
    print(f"# {L} (local) vs {V} (visitante) — {a.liga} {a.temp}, solo partidos jugados")
    print(f"{L}: {len(l_todos)} partidos ({len(l_casa)} en casa) | {V}: {len(v_todos)} ({len(v_fuera)} fuera)\n")
    for nombre, x in ((L, l_todos[-6:]), (V, v_todos[-6:])):
        print(f"Últimos 6 de {nombre}: " + " · ".join(
            f"{f['h']} {f['goles'][0]:.0f}-{f['goles'][1]:.0f} {f['a']}" for f in x))
    print()
    cab = f"{'mercado':40} {'LOCAL en casa':>13} {'LOCAL todos':>13} {'LOCAL últ.6':>13} | {'VISIT. fuera':>13} {'VISIT. todos':>13} {'VISIT. últ.6':>13} | {'mín.':>5}"
    candidatos = []
    grupo_actual = None
    for nombre, grupo, fn in mercados():
        tl = [tasa(x, L, "L", fn) for x in (l_casa, l_todos, l_todos[-6:])]
        tv = [tasa(x, V, "V", fn) for x in (v_fuera, v_todos, v_todos[-6:])]
        if tl[1][1] == 0 or tv[1][1] == 0:
            continue
        if grupo != grupo_actual:
            print(f"\n## {grupo.upper()}\n{cab}")
            grupo_actual = grupo
        validos = [s / n for s, n in tl + tv if n >= 3]
        minimo = min(validos) if validos else 0
        print(f"{nombre:40} {fmt(tl[0]):>13} {fmt(tl[1]):>13} {fmt(tl[2]):>13} | "
              f"{fmt(tv[0]):>13} {fmt(tv[1]):>13} {fmt(tv[2]):>13} | {minimo:5.0%}")
        candidatos.append((minimo, nombre, grupo))
    print("\n## CANDIDATOS POR DATOS (se cumplió en TODAS las columnas al menos este %)")
    print("Bajo >= 80% · Medio 65-80%. Después se comprueba el precio de bet365 y las bajas.")
    for m, nombre, grupo in sorted(candidatos, reverse=True):
        if m >= 0.65:
            print(f"  {'BAJO ' if m >= 0.8 else 'MEDIO'} {m:4.0%}  {nombre} ({grupo})")


if __name__ == "__main__":
    main()
