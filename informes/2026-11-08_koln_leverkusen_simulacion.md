# Simulación auditada: 1. FC Köln vs Bayer 04 Leverkusen
Bundesliga 2026/27 - Jornada 9 · 2026-11-08 15:30 CET

## 1. Auditoría de datos
```
OK  1. FC Köln: 8 PJ, 2G 3E 3P, 9:12, 9 pts = coincide con la tabla publicada
    estados de los resultados de 1. FC Köln: {'VERIFICADO': 4, 'UNA_FUENTE': 3, 'CONFLICTO_MARCADOR': 1}
OK  Bayer 04 Leverkusen: 8 PJ, 4G 1E 3P, 18:16, 13 pts = coincide con la tabla publicada
    estados de los resultados de Bayer 04 Leverkusen: {'VERIFICADO': 5, 'UNA_FUENTE': 3}
OK  tiros 1. FC Köln: 105 en 7 PJ (15.00 por partido), 13.12 tiros por gol
OK  tiros Bayer 04 Leverkusen: 146 en 8 PJ (18.25 por partido), 8.11 tiros por gol
NO_DISPONIBLE tiros_a_puerta: no se usa
NO_DISPONIBLE corners: no se usa
EXCLUIDO (conflicto entre fuentes) h2h.historico_total: wettbasis.com cuenta 94 duelos con 39 triunfos del Leverkusen
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): tiros_a_puerta, corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (Bundesliga 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. FC Köln | Total | 8 | 2-3-3 | 9 | 12 | 1.12 | 1.50 | 2.62 | 75.0% | 12.5% | 25.0% | 50.0% |
| 1. FC Köln | Local | 4 | 2-2-0 | 6 | 4 | 1.50 | 1.00 | 2.50 | 75.0% | 25.0% | 25.0% | 50.0% |
| Bayer 04 Leverkusen | Total | 8 | 4-1-3 | 18 | 16 | 2.25 | 2.00 | 4.25 | 62.5% | 25.0% | 12.5% | 87.5% |
| Bayer 04 Leverkusen | Visitante | 4 | 1-1-2 | 8 | 11 | 2.00 | 2.75 | 4.75 | 75.0% | 0.0% | 25.0% | 100.0% |

## 3. Modelo
- Goles esperados (global): 1. FC Köln 1.56 · Bayer 04 Leverkusen 1.88
- Goles esperados (local en casa / visitante fuera): 1. FC Köln 2.12 · Bayer 04 Leverkusen 1.50
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- **λ final: 1. FC Köln 1.76 · Bayer 04 Leverkusen 1.74** (total esperado 3.50)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 39.2% · X 22.3% · 2 38.4% · BTTS 68.3% · +2.5 68.0%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 39.2% | 2.55 |
| X | 22.3% | 4.49 |
| 2 | 38.5% | 2.59 |
| 1X | 61.5% | 1.63 |
| X2 | 60.8% | 1.64 |
| 12 | 77.7% | 1.29 |
| BTTS sí | 68.3% | 1.46 |
| BTTS no | 31.7% | 3.16 |
| Más de 1.5 | 86.4% | 1.16 |
| Más de 2.5 | 68.0% | 1.47 |
| Menos de 2.5 | 32.0% | 3.12 |
| Más de 3.5 | 46.4% | 2.16 |
| Menos de 3.5 | 53.6% | 1.87 |
| Local portería a cero | 17.5% | 5.72 |
| Visitante portería a cero | 17.2% | 5.81 |
| Local menos de 1.5 | 47.5% | 2.11 |
| Visitante más de 0.5 | 82.5% | 1.21 |
| Visitante más de 1.5 | 52.0% | 1.92 |
| Visitante gana por 2+ | 19.9% | 5.03 |
| Visitante gana a cero | 14.2% | 7.04 |

Marcadores más probables: 1-1 (9.2%), 2-1 (8.1%), 1-2 (8.1%), 2-2 (7.1%), 1-0 (5.3%), 0-1 (5.2%), 3-1 (4.8%), 1-3 (4.7%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Leverkusen gana | 1.85 | 54.1% | 38.5% | -0.287 |
| Köln menos de 1.5 goles | 1.61 | 62.1% | 47.5% | -0.235 |
| Köln handicap +1 | 1.609 | 62.2% | gana 61.5% / push 18.7% | +0.175 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.56 | 1.88 | 32.4% | 22.2% | 45.3% | 66.7% | 66.9% |
| 0.20 | 1.68 | 1.80 | 36.3% | 22.3% | 41.4% | 67.4% | 67.8% |
| 0.35 | 1.76 | 1.74 | 39.2% | 22.3% | 38.5% | 68.0% | 68.3% |
| 0.50 | 1.84 | 1.69 | 42.1% | 22.1% | 35.8% | 68.5% | 68.6% |
| 0.70 | 1.96 | 1.61 | 46.1% | 21.7% | 32.2% | 69.2% | 68.7% |

## 7. Limitaciones
- Muestra pequeña (8 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
