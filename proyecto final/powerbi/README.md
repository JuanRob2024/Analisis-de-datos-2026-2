# Dashboard en Power BI — guía de construcción

Guardar el archivo final como `powerbi/proyecto_final_equipo5.pbix`.

## 1. Cargar los datos
*Obtener datos → Texto/CSV* y cargar los 5 archivos de `../data/modelo_estrella/`. En Power Query revisar los tipos de columna:
- `dim_tiempo[fecha]` → Fecha.
- Montos (`cupo`, `monto_facturado`, `monto_pagado`, `exposicion`, `exposicion_sep`, `perdida_esperada`) → Número entero.
- `prob_incumplimiento`, `utilizacion` → Número decimal (formato %).

## 2. Relaciones (vista de modelo)
| Desde (1) | Hacia (*) | Columna |
|---|---|---|
| `dim_cliente` | `fact_estado_cuenta` | `id_cliente` |
| `dim_cliente` | `fact_riesgo_cliente` | `id_cliente` (1:1; dejar dirección única desde `dim_cliente`) |
| `dim_tiempo` | `fact_estado_cuenta` | `id_mes` |
| `dim_estado_pago` | `fact_estado_cuenta` | `id_estado_pago` |

Marcar `dim_tiempo` como tabla de fechas (columna `fecha`). Ordenar `nombre_mes` por `mes`.

## 3. Medidas DAX (crear una tabla `_Medidas`)
```DAX
Clientes = DISTINCTCOUNT ( dim_cliente[id_cliente] )
Tasa incumplimiento real = AVERAGE ( fact_riesgo_cliente[incumplio_real] )
Prob. media predicha = AVERAGE ( fact_riesgo_cliente[prob_incumplimiento] )
Pérdida esperada = SUM ( fact_riesgo_cliente[perdida_esperada] )
Exposición septiembre = SUM ( fact_riesgo_cliente[exposicion_sep] )
% Pérdida sobre exposición = DIVIDE ( [Pérdida esperada], [Exposición septiembre] )
Clientes alto riesgo =
    CALCULATE ( [Clientes], fact_riesgo_cliente[segmento_riesgo] IN { "3-Alto", "4-Muy alto" } )

Facturado = SUM ( fact_estado_cuenta[monto_facturado] )
Pagado = SUM ( fact_estado_cuenta[monto_pagado] )
% Pago sobre facturado = DIVIDE ( [Pagado], [Facturado] )
% Clientes en mora = AVERAGE ( fact_estado_cuenta[en_mora] )
% Mora grave = AVERAGE ( fact_estado_cuenta[mora_grave] )
Utilización media = AVERAGE ( fact_estado_cuenta[utilizacion] )

-- Desempeño del modelo (filtrar conjunto = "Prueba")
VP = CALCULATE ( [Clientes], fact_riesgo_cliente[prediccion_incumple] = 1, fact_riesgo_cliente[incumplio_real] = 1 )
Predichos positivos = CALCULATE ( [Clientes], fact_riesgo_cliente[prediccion_incumple] = 1 )
Reales positivos = CALCULATE ( [Clientes], fact_riesgo_cliente[incumplio_real] = 1 )
Precision = DIVIDE ( [VP], [Predichos positivos] )
Recall = DIVIDE ( [VP], [Reales positivos] )
```

## 4. Páginas propuestas
1. **Resumen ejecutivo:** tarjetas (Clientes, Tasa de incumplimiento real, Exposición, Pérdida esperada, Clientes alto riesgo); dona de clientes por segmento; barras de pérdida esperada por segmento.
2. **Evolución de la cartera:** líneas Facturado vs. Pagado por `nombre_mes`; línea % clientes en mora y % mora grave; barras apiladas de clientes por `dim_estado_pago[categoria]` y mes.
3. **Perfiles de riesgo:** tasa de incumplimiento por rango de cupo, rango de edad, educación y estado civil; matriz rango de cupo × segmento con pérdida esperada (formato condicional).
4. **Priorización de cobro:** tabla de clientes ordenada por pérdida esperada (id, segmento, probabilidad, exposición, meses en mora, utilización), con segmentadores por segmento y rango de cupo.
5. **Desempeño del modelo:** tarjetas Precision/Recall filtradas a `conjunto = "Prueba"`, tasa real vs. probabilidad media por segmento, e imágenes `../figuras/05_roc_pr.png` y `07_importancia.png`.

Segmentadores globales sugeridos: `segmento_riesgo`, `rango_cupo`, `sexo`, `educacion`.

> Nota: `prob_incumplimiento` ya está calibrada (calibración isotónica, §5.5 del notebook), así que la pérdida esperada se puede presentar como monto en NT$. En la página 5 conviene incluir también `../figuras/08_calibracion.png`.
