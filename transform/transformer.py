"Modulo de Transformacion: Corrijo fechas y filtros"

import pandas as pd

MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
            "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

def crear_fecha(df: pd.DataFrame) -> pd.DataFrame:
    "En esta funcion, unifico las columnas Start Year, Month y Day en una unica columna fecha"
   
    """Criterios de imputación:
    - Día faltante: uso el día 1 (el análisis es mensual).
        - Día inválido (por ejemplo 31 de septiembre del 92): se usa el día 1 del mismo mes.
        - Mes faltante: la fecha queda como NaT. No pongo un mes para no inflarlo con estadisticas que no le corresponden."""
    df = df.copy()

    partes = pd.DataFrame({
        "year": df["Start Year"],
        "month": df["Start Month"],
        "day": df["Start Day"].fillna(1),
    })
    fecha = pd.to_datetime(partes, errors="coerce")
    
    
    # Reintento con día 1 donde hay mes pero el día era inválido
    invalidas = fecha.isna() & df["Start Month"].notna()
    if invalidas.any():
        partes.loc[invalidas, "day"] = 1
        fecha = pd.to_datetime(partes, errors="coerce")

    df["fecha"] = fecha
    df["anio"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    return df


def filtrar_periodo_reciente(df: pd.DataFrame, anios: int = 20) -> pd.DataFrame:
    "Me Devuelve solo los eventos de los últimos `anios` años del registro."
    anio_max = int(df["Start Year"].max())
    anio_min = anio_max - anios + 1
    return df[df["Start Year"].between(anio_min, anio_max)].copy()

def eventos_por_anio(df: pd.DataFrame) -> pd.Series:
    """Cantidad de eventos por año de inicio."""
    return df.groupby("Start Year").size().rename("eventos")

def calcular_estacionalidad(df: pd.DataFrame) -> pd.DataFrame:
    "Eventos totales y promedio anual por mes (solo filas con fecha valida)"
    validos = df.dropna(subset=["fecha"])
    n_anios = validos["anio"].nunique()
    conteo = validos.groupby("mes").size().reindex(range(1, 13), fill_value=0)
    return pd.DataFrame({
        "mes": MESES,
        "eventos": conteo.values,
        "promedio_por_anio": (conteo.values / n_anios).round(1),
    })

def tabla_anios_mes(df: pd.DataFrame) -> pd.DataFrame:
    "Matriz año x mes con la cantidad de eventos"
    validos = df.dropna(subset=["fecha"])
    tabla = validos.pivot_table(index="anio", columns="mes", values="Dis No",
                                aggfunc="count", fill_value=0)
    tabla = tabla.reindex(columns=range(1, 13), fill_value=0)
    tabla.columns = MESES
    tabla.index = tabla.index.astype(int)
    tabla.index.name = "anio"
    return tabla



