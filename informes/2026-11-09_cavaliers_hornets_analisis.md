# NBA · Cleveland Cavaliers @ Charlotte Hornets · 9/11/2026 (Spectrum Center, 19:00 ET)

Datos: `data/2026-11-09_cavaliers_hornets_nba.json`. Simulación completa: `informes/2026-11-09_cavaliers_hornets_simulacion.md`
(`python3 simulador_nba.py data/2026-11-09_cavaliers_hornets_nba.json`). Cuotas: bet365, capturas de las 3:50 p. m.

## 1. Contexto

| | Cavaliers | Hornets |
|---|---|---|
| Récord | 5-5 (perdieron el sábado ante los Knicks) | 3-7, **6 derrotas seguidas** (la última, 80-119 ante Boston) |
| Ritmo de juego | 100.1 (9.º) | 95.4 (**30.º**, el más lento) |
| Ataque (por 100 posesiones) | 115.7 (11.º) | 101.0 (**30.º**) |
| Defensa (por 100 posesiones) | 112.9 (13.º) | 115.6 (23.º) |
| Puntos por partido | 117.0 | 96.3 (30.º) / reciben 110.2 |

## 2. Bajas
**Cavaliers**: Jarrett Allen DUDA (rodilla; se perdió los 2 últimos partidos). BAJAS: Sam Merrill, Jaylon Tyson y Nae'Qwan Tomlin.
**Hornets**: Brandon Miller BAJA (cadera/ingle; ⚠️ NBA.com llegó a ponerlo en duda), Kon Knueppel BAJA, Dennis Schröder BAJA
(⚠️ NBA.com: duda) y Grant Williams BAJA. Moussa Diabaté DUDA. LaMelo Ball ya no está en el equipo (juega en Minnesota).
Sin Miller (unos 22-24 puntos por partido) ni Knueppel, Charlotte pierde a sus dos mejores anotadores exteriores.

## 3. Jugadores (temporada + últimos 5 de bet365)
| Jugador | Pts | Reb | Ast | Últimos 5 (pts) |
|---|---|---|---|---|
| Donovan Mitchell (CLE) | 22.5 | 5.0 | 5.5 | 15 17 27 23 37 |
| Evan Mobley (CLE) | 18.8 | 8.2 | 3.5 | 27 16 16 22 12 |
| James Harden (CLE) | 16.6 | 5.3 | 6.3 | 13 14 19 17 7 |
| Naz Reid (CHA) | 20.5 ⚠️ una fuente | — | — | 12 14 13 28 14 |
| Grayson Allen (CHA) | 15.7-19.6 ⚠️ las fuentes no coinciden | — | — | 5 27 11 22 0 |

**Rebotes**: en tus capturas no hay cuotas de rebotes. Como referencia, Mobley promedia 8.2 y Harden 5.3.

## 4. Simulador del partido
- **Mercado (sin margen)**: Cavs por 8.5 puntos, total 215.2.
- **Modelo de ratings**: Cavs por 8.5 puntos, total 217.6.
- **Mezcla**: Cavs 112.3 - Hornets 103.8.

El modelo y el mercado coinciden en el margen. El total del modelo sale algo más alto, pero los ratings de Charlotte incluyen
partidos con Miller y Knueppel: sin ellos, su ataque será todavía peor. El filtro del analista descarta el más.

| Mercado | Prob. | Justa | bet365 | Valor |
|---|---|---|---|---|
| Gana Cavaliers | 71-74% | 1.35-1.40 | 1.29 | negativo |
| Cavaliers −8.5 | 50.3% | 1.99 | 1.86 | −6.5% |
| Hornets +8.5 | 49.7% | 2.01 | 1.95 | −3.0% |
| Más de 215.5 | 52.1% | 1.92 | 1.92 | 0% |
| Cavaliers más de 102.5 pts | 79.2% | 1.26 | 1.20 | −4.9% |

Conclusión: **sin valor en ganador, spread ni total**. bet365 cobra un 8% de margen en la victoria de Cleveland a 1.29.

## 5. Picks por riesgo
Lectura única: Cleveland controla el partido y su producción pasa por Mitchell y Mobley. Charlotte, sin sus anotadores, tiene muy poco.

| Riesgo | Pick | Cuota | Prob. | Justa | Últimos 5 | Stake |
|---|---|---|---|---|---|---|
| 🟢 BAJO | **Donovan Mitchell 2+ triples** | 1.22 | 81% | 1.23 | 4/5 | 1 u |
| 🟢 BAJO (alternativa de partido) | Cavaliers más de 102.5 puntos | 1.20 | 79% | 1.26 | — | 1 u |
| 🟡 MEDIO | **Evan Mobley 15+ puntos** | 1.44 | 76% | 1.32 | 4/5 | 0.75 u |
| 🟡 MEDIO | Donovan Mitchell 5+ asistencias | 1.80 | 64% | 1.58 | 3/5 | 0.75 u |
| 🔴 ALTO | **Evan Mobley 20+ puntos** | 2.60 | 45% | 2.24 | 2/5 | 0.5 u |

Por qué Mobley: promedia 18.8 puntos, Charlotte tiene a Diabaté en duda y le faltan jugadores interiores (Grant Williams).
Si Jarrett Allen no juega, Mobley tendrá todavía más balones dentro. Confirma la alineación antes de apostar.

Avisos:
1. **Nada de props de los Hornets.** bet365 ya les sube las líneas porque, con tantas bajas, tendrán más balones
   (Naz Reid 2+ triples a 1.27 con un acierto del 45%, Coby White 1+ triple a 1.11). El modelo no puede medir eso y sale negativo en todos.
2. No combines Mobley 15+ y Mobley 20+: dependen del mismo jugador.
3. Jarrett Allen 15+ a 3.05: descartado porque está en duda y uno de sus últimos 5 fue un 0.
4. En un partido que se decide pronto, los titulares de Cleveland pueden jugar menos minutos en el último cuarto.
   Eso perjudica a los "más de" de Mitchell y Mobley. Es el riesgo principal de estos picks.
