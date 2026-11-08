# Simulación auditada: Crystal Palace vs Liverpool
Premier League 2026/27 - Jornada 10 · 2026-11-08 15:00 CET

## 1. Auditoría de datos
```
OK  Crystal Palace: 9 PJ, 2G 1E 6P, 9:21, 7 pts = coincide con la tabla publicada
    estados de los resultados de Crystal Palace: {'VERIFICADO': 9}
OK  Liverpool: 9 PJ, 4G 3E 2P, 11:9, 15 pts = coincide con la tabla publicada
    estados de los resultados de Liverpool: {'VERIFICADO': 9}
NO_DISPONIBLE tiros_totales: no se usa
NO_DISPONIBLE tiros_a_puerta: no se usa
NO_DISPONIBLE corners: no se usa
EXCLUIDO (conflicto entre fuentes) h2h.historico_total: 28 o 30 duelos según la ventana; no se usa
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): tiros_totales, tiros_a_puerta, corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (Premier League 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Crystal Palace | Total | 9 | 2-1-6 | 9 | 21 | 1.00 | 2.33 | 3.33 | 44.4% | 11.1% | 55.6% | 55.6% |
| Crystal Palace | Local | 4 | 1-0-3 | 6 | 10 | 1.50 | 2.50 | 4.00 | 75.0% | 0.0% | 25.0% | 75.0% |
| Liverpool | Total | 9 | 4-3-2 | 11 | 9 | 1.22 | 1.00 | 2.22 | 33.3% | 44.4% | 33.3% | 44.4% |
| Liverpool | Visitante | 4 | 3-1-0 | 7 | 3 | 1.75 | 0.75 | 2.50 | 50.0% | 50.0% | 0.0% | 50.0% |

## 3. Modelo
- Goles esperados (global): Crystal Palace 1.00 · Liverpool 1.78
- Goles esperados (local en casa / visitante fuera): Crystal Palace 1.12 · Liverpool 2.12
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- **λ final: Crystal Palace 1.04 · Liverpool 1.90** (total esperado 2.94)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 20.6% · X 22.3% · 2 57.1% · BTTS 55.0% · +2.5 56.2%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 20.5% | 4.89 |
| X | 22.2% | 4.51 |
| 2 | 57.3% | 1.74 |
| 1X | 42.7% | 2.34 |
| X2 | 79.5% | 1.26 |
| 12 | 77.8% | 1.29 |
| BTTS sí | 55.1% | 1.82 |
| BTTS no | 44.9% | 2.23 |
| Más de 1.5 | 79.2% | 1.26 |
| Más de 2.5 | 56.4% | 1.77 |
| Menos de 2.5 | 43.6% | 2.29 |
| Más de 3.5 | 34.0% | 2.94 |
| Menos de 3.5 | 66.0% | 1.52 |
| Local portería a cero | 15.0% | 6.68 |
| Visitante portería a cero | 35.2% | 2.84 |
| Local menos de 1.5 | 72.0% | 1.39 |
| Visitante más de 0.5 | 85.0% | 1.18 |
| Visitante más de 1.5 | 56.6% | 1.77 |
| Visitante gana por 2+ | 33.5% | 2.98 |
| Visitante gana a cero | 29.9% | 3.34 |

Marcadores más probables: 1-1 (10.4%), 0-1 (10.0%), 1-2 (9.9%), 0-2 (9.5%), 1-3 (6.3%), 0-3 (6.0%), 1-0 (5.5%), 2-1 (5.5%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Gana Liverpool | 1.66 | 60.2% | 57.3% | -0.048 |
| Empate | 4.2 | 23.8% | 22.2% | -0.068 |
| Gana Crystal Palace | 4.75 | 21.1% | 20.5% | -0.028 |
| Ambos anotan: sí | 1.62 | 61.7% | 55.1% | -0.108 |
| Ambos anotan: no | 2.33 | 42.9% | 44.9% | +0.046 |
| Liverpool gana a cero | 3.25 | 30.8% | 29.9% | -0.027 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.00 | 1.78 | 21.1% | 23.3% | 55.6% | 52.5% | 52.5% |
| 0.20 | 1.03 | 1.85 | 20.7% | 22.6% | 56.6% | 54.8% | 54.0% |
| 0.35 | 1.04 | 1.90 | 20.5% | 22.2% | 57.3% | 56.4% | 55.1% |
| 0.50 | 1.06 | 1.95 | 20.2% | 21.8% | 58.0% | 58.0% | 56.1% |
| 0.70 | 1.09 | 2.02 | 19.9% | 21.2% | 58.9% | 60.1% | 57.5% |

## 7. Limitaciones
- Muestra pequeña (9 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
