"Entrada del proceso ETL"

import matplotlib
matplotlib.use("Agg")  # Backend sin ventanas: el proceso solo guarda archivos PNG


from extract.extractor import extraer_datos
from transform.transformer import (
    crear_fecha, filtrar_periodo_reciente, eventos_por_anio,
    calcular_estacionalidad, tabla_anios_mes,
)
from transform.curacion import curar_variables, reporte_curacion
from transform.cruces import (
    tipo_por_continente, top_paises_por_tipo, inundaciones_por_region,
    terremotos_por_pais, terremotos_por_region, cantidad_vs_gravedad,
)
from load.loader import (
    guardar_dataset, guardar_figura, graficar_serie_anual,
    graficar_estacionalidad, graficar_heatmap_anio_mes,
    graficar_tipo_continente, graficar_top_paises, graficar_inundaciones_region,
    graficar_terremotos, graficar_cantidad_vs_gravedad,
)


def main():
    # EXTRACT
    bruto = extraer_datos()

    # TRANSFORM
    df = crear_fecha(bruto)
    print(f"Fechas creadas: {df['fecha'].notna().sum()} | sin fecha (mes faltante): {df['fecha'].isna().sum()}")
    df = curar_variables(df)
    print("\nResumen de la curación:")
    reporte_curacion(bruto, df)
    reciente = filtrar_periodo_reciente(df, anios=20)

    serie = eventos_por_anio(df)
    est_total = calcular_estacionalidad(df)
    est_reciente = calcular_estacionalidad(reciente)
    matriz = tabla_anios_mes(reciente)

    print("\nEstacionalidad (últimos 20 años):")
    print(est_reciente.to_string(index=False))

    # Los 5 cruces de variables
    cruce1 = tipo_por_continente(df)
    cruce2 = top_paises_por_tipo(df)
    cruce3 = inundaciones_por_region(df)
    cruce4_pais = terremotos_por_pais(df)
    cruce4_region = terremotos_por_region(df)
    cruce5 = cantidad_vs_gravedad(df)

    # LOAD
    guardar_dataset(df, "disasters_curado.csv")
    guardar_figura(graficar_serie_anual(serie), "serie_anual.png")
    guardar_figura(graficar_estacionalidad(est_total, "Estacionalidad 1970-2021"), "estacionalidad_total.png")
    guardar_figura(graficar_estacionalidad(est_reciente, "Estacionalidad últimos 20 años"), "estacionalidad_reciente.png")
    guardar_figura(graficar_heatmap_anio_mes(matriz, "Eventos por año y mes (últimos 20 años)"), "heatmap_anio_mes.png")
    guardar_figura(graficar_tipo_continente(cruce1), "cruce1_tipo_continente.png")
    guardar_figura(graficar_top_paises(cruce2), "cruce2_top_paises.png")
    guardar_figura(graficar_inundaciones_region(cruce3), "cruce3_inundaciones_region.png")
    guardar_figura(graficar_terremotos(cruce4_pais, cruce4_region), "cruce4_terremotos.png")
    guardar_figura(graficar_cantidad_vs_gravedad(cruce5), "cruce5_cantidad_vs_gravedad.png")
    print("\nProceso completado. Ver carpetas data/processed y output/figures.")


if __name__ == "__main__":
    main()