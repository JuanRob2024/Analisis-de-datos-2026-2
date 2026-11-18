# Riesgo de incumplimiento en tarjetas de crédito: de los datos al tablero de decisiones

**Proyecto Final — Inteligencia de Negocios, Analítica de Datos y Aprendizaje Computacional**
Institución Universitaria ITM · 2026-2 · Equipo 5
Juan Pablo Robledo · María Camila Álvarez · Duban Guerra · Andrés Villa

## Resumen

Este proyecto construye una solución de inteligencia de negocios para anticipar el incumplimiento de pago en tarjetas de crédito, a partir del dataset de Yeh y Lien (2009): 30.000 clientes de un banco de Taiwán observados entre abril y septiembre de 2005. Se aplicó un proceso ETL con reglas de negocio documentadas, un análisis exploratorio, un modelo dimensional en esquema estrella y un tablero en Power BI de cinco páginas. Se compararon tres modelos supervisados (regresión logística, árbol de decisión y Gradient Boosting); el mejor fue Gradient Boosting, con ROC-AUC de 0,780 y PR-AUC de 0,557 en prueba. Sus probabilidades se calibraron con regresión isotónica (Brier de 0,177 a 0,134), lo que permite expresar la pérdida esperada como monto: NT$ 318,4 millones, el 20,7 % de la exposición. Con el modelo calibrado, en el conjunto de prueba (6.000 clientes), la Precision es 54,4 % y el Recall 53,7 %. La tasa de incumplimiento real es 22,12 %; el cupo y la mora reciente son los factores que más separan el riesgo, y los segmentos Alto y Muy alto reúnen el 15,8 % de los clientes y el 50,7 % de la pérdida esperada. Se recomienda priorizar la cobranza según la pérdida esperada, usando el modelo como apoyo a la decisión y no como decisor automático.

## 1. Introducción y problema de negocio

- **Contexto:** el crédito de consumo con tarjeta expone a la entidad a pérdidas cuando los clientes dejan de pagar. Anticipar quién incumplirá el próximo mes permite actuar antes: cobrar de forma preventiva, ajustar cupos o reforzar el seguimiento.
- **Pregunta de negocio:** ¿qué clientes tienen mayor probabilidad de incumplir y cuánto dinero está en riesgo, para decidir a quién cobrar primero?
- **Usuarios:** el área de cartera y cobranza, y la gerencia de riesgo de crédito.
- **Objetivo general:** transformar los datos de clientes de tarjeta de crédito en un tablero de decisiones respaldado por un modelo predictivo calibrado.
- **Objetivos específicos:**
  1. Extraer, validar y transformar los datos aplicando reglas de negocio documentadas.
  2. Caracterizar el comportamiento de pago y los perfiles de riesgo.
  3. Construir un modelo dimensional (esquema estrella) para Power BI.
  4. Entrenar y comparar modelos supervisados, y calibrar sus probabilidades.
  5. Calcular la pérdida esperada por cliente y por segmento, y priorizar la cobranza.

## 2. Datos y fuentes

- **Origen:** *Default of Credit Card Clients*, UCI Machine Learning Repository (Yeh & Lien, 2009).
- **Alcance:** 30.000 clientes de un banco de Taiwán, con seis meses de historia (abril a septiembre de 2005). El objetivo es el incumplimiento en el mes siguiente (`DEFAULT`).
- **Variables:** cupo (`LIMIT_BAL`), sexo, educación, estado civil y edad; estado de pago (`PAY_`), monto facturado (`BILL_AMT`) y monto pagado (`PAY_AMT`) de cada mes.
- **Desbalance:** el 22,12 % de los clientes incumple (aprox. 3,5 clientes cumplidores por cada incumplidor).

## 3. Proceso ETL y reglas de negocio

- **Extracción y validaciones de calidad:** lectura del archivo fuente y verificación de llaves únicas, tipos, rangos y códigos no documentados (por ejemplo, categorías de educación y estado civil fuera del diccionario, y estados de pago negativos).
- **Reglas de negocio:** RN-01 a RN-09, documentadas en `reglas_de_negocio.md`. Entre ellas, RN-03 define la alerta de mora (2 o más meses en mora) y RN-08 define la pérdida esperada como probabilidad de incumplimiento por exposición.
- **Transformación:** paso de formato ancho (una fila por cliente) a formato largo (una fila por cliente y mes), y construcción de variables derivadas como utilización, ratio de pago, meses en mora y tendencia de la deuda.
- **Carga:** el modelo resultante se escribe como archivos CSV en `data/modelo_estrella/`, que consume Power BI.

## 4. Análisis exploratorio

- **Desbalance del objetivo:** 22,12 % de incumplimiento (figura 01).
- **Tendencias mensuales (figura 02):** de abril a septiembre, lo facturado crece (de unos 1.200 a unos 1.500 millones de NT$ al mes) mientras lo pagado se mantiene muy por debajo (cerca de 200 millones). El porcentaje de clientes en mora sube de aproximadamente 10 % a 23 % en septiembre.
- **Perfiles de riesgo (figura 03):**
  - El cupo es el factor más claro: cerca de 32 % de incumplimiento con cupos de hasta 50 mil, frente a cerca de 11 % con cupos de más de 500 mil.
  - La edad muestra más riesgo en los extremos (alrededor de 27 % en los de 21-25 y en los de 61 o más) que entre 31 y 35 años (alrededor de 19 %).
  - Educación y estado civil separan poco el riesgo.
- **Correlaciones (figura 04):** las variables de mora y de estado de pago son las más asociadas con el incumplimiento; los montos facturados de los distintos meses están fuertemente correlacionados entre sí.

## 5. Modelo de datos para BI

- **Esquema estrella con cinco tablas:**
  - `dim_cliente`: una fila por cliente (sexo, educación, estado civil, edad, cupo y sus rangos).
  - `dim_tiempo`: una fila por mes (abril a septiembre de 2005).
  - `dim_estado_pago`: categorías de estado de pago.
  - `fact_estado_cuenta`: grano cliente por mes (facturado, pagado, exposición, utilización, indicadores de mora).
  - `fact_riesgo_cliente`: grano cliente (probabilidad calibrada, segmento de riesgo, exposición de septiembre, pérdida esperada, conjunto de entrenamiento o prueba).
- **Relaciones:** `dim_cliente` (1) a `fact_estado_cuenta` (*) y a `fact_riesgo_cliente` (1:1) por `id_cliente`; `dim_tiempo` (1) a `fact_estado_cuenta` (*) por `id_mes`; `dim_estado_pago` (1) a `fact_estado_cuenta` (*) por `id_estado_pago`.
- **Decisiones de modelado:** la relación 1:1 admite filtro en ambas direcciones, de modo que los segmentadores de riesgo filtran también la historia mensual. `dim_tiempo` tiene granularidad mensual (6 filas), por lo que no se marca como tabla de fechas, que exige días continuos; no se usan funciones de inteligencia de tiempo.
- **Medidas principales (DAX):** Clientes, Tasa de incumplimiento real, Pérdida esperada, Exposición, % Pérdida sobre exposición, Facturado, Pagado, % Pago sobre facturado, % Clientes en mora, % Mora grave, Utilización media, Clientes de alto riesgo, y Precision y Recall (calculadas sobre el conjunto de prueba).

## 6. Dashboard

El tablero (`powerbi/proyecto_final_equipo5.pbix`) tiene cinco páginas, cada una con una pregunta de negocio:

1. **Resumen ejecutivo: ¿cómo está la cartera?** 30.000 clientes, tasa de incumplimiento real de 22,12 % y pérdida esperada de NT$ 318 millones. Cerca de 5.000 clientes están en los segmentos Alto y Muy alto; el 67,9 % de la cartera es de riesgo Bajo.
2. **Evolución de la cartera: ¿cómo cambia el comportamiento de abril a septiembre?** Lo facturado crece, lo pagado se mantiene bajo, y el porcentaje de clientes en mora sube de aproximadamente 10 % a 23 %.
3. **Perfiles de riesgo: ¿quiénes incumplen más?** El incumplimiento disminuye a medida que aumenta el cupo; la edad y el nivel educativo tienen un efecto menor. Una matriz de rango de cupo por segmento muestra dónde se concentra la pérdida esperada.
4. **Priorización de cobro: ¿a quién cobrar primero?** Lista de clientes ordenada por pérdida esperada, con segmento, probabilidad, exposición, meses en mora y utilización.
5. **Desempeño del modelo: ¿es confiable?** En el conjunto de prueba (6.000 clientes), Precision de 54,43 % y Recall de 53,65 % (712 verdaderos positivos). La probabilidad media predicha coincide con la tasa real en cada segmento (por ejemplo, cerca de 72 % frente a 70 % en Muy alto y cerca de 11 % en Bajo), lo que confirma la calibración.

*(Insertar aquí las capturas de `powerbi/capturas/`, si se exportaron.)*

## 7. Modelado predictivo

**Metodología**
- Partición 80/20 estratificada: 24.000 clientes de entrenamiento y 6.000 de prueba.
- Preprocesamiento: montos con logaritmo con signo y estandarización; categóricas con *one-hot*; todo dentro de un `Pipeline` para evitar fuga de información.
- Búsqueda de hiperparámetros con validación cruzada sobre el entrenamiento.
- Umbral de decisión elegido maximizando F1 sobre predicciones *out-of-fold* del entrenamiento, sin usar la prueba.

**Modelos evaluados:** regresión logística (línea base interpretable), árbol de decisión y Gradient Boosting, además de una regla simple de referencia (`PAY_1 ≥ 1`).

**Resultados en prueba (figuras 05 y 06)**

| Modelo | Umbral | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|---|
| Regresión logística | 0,597 | 0,774 | 0,491 | 0,540 | 0,514 | 0,755 | 0,500 |
| Árbol de decisión | 0,563 | 0,754 | 0,458 | 0,608 | 0,523 | 0,771 | 0,528 |
| **Gradient Boosting** | 0,562 | 0,787 | 0,517 | 0,573 | 0,543 | 0,780 | 0,557 |
| Línea base `PAY_1 ≥ 1` | — | 0,778 | 0,498 | 0,497 | 0,498 | 0,678 | 0,359 |

Gradient Boosting fue el modelo seleccionado. La línea de azar de la curva Precision-Recall es 0,22 (la tasa base). Con el modelo sin calibrar, la matriz de confusión en prueba da 3.962 verdaderos negativos, 711 falsos positivos, 567 falsos negativos y 760 verdaderos positivos.

**Importancia de variables (figura 07):** por permutación, domina `PAY_1` (estado de pago del último mes), seguida de `n_meses_mora` y `max_mora`. La mora reciente pesa más que las variables demográficas.

**Calibración de probabilidades (figura 08):** entrenar con `class_weight="balanced"` mejora el recall pero infla las probabilidades. La calibración isotónica (`CalibratedClassifierCV`) corrige esto sin alterar casi el orden de los clientes:

| Versión | Prob. media | Brier | Umbral | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|---|---|
| Sin calibrar | 0,413 | 0,177 | 0,562 | 0,517 | 0,573 | 0,543 | 0,780 | 0,557 |
| Calibrado (isotónica) | 0,222 | 0,134 | 0,307 | 0,544 | 0,537 | 0,540 | 0,781 | 0,560 |

La probabilidad media calibrada (0,222) coincide con la tasa real (22,1 %). Las métricas del tablero corresponden al modelo calibrado (umbral 0,307).

**Segmentación de riesgo y pérdida esperada:** la pérdida esperada de cada cliente es su probabilidad calibrada por su exposición (factura de septiembre). La pérdida total es de NT$ 318,4 millones (20,7 % de la exposición de NT$ 1.537 millones).

| Segmento | Clientes | Tasa real | Pérdida esperada (NT$) | % de la pérdida |
|---|---|---|---|---|
| 1-Bajo | 20.371 | 11,2 % | 123,0 millones | 38,6 % |
| 2-Medio | 4.902 | 28,5 % | 34,2 millones | 10,7 % |
| 3-Alto | 1.816 | 49,0 % | 29,5 millones | 9,3 % |
| 4-Muy alto | 2.911 | 71,0 % | 131,7 millones | 41,4 % |

## 8. Conclusiones y recomendaciones

**Conclusiones**
- Uno de cada cinco clientes (22,12 %) incumple. El riesgo se concentra: los segmentos Alto y Muy alto son el 15,8 % de los clientes (4.727) y aportan el 50,7 % de la pérdida esperada; el Muy alto tiene una tasa real del 71 %.
- El segmento Bajo (67,9 % de la cartera, tasa real 11,2 %) aporta el 38,6 % de la pérdida por su volumen.
- La mora reciente y el cupo explican más el riesgo que el perfil demográfico.
- El modelo ordena bien el riesgo (ROC-AUC 0,78) y sus probabilidades están calibradas, lo que permite expresar la pérdida como monto. Aun así, no es un decisor automático: con Precision y Recall de aproximadamente 54 %, cerca de la mitad de las alertas son falsas y casi la mitad de los incumplidores no se detecta.
- Se detectaron 712 de 1.327 incumplidores en el conjunto de prueba.

**Recomendaciones para el área de cartera**
1. Priorizar la gestión de cobro por pérdida esperada, empezando por los segmentos Alto y Muy alto. El Muy alto concentra el 41 % de la pérdida con el 9,7 % de los clientes. Para el segmento Bajo, usar canales masivos de bajo costo.
2. Generar alertas tempranas cuando un cliente acumula 2 o más meses en mora (RN-03), porque la mora reciente es lo que más pesa en el modelo.
3. Revisar la política de cupos para clientes con alta utilización y cupos bajos.
4. Usar el modelo como herramienta de priorización con revisión humana, y fijar el umbral según el costo de cada tipo de error (falso positivo frente a falso negativo).

**Limitaciones y trabajo futuro**
- Los datos son de 2005, de un solo banco de Taiwán, con predicción a un mes y solo seis meses de historia.
- Las variables demográficas sensibles (sexo, educación, estado civil) no deben usarse para decisiones discriminatorias; se recomienda evaluar el modelo sin ellas.
- La exposición se aproxima con la factura de septiembre.
- Trabajo futuro: explicaciones locales (SHAP), validación con datos recientes y monitoreo de la deriva del modelo.

## Referencias

- Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. *Expert Systems with Applications, 36*(2), 2473–2480.
- Dua, D., & Graff, C. UCI Machine Learning Repository: Default of Credit Card Clients.
