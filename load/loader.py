"Modulo de carga: acomodo los datos y generación de gráficos."

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_PROCESADOS = RAIZ_PROYECTO / "data" / "processed"
RUTA_FIGURAS = RAIZ_PROYECTO / "output" / "figures"


def guardar_dataset(df: pd.DataFrame, nombre: str) -> Path:
    "Guardo un DataFrame como CSV en data/processed/."
    RUTA_PROCESADOS.mkdir(parents=True, exist_ok=True)
    ruta = RUTA_PROCESADOS / nombre
    df.to_csv(ruta, index=False)
    return ruta


def guardar_figura(fig: plt.Figure, nombre: str) -> Path:
    "Guarda una figura como PNG en output/figures/."
    RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
    ruta = RUTA_FIGURAS / nombre
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    return ruta


def graficar_serie_anual(serie: pd.Series) -> plt.Figure:
    "Línea de eventos por año."
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(serie.index, serie.values, marker="o", markersize=3)
    ax.set_title("Desastres naturales registrados por año")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de eventos")
    ax.grid(alpha=0.3)
    return fig


def graficar_estacionalidad(est: pd.DataFrame, titulo: str) -> plt.Figure:
    "Barras de eventos promedio por mes."
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(est["mes"], est["promedio_por_anio"])
    ax.set_title(titulo)
    ax.set_xlabel("Mes")
    ax.set_ylabel("Eventos promedio por año")
    ax.grid(axis="y", alpha=0.3)
    return fig


def graficar_heatmap_anio_mes(tabla: pd.DataFrame, titulo: str) -> plt.Figure:
    "Heatmap año x mes."
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(tabla, cmap="YlOrRd", annot=True, fmt="d",
                linewidths=0.5, cbar_kws={"label": "Eventos"}, ax=ax)
    ax.set_title(titulo)
    ax.set_xlabel("Mes")
    ax.set_ylabel("Año")
    return fig


def graficar_tipo_continente(tabla: pd.DataFrame) -> plt.Figure:
    "Heatmap con el % de cada tipo de desastre por continente."
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(tabla, cmap="Blues", annot=True, fmt=".1f", linewidths=0.5,
                cbar_kws={"label": "% de los eventos del continente"}, ax=ax)
    ax.set_title("Composición de desastres por continente (%)")
    ax.set_xlabel("Continente")
    ax.set_ylabel("Tipo de desastre")
    return fig


def graficar_top_paises(tabla: pd.DataFrame) -> plt.Figure:
    "Barras apiladas horizontales: top países por tipo de desastre."
    fig, ax = plt.subplots(figsize=(10, 6))
    tabla.iloc[::-1].plot(kind="barh", stacked=True, ax=ax, colormap="tab20")
    ax.set_title("Top 10 países con más desastres, por tipo")
    ax.set_xlabel("Cantidad de eventos")
    ax.set_ylabel("")
    ax.legend(title="Tipo", bbox_to_anchor=(1.02, 1), loc="upper left")
    return fig


def graficar_inundaciones_region(tabla: pd.DataFrame) -> plt.Figure:
    "Barras horizontales de inundaciones por región."
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.barh(tabla.index[::-1], tabla["eventos"][::-1])
    ax.set_title("Inundaciones por región (1970-2021)")
    ax.set_xlabel("Cantidad de eventos")
    ax.grid(axis="x", alpha=0.3)
    return fig


def graficar_terremotos(por_pais: pd.DataFrame, por_region: pd.Series) -> plt.Figure:
    "Dos paneles: terremotos por país (top) y por región."
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.barh(por_pais["Country"][::-1], por_pais["eventos"][::-1])
    ax1.set_title("Países con más terremotos")
    ax1.set_xlabel("Cantidad de eventos")
    top_region = por_region.head(10)
    ax2.barh(top_region.index[::-1], top_region.values[::-1], color="tab:orange")
    ax2.set_title("Regiones con más terremotos")
    ax2.set_xlabel("Cantidad de eventos")
    fig.tight_layout()
    return fig


def graficar_cantidad_vs_gravedad(tabla: pd.DataFrame) -> plt.Figure:
    "Barras agrupadas: % de eventos vs % de muertes por tipo de desastre."
    fig, ax = plt.subplots(figsize=(11, 5))
    tabla[["pct_eventos", "pct_muertes"]].plot(kind="bar", ax=ax)
    ax.set_title("Frecuencia vs. letalidad por tipo de desastre")
    ax.set_xlabel("")
    ax.set_ylabel("% del total")
    ax.legend(["% de eventos", "% de muertes"])
    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    ax.grid(axis="y", alpha=0.3)
    return fig