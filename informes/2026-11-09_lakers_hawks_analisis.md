# NBA · LA Lakers @ Atlanta Hawks · 9/11/2026 (State Farm Arena)

Datos: `data/2026-11-09_lakers_hawks_nba.json` (cada dato con su fuente). Simulación completa:
`informes/2026-11-09_lakers_hawks_simulacion.md` (`python3 simulador_nba.py data/2026-11-09_lakers_hawks_nba.json`).
Cuotas: bet365, capturas del usuario a las 3:30 p. m.

## 1. Contexto verificado

| | Lakers | Hawks |
|---|---|---|
| Récord | 10-2 (Yahoo, tras ganar 121-116 en Detroit el 8/11) | 7-4 (BBRef + Wikipedia) |
| Racha | 6 victorias | 4 victorias |
| Ritmo (posesiones) | 99.8 (14.º) | 102.6 (3.º) |
| Rating ofensivo | 122.2 (1.º) | 115.6 (12.º) |
| Rating defensivo | 114.5 (20.º) | 112.5 (12.º) |
| Puntos a favor / en contra | — / 114.3 | 118.6 / 115.5 |
| Calendario | **2.º partido de un back-to-back** (anoche en Detroit) | descansado |

## 2. Bajas (parte oficial de las 13:00 ET)

**Lakers**: Quentin Grimes BAJA (dedo). **Austin Reaves DUDA** (enfermedad, tras 43 puntos en 37 min anoche).
**Luka Doncic juega**: fuera del parte tras perderse Detroit por molestias lumbares (2.ª ausencia del año por la espalda).

**Hawks**: Jock Landale DUDA (cadera, fuera desde el 31/10). BAJAS: Asa Newell (dedo del pie), Mouhamed Gueye (pie),
Henri Veesaar (cruzado, toda la temporada), Keshon Gilbert y Kristaps Porzingis (ESPN calcula que vuelve el 2/1).

⚠️ No encontré la situación de Trae Young en noviembre de 2026 y no aparece en los props de bet365. No doy nada por supuesto.

## 3. Jugadores (temporada 2026-27 + últimos 5 de bet365)

| Jugador | Pts | Reb | Ast | Últimos 5 (pts) | Nota |
|---|---|---|---|---|---|
| Luka Doncic (LAL) | 40.1 | 7.8 | 7.7 | 37 45 42 40 53 | máximo anotador de la NBA; espalda |
| Austin Reaves (LAL) | 23.5 | — | — | 19 27 21 25 43 | duda por enfermedad |
| Walker Kessler (LAL) | — | 10.4 | — | 16 15 15 16 12 | mejor reboteador de LAL (16 reb anoche) |
| Jalen Johnson (ATL) | 19.8 | 8.8 | 7.6 | 21 12 17 13 30 | 30-7-6 en el último partido |
| N. Alexander-Walker (ATL) | 22.1 | — | — | 12 34 26 28 20 | máximo anotador de ATL |
| Onyeka Okongwu (ATL) | 13.5 | 8.0 | — | 6 13 14 22 16 | pívot titular mientras falte Landale |
| Dyson Daniels (ATL) | 9.8 | 6.9 | — | 8 6 8 13 9 | 10 reb y 7 ast en el último partido |
| CJ McCollum (ATL) | 12.9 | — | — | 14 13 15 4 9 | |

**Rebotes**: en tus capturas no hay cuotas de rebotes, así que no hay pick. Si las abres, la referencia es Kessler 10.4,
Johnson 8.8, Okongwu 8.0, Doncic 7.8 y Daniels 6.9 por partido.

## 4. Simulador del partido (200.000 simulaciones)

- **Mercado bet365 (sin margen)**: Hawks por 1.3 puntos, total 235.9 (desviación 17.8).
- **Modelo de ratings**: Lakers por 2.3 puntos, total 235.2 (sin contar cancha ni back-to-back).
- **Mezcla (60% mercado)**: Lakers 117.9 - Hawks 117.7 → **partido 50/50, total ~236**.

| Mercado | Prob. | Cuota justa | bet365 | Valor |
|---|---|---|---|---|
| Gana Lakers | 50.4% | 1.98 | 2.07 | +4.4% |
| Gana Hawks | 49.6% | 2.02 | 1.78 | −11.7% |
| Lakers +1.5 | 53.0% | 1.89 | 1.91 | +1.2% |
| Lakers +4.5 | 60.6% | 1.65 | 1.58 | −4.2% |
| Más de 235.5 | 51.1% | 1.96 | 1.87 | −4.4% |
| Menos de 235.5 | 48.9% | 2.05 | 1.94 | −5.2% |
| Lakers más de 117.5 | 52.2% | 1.92 | 1.86 | −3.0% |
| Hawks menos de 118.5 | 51.5% | 1.94 | 1.86 | −4.3% |

**Lectura**: el pequeño valor de los Lakers sale de un modelo que no cuenta la cancha ni el back-to-back, y Reaves está en duda.
El filtro del analista lo descarta: **no hay pick de ganador, spread ni total**. Ninguna línea de partido llega al 75%.

## 5. Picks por nivel de riesgo (props de jugador)

La probabilidad es la del modelo: 50% promedio de temporada y 50% últimos 5. Si el jugador no juega, bet365 suele anular
el prop (revisa las reglas en tu cuenta). Una sola lectura: Doncic con mucho volumen, ATL anotando por fuera ante la 20.ª defensa.

| Riesgo | Pick | Cuota | Prob. | Cuota justa | Últimos 5 | Stake |
|---|---|---|---|---|---|---|
| 🟢 BAJO | **Luka Doncic 30+ puntos** | 1.27 | 91% | 1.10 | 5/5 | 1 u |
| 🟢 BAJO (alternativa sin Doncic) | Dyson Daniels 3+ asistencias | 1.13 | 91% | 1.10 | 5/5 | 1 u |
| 🟡 MEDIO | **Nickeil Alexander-Walker 20+ puntos** | 1.95 | 67% | 1.50 | 4/5 | 0.75 u |
| 🟡 MEDIO | Luka Doncic 5+ triples | 1.90 | 71% | 1.42 | 5/5 | 0.75 u |
| 🔴 ALTO | **Nickeil Alexander-Walker 4+ triples** | 2.25 | 49% | 2.05 | 3/5 | 0.5 u |

Avisos honestos:
1. **Los valores tan altos de los props de Doncic indican riesgo**: bet365 paga 35+ a 1.74 (55%) y el modelo dice 79%.
   La diferencia es la espalda: si se resiente y sale antes, se pierde todo. Por eso el pick bajo es 30+, no 35+.
   Con 30+ en 5 de 5 y 40.1 de media, solo falla si juega pocos minutos.
2. No metas Doncic 30+ y Doncic 5+ triples en la misma combinada: dependen de lo mismo (su espalda).
3. Reaves: no lo juegues hasta que confirmen que juega. Si es baja, sube el uso de Doncic.
4. Descartados: Ziaire Williams 3+ y 4+ triples, y Luguentz Dort 3+ triples. El modelo les da mucho valor, pero solo con 5 partidos
   y sin promedio de temporada verificado; además, las cuotas de más de 3.5 están fuera por la regla de Getafe.
5. Datos de una sola fuente (⚠️): ritmo y ratings de ATL y el récord 10-2 de LAL. Con 11-12 partidos, la muestra es corta.
