# Predicciones

Análisis de partidos de fútbol con datos reales y auditados.

- `data/*.json`: datos de cada partido. Cada dato lleva su fuente y un estado
  (`VERIFICADO`, `UNA_FUENTE`, `CONFLICTO`, `NO_DISPONIBLE`). Lo que no se pudo verificar no se rellena.
- `simulador.py`: audita que los resultados sumen exactamente la tabla publicada y luego simula
  (Poisson exacto + Monte Carlo con semilla fija, sin dependencias externas).
- `informes/`: informes generados.

```bash
python3 simulador.py data/2026-11-08_koln_leverkusen.json --salida informes/2026-11-08_koln_leverkusen_simulacion.md
python3 simulador.py data/2026-11-08_koln_leverkusen.json --peso-condicion 0.5   # prueba de sensibilidad
```

El script termina con código 1 si la auditoría encuentra inconsistencias.

## Metodología v2 (tras la auditoría del 8/11/2026)

1. **Anclaje al mercado**: el 1X2 del modelo se mezcla con las cuotas sin margen (60% mercado por defecto,
   `--peso-mercado`). Con 8-13 partidos por equipo el mercado sabe más que el modelo.
2. **Filtro de picks**: solo hay pick si hay cuota publicada, valor esperado >= +5% (`--umbral-valor`),
   datos de calidad alta y el modelo no discrepa más de 15 puntos del mercado. Máximo 2 picks por partido.
3. **Sin riesgo "bajo" puro**: el mejor nivel posible es "bajo-medio" (prob. >= 75% y datos de calidad alta).
4. **Remates y tarjetas** solo son aptos para pick si hay datos del rival o del árbitro, no solo del propio equipo.
5. **Registro obligatorio**: cada pick va a `registro/picks.csv`; `python3 evaluar.py` mide aciertos,
   calibración (Brier) y ROI.

## Backtest con datos reales (8.390 partidos, 5 ligas, 2021/22-2025/26)

`./descargar_historico.sh && python3 backtest.py` — sin mirar el futuro: cada partido se predice solo con los anteriores.

Resultados clave:
- Los picks de probabilidad ~80% (más de 1.5, "X marca") están bien calibrados: aciertan ~82%. Pierden 1 de cada 5;
  combinarlos multiplica el riesgo.
- Ningún modelo propio (goles, tiros a puerta, con o sin anclaje) gana al mercado: ROI -6% a -13% y CLV negativo.
- La única señal de ventaja real es de precio: apostar cuando la mejor cuota disponible supera el precio justo
  de Pinnacle (casa "afilada") da CLV positivo (+3.8% a +3.9%). Esa es la base del método v3.

## Oportunidades en bet365 sin capturas (`oportunidades.py`)

`python3 oportunidades.py` descarga las cuotas de los próximos partidos (football-data.co.uk, se actualizan
martes y viernes) y lista solo las apuestas donde bet365 paga al menos un 4% más que el precio justo
(media del mercado sin margen). Da la **cuota mínima**: abres bet365, y si paga eso o más, hay apuesta.

Validación (`python3 backtest_bet365.py`): media del mercado con umbral +4% → 275 apuestas, ROI +4.1%,
CLV +2.2% en 1X2; Betfair Exchange como referencia NO funciona (CLV negativo).
