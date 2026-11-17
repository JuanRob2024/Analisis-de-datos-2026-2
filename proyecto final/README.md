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
| Notebook de Python con código y explicaciones | `notebooks/proyecto_final_equipo5_riesgo_credito.ipynb` | Base lista; falta completar textos de §4 y §7 |
| Documento formal con análisis y resultados | `docs/documento_formal.md` (exportar a PDF/Word) | Esqueleto |
| Dashboard con herramientas de BI | `powerbi/` (archivo `.pbix`) | Por construir; guía en `powerbi/README.md` |
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
*Run All* tarda ≈ 1,5 minutos y regenera las figuras y los CSV del modelo estrella.

### Fases y resultados preliminares
1. **ETL:** 9 reglas de negocio (`docs/reglas_de_negocio.md`), validaciones de calidad (0 registros inválidos), recodificación de categorías no documentadas, paso de formato ancho a largo (cliente × mes) y carga en esquema estrella con verificación de integridad referencial.
2. **EDA:** 22 % incumple; el % de clientes en mora sube de 10 % (abril) a 23 % (septiembre) y la utilización del cupo de 32 % a 42 %; la tasa de incumplimiento pasa de 12 % (sin meses en mora) a 70 % (6 de 6 meses); cupos ≤ 50 mil NT$ incumplen 32 % frente a 11 % de cupos > 500 mil.
3. **BI:** modelo estrella con 3 dimensiones y 2 tablas de hechos; dashboard en Power BI (pendiente).
4. **Modelo supervisado** (prueba, 6.000 clientes):

   | Modelo | Precision | Recall | F1 | ROC-AUC | PR-AUC |
   |---|---|---|---|---|---|
   | Regresión logística | 0,491 | 0,540 | 0,514 | 0,755 | 0,500 |
   | Árbol de decisión | 0,458 | 0,608 | 0,523 | 0,771 | 0,528 |
   | **Gradient Boosting** | **0,517** | 0,573 | **0,543** | **0,780** | **0,557** |
   | Línea base `PAY_1 ≥ 1` | 0,498 | 0,497 | 0,498 | 0,678 | 0,359 |
   | **Gradient Boosting calibrado** (isotónica, umbral 0,31) | 0,544 | 0,537 | 0,540 | 0,781 | 0,560 |

   **Calibración:** `class_weight="balanced"` inflaba las probabilidades (media 0,41 frente a una tasa real de 0,22). Con calibración isotónica la probabilidad media queda en 0,22 y el Brier baja de 0,177 a 0,134, sin perder capacidad de ordenamiento. Las probabilidades del tablero son las calibradas.

   **Segmentos de riesgo (probabilidades calibradas, toda la cartera):**

   | Segmento | Clientes | Prob. media | Tasa real | % de la pérdida esperada |
   |---|---|---|---|---|
   | Bajo (< 20 %) | 20.371 | 11 % | 11 % | 39 % |
   | Medio (20–40 %) | 4.902 | 28 % | 29 % | 11 % |
   | Alto (40–60 %) | 1.816 | 49 % | 49 % | 9 % |
   | Muy alto (≥ 60 %) | 2.911 | 72 % | 71 % | 41 % |

   La probabilidad predicha coincide con la tasa real en cada segmento. Pérdida esperada total: NT$ 318 millones (20,7 % de la exposición de septiembre). El 10 % de clientes en *Muy alto* concentra el 41 % de la pérdida esperada.
5. **Conclusiones:** pendientes (§7 del notebook y documento formal).

### Pendientes
- [x] Calibrar probabilidades (§5.5 del notebook, figura `08_calibracion.png`).
- [ ] Revisar y explicar la calibración en la sustentación (Duban).
- [ ] Construir el `.pbix` siguiendo `powerbi/README.md` (Andrés).
- [ ] Completar la lectura del EDA (§4) y revisar reglas de negocio (María Camila).
- [ ] Redactar documento formal, conclusiones y recomendaciones (Juan Pablo).
- [ ] Preparar diapositivas de la sustentación (todo el equipo).

### Flujo de trabajo en Git
Igual que en el Evento 4: cada integrante hace sus commits sobre `main` desde su propia cuenta, en este orden:
1. Juan Pablo — estructura → 2. Juan Pablo — plan de trabajo y esqueleto del documento formal → 3. María Camila — reglas, ETL y EDA → 4. Duban — modelos y calibración → 5. María Camila — carga del modelo estrella → 6. Andrés — dashboard Power BI y README con resultados.
