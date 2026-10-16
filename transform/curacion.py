"Módulo de curación: depuro y estandarizo variables categóricas."

import pandas as pd

# Nombres oficiales largos -> nombres de uso común
NOMBRES_PAISES = {
    "United States of America (the)": "United States",
    "United Kingdom of Great Britain and Northern Ireland (the)": "United Kingdom",
    "Russian Federation (the)": "Russia",
    "Iran (Islamic Republic of)": "Iran",
    "Korea (the Republic of)": "South Korea",
    "Korea (the Democratic People's Republic of)": "North Korea",
    "Congo (the Democratic Republic of the)": "DR Congo",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Taiwan (Province of China)": "Taiwan",
    "Lao People's Democratic Republic (the)": "Laos",
    "Moldova (the Republic of)": "Moldova",
    "Macedonia (the former Yugoslav Republic of)": "North Macedonia",
    "Micronesia (Federated States of)": "Micronesia",
    "Tanzania, United Republic of": "Tanzania",
    "Palestine, State of": "Palestine",
    "Syrian Arab Republic": "Syria",
    "Viet Nam": "Vietnam",
    "Swaziland": "Eswatini",
}

# Países que ya no existen (se conservan, pero quedan marcados)
PAISES_HISTORICOS = [
    "Soviet Union", "Yugoslavia", "Czechoslovakia", "Germany Dem Rep",
    "Germany Fed Rep", "Serbia Montenegro", "Yemen Arab Rep",
    "Yemen P Dem Rep", "Netherlands Antilles",
]

COLUMNAS_TEXTO = ["Disaster Type", "Disaster Subtype", "Country", "Region",
                  "Continent", "Location"]


def limpiar_texto(df: pd.DataFrame, columnas: list = COLUMNAS_TEXTO) -> pd.DataFrame:
    "Quito espacios al inicio/final y espacios dobles en las columnas indicadas."
    df = df.copy()
    for col in columnas:
        df[col] = (df[col].str.strip()
                          .str.replace(r"\s+", " ", regex=True))
    return df


def estandarizar_paises(df: pd.DataFrame) -> pd.DataFrame:
    "Unifica los nombres de países a su forma corta de uso común."
    df = df.copy()
    df["Country"] = df["Country"].replace(NOMBRES_PAISES)
    # El resto de los países con sufijo " (the)" (Philippines (the), etc.)
    df["Country"] = df["Country"].str.replace(r"\s*\(the\)$", "", regex=True)
    return df


def estandarizar_regiones(df: pd.DataFrame) -> pd.DataFrame:
    "Corrige valores de Region que no son regiones (la URSS figura como 'Russian Federation')."
    df = df.copy()
    df["Region"] = df["Region"].replace({"Russian Federation": "Eastern Europe"})
    return df


def marcar_paises_historicos(df: pd.DataFrame) -> pd.DataFrame:
    "Agrega una columna booleana que indica si el país ya no existe."
    df = df.copy()
    df["pais_historico"] = df["Country"].isin(PAISES_HISTORICOS)
    return df


def imputar_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa nulos de variables categóricas con una etiqueta explícita.

    Las variables numéricas (muertes, afectados, daños) NO se imputan:
    rellenarlas con 0 o con el promedio inventaría datos.
    """
    df = df.copy()
    df["Disaster Subtype"] = df["Disaster Subtype"].fillna("Sin especificar")
    df["Location"] = df["Location"].fillna("Desconocida")
    return df


def curar_variables(df: pd.DataFrame) -> pd.DataFrame:
    "Aplica toda la curación de categorías y ubicación, en orden."
    df = limpiar_texto(df)
    df = estandarizar_paises(df)
    df = estandarizar_regiones(df)
    df = marcar_paises_historicos(df)
    df = imputar_categoricas(df)
    return df


def reporte_curacion(antes: pd.DataFrame, despues: pd.DataFrame) -> None:
    "Imprime un resumen comparando el dataset antes y después de la curación."
    print("Países distintos      :", antes["Country"].nunique(), "->", despues["Country"].nunique())
    print("Regiones distintas    :", antes["Region"].nunique(), "->", despues["Region"].nunique())
    print("Tipos de desastre     :", antes["Disaster Type"].nunique(), "->", despues["Disaster Type"].nunique())
    esp_antes = (antes["Disaster Type"] != antes["Disaster Type"].str.strip()).sum()
    esp_desp = (despues["Disaster Type"] != despues["Disaster Type"].str.strip()).sum()
    print("Tipos con espacios    :", esp_antes, "->", esp_desp)
    print("Nulos en Subtype      :", antes["Disaster Subtype"].isna().sum(), "->", despues["Disaster Subtype"].isna().sum())
    print("Nulos en Location     :", antes["Location"].isna().sum(), "->", despues["Location"].isna().sum())
    print("Registros de países históricos:", despues["pais_historico"].sum())