# Simulación auditada: FC Twente vs Ajax
Eredivisie 2026/27 - Jornada 12 · 2026-11-08 14:30 CET

## 1. Auditoría de datos
```
OK  FC Twente: 11 PJ, 7G 2E 2P, 28:10, 23 pts = coincide con la tabla publicada
    estados de los resultados de FC Twente: {'VERIFICADO': 11}
OK  Ajax: 11 PJ, 7G 3E 1P, 30:13, 24 pts = coincide con la tabla publicada
    estados de los resultados de Ajax: {'VERIFICADO': 10, 'CONFLICTO_RESUELTO': 1}
OK  tiros FC Twente: 230 en 11 PJ (20.91 por partido), 8.21 tiros por gol, a puerta 88 (8.00/p, precisión 38.3%); goles 28 <= a puerta <= tiros: coherente
OK  tiros Ajax: 231 en 11 PJ (21.00 por partido), 7.70 tiros por gol, a puerta 78 (7.09/p, precisión 33.8%); goles 30 <= a puerta <= tiros: coherente
NO_DISPONIBLE corners: no se usa
OK  árbitro Joey Kooij: 21 amarillas / 7 PJ = 3.00 por partido
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (Eredivisie 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FC Twente | Total | 11 | 7-2-2 | 28 | 10 | 2.55 | 0.91 | 3.45 | 54.5% | 36.4% | 9.1% | 54.5% |
| FC Twente | Local | 5 | 4-0-1 | 10 | 5 | 2.00 | 1.00 | 3.00 | 60.0% | 40.0% | 0.0% | 60.0% |
| Ajax | Total | 11 | 7-3-1 | 30 | 13 | 2.73 | 1.18 | 3.91 | 72.7% | 27.3% | 0.0% | 72.7% |
| Ajax | Visitante | 5 | 5-0-0 | 18 | 4 | 3.60 | 0.80 | 4.40 | 60.0% | 40.0% | 0.0% | 80.0% |

## 3. Modelo
- Goles esperados (global): FC Twente 1.86 · Ajax 1.82
- Goles esperados (local en casa / visitante fuera): FC Twente 1.40 · Ajax 2.30
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- λ solo con datos: FC Twente 1.70 · Ajax 1.99
- Mercado sin margen (5.2% de margen quitado): 1 42.2% · X 25.0% · 2 32.8%
- Modelo puro: 1 33.6% · X 21.4% · 2 45.0%
- Mezcla (peso mercado 60%): 1 38.8% · X 23.6% · 2 37.7%
- **λ final: FC Twente 1.84 · Ajax 1.84** (total esperado 3.69)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 39.2% · X 21.7% · 2 39.1% · BTTS 70.9% · +2.5 71.2%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 39.2% | 2.55 |
| X | 21.6% | 4.62 |
| 2 | 39.2% | 2.55 |
| 1X | 60.8% | 1.64 |
| X2 | 60.8% | 1.64 |
| 12 | 78.4% | 1.28 |
| BTTS sí | 70.9% | 1.41 |
| BTTS no | 29.1% | 3.43 |
| Más de 1.5 | 88.3% | 1.13 |
| Más de 2.5 | 71.3% | 1.40 |
| Menos de 2.5 | 28.7% | 3.48 |
| Más de 3.5 | 50.3% | 1.99 |
| Menos de 3.5 | 49.7% | 2.01 |
| Local portería a cero | 15.8% | 6.32 |
| Visitante portería a cero | 15.8% | 6.32 |
| Local menos de 1.5 | 45.0% | 2.22 |
| Visitante más de 0.5 | 84.2% | 1.19 |
| Visitante más de 1.5 | 55.0% | 1.82 |
| Visitante gana por 2+ | 20.8% | 4.81 |
| Visitante gana a cero | 13.3% | 7.51 |

Marcadores más probables: 1-1 (8.5%), 2-1 (7.8%), 1-2 (7.8%), 2-2 (7.2%), 3-1 (4.8%), 1-3 (4.8%), 1-0 (4.6%), 0-1 (4.6%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Gana Twente | 2.25 | 44.4% | 39.2% | -0.118 |
| Empate | 3.8 | 26.3% | 21.6% | -0.178 |
| Gana Ajax | 2.9 | 34.5% | 39.2% | +0.136 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.86 | 1.82 | 40.1% | 21.7% | 38.3% | 71.1% | 70.8% |
| 0.20 | 1.77 | 1.91 | 36.3% | 21.6% | 42.1% | 71.2% | 70.7% |
| 0.35 | 1.70 | 1.99 | 33.6% | 21.4% | 45.0% | 71.3% | 70.5% |
| 0.50 | 1.63 | 2.06 | 30.9% | 21.2% | 47.9% | 71.3% | 70.2% |
| 0.70 | 1.54 | 2.16 | 27.5% | 20.7% | 51.8% | 71.4% | 69.4% |

## 6b. Remates, remates a puerta y tarjetas (Poisson sobre promedios auditados)

**Remates Twente: media proyectada 20.68**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Twente remata por partido=20.91 (UNA_FUENTE) | Twente (footystats)=20.44 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 16.5 | 82.0% | 18.0% | 1.22 | 5.54 |
| 18.5 | 67.3% | 32.7% | 1.48 | 3.06 |
| 20.5 | 50.1% | 49.9% | 2.00 | 2.00 |
| 22.5 | 33.3% | 66.7% | 3.00 | 1.50 |

**Remates Ajax: media proyectada 20.10**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Ajax remata por partido=21.00 (UNA_FUENTE) | Ajax (otra fuente)=19.20 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 16.5 | 78.5% | 21.5% | 1.27 | 4.66 |
| 18.5 | 62.7% | 37.3% | 1.59 | 2.68 |
| 20.5 | 45.0% | 55.0% | 2.22 | 1.82 |
| 22.5 | 28.7% | 71.3% | 3.48 | 1.40 |

**Remates totales: media proyectada 40.78**  
Base: suma de Remates Twente + Remates Ajax

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 34.5 | 83.7% | 16.3% | 1.19 | 6.14 |
| 36.5 | 74.4% | 25.6% | 1.34 | 3.90 |
| 38.5 | 63.1% | 36.9% | 1.59 | 2.71 |
| 40.5 | 50.7% | 49.3% | 1.97 | 2.03 |
| 42.5 | 38.4% | 61.6% | 2.60 | 1.62 |

**Remates a puerta Twente: media proyectada 8.00**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Twente a puerta por partido=8.00 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 5.5 | 80.9% | 19.1% | 1.24 | 5.23 |
| 6.5 | 68.7% | 31.3% | 1.46 | 3.19 |
| 7.5 | 54.7% | 45.3% | 1.83 | 2.21 |
| 8.5 | 40.7% | 59.3% | 2.45 | 1.69 |

**Remates a puerta Ajax: media proyectada 7.55**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Ajax a puerta (statz)=7.10 (UNA_FUENTE) | Ajax a puerta (footystats)=8.00 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 5.5 | 76.4% | 23.6% | 1.31 | 4.24 |
| 6.5 | 62.9% | 37.1% | 1.59 | 2.69 |
| 7.5 | 48.3% | 51.7% | 2.07 | 1.93 |
| 8.5 | 34.5% | 65.5% | 2.90 | 1.53 |

**Remates a puerta totales: media proyectada 15.55**  
Base: suma de Remates a puerta Twente + Remates a puerta Ajax

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 12.5 | 77.5% | 22.5% | 1.29 | 4.45 |
| 13.5 | 68.7% | 31.3% | 1.45 | 3.20 |
| 14.5 | 58.9% | 41.1% | 1.70 | 2.44 |
| 15.5 | 48.8% | 51.2% | 2.05 | 1.95 |
| 16.5 | 38.9% | 61.1% | 2.57 | 1.64 |

**Tarjetas totales: media proyectada 2.95**  
Base: Equipos (1.00 + 1.82)=2.82 (UNA_FUENTE) | Árbitro Kooij 2026/27=3.00 (UNA_FUENTE) | Media de la liga=3.04 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 1.5 | 79.4% | 20.6% | 1.26 | 4.85 |
| 2.5 | 56.6% | 43.4% | 1.77 | 2.31 |
| 3.5 | 34.2% | 65.8% | 2.92 | 1.52 |
| 4.5 | 17.7% | 82.3% | 5.65 | 1.22 |

> Aviso: remates y tarjetas tienen más varianza que una Poisson; las probabilidades en líneas alejadas de la media son optimistas. Usa sobre todo las líneas cercanas a la media.

## 8. Selección de picks (filtro estricto)
Calidad de datos: **alta** (100.0% de resultados con 2+ fuentes o resueltos por la tabla). Regla: solo es pick si hay cuota publicada, el valor esperado es >= +5% con la probabilidad ya anclada al mercado, y como máximo 2 picks por partido. Sin cuota no hay pick: una probabilidad sin precio no dice si la apuesta vale la pena.

| Apuesta | Cuota | Prob. anclada | Valor esperado | Riesgo | ¿Pick? |
|---|---|---|---|---|---|
| Gana Ajax | 2.9 | 39.2% | +0.136 | Alto | SÍ |
| Gana Twente | 2.25 | 39.2% | -0.118 | Alto | no |
| Empate | 3.8 | 21.6% | -0.178 | Alto | no |

Stake sugerido: 1 unidad (1-2% del bankroll) por pick; nunca más de 2 selecciones en una combinada.

## 9. Limitaciones
- Muestra pequeña (11 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
