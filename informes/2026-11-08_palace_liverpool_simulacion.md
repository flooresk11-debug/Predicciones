# Simulación auditada: Crystal Palace vs Liverpool
Premier League 2026/27 - Jornada 10 · 2026-11-08 15:00 CET

## 1. Auditoría de datos
```
OK  Crystal Palace: 9 PJ, 2G 1E 6P, 9:21, 7 pts = coincide con la tabla publicada
    estados de los resultados de Crystal Palace: {'VERIFICADO': 9}
OK  Liverpool: 9 PJ, 4G 3E 2P, 11:9, 15 pts = coincide con la tabla publicada
    estados de los resultados de Liverpool: {'VERIFICADO': 9}
OK  tiros Liverpool: 140 en 9 PJ (15.56 por partido), 12.73 tiros por gol, a puerta 39 (4.33/p, precisión 27.9%); goles 11 <= a puerta <= tiros: coherente
AVISO tiros Crystal Palace: 90 en 9 PJ (10.00 por partido), 10.00 tiros por gol, a puerta 31 (3.44/p, precisión 34.4%); goles 9 <= a puerta <= tiros: coherente
NO_DISPONIBLE corners: no se usa
OK  tarjetas Liverpool: 21 amarillas / 9 PJ = 2.33 (publicado 2.33)
OK  árbitro Tony Harrington: 14 amarillas / 4 PJ = 3.50 por partido
EXCLUIDO (conflicto entre fuentes) h2h.historico_total: 28 o 30 duelos según la ventana; no se usa
```
**Resultado de la auditoría:** todos los totales cuadran con la tabla publicada.

Datos **no disponibles** (no se inventan): corners, asistencias, estadísticas de primer tiempo completas, tabla completa.

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

## 6b. Remates, remates a puerta y tarjetas (Poisson sobre promedios auditados)

**Remates Liverpool: media proyectada 14.13**  
Base: Liverpool remata por partido=15.56 (VERIFICADO) | Palace concede por partido=12.70 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 11.5 | 75.1% | 24.9% | 1.33 | 4.01 |
| 12.5 | 65.4% | 34.6% | 1.53 | 2.89 |
| 13.5 | 54.9% | 45.1% | 1.82 | 2.22 |
| 14.5 | 44.3% | 55.7% | 2.26 | 1.80 |
| 15.5 | 34.4% | 65.6% | 2.91 | 1.52 |

**Remates Crystal Palace: media proyectada 10.00**  
Base: Palace remata por partido=10.00 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 7.5 | 78.0% | 22.0% | 1.28 | 4.54 |
| 8.5 | 66.7% | 33.3% | 1.50 | 3.00 |
| 9.5 | 54.2% | 45.8% | 1.84 | 2.18 |
| 10.5 | 41.7% | 58.3% | 2.40 | 1.72 |
| 11.5 | 30.3% | 69.7% | 3.30 | 1.44 |

**Remates totales: media proyectada 24.13**  
Base: suma de Remates Liverpool + Remates Crystal Palace

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 20.5 | 76.5% | 23.5% | 1.31 | 4.26 |
| 21.5 | 69.5% | 30.5% | 1.44 | 3.28 |
| 22.5 | 61.8% | 38.2% | 1.62 | 2.62 |
| 23.5 | 53.8% | 46.2% | 1.86 | 2.16 |
| 24.5 | 45.7% | 54.3% | 2.19 | 1.84 |
| 25.5 | 37.8% | 62.2% | 2.64 | 1.61 |

**Remates a puerta Liverpool: media proyectada 4.33**  
Base: Liverpool a puerta por partido=4.33 (VERIFICADO)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 2.5 | 80.6% | 19.4% | 1.24 | 5.16 |
| 3.5 | 62.8% | 37.2% | 1.59 | 2.69 |
| 4.5 | 43.5% | 56.5% | 2.30 | 1.77 |
| 5.5 | 26.8% | 73.2% | 3.73 | 1.37 |

**Remates a puerta Crystal Palace: media proyectada 3.62**  
Base: Palace a puerta por partido=3.44 (VERIFICADO) | Liverpool concede a puerta=3.80 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 1.5 | 87.6% | 12.4% | 1.14 | 8.08 |
| 2.5 | 70.1% | 29.9% | 1.43 | 3.34 |
| 3.5 | 48.9% | 51.1% | 2.04 | 1.96 |
| 4.5 | 29.7% | 70.3% | 3.36 | 1.42 |

**Remates a puerta totales: media proyectada 7.95**  
Base: suma de Remates a puerta Liverpool + Remates a puerta Crystal Palace

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 5.5 | 80.4% | 19.6% | 1.24 | 5.11 |
| 6.5 | 68.0% | 32.0% | 1.47 | 3.13 |
| 7.5 | 54.0% | 46.0% | 1.85 | 2.17 |
| 8.5 | 40.0% | 60.0% | 2.50 | 1.67 |
| 9.5 | 27.7% | 72.3% | 3.61 | 1.38 |

**Amarillas Liverpool: media proyectada 2.00**  
Base: Liverpool recibe por partido=2.33 (VERIFICADO) | Rivales de Palace reciben por partido=1.67 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 0.5 | 86.5% | 13.5% | 1.16 | 7.39 |
| 1.5 | 59.4% | 40.6% | 1.68 | 2.46 |
| 2.5 | 32.3% | 67.7% | 3.09 | 1.48 |

**Amarillas Crystal Palace: media proyectada 1.89**  
Base: Palace recibe por partido=1.44 (UNA_FUENTE) | Rivales de Liverpool reciben por partido=2.33 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 0.5 | 84.8% | 15.2% | 1.18 | 6.59 |
| 1.5 | 56.2% | 43.8% | 1.78 | 2.28 |
| 2.5 | 29.2% | 70.8% | 3.42 | 1.41 |

**Amarillas totales: media proyectada 3.52**  
Base: Equipos (2.00 + 1.89)=3.89 (UNA_FUENTE) | Árbitro Harrington 2026/27=3.50 (VERIFICADO) | Árbitro Harrington 2025/26=3.17 (UNA_FUENTE)

| Línea | Más de | Menos de | Cuota justa más | Cuota justa menos |
|---|---|---|---|---|
| 2.5 | 68.3% | 31.7% | 1.46 | 3.15 |
| 3.5 | 46.8% | 53.2% | 2.14 | 1.88 |
| 4.5 | 27.8% | 72.2% | 3.59 | 1.39 |
| 5.5 | 14.5% | 85.5% | 6.89 | 1.17 |

Cuota publicada: mas de 3.5 a 1.8 (squawka.com (4/5, bet365; 'más de 3.5 tarjetas')) -> prob. modelo 46.8%, implícita 55.6%, valor esperado -0.158

Estimadores **excluidos** por conflicto o falta de datos:
- Remates Crystal Palace · Palace remata (premierleague.com): CONFLICTO (62 tiros en 9 PJ, no cuadra con fbref/statz)
- Remates Crystal Palace · Liverpool concede por partido: NO_DISPONIBLE (no encontrado)
- Remates a puerta Liverpool · Palace concede a puerta: NO_DISPONIBLE (no encontrado)

> Aviso: remates y tarjetas tienen más varianza que una Poisson; las probabilidades en líneas alejadas de la media son optimistas. Usa sobre todo las líneas cercanas a la media.

## 7. Limitaciones
- Muestra pequeña (9 partidos de liga por equipo): intervalos de confianza amplios.
- El modelo Poisson no incorpora bajas, H2H ni motivación; esos factores se tratan en el análisis cualitativo.
- Varios resultados tienen una sola fuente; la auditoría confirma que los totales cuadran con la tabla.
