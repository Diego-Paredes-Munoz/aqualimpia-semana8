from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import joblib


def preparar_indicadores(df: pd.DataFrame, umbral_eficiencia: float = 85) -> pd.DataFrame:
    """
    Calcula indicadores operacionales y ambientales para el análisis de AquaLimpia.
    Usa NumPy para condiciones vectorizadas.
    """
    df = df.copy()

    df["fecha_registro"] = pd.to_datetime(df["fecha_registro"])

    # Evita división por cero si existiera algún valor 0 en DBO de entrada
    dbo_entrada_segura = df["DBO_entrada_mg_L"].replace(0, np.nan)

    df["eficiencia_DBO_pct"] = (
        (df["DBO_entrada_mg_L"] - df["DBO_salida_mg_L"]) / dbo_entrada_segura
    ) * 100

    df["estado_cumplimiento"] = np.where(
        df["cumplimiento_norma"] == 1,
        "Cumple",
        "No cumple"
    )

    df["alerta_operativa"] = np.where(
        (df["cumplimiento_norma"] == 0) |
        (df["eficiencia_DBO_pct"] < umbral_eficiencia),
        "Alerta",
        "Normal"
    )

    return df


def calcular_correlacion_spearman(
    df: pd.DataFrame,
    columna_x: str,
    columna_y: str
) -> dict:
    """
    Calcula correlación de Spearman entre dos variables numéricas.
    Usa SciPy para evaluar relación monotónica entre variables.
    """
    datos = df[[columna_x, columna_y]].dropna()

    if len(datos) < 3:
        return {
            "variable_x": columna_x,
            "variable_y": columna_y,
            "correlacion_spearman": np.nan,
            "p_value": np.nan,
            "interpretacion": "No hay datos suficientes para calcular la correlación."
        }

    coeficiente, p_value = stats.spearmanr(datos[columna_x], datos[columna_y])

    if abs(coeficiente) >= 0.7:
        fuerza = "fuerte"
    elif abs(coeficiente) >= 0.4:
        fuerza = "moderada"
    else:
        fuerza = "débil"

    return {
        "variable_x": columna_x,
        "variable_y": columna_y,
        "correlacion_spearman": coeficiente,
        "p_value": p_value,
        "interpretacion": f"Relación {fuerza} entre {columna_x} y {columna_y}."
    }


def detectar_outliers_zscore(
    df: pd.DataFrame,
    columna: str,
    limite: float = 3
) -> pd.DataFrame:
    """
    Detecta valores atípicos usando z-score.
    Usa SciPy para estandarizar la variable seleccionada.
    """
    df = df.copy()

    z_scores = stats.zscore(df[columna], nan_policy="omit")
    df[f"zscore_{columna}"] = z_scores
    df[f"outlier_{columna}"] = np.abs(z_scores) > limite

    return df


def generar_resumen_por_planta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un resumen estadístico por planta de tratamiento.
    """
    resumen = df.groupby("planta").agg(
        registros=("planta", "count"),
        cumplimiento_pct=("cumplimiento_norma", "mean"),
        DBO_salida_promedio=("DBO_salida_mg_L", "mean"),
        eficiencia_DBO_promedio=("eficiencia_DBO_pct", "mean"),
        caudal_promedio=("caudal_entrada_m3_d", "mean"),
        energia_promedio=("energia_aeracion_kWh", "mean"),
        lodos_promedio=("lodos_generados_kg_d", "mean"),
        alertas_operativas=("alerta_operativa", lambda x: (x == "Alerta").sum())
    ).reset_index()

    resumen["cumplimiento_pct"] *= 100

    return resumen


def guardar_joblib(objeto, ruta_salida: Path) -> None:
    """
    Guarda objetos del análisis usando Joblib.
    Esto permite reutilizar resultados sin recalcularlos.
    """
    joblib.dump(objeto, ruta_salida)


def evaluar_calidad_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evalúa la calidad de los datos del proyecto AquaLimpia.
    Revisa nulos, duplicados, valores negativos e inconsistencias básicas.
    """

    columnas_numericas = [
        "caudal_entrada_m3_d",
        "DBO_entrada_mg_L",
        "DBO_salida_mg_L",
        "energia_aeracion_kWh",
        "lodos_generados_kg_d"
    ]

    resultados = []

    # Total de registros
    resultados.append({
        "criterio": "Total de registros",
        "resultado": len(df),
        "detalle": "Cantidad total de filas del dataset."
    })

    # Valores nulos por columna
    for columna in df.columns:
        cantidad_nulos = df[columna].isna().sum()
        resultados.append({
            "criterio": f"Valores nulos en {columna}",
            "resultado": int(cantidad_nulos),
            "detalle": "Cantidad de registros sin información en la columna."
        })

    # Registros duplicados
    duplicados = df.duplicated().sum()
    resultados.append({
        "criterio": "Registros duplicados",
        "resultado": int(duplicados),
        "detalle": "Cantidad de filas completamente repetidas."
    })

    # Valores negativos en variables numéricas
    for columna in columnas_numericas:
        negativos = (df[columna] < 0).sum()
        resultados.append({
            "criterio": f"Valores negativos en {columna}",
            "resultado": int(negativos),
            "detalle": "Cantidad de valores físicamente inválidos para el proceso."
        })

    # DBO salida mayor que DBO entrada
    dbo_inconsistente = (df["DBO_salida_mg_L"] > df["DBO_entrada_mg_L"]).sum()
    resultados.append({
        "criterio": "DBO salida mayor que DBO entrada",
        "resultado": int(dbo_inconsistente),
        "detalle": "Registros donde la eficiencia del tratamiento sería negativa."
    })

    # Valores inválidos en cumplimiento normativo
    cumplimiento_invalido = (~df["cumplimiento_norma"].isin([0, 1])).sum()
    resultados.append({
        "criterio": "Valores inválidos en cumplimiento_norma",
        "resultado": int(cumplimiento_invalido),
        "detalle": "Registros con valores distintos de 0 o 1."
    })

    return pd.DataFrame(resultados)