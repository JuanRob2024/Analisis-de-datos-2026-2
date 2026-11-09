"""
Funciones de apoyo compartidas por todos los notebooks del proyecto.
Proyecto: EDA - Bank Marketing (UCI) | Análisis de Datos - ITM 2026-2
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Rutas del proyecto (funcionan si el notebook se ejecuta desde /notebooks)
RAIZ = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ / "data" / "raw" / "bank_marketing.csv"
RUTA_PROCESADOS = RAIZ / "data" / "processed"
RUTA_FIGURAS = RAIZ / "reports" / "figures"

# Variables del dataset agrupadas por tipo
VARIABLES_NUMERICAS = [
    "age", "duration", "campaign", "pdays", "previous",
    "emp_var_rate", "cons_price_idx", "cons_conf_idx", "euribor3m", "nr_employed",
]
VARIABLES_CATEGORICAS = [
    "job", "marital", "education", "default", "housing", "loan",
    "contact", "month", "day_of_week", "poutcome",
]
OBJETIVO = "y"  # 1 = el cliente suscribió el depósito a plazo, 0 = no


def configurar_graficos():
    """Estilo común para que todas las gráficas del equipo se vean iguales."""
    sns.set_theme(style="whitegrid", palette="Set2")
    plt.rcParams["figure.figsize"] = (10, 5)
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["axes.titlesize"] = 13


def cargar_datos() -> pd.DataFrame:
    """Carga el dataset original (41.188 registros x 21 columnas)."""
    return pd.read_csv(RUTA_DATOS)


def guardar_figura(nombre: str):
    """Guarda la figura activa en reports/figures/<nombre>.png"""
    RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
    plt.savefig(RUTA_FIGURAS / f"{nombre}.png", bbox_inches="tight", dpi=110)
