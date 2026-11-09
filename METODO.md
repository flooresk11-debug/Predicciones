# Método de análisis (versión acordada el 9/11/2026)

Sin APIs de pago. Datos de **búsquedas en plataformas públicas** + datos oficiales descargables + simulador calibrado.

## 1. Fuentes por orden de uso
| Fuente | Cómo se usa | Para qué |
|---|---|---|
| football-data.co.uk (descarga oficial) | `simulador_real.py`, `picks_por_riesgo.py` | Resultados, tiros, tiros a puerta, corners, tarjetas, árbitro (Premier), cuotas bet365 y media del mercado |
| OpenLigaDB (descarga oficial) | consulta directa | Resultados oficiales Bundesliga y 2. Bundesliga |
| FootyStats, Sofascore, FotMob, StatsHub, Flashscore, ESPN, webs oficiales de ligas y clubes | **búsqueda web** (se leen los resultados públicos, no se extraen datos con programas) | Alineaciones, bajas, árbitro, estadísticas de jugadores, ligas fuera de la base (Colombia, El Salvador...) |
| Prensa deportiva (Marca, AS, Sky, kicker, Infobae...) | búsqueda web | Contexto: presión, rotaciones, calendario |

## 2. Reglas de verificación
- Un dato es **verificado** si coincide en 2 o más fuentes, o si cuadra con la suma de la tabla oficial.
- Un dato de **una sola fuente** se marca ⚠️ y no puede sostener por sí solo un pick de riesgo bajo.
- Si las fuentes se contradicen y no se puede resolver, el dato **no se usa**.
- Nunca se inventa un dato: lo que no se encuentra se dice que falta.

## 3. Cómo se decide cada pick
1. **Lectura única del partido** (por ejemplo: "partido cerrado, local favorito"). Todos los picks del partido van en esa dirección: nunca picks contradictorios.
2. **Probabilidad**: del mercado (cuotas sin margen) para goles y ganador; de las estadísticas calibradas para tarjetas; de los datos de jugador para apuestas de jugador.
3. **Precio**: cada pick lleva su **cuota justa**. Solo se apuesta si bet365 paga eso o más.
4. **Filtro de analista**: si el precio dice "valor" pero los datos lo contradicen (equipo que no marca, rachas, bajas), se descarta (lección de Getafe).
5. **Riesgo**: bajo >= 75%, medio 50-75%, alto < 50%. "Bajo" no es "seguro": se pierde 1 de cada 4-8 veces.

## 4. Gestión
- Stake fijo: bajo 1 u, medio 0.75 u, alto 0.5 u (la mitad en ligas con pocos datos).
- Combinadas: máximo 2 selecciones, de partidos distintos y sin depender de lo mismo.
- Todo pick va a `registro/picks.csv`; `python3 evaluar.py` mide aciertos frente a lo prometido y la rentabilidad.

## 5. Mercados que se trabajan en cada pick (todos calculados con `simulador_real.py`)
Corners (totales, por equipo y quién tiene más) · Ganador · Doble oportunidad · Goles (totales, por equipo,
rango, gol en el 1.er tiempo) · Tarjetas (totales, por equipo, quién tiene más, ambos reciben) · Remates y
remates a puerta (totales, por equipo y quién tiene más) · Hándicap asiático · Ambos marcan · Gana cualquier
mitad · Gana ambas mitades · Marca en ambas mitades.

Cada bloque muestra su **fiabilidad medida con partidos reales** (`validar_mercados.py`, `calibrar.py`).
Los remates totales son NO FIABLES (peor que la media de la liga) y no se usan para picks de riesgo bajo.

## 6. Regla por calidad de liga (tras los resultados del 8/11/2026)
Primer balance real por nivel de datos:
- Ligas con datos completos o mercado líquido (Bundesliga, LaLiga, Serie A, Liga MX): 10/12 picks ganados (esperados 7.6).
- Colombia y El Salvador (sin estadísticas partido a partido, margen de las casas ~11%): 2/9 (esperados 5.2).

Desde ahora, en ligas sin datos completos: **solo picks de riesgo bajo, con la mitad de stake, o sin pick**.
Los picks de riesgo medio y alto quedan reservados a ligas con datos completos.

## 7. Protocolo del pick de RIESGO BAJO (petición del usuario, 9/11/2026)
Objetivo: que el pick de riesgo bajo sea el que MÁS probabilidad tiene de ganar, no el mejor pagado.
Un pick solo es "riesgo bajo" si cumple TODO esto:
1. **Mercado y datos coinciden**: probabilidad >= 78% según las cuotas actuales (sin margen) Y según los datos
   del equipo (se cumplió en >= 80% de sus partidos de la temporada y en sus últimos 5-10).
2. **Mercados amplios**, que no dependen de un solo gol: equipo marca, más de 1.5, menos de 4.5,
   doble oportunidad del favorito claro, ambos reciben tarjeta. Nunca menos de 2.5, ambos marcan o resultado exacto.
3. **Alineaciones y bajas**: se revisan; si falta un jugador clave para ese mercado (goleador, central,
   portero), el pick se cambia o se elimina. Si no se encuentran, se avisa.
4. **Contexto**: motivación, partido europeo entre semana, rotaciones, clima, movimiento fuerte de cuotas.
5. **Cuotas actuales**: si la cuota se movió en contra del pick desde el análisis, se revisa.
6. **Precio**: no hace falta que tenga valor, pero se descarta si bet365 paga más de un 8% por debajo de lo justo.
Aun así, un 80-85% se pierde 1 de cada 6-7 veces: nunca es seguro, y nunca más de 2 en una combinada.

## 8. Tarjetas: no descartar por precio cuando todo apunta a muchas (lección Las Palmas-Eldense, 9/11/2026)
El modelo esperaba 5 amarillas; bet365 ~6; hubo 9. Los datos de la temporada ya decían 4+ en 20/24.
Si el mercado Y los datos de la temporada (>= 80% de los partidos) coinciden en una línea de tarjetas,
el pick NO se descarta aunque bet365 pague por debajo de la cuota justa del modelo: el modelo se queda corto.
