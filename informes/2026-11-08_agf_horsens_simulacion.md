# Simulación auditada: AGF vs AC Horsens
Superliga Dinamarca 2026/27 - Jornada 14 · 2026-11-08 14:00 CET

## 1. Auditoría de datos
```
OK  AGF (agregados): 13 PJ, 2G 6E 5P, 17:21, 12 pts = 3x2+6 y coincide con la tabla
OK  AGF: casa + fuera suman el total en todos los campos disponibles
    nota: AGF sin lista partido a partido completa -> BTTS/porterías a cero n/d
OK  AC Horsens (agregados): 13 PJ, 4G 4E 5P, 23:21, 16 pts = 3x4+4 y coincide con la tabla
OK  AC Horsens: casa + fuera suman el total en todos los campos disponibles
    nota: AC Horsens sin lista partido a partido completa -> BTTS/porterías a cero n/d
NO_DISPONIBLE tiros_totales: no se usa
NO_DISPONIBLE tiros_a_puerta: no se usa
NO_DISPONIBLE corners: no se usa
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): tiros_totales, tiros_a_puerta, corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (Superliga Dinamarca 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AGF | Total | 13 | 2-6-5 | 17 | 21 | 1.31 | 1.62 | 2.92 | n/d | n/d | n/d | n/d |
| AGF | Local | 6 | 2-3-1 | 10 | 8 | 1.67 | 1.33 | 3.00 | n/d | n/d | n/d | n/d |
| AC Horsens | Total | 13 | 4-4-5 | 23 | 21 | 1.77 | 1.62 | 3.38 | n/d | n/d | n/d | n/d |
| AC Horsens | Visitante | 6 | ?-?-? | n/d | n/d | n/d | n/d | n/d | n/d | n/d | n/d | n/d |

## 3. Modelo
- Goles esperados (global): AGF 1.46 · AC Horsens 1.69
- Goles esperados (local en casa / visitante fuera): AGF 1.64 · AC Horsens 1.55
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- λ solo con datos: AGF 1.52 · AC Horsens 1.64
- Sin cuotas 1X2 completas: el modelo NO está anclado al mercado (más incertidumbre).
- **λ final: AGF 1.52 · AC Horsens 1.64** (total esperado 3.17)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 35.7% · X 23.6% · 2 40.7% · BTTS 63.2% · +2.5 61.3%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 35.7% | 2.80 |
| X | 23.5% | 4.25 |
| 2 | 40.8% | 2.45 |
| 1X | 59.2% | 1.69 |
| X2 | 64.3% | 1.56 |
| 12 | 76.5% | 1.31 |
| BTTS sí | 63.1% | 1.58 |
| BTTS no | 36.9% | 2.71 |
| Más de 1.5 | 82.4% | 1.21 |
| Más de 2.5 | 61.3% | 1.63 |
| Menos de 2.5 | 38.7% | 2.59 |
| Más de 3.5 | 39.0% | 2.56 |
| Menos de 3.5 | 61.0% | 1.64 |
| Local portería a cero | 19.3% | 5.17 |
| Visitante portería a cero | 21.8% | 4.59 |
| Local menos de 1.5 | 55.0% | 1.82 |
| Visitante más de 0.5 | 80.7% | 1.24 |
| Visitante más de 1.5 | 48.9% | 2.05 |
| Visitante gana por 2+ | 20.7% | 4.83 |
| Visitante gana a cero | 17.6% | 5.69 |

Marcadores más probables: 1-1 (10.5%), 1-2 (8.7%), 2-1 (8.0%), 0-1 (6.9%), 2-2 (6.6%), 1-0 (6.4%), 0-2 (5.7%), 2-0 (4.9%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Gana AGF | 1.55 | 64.5% | 35.7% | -0.447 |
| Gana AC Horsens | 5.25 | 19.0% | 40.8% | +1.141 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.46 | 1.69 | 33.3% | 23.5% | 43.2% | 61.0% | 62.7% |
| 0.20 | 1.50 | 1.66 | 34.7% | 23.5% | 41.8% | 61.2% | 62.9% |
| 0.35 | 1.52 | 1.64 | 35.7% | 23.5% | 40.8% | 61.3% | 63.1% |
| 0.50 | 1.55 | 1.62 | 36.7% | 23.5% | 39.7% | 61.4% | 63.2% |
| 0.70 | 1.59 | 1.59 | 38.1% | 23.5% | 38.4% | 61.6% | 63.4% |

## 8. Selección de picks (filtro estricto)
Calidad de datos: **baja** (sin lista completa partido a partido). Regla: solo es pick si hay cuota publicada, el valor esperado es >= +5% con la probabilidad ya anclada al mercado, y como máximo 2 picks por partido. Sin cuota no hay pick: una probabilidad sin precio no dice si la apuesta vale la pena.

| Apuesta | Cuota | Prob. anclada | Valor esperado | Riesgo | ¿Pick? |
|---|---|---|---|---|---|
| Gana AC Horsens | 5.25 | 40.8% | +1.141 | Alto | no |
| Gana AGF | 1.55 | 35.7% | -0.447 | Alto | no |

**Sin pick (bloqueado):** calidad de datos baja. Los valores esperados de arriba son solo informativos.

Stake sugerido: 1 unidad (1-2% del bankroll) por pick; nunca más de 2 selecciones en una combinada.

## 9. Limitaciones
- Muestra pequeña (13 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
