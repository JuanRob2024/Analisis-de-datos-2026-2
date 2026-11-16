# Reglas de negocio — Proyecto Final, Equipo 5

Estas reglas se implementan en el notebook (§3 y §5.5) y definen cómo se interpretan los datos en el modelo dimensional y en el tablero.

| Código | Regla | Dónde se aplica |
|---|---|---|
| RN-01 | `EDUCATION` con códigos 0, 5 y 6 (no documentados) se agrupa en 4 = "Otros"; `MARRIAGE` = 0 se agrupa en 3 = "Otros". | `dim_cliente` |
| RN-02 | Estado de pago: −2 = sin consumo, −1 = pagó el total, 0 = pago mínimo (revolvente), k ≥ 1 = k meses de retraso; 8 representa "8 o más". | `dim_estado_pago`, `fact_estado_cuenta` |
| RN-03 | Un cliente está **en mora** en un mes si su estado de pago es ≥ 1, y en **mora grave** si es ≥ 2. | `fact_estado_cuenta.en_mora`, `mora_grave`; `dim_estado_pago.categoria` |
| RN-04 | Una factura negativa es **saldo a favor** del cliente; la exposición del mes es `max(factura, 0)`. | `fact_estado_cuenta.exposicion`, `saldo_a_favor` |
| RN-05 | Utilización del cupo = factura / cupo, acotada a [−0,5; 2] para limitar valores extremos. | `fact_estado_cuenta.utilizacion` |
| RN-06 | Rangos de edad: 21–25, 26–30, 31–35, 36–40, 41–50, 51–60, 61+. Rangos de cupo (NT$): ≤ 50 mil, 50–100 mil, 100–200 mil, 200–500 mil, > 500 mil. | `dim_cliente` |
| RN-07 | Segmento de riesgo según la probabilidad **calibrada** de incumplimiento: Bajo < 20 %, Medio 20–40 %, Alto 40–60 %, Muy alto ≥ 60 %. | `fact_riesgo_cliente.segmento_riesgo` |
| RN-08 | Pérdida esperada (NT$) = probabilidad de incumplimiento × exposición de septiembre. | `fact_riesgo_cliente.perdida_esperada` |
| RN-09 | Validaciones de calidad: `ID` único, cupo > 0, edad entre 18 y 100, estados de pago entre −2 y 9, objetivo ∈ {0, 1}, sin nulos. Un registro que no cumpla se reporta y se excluye. | §3.1 del notebook |

**Supuestos:**
- El índice 1 de las columnas mensuales corresponde a septiembre de 2005 y el 6 a abril de 2005.
- `PAY_AMT_k` es el pago realizado en el mes k y abona la factura del mes anterior (`BILL_AMT_{k+1}`).
- Los montos están en dólares nuevos de Taiwán (NT$).
