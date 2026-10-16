"Modulo de extraccion: Leo y valido el dataset"
from pathlib import Path
import pandas as pd

#Con esto la ruta del csv se calcula respecto a su ubicacion y no usando C:\

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATASET = RAIZ_PROYECTO / "data" / "emdat_disasters_1970_2021.csv"

COLUMNAS_REQUERIDAS = [
    "Year",
    "Start Year",
    "Start Month",
    "Disaster Type",
    "Country",
    "Region",
    "Continent",
]

def extraer_datos(ruta=RUTA_DATASET) -> pd.DataFrame:
    ruta = Path(ruta)
    if not ruta.exists():
        f"No se encontro el archivo en la ruta."
        "Asegurate que el archivo este en la carpeta data/."
    return pd.read_csv(ruta)

def validar_carga(df: pd.DataFrame) -> bool:
    "Verifico que el DataFrame no esté vacío y tenga las columnas necesarias."
    if df.empty:
        raise ValueError("El dataset se cargó vacío.")

    faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")
    print("Carga validada")
    return True

def explorar_estructura(df: pd.DataFrame) -> None:
    """Imprime una exploración inicial de la estructura del dataset."""
    print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"Rango de años: {df['Year'].min()} - {df['Year'].max()}")

    print("\nTipos de datos:")
    print(df.dtypes.to_string())

    print("\nPrimeras filas:")
    print(df.head())

    print("\nNulos por columna (top 10):")
    print(df.isna().sum().sort_values(ascending=False).head(10).to_string())

    print(f"\nFilas duplicadas: {df.duplicated().sum()}")

