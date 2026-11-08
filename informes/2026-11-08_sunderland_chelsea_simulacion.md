# Simulación auditada: Sunderland vs Chelsea
Premier League 2026/27 - Jornada 10 · 2026-11-08 15:00 CET


## 1. Auditoría de datos
```
OK  Sunderland: 9 PJ, 1G 2E 6P, 7:17, 5 pts = coincide con la tabla publicada
    estados de los resultados de Sunderland: {'VERIFICADO': 9}
OK  Chelsea: 9 PJ, 5G 1E 3P, 19:15, 16 pts = coincide con la tabla publicada
    estados de los resultados de Chelsea: {'VERIFICADO': 9}
OK  tiros Sunderland: 113 en 9 PJ (12.56 por partido), 16.14 tiros por gol, a puerta 36 (4.00/p, precisión 31.9%); goles 7 <= a puerta <= tiros: coherente
OK  tiros Chelsea: 126 en 9 PJ (14.00 por partido), 6.63 tiros por gol, a puerta 53 (5.89/p, precisión 42.1%); goles 19 <= a puerta <= tiros: coherente
NO_DISPONIBLE corners: no se usa
OK  árbitro Jarred Gillett: 28 amarillas / 6 PJ = 4.67 por partido
EXCLUIDO (conflicto entre fuentes) h2h.historico_total: otras fuentes dan muestras distintas; no se usa
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (Premier League 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sunderland | Total | 9 | 1-2-6 | 7 | 17 | 0.78 | 1.89 | 2.67 | 44.4% | 22.2% | 44.4% | 33.3% |
| Sunderland | Local | 4 | 1-1-2 | 1 | 4 | 0.25 | 1.00 | 1.25 | 0.0% | 50.0% | 75.0% | 0.0% |
| Chelsea | Total | 9 | 5-1-3 | 19 | 15 | 2.11 | 1.67 | 3.78 | 55.6% | 22.2% | 22.2% | 66.7% |
| Chelsea | Visitante | 4 | 2-0-2 | 6 | 7 | 1.50 | 1.75 | 3.25 | 50.0% | 25.0% | 25.0% | 75.0% |

## 3. Modelo
- Goles esperados (global): Sunderland 1.22 · Chelsea 2.00
- Goles esperados (local en casa / visitante fuera): Sunderland 1.00 · Chelsea 1.25
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- λ solo con datos: Sunderland 1.14 · Chelsea 1.74
- Mercado sin margen (5.7% de margen quitado): 1 25.2% · X 26.3% · 2 48.5%
- Modelo puro: 1 25.1% · X 23.7% · 2 51.3%
- Mezcla (peso mercado 60%): 1 25.2% · X 25.2% · 2 49.6%
- **λ final: Sunderland 1.18 · Chelsea 1.70** (total esperado 2.88)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 26.6% · X 24.0% · 2 49.3% · BTTS 56.8% · +2.5 55.0%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 26.5% | 3.77 |
| X | 23.9% | 4.18 |
| 2 | 49.5% | 2.02 |
| 1X | 50.5% | 1.98 |
| X2 | 73.5% | 1.36 |
| 12 | 76.1% | 1.31 |
| BTTS sí | 56.7% | 1.76 |
| BTTS no | 43.3% | 2.31 |
| Más de 1.5 | 78.3% | 1.28 |
| Más de 2.5 | 55.0% | 1.82 |
| Menos de 2.5 | 45.0% | 2.22 |
| Más de 3.5 | 32.6% | 3.06 |
| Menos de 3.5 | 67.4% | 1.48 |
| Local portería a cero | 18.3% | 5.48 |
| Visitante portería a cero | 30.7% | 3.26 |
| Local menos de 1.5 | 66.9% | 1.49 |
| Visitante más de 0.5 | 81.7% | 1.22 |
| Visitante más de 1.5 | 50.7% | 1.97 |
| Visitante gana por 2+ | 26.6% | 3.76 |
| Visitante gana a cero | 25.1% | 3.99 |

Marcadores más probables: 1-1 (11.3%), 1-2 (9.6%), 0-1 (9.5%), 0-2 (8.1%), 2-1 (6.7%), 1-0 (6.6%), 2-2 (5.7%), 0-0 (5.6%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Gana Sunderland | 3.75 | 26.7% | 26.5% | -0.005 |
| Empate | 3.6 | 27.8% | 23.9% | -0.138 |
| Gana Chelsea | 1.95 | 51.3% | 49.5% | -0.034 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.22 | 2.00 | 23.0% | 21.6% | 55.4% | 62.5% | 61.0% |
| 0.20 | 1.18 | 1.85 | 24.2% | 22.7% | 53.1% | 58.3% | 58.3% |
| 0.35 | 1.14 | 1.74 | 25.1% | 23.7% | 51.3% | 55.0% | 56.2% |
| 0.50 | 1.11 | 1.62 | 26.0% | 24.7% | 49.3% | 51.5% | 53.9% |
| 0.70 | 1.07 | 1.48 | 27.4% | 26.1% | 46.6% | 46.7% | 50.6% |

## 6b. Remates, remates a puerta y tarjetas (Poisson sobre promedios auditados)

**Remates Sunderland: media proyectada 12.56**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Sunderland remata por partido=12.56 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 9.5 | 80.3% | 19.7% | 1.25 | 5.08 |
| 10.5 | 70.9% | 29.1% | 1.41 | 3.43 |
| 11.5 | 60.1% | 39.9% | 1.66 | 2.50 |
| 12.5 | 48.8% | 51.2% | 2.05 | 1.95 |
| 13.5 | 37.9% | 62.1% | 2.64 | 1.61 |

**Remates Chelsea: media proyectada 14.00**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Chelsea remata por partido=14.00 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 11.5 | 74.0% | 26.0% | 1.35 | 3.85 |
| 12.5 | 64.2% | 35.8% | 1.56 | 2.79 |
| 13.5 | 53.6% | 46.4% | 1.87 | 2.15 |
| 14.5 | 43.0% | 57.0% | 2.33 | 1.75 |
| 15.5 | 33.1% | 66.9% | 3.02 | 1.49 |

**Remates totales: media proyectada 26.56**  
Base: suma de Remates Sunderland + Remates Chelsea

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 22.5 | 78.1% | 21.9% | 1.28 | 4.57 |
| 23.5 | 71.7% | 28.3% | 1.40 | 3.53 |
| 24.5 | 64.5% | 35.5% | 1.55 | 2.82 |
| 25.5 | 56.9% | 43.1% | 1.76 | 2.32 |
| 26.5 | 49.2% | 50.8% | 2.03 | 1.97 |
| 27.5 | 41.5% | 58.5% | 2.41 | 1.71 |

**Remates a puerta Sunderland: media proyectada 4.00**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Sunderland a puerta por partido=4.00 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 2.5 | 76.2% | 23.8% | 1.31 | 4.20 |
| 3.5 | 56.7% | 43.3% | 1.77 | 2.31 |
| 4.5 | 37.1% | 62.9% | 2.69 | 1.59 |
| 5.5 | 21.5% | 78.5% | 4.65 | 1.27 |

**Remates a puerta Chelsea: media proyectada 5.89**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Chelsea a puerta por partido=5.89 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 3.5 | 83.9% | 16.1% | 1.19 | 6.20 |
| 4.5 | 70.0% | 30.0% | 1.43 | 3.33 |
| 5.5 | 53.6% | 46.4% | 1.86 | 2.16 |
| 6.5 | 37.6% | 62.4% | 2.66 | 1.60 |
| 7.5 | 24.1% | 75.9% | 4.15 | 1.32 |

**Remates a puerta totales: media proyectada 9.89**  
Base: suma de Remates a puerta Sunderland + Remates a puerta Chelsea

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 7.5 | 77.0% | 23.0% | 1.30 | 4.34 |
| 8.5 | 65.5% | 34.5% | 1.53 | 2.90 |
| 9.5 | 52.8% | 47.2% | 1.89 | 2.12 |
| 10.5 | 40.3% | 59.7% | 2.48 | 1.68 |
| 11.5 | 29.1% | 70.9% | 3.44 | 1.41 |

**Amarillas Sunderland: media proyectada 1.93**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Sunderland recibe por partido=1.93 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 0.5 | 85.5% | 14.5% | 1.17 | 6.89 |
| 1.5 | 57.5% | 42.5% | 1.74 | 2.35 |
| 2.5 | 30.4% | 69.6% | 3.29 | 1.44 |

**Amarillas Chelsea: media proyectada 1.75**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Chelsea recibe por partido=1.75 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 0.5 | 82.6% | 17.4% | 1.21 | 5.75 |
| 1.5 | 52.2% | 47.8% | 1.92 | 2.09 |
| 2.5 | 25.6% | 74.4% | 3.91 | 1.34 |

**Amarillas totales: media proyectada 3.98**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Equipos (1.93 + 1.75)=3.68 (UNA_FUENTE) | Gillett 2026/27=4.67 (VERIFICADO) | Gillett 2025/26 + 2026/27=3.58 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 2.5 | 75.8% | 24.2% | 1.32 | 4.14 |
| 3.5 | 56.2% | 43.8% | 1.78 | 2.28 |
| 4.5 | 36.7% | 63.3% | 2.73 | 1.58 |
| 5.5 | 21.1% | 78.9% | 4.73 | 1.27 |

Estimadores **excluidos** por conflicto o falta de datos:
- Remates Sunderland · Chelsea concede: NO_DISPONIBLE (no encontrado)
- Remates Chelsea · Sunderland concede: NO_DISPONIBLE (no encontrado)

> Aviso: remates y tarjetas tienen más varianza que una Poisson; las probabilidades en líneas alejadas de la media son optimistas. Usa sobre todo las líneas cercanas a la media.

## 8. Selección de picks (filtro estricto)
Calidad de datos: **alta** (100.0% de resultados con 2+ fuentes o resueltos por la tabla). Regla: solo es pick si hay cuota publicada, el valor esperado es >= +5% con la probabilidad ya anclada al mercado, y como máximo 2 picks por partido. Sin cuota no hay pick: una probabilidad sin precio no dice si la apuesta vale la pena.

| Apuesta | Cuota | Prob. anclada | Valor esperado | Riesgo | ¿Pick? |
|---|---|---|---|---|---|
| Gana Sunderland | 3.75 | 26.5% | -0.005 | Alto | no |
| Gana Chelsea | 1.95 | 49.5% | -0.034 | Alto | no |
| Empate | 3.6 | 23.9% | -0.138 | Alto | no |

**Sin pick:** ninguna cuota publicada tiene valor suficiente. No apostar también es una decisión.

Stake sugerido: 1 unidad (1-2% del bankroll) por pick; nunca más de 2 selecciones en una combinada.

## 9. Limitaciones
- Muestra pequeña (9 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
