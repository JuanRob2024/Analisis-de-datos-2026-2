# Evento Evaluativo 4 — Equipo 5
## Predicción de incumplimiento financiero y análisis de perfiles de riesgo

**Asignatura:** Análisis de Datos · **Docente:** Daniel Alexis Nieto Mora · **Grupo:** 190304018-1 · **Periodo:** 2026-2

### Integrantes
| Nombre | Usuario GitHub | Responsabilidad principal |
|---|---|---|
| Juan Pablo Robledo (líder) | @JuanRob2024 | Estructura del repositorio, análisis comparativo, conclusiones y README |
| María Camila Álvarez | @1005663486 | Descripción del problema, EDA y preprocesamiento |
| Duban Guerra | @duguerrac | Componente supervisado |
| Andrés Villa | @andresvilla12 | Componente no supervisado, reducción de dimensionalidad y guion del video |

### Descripción del problema
A partir de los datos de 30.000 clientes de tarjeta de crédito de un banco de Taiwán (abril–septiembre de 2005) se busca:

- **Supervisado:** predecir si un cliente incumplirá el pago en el mes siguiente (`default payment next month`).
- **No supervisado:** segmentar a los clientes según su comportamiento financiero (uso del cupo, patrón de pago, mora) sin usar la etiqueta, y contrastar después los segmentos con el incumplimiento real.

### Fuente de datos
*Default of Credit Card Clients* — UCI Machine Learning Repository (Yeh, I. C. & Lien, C. H., 2009).
https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients

El notebook descarga el archivo automáticamente si no existe en `data/`.

### Estructura del proyecto
```
evaluacion 4/
├── README.md
├── requirements.txt
├── guion_video.md                 # Guion y reparto del video (≤ 12 min)
├── data/
│   └── default of credit card clients.xls
├── notebooks/
│   └── evento4_equipo5_default_credito.ipynb
└── figuras/                       # Gráficas exportadas por el notebook
```

### Instrucciones de ejecución
```bash
pip install -r requirements.txt
jupyter notebook notebooks/evento4_equipo5_default_credito.ipynb
```
Ejecutar todas las celdas (*Run All*). Tiempo aproximado: 8–10 minutos en un solo núcleo (la búsqueda de hiperparámetros de Random Forest es la parte más costosa). También funciona en Google Colab subiendo el notebook (los datos se descargan solos).

### Metodología
1. **EDA:** calidad de datos (códigos no documentados en `EDUCATION`, `MARRIAGE`, `PAY_k`), desbalance, demografía, historial de pagos, asimetría y atípicos, correlaciones.
2. **Preprocesamiento:** recodificación de categorías no documentadas; 7 variables derivadas (meses en mora, mora máxima, utilización, ratio de pago, etc.); partición estratificada 80/20 **antes** de cualquier transformación aprendida; `Pipeline` con log con signo + estandarización + *one-hot* para evitar fuga de información.
3. **Supervisado:** Regresión logística, Random Forest y Histogram Gradient Boosting con `class_weight`, búsqueda aleatoria de hiperparámetros optimizando PR-AUC y umbral de decisión elegido con predicciones *out-of-fold*.
4. **No supervisado:** K-Means, Mezcla de Gaussianas y Aglomerativo (Ward) sobre 7 indicadores de comportamiento; selección de *k* con codo, Silhouette, Davies-Bouldin y BIC; estabilidad con ARI *bootstrap*.
5. **Visualización:** PCA y t-SNE.

### Principales resultados

**Supervisado (conjunto de prueba, 6.000 clientes)**

| Modelo | Umbral | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Regresión logística | 0,60 | 0,490 | 0,543 | 0,515 | 0,755 | 0,499 |
| Random Forest | 0,54 | 0,524 | 0,566 | 0,544 | 0,779 | 0,555 |
| **Gradient Boosting** | 0,56 | 0,514 | 0,584 | **0,547** | **0,782** | **0,561** |
| Regla base `PAY_1 ≥ 1` | — | 0,498 | 0,497 | 0,498 | 0,678 | 0,359 |

- El **historial de pagos** concentra la señal predictiva (ROC-AUC 0,75 por sí solo); las variables demográficas casi no aportan y pueden eliminarse sin perder desempeño (0,785 vs. 0,787).

**No supervisado (K-Means, k = 4; Silhouette 0,32; Davies-Bouldin 1,14; ARI bootstrap 0,97)**

| Segmento | % clientes | Impago real |
|---|---|---|
| Morosos persistentes | 22 % | 50,1 % |
| Inactivos / bajo uso | 13 % | 18,9 % |
| Revolventes endeudados | 33 % | 13,5 % |
| Totaleros / pagadores al día | 32 % | 12,9 % |

- La utilización alta del cupo no es riesgosa por sí sola: lo que dispara el impago es el **atraso**.
- El segmento de morosos persistentes reúne el 22 % de los clientes y el 50 % de los incumplimientos.

### Conclusión
Se recomienda un enfoque combinado: Gradient Boosting **sin variables sensibles** para la puntuación individual de riesgo (con umbral definido según el costo de los errores) y la segmentación K-Means para diseñar estrategias comerciales y de cobranza por perfil. El detalle de riesgos y recomendaciones está en las secciones 7 y 8 del notebook.

### Video
Enlace: _pegar aquí el enlace del video (≤ 12 min)_
