# Simulación auditada: Villarreal vs Getafe
LaLiga EA Sports 2026/27 - Jornada 12 · 2026-11-08 18:30 CET


## 0. Ventaja de precio frente a Pinnacle (método v3, el único con CLV positivo en el backtest)
- Pinnacle 1X2: 1 1.45 · X 4.74 · 2 7.42 (margen 3.5%) -> justo: 1 66.6% · X 20.4% · 2 13.0%
- Fuente Pinnacle: rcdm.es (previa del 8/11; puede haber cambiado)

| Mercado | Casa | Cuota | Prob. justa (Pinnacle) | Ventaja | ¿Pick? |
|---|---|---|---|---|---|
| 1 | Novibet | 1.58 | 66.6% | +5.2% | SÍ |
| 1 | n/d | 1.53 | 66.6% | +1.9% | no |
| 1 | JokerBet | 1.43 | 66.6% | -4.8% | no |
| X | JokerBet | 4.6 | 20.4% | -6.3% | no |
| 2 | JokerBet | 7.6 | 13.0% | -1.1% | no |
| 2 | Betwinner | 7.1 | 13.0% | -7.6% | no |

Regla: pick solo si ventaja >= +2%. 
⚠️ Las cuotas cambian: confirma en el momento que Pinnacle y tu casa siguen en estos precios; si la ventaja desaparece, no hay apuesta.

## 1. Auditoría de datos
```
OK  Getafe (agregados): 11 PJ, 3G 3E 5P, 8:16, 12 pts = 3x3+3 y coincide con la tabla
    nota: Getafe sin lista partido a partido completa -> BTTS/porterías a cero n/d
OK  Villarreal: 11 PJ, 3G 3E 5P, 15:15, 12 pts = coincide con la tabla publicada
    estados de los resultados de Villarreal: {'VERIFICADO': 11}
NO_DISPONIBLE tiros_totales: no se usa
NO_DISPONIBLE corners: no se usa
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): , asistencias, estadísticas de primer tiempo completas, tabla completa.

## 2. Estadísticas reales (LaLiga EA Sports 2026/27)
| Equipo | Condición | PJ | G-E-P | GF | GC | GF/p | GC/p | Goles/p | BTTS | Port. cero | Sin marcar | +2.5 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Villarreal | Total | 11 | 3-3-5 | 15 | 15 | 1.36 | 1.36 | 2.73 | 63.6% | 9.1% | 36.4% | 63.6% |
| Villarreal | Local | 5 | 1-1-3 | 6 | 7 | 1.20 | 1.40 | 2.60 | 60.0% | 20.0% | 40.0% | 60.0% |
| Getafe | Total | 11 | 3-3-5 | 8 | 16 | 0.73 | 1.45 | 2.18 | n/d | n/d | n/d | n/d |

## 3. Modelo
- Goles esperados (global): Villarreal 1.41 · Getafe 1.05
- Goles esperados (local en casa / visitante fuera): Villarreal 1.33 · Getafe 1.06
- Peso de la condición local/visitante: 0.35 (muestra pequeña por condición)
- λ solo con datos: Villarreal 1.38 · Getafe 1.05
- Mercado sin margen (3.5% de margen quitado): 1 66.6% · X 20.4% · 2 13.0%
- Modelo puro: 1 44.4% · X 27.0% · 2 28.6%
- Mezcla (peso mercado 60%): 1 57.7% · X 23.0% · 2 19.3%
- **λ final: Villarreal 1.63 · Getafe 0.80** (total esperado 2.43)
- Monte Carlo 200,000 simulaciones (semilla 2026): 1 56.8% · X 24.8% · 2 18.3% · BTTS 44.3% · +2.5 43.6%

## 4. Probabilidades (cálculo exacto Poisson)
| Mercado | Probabilidad | Cuota justa |
|---|---|---|
| 1 | 57.0% | 1.75 |
| X | 24.6% | 4.06 |
| 2 | 18.3% | 5.45 |
| 1X | 81.7% | 1.22 |
| X2 | 43.0% | 2.33 |
| 12 | 75.4% | 1.33 |
| BTTS sí | 44.4% | 2.25 |
| BTTS no | 55.6% | 1.80 |
| Más de 1.5 | 69.9% | 1.43 |
| Más de 2.5 | 43.9% | 2.28 |
| Menos de 2.5 | 56.1% | 1.78 |
| Más de 3.5 | 22.8% | 4.39 |
| Menos de 3.5 | 77.2% | 1.30 |
| Local portería a cero | 44.8% | 2.23 |
| Visitante portería a cero | 19.6% | 5.10 |
| Local menos de 1.5 | 51.5% | 1.94 |
| Visitante más de 0.5 | 55.2% | 1.81 |
| Visitante más de 1.5 | 19.2% | 5.20 |
| Visitante gana por 2+ | 5.6% | 18.01 |
| Visitante gana a cero | 10.8% | 9.25 |

Marcadores más probables: 1-0 (14.3%), 2-0 (11.7%), 1-1 (11.5%), 2-1 (9.4%), 0-0 (8.8%), 0-1 (7.1%), 3-0 (6.3%), 3-1 (5.1%)

## 5. Comparación con cuotas publicadas
| Apuesta | Cuota | Prob. implícita | Prob. modelo | Valor esperado por 1 unidad |
|---|---|---|---|---|
| Gana Villarreal | 1.58 | 63.3% | 57.0% | -0.099 |
| Empate | 4.6 | 21.7% | 24.6% | +0.133 |
| Gana Getafe | 7.6 | 13.2% | 18.3% | +0.394 |
| Menos de 3.5 goles | 1.33 | 75.2% | 77.2% | +0.027 |

## 6. Sensibilidad (¿cambia la conclusión si cambio supuestos?)
| Peso condición | λ local | λ visit. | 1 | X | 2 | +2.5 | BTTS |
|---|---|---|---|---|---|---|---|
| 0.00 | 1.41 | 1.05 | 45.3% | 26.7% | 27.9% | 44.4% | 49.0% |
| 0.20 | 1.39 | 1.05 | 44.8% | 26.9% | 28.3% | 44.1% | 48.8% |
| 0.35 | 1.38 | 1.05 | 44.4% | 27.0% | 28.6% | 43.9% | 48.7% |
| 0.50 | 1.37 | 1.05 | 44.0% | 27.1% | 28.9% | 43.6% | 48.6% |
| 0.70 | 1.35 | 1.06 | 43.5% | 27.2% | 29.3% | 43.3% | 48.4% |

## 6b. Remates, remates a puerta y tarjetas (Poisson sobre promedios auditados)

**Amarillas totales: media proyectada 4.45**  
Base: Getafe 25/26 propias + rival de Villarreal=5.00 (VERIFICADO) | H2H 10 partidos=3.90 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 2.5 | 82.1% | 17.9% | 1.22 | 5.58 |
| 3.5 | 64.9% | 35.1% | 1.54 | 2.85 |
| 4.5 | 45.8% | 54.2% | 2.18 | 1.85 |
| 5.5 | 28.9% | 71.1% | 3.47 | 1.41 |

> Aviso: remates y tarjetas tienen más varianza que una Poisson; las probabilidades en líneas alejadas de la media son optimistas. Usa sobre todo las líneas cercanas a la media.

## 8. Selección de picks (filtro estricto)
Calidad de datos: **baja** (sin lista completa partido a partido). Regla: solo es pick si hay cuota publicada, el valor esperado es >= +5% con la probabilidad ya anclada al mercado, y como máximo 2 picks por partido. Sin cuota no hay pick: una probabilidad sin precio no dice si la apuesta vale la pena.

| Apuesta | Cuota | Prob. anclada | Valor esperado | Riesgo | ¿Pick? |
|---|---|---|---|---|---|
| Gana Getafe | 7.6 | 18.3% | +0.394 | Alto | no |
| Empate | 4.6 | 24.6% | +0.133 | Alto | no |
| Menos de 3.5 goles | 1.33 | 77.2% | +0.027 | Medio | no |
| Gana Villarreal | 1.58 | 57.0% | -0.099 | Medio | no |

**Sin pick (bloqueado):** calidad de datos baja. Los valores esperados de arriba son solo informativos.

Stake sugerido: 1 unidad (1-2% del bankroll) por pick; nunca más de 2 selecciones en una combinada.

## 9. Limitaciones
- Muestra pequeña (11 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
