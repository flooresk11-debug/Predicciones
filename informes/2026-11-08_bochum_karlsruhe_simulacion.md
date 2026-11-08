# Simulación auditada: VfL Bochum vs Karlsruher SC
2. Bundesliga 2026/27 - Jornada 11 · 2026-11-08 13:30 CET


## 1. Auditoría de datos
```
OK  VfL Bochum: 10 PJ, 3G 2E 5P, 8:11, 11 pts = coincide con la tabla publicada
    estados de los resultados de VfL Bochum: {'VERIFICADO': 9, 'CONFLICTO_RESUELTO': 1}
OK  Karlsruher SC: 10 PJ, 3G 2E 5P, 13:21, 11 pts = coincide con la tabla publicada
    estados de los resultados de Karlsruher SC: {'VERIFICADO': 10}
NO_DISPONIBLE tiros_totales: no se usa
NO_DISPONIBLE tiros_a_puerta: no se usa
NO_DISPONIBLE corners: no se usa
EXCLUIDO (conflicto entre fuentes) h2h.historico_total: 62, 63 o 64 duelos según la fuente; no se usa en el modelo
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): tiros_totales, tiros_a_puerta, corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (2. Bundesliga 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VfL Bochum | Total | 10 | 3-2-5 | 8 | 11 | 0.80 | 1.10 | 1.90 | 50.0% | 10.0% | 40.0% | 30.0% |
| VfL Bochum | Local | 5 | 0-2-3 | 2 | 5 | 0.40 | 1.00 | 1.40 | 40.0% | 0.0% | 60.0% | 0.0% |
| Karlsruher SC | Total | 10 | 3-2-5 | 13 | 21 | 1.30 | 2.10 | 3.40 | 50.0% | 20.0% | 40.0% | 70.0% |
| Karlsruher SC | Visitante | 4 | 0-2-2 | 3 | 10 | 0.75 | 2.50 | 3.25 | 50.0% | 25.0% | 50.0% | 50.0% |

## 3. Modelo
- Goles esperados (global): VfL Bochum 1.45 · Karlsruher SC 1.20
- Goles esperados (local en casa / visitante fuera): VfL Bochum 1.45 · Karlsruher SC 0.88
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- λ solo con datos: VfL Bochum 1.45 · Karlsruher SC 1.09
- Sin cuotas 1X2 completas: el modelo NO está anclado al mercado (más incertidumbre).
- **λ final: VfL Bochum 1.45 · Karlsruher SC 1.09** (total esperado 2.54)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 45.4% · X 26.3% · 2 28.3% · BTTS 50.7% · +2.5 46.5%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 45.4% | 2.20 |
| X | 26.2% | 3.81 |
| 2 | 28.3% | 3.53 |
| 1X | 71.7% | 1.39 |
| X2 | 54.6% | 1.83 |
| 12 | 73.8% | 1.36 |
| BTTS sí | 50.7% | 1.97 |
| BTTS no | 49.3% | 2.03 |
| Más de 1.5 | 72.0% | 1.39 |
| Más de 2.5 | 46.5% | 2.15 |
| Menos de 2.5 | 53.5% | 1.87 |
| Más de 3.5 | 25.0% | 4.00 |
| Menos de 3.5 | 75.0% | 1.33 |
| Local portería a cero | 33.7% | 2.96 |
| Visitante portería a cero | 23.5% | 4.26 |
| Local menos de 1.5 | 57.5% | 1.74 |
| Visitante más de 0.5 | 66.3% | 1.51 |
| Visitante más de 1.5 | 29.6% | 3.38 |
| Visitante gana por 2+ | 10.9% | 9.17 |
| Visitante gana a cero | 15.5% | 6.43 |

Marcadores más probables: 1-1 (12.5%), 1-0 (11.5%), 2-1 (9.0%), 0-1 (8.6%), 2-0 (8.3%), 0-0 (7.9%), 1-2 (6.8%), 2-2 (4.9%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Gana Bochum | 1.75 | 57.1% | 45.4% | -0.205 |
| Empate | 4.0 | 25.0% | 26.2% | +0.050 |
| Ambos anotan: sí | 1.53 | 65.4% | 50.7% | -0.224 |
| Menos de 3.5 goles | 1.59 | 62.9% | 75.0% | +0.192 |
| Menos de 2.5 goles | 2.4 | 41.7% | 53.5% | +0.283 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.45 | 1.20 | 42.9% | 25.9% | 31.3% | 49.4% | 53.5% |
| 0.20 | 1.45 | 1.14 | 44.3% | 26.1% | 29.6% | 47.8% | 51.9% |
| 0.35 | 1.45 | 1.09 | 45.4% | 26.2% | 28.3% | 46.5% | 50.7% |
| 0.50 | 1.45 | 1.04 | 46.6% | 26.4% | 27.0% | 45.3% | 49.4% |
| 0.70 | 1.45 | 0.97 | 48.1% | 26.5% | 25.3% | 43.6% | 47.6% |

## 8. Selección de picks (filtro estricto)
Calidad de datos: **alta** (100.0% de resultados con 2+ fuentes o resueltos por la tabla). Regla: solo es pick si hay cuota publicada, el valor esperado es >= +5% con la probabilidad ya anclada al mercado, y como máximo 2 picks por partido. Sin cuota no hay pick: una probabilidad sin precio no dice si la apuesta vale la pena.

| Apuesta | Cuota | Prob. anclada | Valor esperado | Riesgo | ¿Pick? |
|---|---|---|---|---|---|
| Menos de 2.5 goles | 2.4 | 53.5% | +0.283 | Alto | no |
| Menos de 3.5 goles | 1.59 | 75.0% | +0.192 | Medio | no |
| Empate | 4.0 | 26.2% | +0.050 | Alto | no |
| Gana Bochum | 1.75 | 45.4% | -0.205 | Alto | no |
| Ambos anotan: sí | 1.53 | 50.7% | -0.224 | Alto | no |

**Sin pick (bloqueado):** sin cuotas 1X2 completas para anclar el modelo al mercado. Los valores esperados de arriba son solo informativos.

Stake sugerido: 1 unidad (1-2% del bankroll) por pick; nunca más de 2 selecciones en una combinada.

## 9. Limitaciones
- Muestra pequeña (10 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
