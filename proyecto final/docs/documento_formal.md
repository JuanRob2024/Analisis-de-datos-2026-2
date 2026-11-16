# Riesgo de incumplimiento en tarjetas de crédito: de los datos al tablero de decisiones

**Proyecto Final — Inteligencia de Negocios, Analítica de Datos y Aprendizaje Computacional**
Institución Universitaria ITM · 2026-2 · Equipo 5
Juan Pablo Robledo · María Camila Álvarez · Duban Guerra · Andrés Villa

> Esqueleto del documento formal. Completar cada sección y exportar a PDF para la entrega.

## Resumen
*(150–250 palabras: problema, datos, método, resultado principal del modelo, hallazgo de negocio y recomendación clave.)*

## 1. Introducción y problema de negocio
- Contexto del crédito de consumo y del riesgo de incumplimiento.
- Pregunta de negocio y usuarios de la solución.
- Objetivo general y objetivos específicos.

## 2. Datos y fuentes
- Origen del dataset (UCI, Yeh & Lien, 2009), periodo, número de registros y variables.
- Diccionario de variables (resumido).

## 3. Proceso ETL y reglas de negocio
- Extracción, validaciones de calidad y resultados.
- Reglas de negocio RN-01 a RN-09 (ver `reglas_de_negocio.md`).
- Transformación de formato ancho a largo.

## 4. Análisis exploratorio
- Desbalance del objetivo.
- Tendencias mensuales de facturación, pagos, mora y utilización (figura 02).
- Perfiles de riesgo (figura 03) y correlaciones (figura 04).

## 5. Modelo de datos para BI
- Diagrama del esquema estrella, grano de cada tabla y relaciones.
- Medidas principales.

## 6. Dashboard
- Capturas de cada página y qué pregunta responde.
- Principales insights obtenidos del tablero.

## 7. Modelado predictivo
- Modelos evaluados y justificación.
- Metodología: partición, *pipeline*, búsqueda de hiperparámetros, umbral.
- Resultados en prueba (tabla de métricas, figuras 05–07).
- Calibración de probabilidades (figura 08).
- Segmentación de riesgo y pérdida esperada.

## 8. Conclusiones y recomendaciones
- Conclusiones del análisis y del modelo.
- Recomendaciones accionables para el área de cartera.
- Limitaciones y trabajo futuro.

## Referencias
- Yeh, I. C., & Lien, C. H. (2009). The comparisons of data mining techniques for the predictive accuracy of probability of default of credit card clients. *Expert Systems with Applications, 36*(2), 2473–2480.
- Dua, D., & Graff, C. UCI Machine Learning Repository: Default of Credit Card Clients.
