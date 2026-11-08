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
