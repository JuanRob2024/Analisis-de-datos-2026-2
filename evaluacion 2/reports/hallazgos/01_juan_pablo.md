# Hallazgos – Juan Pablo (Notebooks 01 y 05)

## Fase 1 – Exploración de bases de datos
- Se exploraron 3 bases de 3 tipos: **Bank Marketing** (tabular, 41.188 × 21), **SMS Spam** (texto, 5.572 mensajes, 13,4 % spam) y **Fashion-MNIST** (imágenes, 70.000 de 28×28 px, 10 clases balanceadas).
- Las tres son fuentes **secundarias**.
- Puntaje por criterios: Bank Marketing 24/25, SMS Spam 20/25, Fashion-MNIST 19/25 → se eligió **Bank Marketing**.

## Fase 3 – Preprocesamiento y PCA
- Se eliminaron `duration` (fuga de información) y `pdays` (reemplazada por `contactado_antes`).
- One-Hot para nominales, Ordinal para `education`, log(1+x) + StandardScaler para `campaign` y `previous`, StandardScaler para el resto → **51 columnas**.
- PCA: **17 componentes explican el 90 %** de la varianza (22 para el 95 %). PC1 + PC2 = 38,5 %.
- PC1 = ciclo económico (euribor3m, emp_var_rate, nr_employed); PC2 = perfil demográfico (edad +, educación −).
- Las clases se solapan en 2D → se recomiendan modelos no lineales y manejo del desbalance.
