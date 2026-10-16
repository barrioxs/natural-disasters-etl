"Modulo de cruces: Creo las relaciones entre los tipos de desastre y su ubicacion geografica"

import pandas as pd
from transform.transformer import MESES

def tipo_por_continente(df: pd.DataFrame, min_eventos: int = 40) -> pd.DataFrame:
    """"Porcentaje de cada tipo de desastre en cada continente

    Descarto los que tienen menos de 40 registros porque con tan pocos casos
    es dificil de interpretar el porcentaje"""

    frecuentes = df["Disaster Type"].value_counts()
    frecuentes = frecuentes[frecuentes >= min_eventos].index
    base = df[df["Disaster Type"].isin(frecuentes)]
    tabla = pd.crosstab(base["Disaster Type"], base["Continent"], normalize="columns") * 100
    return tabla.round(1)

def top_paises_por_tipo(df: pd.DataFrame, n: int = 10, min_eventos: int = 40) -> pd.DataFrame:
    "Los `n` países con más eventos, desglosados por tipo de desastre."
    frecuentes = df["Disaster Type"].value_counts()
    frecuentes = frecuentes[frecuentes >= min_eventos].index
    base = df[df["Disaster Type"].isin(frecuentes)]
    tabla = pd.crosstab(base["Country"], base["Disaster Type"])
    top = tabla.sum(axis=1).sort_values(ascending=False).head(n).index
    tabla = tabla.loc[top]
    return tabla[tabla.sum().sort_values(ascending=False).index]

def inundaciones_por_region(df: pd.DataFrame) -> pd.DataFrame:
    "Cantidad y porcentaje de inundaciones por región, de mayor a menor."
    inundaciones = df[df["Disaster Type"] == "Flood"]
    conteo = inundaciones.groupby("Region").size().sort_values(ascending=False)
    return pd.DataFrame({
        "eventos": conteo,
        "porcentaje": (conteo / conteo.sum() * 100).round(1),
    })


def terremotos_por_pais(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    "Los `n` países con más terremotos, con su región."
    sismos = df[df["Disaster Type"] == "Earthquake"]
    conteo = (sismos.groupby(["Country", "Region"]).size()
                    .rename("eventos").reset_index()
                    .sort_values("eventos", ascending=False)
                    .head(n))
    return conteo.reset_index(drop=True)


def terremotos_por_region(df: pd.DataFrame) -> pd.Series:
    "Cantidad de terremotos por región, de mayor a menor."
    sismos = df[df["Disaster Type"] == "Earthquake"]
    return sismos.groupby("Region").size().sort_values(ascending=False).rename("eventos")


def cantidad_vs_gravedad(df: pd.DataFrame, min_eventos: int = 40) -> pd.DataFrame:
    """Compara qué porcentaje de los eventos y de las muertes aporta cada tipo.

    Las filas sin dato de muertes se ignoran en la suma (no se imputan).
    """
    por_tipo = df.groupby("Disaster Type").agg(
        eventos=("Dis No", "count"),
        muertes=("Total Deaths", "sum"),
    )
    por_tipo = por_tipo[por_tipo["eventos"] >= min_eventos]
    por_tipo["pct_eventos"] = (por_tipo["eventos"] / por_tipo["eventos"].sum() * 100).round(1)
    por_tipo["pct_muertes"] = (por_tipo["muertes"] / por_tipo["muertes"].sum() * 100).round(1)
    return por_tipo.sort_values("eventos", ascending=False)

def tipo_por_mes(df: pd.DataFrame, tipos: list = None) -> pd.DataFrame:
    """Cantidad de eventos por tipo de desastre y mes (estacionalidad por tipo).

    Si se pasa `tipos`, solo se incluyen esos tipos. Se ignoran las filas sin fecha.
    """
    base = df.dropna(subset=["fecha"])
    if tipos:
        base = base[base["Disaster Type"].isin(tipos)]
    tabla = base.pivot_table(index="Disaster Type", columns="mes", values="Dis No",
                             aggfunc="count", fill_value=0)
    tabla = tabla.reindex(columns=range(1, 13), fill_value=0)
    tabla.columns = MESES
    return tabla
