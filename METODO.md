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

## 9. Protocolo del pick de RIESGO MEDIO (auditoría del 9/11/2026, `auditar_medios.py`)
Registro: medios 8/16 (50%) frente a 9.4 esperados. Prueba con ~12.000 casos reales (7 ligas, 2025-27):
- Franja 50-62%: se cumple el 56% -> es una moneda al aire; ya no es "medio" (pasa a alto o se descarta).
- Franja 62-77%: se cumple el 70%; si los datos de la temporada de AMBOS equipos lo confirman (>= 65%): 72%.
- Mejores mercados: Local o empate (77.7% real vs 71.8% prometido), Visitante o empate (72.0 vs 69.7),
  Menos de 3.5 (72.6 vs 70.3), Más de 1.5 (74.2 vs 73.0), equipo marca.
- Peores: Menos de 2.5 (57.3 vs 64.3) y Ambos marcan sí (59.6 vs 64.6) cuando los datos no confirman.
Reglas del medio:
1. Probabilidad del mercado 62-77% Y datos de temporada de ambos equipos >= 65%.
2. Mercados: doble oportunidad, hándicap +0.5/+1.0, menos de 3.5, más de 1.5, equipo marca, tarjetas
   (con datos). No: ambos marcan, menos/más de 2.5 (salvo datos >= 70% en ambos y en el H2H), resultado exacto.
3. Misma lectura que el pick bajo: el medio es "un paso más" en la misma dirección (bajo DC -> medio gana, etc.).
4. Ligas sin datos completos: sin pick medio (registro 1/4).
5. Precio: bet365 no más de un 5% por debajo de la cuota justa.
Aplicado al registro: los medios que habrían pasado ganaron 4/6; los que habría quitado, 4/10.

## 10. Lección Técnico-Manta (9/11/2026): el 80% de datos es OBLIGATORIO
Se dio como bajo "Técnico o empate" con mercado 85% pero datos de 75% (6/8 en casa), en liga sin datos
completos y con Manta ganador del último cruce. Perdió 1-2. Si los datos no llegan al 80%, NO es bajo,
aunque el mercado diga 85%: se baja a medio (si cumple §9) o se queda sin pick.

## 11. Lección Luqueño-2 de Mayo (3-0, 9/11/2026): ligas sin datos
Bajo "2 de Mayo +1.5" con mercado 85% y solo 6 partidos de local encontrados; Luqueño venía de ganar 5-0
y peleaba el descenso. Perdió. En ligas sin datos completos, el pick bajo exige además:
- al menos 10 partidos de la temporada encontrados y verificados del equipo clave (no 6);
- que el rival NO llegue con racha fuerte reciente ni con necesidad máxima (descenso/título) contra el pick.
Si no se cumple, no hay pick.

## 12. Primero los DATOS de la temporada, después las cuotas (petición del usuario, 10/11/2026)
Orden de trabajo en ligas con base de datos (football-data: Premier, Championship, LaLiga, LaLiga2, Bundesliga,
2. Bundesliga, Serie A, Eredivisie, Ligue 1, y otras de la misma web):
1. `python3 perfil_equipos.py --liga X --local A --visitante B`: ~50 mercados (resultado, hándicap, goles,
   goles por equipo, mitades, corners, tarjetas, remates a puerta) contados en los partidos REALES de la
   temporada: local en casa / todos / últimos 6 y visitante fuera / todos / últimos 6.
2. Candidatos = mercados que se cumplen en TODAS esas columnas (>= 80% bajo, 65-80% medio), del tipo que sea.
3. Solo entonces se mira la cuota de bet365 (precio) y las bajas/contexto.
Comprobación con Las Palmas-Eldense: por datos salían "Más de 3.5 tarjetas" (83%) y "Corners Eldense más de 3.5"
(83%) como bajos, y Eldense +1.5 solo 67%; las tarjetas se cumplieron (9) y Eldense +1.5 perdió.

## 13. Formato del informe (petición del usuario, 10/11/2026)
Cada partido se entrega como página (artifact) con: pick principal, claves, forma reciente, resultado 1X2,
marcadores más probables, picks ordenados con cuota mínima, por qué sí / por qué no, tabla de datos reales,
tabla de todos los mercados (goles, mitades, tarjetas, corners) con su fuente, jugadores y alineaciones
(solo si hay datos; si no, se dice), calidad de los datos, método y fuentes. Ejemplo: informes/trival_leganes.html.

## 14. Protocolo de CONFIRMACIÓN antes de dar un pick (petición del usuario, 10/11/2026)
El modelo solo ordena ideas; un pick se da cuando lo confirman los datos de varias fuentes:
1. Dato clave del pick en al menos 3 fuentes independientes (base oficial, webs de estadísticas, prensa, web del club).
2. Árbitro designado y su media de tarjetas (para mercados de tarjetas), alineación probable, bajas y sanciones.
3. Forma real de ambos equipos (no solo del favorito) y contexto (motivación, rotaciones, sede).
4. Cuota de bet365 vista (captura del usuario) frente a la cuota mínima.
Si falta alguno de los puntos 1-3, se dice "sin confirmar" y no hay pick, aunque el modelo dé un número alto.

## 15. Kalshi como referencia de precio (10/11/2026)
Kalshi (mercado de predicción, poco margen) sirve para medir si bet365 paga bien. Si los datos y Kalshi coinciden
y bet365 paga igual o más que la cuota justa de Kalshi, el pick sube; si bet365 paga >5% menos que Kalshi, se retira.
Buscar siempre el "Rango de goles" de bet365: a menudo paga más que "Más de X" con casi el mismo riesgo.

## 16. No descartar apuestas: se entregan TODAS (petición del usuario, 12/11/2026)
El usuario quiere ver siempre todas las apuestas analizadas, no solo las que pasan el filtro.
- Cada informe lista TODOS los mercados trabajados como apuestas jugables, ordenados de mayor a menor
  probabilidad, con probabilidad, cuota justa, cuota mínima y stake sugerido. Ninguno se etiqueta "Descartado".
- En vez de descartar, cada apuesta lleva su nivel: bajo / medio / alto / muy alto, y una línea con lo que
  dicen los datos a favor y en contra. El usuario decide cuáles juega.
- Se sigue marcando con claridad cuál es la recomendada y cuáles pagan por debajo de lo justo (el aviso de
  precio se mantiene; lo que cambia es que ya no se ocultan ni se retiran).
- Todas van a `registro/picks.csv` para medir también las que antes se descartaban.
Motivo: el 12/11 varios descartes habrían ganado (Inglaterra 1.25, Ghana 1.05, más de 2.5 en Inglaterra-Croacia).

## 17. Cuota mínima 1.30 y "pick fuerte" (petición del usuario, 13/11/2026)
- La apuesta RECOMENDADA de cada partido debe pagar 1.30 o más. Las de menos de 1.30 se siguen listando (§16),
  pero marcadas "paga menos de 1.30" y nunca como recomendada.
- A 1.30 hay que acertar el 77% para no perder; a 1.50, el 67%. Ninguna apuesta a esas cuotas es segura.
- "Pick fuerte" (lo más parecido a un stakazo; máximo 1 u, nunca más): cuota real vista >= 1.50, probabilidad
  del mercado sin margen >= 67%, datos de AMBOS equipos >= 70% en 10+ partidos verificados, cuota real >= cuota
  justa, y liga con datos completos. Si falta una condición, no hay pick fuerte ese día.
- Lecciones del 12/11: (a) un solo partido no es referencia (Pasto Sub-20); (b) 5 enfrentamientos directos no
  bastan para ir a pocos goles en la altura (Potosí 5-5): en Bolivia "menos de 4.5" no es riesgo bajo;
  (c) "más de 1.5" no es la más segura en partidos sin nada en juego.
