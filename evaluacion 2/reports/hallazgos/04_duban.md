# Hallazgos – Duban (Notebook 04: multivariado, hipótesis e insights)
- Multicolinealidad: `emp_var_rate`, `euribor3m` y `nr_employed` tienen correlación entre 0,91 y 0,97 (Pearson y Spearman). Conviene usar solo una o resumirlas con PCA.
- Correlación con `y` (punto-biserial): duration 0,41 (fuga de información), nr_employed −0,36, contactado_antes 0,33, euribor3m −0,31, emp_var_rate −0,30. `age` casi no tiene relación lineal (0,03).
- V de Cramer con `y`: contactado_antes 0,33 y poutcome 0,32 (fuerte), month 0,28, job 0,15 y contact 0,15 (moderada). housing, loan y day_of_week < 0,03 (no aportan).
- Mes × contacto: marzo, septiembre, octubre y diciembre superan el 40 % de éxito por celular. En junio: celular 42,6 % vs fijo 4,7 %.
- Euribor × historial: Euribor < 2 % con campaña anterior exitosa → 66,6 %. Con Euribor ≥ 4 % ningún grupo supera el 8,6 %.

## Verificación de hipótesis (α = 0,05)
| # | Hipótesis | Prueba | Resultado | Efecto | Decisión |
|---|---|---|---|---|---|
| H1 | `poutcome` se asocia con `y` | Chi-cuadrado | success 65,1 % · failure 14,2 % · nonexistent 8,8 % | V = 0,32 (fuerte) | Se confirma |
| H2 | Quienes suscriben tienen menor Euribor | U de Mann-Whitney | mediana 1,27 % vs 4,86 % | r_rb = 0,49 (grande) | Se confirma |
| H3 | Celular suscribe más que fijo | Chi-cuadrado | 14,7 % vs 5,2 % | V = 0,15 (moderada) | Se confirma |
| H4 | La edad influye (jóvenes y mayores suscriben más) | Chi-cuadrado | 17-25: 21,0 % · 36-55: ≈ 8,5 % · 66+: 46,9 % | V = 0,17 (moderada) | Se confirma |
| H5 | Quienes suscriben recibieron menos llamadas | U de Mann-Whitney | media 2,05 vs 2,56; 13,0 % con 1 llamada → 3,6 % con 10+ | r_rb = 0,11 (pequeño) | Se confirma |

## Insights principales
1. **El momento económico es el factor de mayor peso:** con tasas de interés bajas la suscripción se multiplica por 5 (24,5 % vs 4,8 %).
2. **El historial es el mejor predictor del cliente:** quien ya aceptó en una campaña anterior vuelve a aceptar en dos de cada tres casos.
3. **Canal y momento:** llamar por celular y fuera de mayo/julio mejora mucho la tasa de éxito.
4. **Perfil:** la relación con la edad tiene forma de U; jubilados y estudiantes son los segmentos más receptivos.
5. **Insistir no sirve:** cada llamada adicional reduce la probabilidad de éxito; a partir de 5 llamadas la tasa cae por debajo del 8 %.
