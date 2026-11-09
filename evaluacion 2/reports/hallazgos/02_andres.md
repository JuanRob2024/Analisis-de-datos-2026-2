# Hallazgos – Andrés (Notebook 02: faltantes y atípicos)
- 12 filas duplicadas eliminadas → 41.176 registros.
- 0 `NaN` explícitos, pero faltantes ocultos como `unknown`: default 20,88 %, education 4,20 %, housing 2,40 %, loan 2,40 % (siempre en las mismas filas), job 0,80 %, marital 0,19 %.
- `pdays = 999` en 96,3 % → indicador `contactado_antes`.
- `default = unknown` suscribe 5,2 % vs 12,9 % con dato → faltante informativo, se conserva como categoría. Resto: imputación por moda.
- Atípicos (IQR): previous 13,7 %, duration 7,2 %, campaign 5,8 %, age 1,1 %. Variables macro: 0 %.
- `campaign` acotada al percentil 99 (14 llamadas). `age` y `duration` se conservan (valores reales).
- Clientes contactados más de 10 veces: solo 3,1 % de éxito.
