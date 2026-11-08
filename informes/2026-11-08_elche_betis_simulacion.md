# Simulación auditada: Elche CF vs Real Betis
LaLiga EA Sports 2026/27 - Jornada 12 · 2026-11-08 14:00 CET


## 1. Auditoría de datos
```
OK  Elche CF: 11 PJ, 2G 4E 5P, 14:18, 10 pts = coincide con la tabla publicada
    estados de los resultados de Elche CF: {'VERIFICADO': 11}
OK  Real Betis: 11 PJ, 7G 2E 2P, 18:15, 23 pts = coincide con la tabla publicada
    estados de los resultados de Real Betis: {'VERIFICADO': 7, 'UNA_FUENTE': 4}
OK  tiros Elche CF: 105 en 11 PJ (9.55 por partido), 7.50 tiros por gol, a puerta 50 (4.55/p, precisión 47.6%); goles 14 <= a puerta <= tiros: coherente
OK  tiros Real Betis: 139 en 11 PJ (12.64 por partido), 7.72 tiros por gol, a puerta 65 (5.91/p, precisión 46.8%); goles 18 <= a puerta <= tiros: coherente
NO_DISPONIBLE corners: no se usa
OK  tarjetas Real Betis: 18 amarillas / 11 PJ = 1.64 (publicado 1.64)
OK  tarjetas Elche CF: 28 amarillas / 11 PJ = 2.55 (publicado 2.55)
OK  árbitro César Soto Grado: 14 amarillas / 3 PJ = 4.67 por partido
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (LaLiga EA Sports 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Elche CF | Total | 11 | 2-4-5 | 14 | 18 | 1.27 | 1.64 | 2.91 | 54.5% | 27.3% | 36.4% | 54.5% |
| Elche CF | Local | 5 | 0-1-4 | 4 | 12 | 0.80 | 2.40 | 3.20 | 40.0% | 20.0% | 60.0% | 60.0% |
| Real Betis | Total | 11 | 7-2-2 | 18 | 15 | 1.64 | 1.36 | 3.00 | 54.5% | 45.5% | 9.1% | 45.5% |
| Real Betis | Visitante | 5 | 2-2-1 | 6 | 7 | 1.20 | 1.40 | 2.60 | 60.0% | 40.0% | 20.0% | 40.0% |

## 3. Modelo
- Goles esperados (global): Elche CF 1.32 · Real Betis 1.64
- Goles esperados (local en casa / visitante fuera): Elche CF 1.10 · Real Betis 1.80
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- λ solo con datos: Elche CF 1.24 · Real Betis 1.69
- Mercado sin margen (4.7% de margen quitado): 1 29.4% · X 25.1% · 2 45.5%
- Modelo puro: 1 28.1% · X 23.9% · 2 48.0%
- Mezcla (peso mercado 60%): 1 28.9% · X 24.6% · 2 46.5%
- **λ final: Elche CF 1.26 · Real Betis 1.67** (total esperado 2.94)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 28.9% · X 24.1% · 2 47.0% · BTTS 58.3% · +2.5 56.3%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 28.9% | 3.46 |
| X | 24.0% | 4.16 |
| 2 | 47.0% | 2.13 |
| 1X | 53.0% | 1.89 |
| X2 | 71.1% | 1.41 |
| 12 | 76.0% | 1.32 |
| BTTS sí | 58.2% | 1.72 |
| BTTS no | 41.8% | 2.39 |
| Más de 1.5 | 79.1% | 1.26 |
| Más de 2.5 | 56.2% | 1.78 |
| Menos de 2.5 | 43.8% | 2.28 |
| Más de 3.5 | 33.8% | 2.96 |
| Menos de 3.5 | 66.2% | 1.51 |
| Local portería a cero | 18.8% | 5.33 |
| Visitante portería a cero | 28.3% | 3.53 |
| Local menos de 1.5 | 64.0% | 1.56 |
| Visitante más de 0.5 | 81.2% | 1.23 |
| Visitante más de 1.5 | 49.8% | 2.01 |
| Visitante gana por 2+ | 24.8% | 4.03 |
| Visitante gana a cero | 23.0% | 4.35 |

Marcadores más probables: 1-1 (11.2%), 1-2 (9.4%), 0-1 (8.9%), 0-2 (7.4%), 2-1 (7.1%), 1-0 (6.7%), 2-2 (5.9%), 0-0 (5.3%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Gana Elche | 3.25 | 30.8% | 28.9% | -0.060 |
| Empate | 3.8 | 26.3% | 24.0% | -0.087 |
| Gana Betis | 2.1 | 47.6% | 47.0% | -0.012 |
| Ambos anotan: sí | 1.6 | 62.5% | 58.2% | -0.068 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.32 | 1.64 | 30.9% | 24.2% | 44.9% | 56.7% | 59.0% |
| 0.20 | 1.27 | 1.67 | 29.3% | 24.0% | 46.7% | 56.4% | 58.5% |
| 0.35 | 1.24 | 1.69 | 28.1% | 23.9% | 48.0% | 56.2% | 58.0% |
| 0.50 | 1.21 | 1.72 | 26.9% | 23.8% | 49.3% | 56.0% | 57.6% |
| 0.70 | 1.17 | 1.75 | 25.4% | 23.5% | 51.1% | 55.8% | 56.9% |

## 6b. Remates, remates a puerta y tarjetas (Poisson sobre promedios auditados)

**Remates Elche: media proyectada 9.55**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Elche remata por partido=9.55 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 7.5 | 73.6% | 26.4% | 1.36 | 3.79 |
| 8.5 | 61.4% | 38.6% | 1.63 | 2.59 |
| 9.5 | 48.5% | 51.5% | 2.06 | 1.94 |
| 10.5 | 36.1% | 63.9% | 2.77 | 1.56 |
| 11.5 | 25.3% | 74.7% | 3.95 | 1.34 |

**Remates Betis: media proyectada 12.64**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Betis remata por partido=12.64 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 9.5 | 80.9% | 19.1% | 1.24 | 5.24 |
| 10.5 | 71.6% | 28.4% | 1.40 | 3.52 |
| 11.5 | 60.9% | 39.1% | 1.64 | 2.56 |
| 12.5 | 49.7% | 50.3% | 2.01 | 1.99 |
| 13.5 | 38.7% | 61.3% | 2.58 | 1.63 |

**Remates totales: media proyectada 22.19**  
Base: suma de Remates Elche + Remates Betis

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 18.5 | 77.9% | 22.1% | 1.28 | 4.53 |
| 19.5 | 70.8% | 29.2% | 1.41 | 3.42 |
| 20.5 | 62.8% | 37.2% | 1.59 | 2.69 |
| 21.5 | 54.4% | 45.6% | 1.84 | 2.19 |
| 22.5 | 46.0% | 54.0% | 2.18 | 1.85 |
| 23.5 | 37.8% | 62.2% | 2.65 | 1.61 |

**Remates a puerta Elche: media proyectada 4.55**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Elche a puerta por partido=4.55 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 2.5 | 83.2% | 16.8% | 1.20 | 5.95 |
| 3.5 | 66.6% | 33.4% | 1.50 | 2.99 |
| 4.5 | 47.7% | 52.3% | 2.09 | 1.91 |
| 5.5 | 30.6% | 69.4% | 3.27 | 1.44 |

**Remates a puerta Betis: media proyectada 5.91**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Betis a puerta por partido=5.91 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 3.5 | 84.1% | 15.9% | 1.19 | 6.27 |
| 4.5 | 70.3% | 29.7% | 1.42 | 3.36 |
| 5.5 | 54.0% | 46.0% | 1.85 | 2.17 |
| 6.5 | 37.9% | 62.1% | 2.64 | 1.61 |

**Remates a puerta totales: media proyectada 10.46**  
Base: suma de Remates a puerta Elche + Remates a puerta Betis

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 7.5 | 81.8% | 18.2% | 1.22 | 5.51 |
| 8.5 | 71.7% | 28.3% | 1.40 | 3.53 |
| 9.5 | 59.8% | 40.2% | 1.67 | 2.49 |
| 10.5 | 47.4% | 52.6% | 2.11 | 1.90 |
| 11.5 | 35.7% | 64.3% | 2.80 | 1.55 |

**Amarillas Elche: media proyectada 2.55**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Elche recibe por partido=2.55 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 0.5 | 92.2% | 7.8% | 1.08 | 12.81 |
| 1.5 | 72.3% | 27.7% | 1.38 | 3.61 |
| 2.5 | 46.9% | 53.1% | 2.13 | 1.88 |
| 3.5 | 25.3% | 74.7% | 3.95 | 1.34 |

**Amarillas Betis: media proyectada 1.64**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Betis recibe por partido=1.64 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 0.5 | 80.6% | 19.4% | 1.24 | 5.16 |
| 1.5 | 48.8% | 51.2% | 2.05 | 1.95 |
| 2.5 | 22.7% | 77.3% | 4.40 | 1.29 |

**Amarillas totales: media proyectada 4.51**  
⚠️ NO APTO PARA PICK: solo usa lo que produce el equipo, sin datos del rival/árbitro.
Base: Equipos (2.55 + 1.64)=4.19 (UNA_FUENTE) | Soto Grado 2026/27 (14 en 3)=4.67 (UNA_FUENTE) | Soto Grado histórico=4.67 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 3.5 | 65.9% | 34.1% | 1.52 | 2.94 |
| 4.5 | 47.0% | 53.0% | 2.13 | 1.89 |
| 5.5 | 29.9% | 70.1% | 3.35 | 1.43 |
| 6.5 | 17.0% | 83.0% | 5.87 | 1.21 |

> Aviso: remates y tarjetas tienen más varianza que una Poisson; las probabilidades en líneas alejadas de la media son optimistas. Usa sobre todo las líneas cercanas a la media.

## 8. Selección de picks (filtro estricto)
Calidad de datos: **alta** (81.8% de resultados con 2+ fuentes o resueltos por la tabla). Regla: solo es pick si hay cuota publicada, el valor esperado es >= +5% con la probabilidad ya anclada al mercado, y como máximo 2 picks por partido. Sin cuota no hay pick: una probabilidad sin precio no dice si la apuesta vale la pena.

| Apuesta | Cuota | Prob. anclada | Valor esperado | Riesgo | ¿Pick? |
|---|---|---|---|---|---|
| Gana Betis | 2.1 | 47.0% | -0.012 | Alto | no |
| Gana Elche | 3.25 | 28.9% | -0.060 | Alto | no |
| Ambos anotan: sí | 1.6 | 58.2% | -0.068 | Medio | no |
| Empate | 3.8 | 24.0% | -0.087 | Alto | no |

**Sin pick:** ninguna cuota publicada tiene valor suficiente. No apostar también es una decisión.

Stake sugerido: 1 unidad (1-2% del bankroll) por pick; nunca más de 2 selecciones en una combinada.

## 9. Limitaciones
- Muestra pequeña (11 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
