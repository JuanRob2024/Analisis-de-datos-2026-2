# Evento Evaluativo 4 — Equipo 5: Hallazgos, decisiones y notas

**Asignatura:** Análisis de Datos · **Docente:** Daniel Alexis Nieto Mora · **Grupo:** 190304018-1 · **Periodo:** 2026-2
**Integrantes:** Juan Pablo Robledo (líder) · María Camila Álvarez · Duban Guerra · Andrés Villa
**Entrega:** viernes 13 de noviembre de 2026 (sin prórroga) · carpeta `evaluacion 4` del repositorio del curso

---

## 1. Criterios de evaluación (sección 8 de la guía)

| # | Criterio | Qué se evalúa |
|---|---|---|
| 1 | Comprensión del problema y EDA | Interpretar el contexto, comprender las variables, reconocer características y dificultades del dataset |
| 2 | Preprocesamiento | Transformaciones adecuadas y justificadas, evitando la fuga de información |
| 3 | Algoritmos supervisados | Implementación, justificación y comparación |
| 4 | Algoritmos no supervisados | Implementación, justificación y comparación |
| 5 | Evaluación de modelos | Métricas apropiadas e interpretación crítica |
| 6 | Visualización e interpretación | Calidad de las gráficas y conclusiones extraídas |
| 7 | Análisis crítico y conclusiones | Limitaciones, comparación de enfoques, recomendaciones fundamentadas |
| 8 | Documentación y trabajo colaborativo | Organización del repo, claridad del código, commits claros, evidencia de participación |
| 9 | Presentación en video | Claridad, dominio del tema, organización, síntesis; participación de todos |

La rúbrica detallada se compartirá después. También se tendrá en cuenta la retroalimentación de entregas anteriores.

---

## 2. Qué pide la guía

### Requisitos generales
- Python (notebook, `.py`, Jupyter o Colab).
- Componente supervisado: mínimo **2 algoritmos** de clasificación.
- Componente no supervisado: mínimo **2 algoritmos** de agrupamiento o detección de anomalías.
- Justificar cada algoritmo: por qué es apropiado, supuestos, ventajas y limitaciones.
- El notebook debe incluir: descripción del problema, EDA, preprocesamiento, justificación, entrenamiento, resultados, métricas, visualizaciones y conclusiones.
- Usar reducción de dimensionalidad (PCA, t-SNE o UMAP) cuando sea pertinente.
- No usar la variable objetivo en el clustering (solo para interpretar después).
- Evitar la fuga de información: todo lo que aprenda de los datos se ajusta solo con entrenamiento.
- Si se muestrea, justificar el procedimiento.

### Requisitos específicos del Equipo 5
- Analizar historial de pagos, facturación y límites de crédito.
- Estudiar la distribución de la variable objetivo y el desbalance.
- Comparar al menos 2 modelos supervisados y 2 algoritmos de agrupamiento.
- Evaluar con F1-score, Recall, Precision y ROC-AUC.
- Analizar la importancia de las variables.
- Caracterizar los grupos y contrastarlos con los comportamientos de pago.
- Discutir los riesgos de usar modelos predictivos en decisiones financieras.

### Estructura mínima del notebook
1. Descripción del problema · 2. Comprensión y exploración · 3. Preprocesamiento · 4. Supervisado · 5. No supervisado · 6. Visualización y reducción de dimensionalidad · 7. Comparación e interpretación · 8. Conclusiones

### Entregables
- Notebook(s) de los dos componentes.
- `README.md` con problema, integrantes, estructura, instrucciones de ejecución, fuentes y resultados.
- Visualizaciones y recursos complementarios.
- Video de máximo 12 minutos (o enlace), con participación de todos.
- Documentación de decisiones técnicas y resultados.

---

## 3. Fuente de datos

- **Dataset:** *Default of Credit Card Clients* — UCI Machine Learning Repository.
- **Referencia:** Yeh, I. C. & Lien, C. H. (2009). *The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients.* Expert Systems with Applications, 36(2), 2473–2480.
- **URL:** https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
- **Contenido:** 30.000 clientes de un banco de Taiwán, abril–septiembre de 2005. 23 variables explicativas + objetivo (`default payment next month`: incumple en octubre).
- **Nota técnica:** el notebook descarga el archivo desde la URL oficial de UCI si no existe en `data/`. Para la ejecución de prueba se usó una copia idéntica del `.xls` original.

### Diccionario de variables

| Variable | Descripción |
|---|---|
| `LIMIT_BAL` | Cupo de crédito (dólares NT), individual + familiar |
| `SEX` | 1 = hombre, 2 = mujer |
| `EDUCATION` | 1 = posgrado, 2 = universidad, 3 = secundaria, 4 = otros |
| `MARRIAGE` | 1 = casado, 2 = soltero, 3 = otros |
| `AGE` | Edad |
| `PAY_0`, `PAY_2..PAY_6` | Estado de pago sep. → abr. (−2 sin consumo, −1 pagó total, 0 pago mínimo, 1..9 meses de retraso) |
| `BILL_AMT1..6` | Monto facturado sep. → abr. |
| `PAY_AMT1..6` | Monto pagado sep. → abr. |

---

## 4. Calidad de datos y decisiones de limpieza

| Problema encontrado | Decisión | Justificación |
|---|---|---|
| Sin valores nulos | Ninguna acción | — |
| 35 filas idénticas (sin `ID`) | Se conservan | Son clientes distintos (IDs diferentes), mayormente inactivos |
| `EDUCATION` con 0, 5, 6 (465 registros) | Agrupados en 4 = "otros" | Códigos no documentados; regla fija → no hay fuga de información |
| `MARRIAGE` con 0 (54 registros) | Agrupado en 3 = "otros" | Igual que el anterior |
| `PAY_k` con −2 y 0 | Se mantienen como numéricos | Significan "sin consumo" y "pago mínimo"; la relación con el riesgo es ordinal |
| `BILL_AMT` negativos (1.930 clientes) | Se conservan | Representan saldo a favor, son válidos |
| Miles de atípicos (IQR) en montos | No se eliminan; log con signo `sign(x)·log(1+|x|)` | Son clientes reales con cupos/pagos altos; la transformación reduce su influencia |
| `PAY_0` sin `PAY_1` | Renombrado a `PAY_1` | Alinear sufijos con `BILL_AMT1` y `PAY_AMT1` |

---

## 5. Hallazgos del análisis exploratorio

### Variable objetivo
- 22,1 % incumple (6.636 de 30.000). Desbalance ≈ 3,5 : 1 (moderado).
- Un modelo que siempre prediga "no incumple" tendría 78 % de *accuracy* y 0 % de *recall* → *accuracy* es engañosa.

### Historial de pagos (la señal más fuerte)

| Estado en septiembre (`PAY_1`) | Tasa de incumplimiento |
|---|---|
| −2 (sin consumo) | 13,2 % |
| −1 (pagó total) | 16,8 % |
| 0 (pago mínimo) | 12,8 % |
| 1 mes de retraso | 33,9 % |
| 2 meses de retraso | **69,1 %** |
| 3 meses de retraso | 75,8 % |

| Meses con retraso (de 6) | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Tasa de incumplimiento | 11,7 % | 29,8 % | 38,8 % | 50,9 % | 57,3 % | 57,4 % | 70,3 % |

### Variables demográficas (diferencias pequeñas)
- Sexo: hombres 24,2 % vs. mujeres 20,8 %.
- Educación: posgrado 19,2 %, universidad 23,7 %, secundaria 25,2 %, otros 7,1 % (grupo pequeño con códigos no documentados; no sobreinterpretar).
- Estado civil: casado 23,5 %, soltero 20,9 %, otros 23,6 %.
- Edad: forma de U. ≤25 años 26,7 %; 26–35 ≈ 19–20 %; >45 ≈ 25–27 %.
- Son variables **sensibles** (sexo, edad, estado civil): relevante para la discusión ética.

### Variables financieras
- Quienes incumplen tienen **cupos más bajos** y **mayor utilización** del cupo.
- Montos fuertemente asimétricos a la derecha.
- Correlación de Spearman con `DEFAULT`: `PAY_1` 0,29; `PAY_2` 0,22; `PAY_3` 0,20; `PAY_4` 0,17; `LIMIT_BAL` −0,17; `PAY_AMT1` −0,16.
- `BILL_AMT1..6` casi perfectamente correlacionadas (ρ > 0,9): **multicolinealidad temporal**.

---

## 6. Preprocesamiento

### Ingeniería de características (fila a fila, sin fuga de información)

| Variable | Definición | Media (no incumple / incumple) |
|---|---|---|
| `n_meses_mora` | # meses con `PAY_k > 0` | 0,50 / 2,00 |
| `max_mora` | máximo de `PAY_k` (mín. 0) | 0,47 / 1,43 |
| `meses_inactivo` | # meses con `PAY_k = −2` | 0,85 / 0,68 |
| `util_media` | media de `BILL_AMT_k / LIMIT_BAL` | 0,35 / 0,45 |
| `util_max` | máximo de la utilización | 0,47 / 0,56 |
| `ratio_pago` | Σ pagos / Σ facturas del mes anterior, acotado a [0, 1] | 0,41 / 0,31 |
| `tendencia_deuda` | (`BILL_AMT1` − `BILL_AMT6`) / `LIMIT_BAL` | 0,11 / 0,09 |

Nota: `PAY_AMT_k` paga la factura del mes anterior (`BILL_AMT_{k+1}`), por eso el ratio se calcula con ese desfase.

### Partición
- 80 % entrenamiento (24.000) / 20 % prueba (6.000), estratificado (22,1 % de morosos en ambos).
- Se hace **antes** de cualquier transformación que aprenda de los datos.

### Pipeline (evita fuga de información)
- Montos (`LIMIT_BAL`, `BILL_AMT*`, `PAY_AMT*`): log con signo + `StandardScaler`.
- Numéricas/ordinales (`AGE`, `PAY_k`, variables creadas): `StandardScaler`.
- Categóricas (`SEX`, `EDUCATION`, `MARRIAGE`): `OneHotEncoder` (baja cardinalidad).
- Todo dentro de `Pipeline` + `ColumnTransformer`: el escalador y el codificador se ajustan solo con los pliegues de entrenamiento en la validación cruzada.

---

## 7. Componente supervisado

### Algoritmos y justificación

| Modelo | Por qué | Supuestos | Ventajas | Limitaciones |
|---|---|---|---|---|
| Regresión logística (L2) | Línea base estándar en *credit scoring* | Relación lineal con log-odds; poca colinealidad | Interpretable, rápida, aceptada por reguladores | No captura interacciones; afectada por colinealidad |
| Random Forest | Captura no linealidades e interacciones | Ninguno fuerte | Robusto a atípicos y colinealidad | Menos interpretable, más costoso |
| Histogram Gradient Boosting | Estado del arte en datos tabulares | Ninguno fuerte | Alto desempeño, rápido | Más hiperparámetros, "caja negra" |

### Tratamiento del desbalance
- `class_weight="balanced"` en los tres modelos.
- Selección de hiperparámetros optimizando **PR-AUC** (*average precision*).
- Umbral de decisión elegido maximizando F1 con predicciones **out-of-fold** del entrenamiento (sin tocar prueba).
- **SMOTE descartado**: interpolaría estados de pago discretos (p. ej. "1,4 meses de retraso"), que no tienen sentido; con 3,5 : 1 bastan los pesos.

### Hiperparámetros elegidos (`RandomizedSearchCV`, 4 pliegues estratificados)
- Regresión logística: `C ≈ 0,0053` (regularización fuerte por colinealidad). PR-AUC CV = 0,510.
- Random Forest: `max_depth=8`, `min_samples_leaf=5`, `max_features=0.3`, 200 árboles. PR-AUC CV = 0,565.
- Gradient Boosting: `learning_rate=0.1`, `max_leaf_nodes=15`, `min_samples_leaf=20`, `l2_regularization=5`, `max_iter=200`. PR-AUC CV = 0,564.

### Umbrales óptimos (out-of-fold)
- Regresión logística: 0,60 · Random Forest: 0,54 · Gradient Boosting: 0,56.

### Resultados en prueba (6.000 clientes)

| Modelo | Umbral | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Regresión logística | 0,5 | 0,435 | 0,612 | 0,509 | 0,755 | 0,499 |
| Regresión logística | 0,60 | 0,490 | 0,543 | 0,515 | 0,755 | 0,499 |
| Random Forest | 0,5 | 0,490 | 0,601 | 0,540 | 0,779 | 0,555 |
| Random Forest | 0,54 | 0,524 | 0,566 | 0,544 | 0,779 | 0,555 |
| Gradient Boosting | 0,5 | 0,459 | 0,631 | 0,531 | 0,782 | 0,561 |
| **Gradient Boosting** | **0,56** | **0,514** | **0,584** | **0,547** | **0,782** | **0,561** |
| Regla base `PAY_1 ≥ 1` | — | 0,498 | 0,497 | 0,498 | 0,678 | 0,359 |

**Interpretación**
- Los ensambles superan a la regresión logística, pero la mejora es modesta: la mayor parte de la señal está en el historial de pagos.
- RF y Gradient Boosting están prácticamente empatados (≈ 0,005 en PR-AUC).
- Ajustar el umbral cambia el balance: con 0,5 se detectan más morosos (Recall ≈ 0,60–0,63) pero con más falsas alarmas; con el umbral óptimo la precisión sube a ≈ 0,51–0,52.
- El mejor modelo detecta ≈ 58 % de los morosos y ≈ 1 de cada 2 alertas es correcta. Útil para **priorizar**, no para decidir solo.
- F1 ≈ 0,55 es un techo conocido en este dataset: sin ingresos ni datos de buró, parte del impago no es predecible.

### Importancia de variables
- Permutación (Gradient Boosting): `PAY_1` >> `n_meses_mora` > `max_mora` > `BILL_AMT1`, `tendencia_deuda`, `util_max`, pagos, `LIMIT_BAL`.
- Coeficientes de regresión logística: aumentan el riesgo `n_meses_mora`, `max_mora`, `util_media`, `PAY_1`; lo reducen `LIMIT_BAL`, `meses_inactivo`, `PAY_AMT3`.
- `PAY_3` y `PAY_4` salen con signo negativo por **multicolinealidad** (su información ya está en `n_meses_mora` y `max_mora`): interpretar coeficientes individuales con cautela.
- Las demográficas tienen importancia muy baja.

### Aporte por grupo de variables (Gradient Boosting, CV en entrenamiento)

| Grupo | # vars | ROC-AUC | PR-AUC |
|---|---|---|---|
| Solo demográficas | 4 | 0,563 | 0,256 |
| Solo financieras | 17 | 0,736 | 0,461 |
| Solo historial de pagos | 9 | 0,750 | 0,528 |
| Todas excepto demográficas | 26 | 0,785 | 0,560 |
| Todas | 30 | 0,787 | 0,564 |

- Historial de pagos y variables financieras son **complementarias**.
- **Quitar las demográficas no cambia el desempeño** → se puede construir un modelo igual de útil sin sexo, edad, estado civil ni educación.

### Desempeño por grupo sensible (prueba, Gradient Boosting)

| Grupo | n | Impago real | Marcados como riesgo | Recall | Falsos positivos | Precision |
|---|---|---|---|---|---|---|
| Hombre | 2.402 | 23,4 % | 27,5 % | 0,585 | **18,0 %** | 0,497 |
| Mujer | 3.598 | 21,3 % | 23,6 % | 0,584 | 14,2 % | 0,527 |
| ≤30 años | 2.181 | 22,0 % | 25,6 % | 0,608 | 15,7 % | 0,522 |
| 31–45 | 2.853 | 21,2 % | 23,4 % | 0,556 | 14,7 % | 0,504 |
| >45 | 966 | 25,3 % | 29,4 % | 0,607 | **18,8 %** | 0,521 |

- Recall similar entre grupos, pero más falsos positivos en hombres y mayores de 45: un buen pagador de esos grupos tiene más probabilidad de ser rechazado injustamente.

---

## 8. Componente no supervisado

### Variables de segmentación (sin `DEFAULT` y sin demográficas)
`log_limite`, `util_media`, `ratio_pago`, `n_meses_mora`, `max_mora`, `meses_inactivo`, `tendencia_deuda` → estandarizadas.

- Se usa el conjunto completo (30.000): el clustering no tiene etiqueta ni conjunto de prueba que proteger.
- Métricas costosas ($O(n^2)$, como Silhouette) sobre una muestra aleatoria de 6.000. t-SNE sobre 4.000.

### Algoritmos y justificación

| Algoritmo | Por qué | Supuestos | Ventajas | Limitaciones |
|---|---|---|---|---|
| K-Means | Referencia en segmentación; centroide = "cliente típico" | Grupos esféricos de tamaño similar | Escalable, simple, interpretable | Sensible a escala y atípicos; requiere fijar *k* |
| GMM | Grupos elípticos, distinto tamaño, pertenencia probabilística | Mezcla de normales | Más flexible; BIC | Variables de conteo no son gaussianas |
| Ward (comparación) | Jerárquico, sin inicialización aleatoria | Minimiza varianza intra-grupo | Estructura a varias escalas | $O(n^2)$ → solo sobre muestra |

### Selección de *k*

| k | Inercia | Silhouette KM | Davies-Bouldin KM | Silhouette GMM |
|---|---|---|---|---|
| 2 | 149.469 | 0,278 | 1,425 | 0,232 |
| 3 | 111.298 | 0,316 | 1,242 | 0,183 |
| **4** | 91.554 | **0,316** | **1,142** | **0,255** |
| 5 | 79.958 | 0,308 | 1,154 | 0,220 |
| 6 | 72.184 | 0,304 | 1,270 | 0,157 |

- **k = 4**: Silhouette máximo (empate con 3), Davies-Bouldin mínimo, codo entre 3 y 4, mejor Silhouette de GMM, e interpretable para el negocio.
- El BIC del GMM baja siempre con más componentes (30.000 datos) → no sirve como único criterio.

### Métricas internas (k = 4)

| Algoritmo | Silhouette | Davies-Bouldin | Calinski-Harabasz | Tamaños |
|---|---|---|---|---|
| **K-Means** | **0,316** | **1,143** | **12.936** | 9.792 / 9.623 / 6.669 / 3.916 |
| GMM | 0,255 | 1,850 | 8.159 | 14.480 / 6.703 / 6.156 / 2.661 |
| Ward (muestra) | 0,272 | 1,164 | 2.071 | — |

- Silhouette ≈ 0,3 = estructura **moderada**: los clientes forman un continuo, típico de datos de comportamiento.

### Estabilidad (ARI)
- K-Means, bootstrap: **0,972 ± 0,016** (muy estable).
- K-Means, entre semillas con 1 inicialización: 0,886 ± 0,213 (algunas caen en mínimos locales → se usa `n_init=20`).
- GMM, entre semillas: 0,944 ± 0,111.
- K-Means vs GMM: 0,468 · K-Means vs Ward: 0,531 → los grandes perfiles existen, pero las fronteras dependen del algoritmo.

### Perfiles de los segmentos (K-Means)

| Segmento | % clientes | Cupo mediano | Utilización | Ratio pago | Meses en mora | Meses inactivo | Impago real |
|---|---|---|---|---|---|---|---|
| **Morosos persistentes** | 22 % | 60.000 | 61 % | 0,10 | 3,15 | 0,06 | **50,1 %** |
| Inactivos / bajo uso | 13 % | 210.000 | 2 % | 0,98 | 0,27 | 5,1 | 18,9 % |
| Revolventes endeudados | 33 % | 90.000 | 63 % | 0,09 | 0,05 | 0,12 | 13,5 % |
| Totaleros / pagadores al día | 32 % | 210.000 | 9 % | 0,65 | 0,25 | 0,29 | 12,9 % |

Tabla de contingencia: los morosos persistentes tienen 3.339 de los 6.636 incumplimientos (**50 %** del total).

### Componentes del GMM

| Componente | n | Impago | Composición principal |
|---|---|---|---|
| GMM 3 | 6.703 | 48,9 % | Morosos persistentes |
| GMM 1 | 2.661 | 26,5 % | Mezcla con **mora intermitente** |
| GMM 2 | 6.156 | 17,9 % | Inactivos + parte de totaleros |
| GMM 0 | 14.480 | 10,7 % | Revolventes + totaleros |

### Relación con la etiqueta
- ARI vs `DEFAULT`: K-Means 0,060 · GMM 0,108. NMI ≈ 0,06–0,07.
- Bajo y **esperable**: 4 grupos vs. 2 clases, y los segmentos describen conducta, no impago. Lo relevante es que la tasa de impago varía de 13 % a 50 % entre segmentos.

### Hallazgos no evidentes
1. **Usar mucho cupo no es riesgoso por sí solo.** Los revolventes usan tanto cupo como los morosos, pero si pagan el mínimo a tiempo su impago (13,5 %) es como el de los totaleros. Lo que dispara el riesgo es el **atraso**.
2. **Los inactivos son más riesgosos que los activos al día** (18,9 % vs. ≈ 13 %): poca información y posible reactivación por dificultades financieras.
3. **El GMM detecta un grupo de mora intermitente** (≈ 9 %, impago 26,5 %) que K-Means reparte: perfil de "riesgo emergente" útil para alertas tempranas.

---

## 9. Reducción de dimensionalidad

- **PCA** (variables de segmentación): varianza explicada 40,2 % / 22,9 % / 12,9 % / 10,7 % / … → **2 componentes = 63,2 %**, 3 = 76,1 %.
  - PC1 = eje de **solvencia** (+ cupo, + ratio de pago, + inactividad / − utilización, − mora).
  - PC2 = eje de **mora** (+ meses en mora, + mora máxima / − tendencia de deuda).
- **t-SNE** (perplejidad 40, muestra de 4.000): separa mejor los segmentos visualmente, pero distorsiona distancias globales y tamaños.
- **Qué se pierde:** con PCA ≈ 37 % de la varianza; grupos que se solapan en 2D pueden estar separados en 7D; las variables de conteo generan franjas artificiales. t-SNE sirve para **ver**, no para **medir**.
- Ninguna proyección separa limpiamente a los morosos: el impago es una **zona de mayor densidad dentro de un continuo**, no un grupo compacto.

---

## 10. Respuestas a las 8 preguntas comparativas (sección 5 de la guía)

1. **¿Qué resuelve cada componente?** El supervisado: "¿este cliente va a incumplir?" (probabilidad individual para decidir). El no supervisado: "¿qué tipos de clientes tenemos?" (perfiles para estrategias diferenciadas).
2. **Algoritmos y pertinencia.** Regresión logística (base interpretable), Random Forest y Gradient Boosting (no linealidades, robustez). K-Means (segmentación escalable e interpretable), GMM (grupos elípticos, pertenencia probabilística), Ward (contraste jerárquico).
3. **Dificultades.** Desbalance; códigos no documentados; montos asimétricos con atípicos; multicolinealidad; elección de *k* no unívoca; costo computacional (RF, Silhouette, t-SNE → muestras).
4. **¿El supervisado identificó los casos de interés?** Parcialmente: ROC-AUC 0,78, PR-AUC 0,56 (vs. 0,22 del azar), Recall 0,58, Precision 0,51, F1 0,55. Ordena bien el riesgo, pero no detecta ≈ 4 de cada 10 morosos y la mitad de sus alertas son falsas.
5. **¿El no supervisado descubrió estructuras no evidentes?** Sí: utilización ≠ riesgo, inactivos más riesgosos, grupo de mora intermitente.
6. **Relación etiquetas–grupos.** ARI/NMI bajos (esperable), pero impago entre 13 % y 50 % según segmento; los morosos persistentes concentran la mitad de los incumplimientos.
7. **Qué se conserva/pierde con reducción de dimensionalidad.** PCA conserva 63 % de la varianza y estructura global; t-SNE conserva vecindarios locales pero distorsiona distancias. Ninguna separa limpiamente a los morosos.
8. **Recomendación para aplicación real.** Enfoque combinado: Gradient Boosting **sin variables sensibles** para la puntuación individual (umbral según costos, con explicaciones locales tipo SHAP) + segmentación K-Means para estrategia comercial y monitoreo. Si se exige un modelo totalmente explicable, la regresión logística pierde solo ≈ 0,03 de ROC-AUC.

---

## 11. Riesgos de usar modelos predictivos en decisiones financieras

- **Costos asimétricos:** falso negativo = pérdida de crédito; falso positivo = buen cliente rechazado (pérdida de ingresos, exclusión financiera). El umbral es una decisión de negocio.
- **Discriminación:** más falsos positivos en hombres y mayores de 45. Usar variables sensibles puede violar normas de no discriminación; se pueden excluir sin perder desempeño, aunque otras variables pueden actuar como *proxies*.
- **Profecía autocumplida:** reducir el cupo a quien se marca como riesgoso puede empujarlo al impago.
- **Generalización temporal y geográfica:** datos de Taiwán, 2005, en plena crisis de deuda de tarjetas; los patrones pueden no transferirse (*data drift*). Requiere validación temporal y monitoreo.
- **Explicabilidad:** las decisiones automatizadas de crédito deben poder justificarse al cliente.

---

## 12. Recomendaciones de negocio por segmento

| Segmento | Estrategia |
|---|---|
| Morosos persistentes | Cobranza temprana, acuerdos de pago, congelar aumentos de cupo |
| Revolventes endeudados | Consolidación de deuda o plazos fijos con menor tasa; vigilar el primer atraso (es la transición que dispara el riesgo) |
| Totaleros | Menor riesgo: aumentos de cupo y beneficios de fidelización |
| Inactivos | Campañas de reactivación, vigilando la primera reactivación |

**Mejoras futuras al modelo:** incorporar ingresos y datos de buró; validación por cohortes temporales; calibración de probabilidades; matriz de costos real del banco; búsquedas de hiperparámetros más amplias.

---

## 13. Limitaciones del trabajo (para mencionar con honestidad)

- Búsquedas de hiperparámetros pequeñas (8–12 combinaciones) por costo computacional.
- Silhouette calculado sobre muestra de 6.000 y t-SNE sobre 4.000.
- Ward solo sobre muestra de 6.000.
- Sin validación temporal: la partición es aleatoria, no por fecha.
- El umbral se optimizó por F1, no por un costo real de negocio.
- Los nombres de los segmentos se asignaron con reglas sobre los centroides; son una interpretación del equipo.

---

## 14. Organización del repositorio y commits

```
evaluacion 4/
├── README.md
├── requirements.txt
├── .gitignore
├── guion_video.md
├── hallazgos_y_decisiones_eval4.md
├── data/default of credit card clients.xls
├── notebooks/evento4_equipo5_default_credito.ipynb
└── figuras/01..13_*.png
```

| Orden | Quién | Contenido | Mensaje |
|---|---|---|---|
| 1 | Juan Pablo | Estructura, README inicial, requirements, `.gitignore`, dataset | `feat(eval4): estructura del proyecto, README inicial, requirements y dataset original` |
| 2 | María Camila | Secciones 1–3 + figuras 01–05 | `feat(eval4): descripción del problema, EDA y preprocesamiento sin fuga de información` |
| 3 | Duban | Sección 4 + figuras 06–08 | `feat(eval4): componente supervisado (LogReg, Random Forest, Gradient Boosting), umbral y análisis de riesgos` |
| 4 | Andrés (1) | Sección 5 + figuras 09–11 | `feat(eval4): segmentación con K-Means, GMM y Ward; perfiles y estabilidad` |
| 5 | Andrés (2) | Sección 6 + figuras 12–13 + guion del video | `feat(eval4): reducción de dimensionalidad (PCA, t-SNE) y guion del video` |
| 6 | Juan Pablo | Secciones 7–8 + README final + este documento | `docs(eval4): análisis comparativo, conclusiones y README final` |

Reglas: cada quien desde su cuenta; `git pull` antes de copiar; respetar el orden.

---

## 15. Video (≤ 12 min)

| Tiempo | Quién | Contenido |
|---|---|---|
| 0:00–1:00 | Juan Pablo | Problema, dataset y preguntas |
| 1:00–3:30 | María Camila | EDA y preprocesamiento |
| 3:30–6:30 | Duban | Modelos supervisados, desbalance, resultados, importancia, equidad |
| 6:30–9:30 | Andrés | Clustering, elección de *k*, perfiles, estabilidad, PCA/t-SNE |
| 9:30–12:00 | Juan Pablo + todos | Comparación, riesgos y recomendaciones |

**Frases clave**
- "*Accuracy* sería engañosa: predecir siempre 'no incumple' da 78 %."
- "Quitar sexo, edad y estado civil no reduce el desempeño, así que recomendamos no usarlos."
- "Usar mucho cupo no es lo riesgoso; atrasarse sí."
- "El modelo sirve para priorizar, no para decidir solo: se le escapan 4 de cada 10 morosos."
