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
