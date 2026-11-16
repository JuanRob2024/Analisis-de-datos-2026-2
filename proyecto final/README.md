# Proyecto Final — Equipo 5
## Riesgo de incumplimiento en tarjetas de crédito: de los datos al tablero de decisiones

**Cursos:** Inteligencia de Negocios · Analítica de Datos · Aprendizaje Computacional — ITM 2026-2
**Docentes:** Carlos Jaramillo y Gustavo Macías (BI) · Daniel Nieto (AD) · July Galeano (AC)

### Integrantes y responsabilidades
| Nombre | Usuario GitHub | Responsabilidad principal |
|---|---|---|
| Juan Pablo Robledo (líder) | @JuanRob2024 | Estructura del proyecto, documento formal, conclusiones y recomendaciones |
| María Camila Álvarez | @1005663486 | ETL, reglas de negocio y modelo dimensional |
| Duban Guerra | @duguerrac | Modelo predictivo, métricas y calibración |
| Andrés Villa | @andresvilla12 | Dashboard en Power BI y presentación de la sustentación |

### Problema
Con 30.000 clientes de un banco de Taiwán (abril–septiembre 2005) se busca **predecir qué clientes incumplirán el pago del mes siguiente**, cuantificar el dinero expuesto (pérdida esperada) e identificar los perfiles que concentran el riesgo, para priorizar la gestión de cobro y ajustar la política de cupos. Dataset: *Default of Credit Card Clients* (UCI), el mismo del Evento 4, ahora con ETL, modelo dimensional y dashboard.

### Entregables
| Entregable del enunciado | Ubicación | Estado |
|---|---|---|
| Notebook de Python con código y explicaciones | `notebooks/proyecto_final_equipo5_riesgo_credito.ipynb` | Pendiente (María Camila y Duban) |
| Documento formal con análisis y resultados | `docs/documento_formal.md` (exportar a PDF/Word) | Esqueleto creado (Juan Pablo) |
| Dashboard con herramientas de BI | `powerbi/` (archivo `.pbix`) | Pendiente (Andrés) |
| Presentación y sustentación | `docs/` | Pendiente |

### Estructura
```
proyecto final/
├── README.md
├── requirements.txt
├── data/
│   └── modelo_estrella/        # CSV que genera el notebook y que consume Power BI
│       ├── dim_cliente.csv
│       ├── dim_tiempo.csv
│       ├── dim_estado_pago.csv
│       ├── fact_estado_cuenta.csv      (cliente × mes, 180.000 filas)
│       └── fact_riesgo_cliente.csv     (cliente, con probabilidad y segmento)
├── notebooks/
│   └── proyecto_final_equipo5_riesgo_credito.ipynb
├── figuras/                    # Gráficas exportadas por el notebook
├── powerbi/                    # .pbix + guía de modelo, medidas DAX y páginas
└── docs/
    ├── reglas_de_negocio.md
    └── documento_formal.md
```
El archivo fuente `.xls` no se duplica: el notebook lo toma de `../evaluacion 4/data/` o lo descarga de UCI.

### Ejecución
```bash
pip install -r requirements.txt
jupyter notebook notebooks/proyecto_final_equipo5_riesgo_credito.ipynb
```

### Plan de trabajo
| Fase del enunciado | Responsable | Entregable |
|---|---|---|
| 1. Recopilación y ETL | María Camila | Reglas de negocio, notebook §2–§3 y §6, CSV del modelo estrella |
| 2. Análisis exploratorio | María Camila | Notebook §4 y figuras 01–04 |
| 3. Inteligencia de negocios | Andrés | Modelo en Power BI, medidas DAX y dashboard |
| 4. Modelado predictivo | Duban | Notebook §5 y figuras 05–08 |
| 5. Conclusiones y documento | Juan Pablo | Notebook §7 y documento formal |

### Flujo de trabajo en Git
Igual que en el Evento 4: cada integrante hace sus commits sobre `main` desde su propia cuenta, en este orden:
1. Juan Pablo — estructura → 2. Juan Pablo — plan de trabajo y esqueleto del documento formal → 3. María Camila — reglas, ETL y EDA → 4. Duban — modelos y calibración → 5. María Camila — carga del modelo estrella → 6. Andrés — dashboard Power BI y README con resultados.
