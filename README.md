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
