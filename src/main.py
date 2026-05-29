from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "dataset_set_A_aguas_residuales.xlsx"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

UMBRAL_EFICIENCIA = 85  # criterio operacional ajustable


def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Carga el dataset oficial de AquaLimpia."""
    df = pd.read_excel(ruta)
    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])
    return df


def preparar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega indicadores analíticos para apoyar la toma de decisiones."""
    df = df.copy()

    df["eficiencia_DBO_pct"] = (
        (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"])
        / df["DBO_entrada_mg_L"]
    ) * 100

    df["estado_cumplimiento"] = np.where(
        df["cumplimiento_norma"] == 1,
        "Cumple",
        "No cumple"
    )

    df["alerta_operativa"] = np.where(
        (df["cumplimiento_norma"] == 0) |
        (df["eficiencia_DBO_pct"] < UMBRAL_EFICIENCIA),
        "Alerta",
        "Normal"
    )

    return df


def exportar_reportes(df: pd.DataFrame) -> None:
    """Genera archivos de salida para Operaciones y Gestión Ambiental."""

    reporte_operaciones = df[[
        "fecha_registro",
        "planta",
        "caudal_entrada_m3_d",
        "DBO_entrada_mg_L",
        "DBO_salida_mg_L",
        "energia_aeracion_kWh",
        "lodos_generados_kg_d",
        "eficiencia_DBO_pct",
        "alerta_operativa"
    ]]

    reporte_ambiental = df[[
        "fecha_registro",
        "planta",
        "DBO_salida_mg_L",
        "cumplimiento_norma",
        "estado_cumplimiento"
    ]]

    resumen_planta = df.groupby("planta").agg(
        registros=("planta", "count"),
        cumplimiento_pct=("cumplimiento_norma", "mean"),
        DBO_salida_promedio=("DBO_salida_mg_L", "mean"),
        eficiencia_DBO_promedio=("eficiencia_DBO_pct", "mean"),
        caudal_promedio=("caudal_entrada_m3_d", "mean"),
        energia_promedio=("energia_aeracion_kWh", "mean"),
        lodos_promedio=("lodos_generados_kg_d", "mean")
    ).reset_index()

    resumen_planta["cumplimiento_pct"] *= 100

    reporte_operaciones.to_csv(
        OUTPUT_DIR / "reporte_operaciones.csv",
        index=False,
        encoding="utf-8-sig"
    )

    reporte_ambiental.to_csv(
        OUTPUT_DIR / "reporte_gestion_ambiental.csv",
        index=False,
        encoding="utf-8-sig"
    )

    resumen_planta.to_csv(
        OUTPUT_DIR / "resumen_por_planta.csv",
        index=False,
        encoding="utf-8-sig"
    )


def crear_dashboard(df: pd.DataFrame) -> None:
    """Construye un dashboard exploratorio en HTML."""

    resumen = df.groupby("planta").agg(
        cumplimiento_pct=("cumplimiento_norma", "mean"),
        DBO_salida_promedio=("DBO_salida_mg_L", "mean"),
        eficiencia_DBO_promedio=("eficiencia_DBO_pct", "mean"),
        caudal_promedio=("caudal_entrada_m3_d", "mean")
    ).reset_index()

    resumen["cumplimiento_pct"] *= 100

    tendencia = (
        df.sort_values("fecha_registro")
        .groupby(["fecha_registro", "planta"], as_index=False)
        .agg(DBO_salida_promedio=("DBO_salida_mg_L", "mean"))
    )

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Cumplimiento normativo por planta (%)",
            "DBO salida promedio por planta",
            "Tendencia temporal de DBO salida",
            "Relación entre caudal de entrada y DBO salida"
        )
    )

    fig.add_trace(
        go.Bar(
            x=resumen["planta"],
            y=resumen["cumplimiento_pct"],
            name="Cumplimiento %"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Bar(
            x=resumen["planta"],
            y=resumen["DBO_salida_promedio"],
            name="DBO salida promedio"
        ),
        row=1,
        col=2
    )

    for planta in tendencia["planta"].unique():
        datos_planta = tendencia[tendencia["planta"] == planta]

        fig.add_trace(
            go.Scatter(
                x=datos_planta["fecha_registro"],
                y=datos_planta["DBO_salida_promedio"],
                mode="lines+markers",
                name=f"DBO salida - {planta}"
            ),
            row=2,
            col=1
        )

    for planta in df["planta"].unique():
        datos_planta = df[df["planta"] == planta]

        fig.add_trace(
            go.Scatter(
                x=datos_planta["caudal_entrada_m3_d"],
                y=datos_planta["DBO_salida_mg_L"],
                mode="markers",
                name=f"Caudal vs DBO - {planta}",
                text=datos_planta["estado_cumplimiento"]
            ),
            row=2,
            col=2
        )

    fig.update_layout(
        title_text="Dashboard exploratorio - AquaLimpia S. A.",
        height=850,
        showlegend=True
    )

    fig.write_html(OUTPUT_DIR / "dashboard_aqualimpia.html")


def main() -> None:
    df = cargar_datos(DATA_PATH)
    df = preparar_datos(df)

    exportar_reportes(df)
    crear_dashboard(df)

    print("Proceso finalizado correctamente.")
    print(f"Archivos generados en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()