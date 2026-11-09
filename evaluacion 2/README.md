# Análisis Exploratorio de Datos – Bank Marketing (UCI)

**Instituto Tecnológico Metropolitano (ITM)** · Ingeniería de Sistemas · Curso: Análisis de Datos  
**Docente:** Daniel Alexis Nieto Mora · **Semestre:** 2026-2 · **Evento evaluativo 2**

## Integrantes y responsabilidades
| Integrante | Módulo | Notebook |
|---|---|---|
| Juan Pablo | Fase 1 – Exploración de bases de datos · Fase 3 – Preprocesamiento y PCA · estructura del repo | `01`, `05` |
| Andrés | Fase 2 – Valores faltantes y atípicos (limpieza) | `02` |
| María Camila | Fase 2 – Distribuciones y análisis univariado | `03` |
| Duban | Fase 2 – Análisis multivariado, hipótesis e insights | `04` |

## Pregunta de negocio
Un banco portugués hizo campañas de telemercadeo para vender **depósitos a plazo**. ¿Qué características del cliente y del contexto económico se relacionan con que el cliente acepte (`y = 1`)?

## Bases de datos exploradas (Fase 1)
| Base | Tipo | Registros | Seleccionada |
|---|---|---|---|
| Bank Marketing (UCI) | Tabular | 41.188 × 21 | (ok) |
| SMS Spam Collection (UCI) | Texto | 5.572 mensajes | (no) |
| Fashion-MNIST (Zalando) | Imágenes | 70.000 imágenes 28×28 | (no) |

Se eligió **Bank Marketing** por su mezcla de variables numéricas y categóricas, sus problemas reales de calidad (faltantes ocultos y atípicos), su buena documentación y su tamaño manejable. Ver `notebooks/01_exploracion_bases_de_datos.ipynb`.

## Estructura del repositorio
```
eda-bank-marketing/
├── data/
│   ├── raw/bank_marketing.csv          # dataset original
│   └── processed/bank_limpio.csv       # generado por el notebook 02
├── notebooks/
│   ├── 01_exploracion_bases_de_datos.ipynb
│   ├── 02_eda_faltantes_y_atipicos.ipynb
│   ├── 03_eda_distribuciones_univariado.ipynb
│   ├── 04_eda_multivariado_hipotesis.ipynb
│   └── 05_preprocesamiento_y_pca.ipynb
├── reports/
│   ├── figures/                        # todas las gráficas (png)
│   └── hallazgos/                      # resumen de hallazgos de cada integrante
├── src/utils.py                        # funciones compartidas
├── requirements.txt
└── README.md
```

## Cómo ejecutar
```bash
git clone https://github.com/JuanRob2024/Analisis-de-datos.git
cd eda-bank-marketing
python -m venv .venv
# Windows: .venv\Scripts\activate    |  Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```
Ejecutar los notebooks **en orden (01 → 05)**; el 02 genera `data/processed/bank_limpio.csv`, que usan los siguientes.

## Principales hallazgos
1. **Clases desbalanceadas:** solo el 11,3 % de los clientes suscribió el depósito.
2. **Faltantes ocultos:** no hay `NaN`, pero `default` tiene 20,9 % de `unknown`, y `pdays = 999` (nunca contactado) aparece en el 96,3 % de los registros.
3. **El historial manda:** si la campaña anterior fue exitosa, la tasa de suscripción sube a **65,1 %**; los clientes contactados antes suscriben 63,8 % vs 9,3 %.
4. **Economía:** con Euribor < 2 % la tasa es 24,5 %; con Euribor ≥ 4 % baja a 4,8 %. `euribor3m`, `emp_var_rate` y `nr_employed` tienen correlación > 0,9 entre sí (multicolinealidad).
5. **Perfil:** estudiantes (31,4 %) y jubilados (25,3 %) suscriben mucho más; mayores de 66 años llegan a 46,9 %.
6. **Canal y momento:** celular 14,7 % vs fijo 5,2 %; mayo concentra 1/3 de las llamadas con solo 6,4 % de éxito, mientras marzo, septiembre, octubre y diciembre superan el 44 %.
7. **Insistir no sirve:** 13 % de éxito con 1 llamada vs 3,1 % con 11 o más.
8. **`duration`** es la variable más relacionada con `y`, pero genera **fuga de información** y se excluye del modelado.
9. **PCA:** 17 componentes (de 51 columnas) explican el 90 % de la varianza; PC1 resume el ciclo económico y PC2 el perfil demográfico (edad/educación).

## Fuente de los datos
Moro, S., Cortez, P., & Rita, P. (2014). *A Data-Driven Approach to Predict the Success of Bank Telemarketing.* Decision Support Systems, 62, 22-31. UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/222/bank+marketing
