# Documentación técnica del proyecto AquaLimpia S. A.

## 1. Descripción del proyecto

Este proyecto corresponde al análisis exploratorio de datos aplicado a la empresa AquaLimpia S. A., dedicada al tratamiento de aguas residuales urbanas e industriales.

Durante el último trimestre se identificaron incumplimientos intermitentes en parámetros críticos de calidad del efluente tratado, especialmente en los niveles de DBO y en la eficiencia del tratamiento. Por esta razón, se desarrolla un análisis de datos que permita comparar el desempeño de las plantas, identificar patrones relevantes y generar información útil para la toma de decisiones.

## 2. Objetivo general

Analizar el desempeño operacional y ambiental de las plantas de tratamiento de AquaLimpia S. A. mediante Python, con el fin de apoyar la toma de decisiones, detectar alertas operativas y respaldar reportes de cumplimiento ambiental.

## 3. Objetivos específicos

* Cargar y preparar el dataset oficial del caso.
* Calcular indicadores relevantes para evaluar el proceso de tratamiento.
* Analizar el comportamiento de variables como caudal, DBO, energía y lodos generados.
* Generar reportes diferenciados para el área de Operaciones y Gestión Ambiental.
* Construir un dashboard exploratorio para visualizar el desempeño de las plantas.
* Organizar el proyecto en un repositorio Git para asegurar trazabilidad y reproducibilidad.

## 4. Preguntas de investigación

* ¿Qué plantas presentan mayores niveles de DBO en el efluente tratado?
* ¿Qué porcentaje de cumplimiento normativo presenta cada planta?
* ¿Existen diferencias relevantes de desempeño entre plantas?
* ¿Cómo se relaciona el caudal de entrada con la DBO de salida?
* ¿Qué registros deberían considerarse como alertas operativas?

## 5. Dataset utilizado

El archivo utilizado corresponde al dataset oficial del caso:

```text
data/dataset_set_A_aguas_residuales.xlsx
```

El dataset contiene registros asociados al funcionamiento de plantas de tratamiento, incluyendo variables operacionales y ambientales.

## 6. Variables principales

| Variable               | Descripción                                          |
| ---------------------- | ---------------------------------------------------- |
| `fecha_registro`       | Fecha del registro operacional.                      |
| `planta`               | Planta de tratamiento correspondiente.               |
| `caudal_entrada_m3_d`  | Caudal de entrada recibido por la planta.            |
| `DBO_entrada_mg_L`     | Nivel de DBO antes del tratamiento.                  |
| `DBO_salida_mg_L`      | Nivel de DBO después del tratamiento.                |
| `energia_aeracion_kWh` | Consumo energético asociado al proceso de aireación. |
| `lodos_generados_kg_d` | Cantidad de lodos generados por día.                 |
| `cumplimiento_norma`   | Indicador de cumplimiento normativo.                 |

## 7. Indicadores calculados

### Eficiencia de remoción de DBO

Se calcula la eficiencia del tratamiento mediante la siguiente fórmula:

```text
eficiencia_DBO_pct = ((DBO_entrada_mg_L - DBO_salida_mg_L) / DBO_entrada_mg_L) * 100
```

Este indicador permite evaluar qué porcentaje de la carga contaminante fue removido durante el proceso.

### Estado de cumplimiento

Se transforma la variable `cumplimiento_norma` en una categoría interpretativa:

| Valor original | Estado    |
| -------------- | --------- |
| 1              | Cumple    |
| 0              | No cumple |

### Alerta operativa

Se genera una alerta cuando el registro no cumple la norma o cuando la eficiencia de remoción de DBO se encuentra bajo el umbral definido en el análisis.

## 8. Flujo de trabajo aplicado

El análisis se estructura en las siguientes etapas:

1. Carga del dataset desde la carpeta `data/`.
2. Revisión inicial de estructura y variables.
3. Conversión de fechas y preparación de datos.
4. Cálculo de indicadores operacionales y ambientales.
5. Generación de reportes por área.
6. Construcción de dashboard exploratorio.
7. Exportación de archivos de salida.
8. Publicación del proyecto en repositorio GitHub.

## 9. Librerías utilizadas

El proyecto utiliza las siguientes librerías de Python:

| Librería   | Uso principal                                        |
| ---------- | ---------------------------------------------------- |
| `pandas`   | Carga, transformación y análisis de datos.           |
| `numpy`    | Cálculo de condiciones e indicadores.                |
| `openpyxl` | Lectura del archivo Excel.                           |
| `plotly`   | Construcción del dashboard exploratorio.             |
| `scipy`    | Apoyo para análisis estadístico.                     |
| `joblib`   | Apoyo para reutilización y persistencia de procesos. |

## 10. Estructura del proyecto

```text
Semana 8/
│
├── data/
│   └── dataset_set_A_aguas_residuales.xlsx
│
├── docs/
│   └── documentacion_tecnica.md
│
├── outputs/
│   ├── dashboard_aqualimpia.html
│   ├── reporte_operaciones.csv
│   ├── reporte_gestion_ambiental.csv
│   └── resumen_por_planta.csv
│
├── src/
│   └── main.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 11. Archivos de salida generados

| Archivo                         | Descripción                                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------- |
| `reporte_operaciones.csv`       | Reporte orientado al área de Operaciones, con variables de proceso, eficiencia y alertas.   |
| `reporte_gestion_ambiental.csv` | Reporte orientado al área de Gestión Ambiental, con DBO de salida y estado de cumplimiento. |
| `resumen_por_planta.csv`        | Resumen comparativo del desempeño de cada planta.                                           |
| `dashboard_aqualimpia.html`     | Dashboard exploratorio con gráficos para interpretar el comportamiento de las plantas.      |

## 12. Resultados principales

El análisis permite comparar el desempeño de las plantas de tratamiento a partir de indicadores como cumplimiento normativo, DBO de salida promedio, eficiencia de remoción de DBO, caudal de entrada, consumo de energía y generación de lodos.

El dashboard permite visualizar diferencias entre plantas, tendencias temporales en la calidad del efluente y posibles relaciones entre variables operacionales y resultados ambientales. Estos resultados no deben interpretarse como una prueba causal definitiva, sino como evidencia exploratoria para priorizar revisiones técnicas y apoyar la toma de decisiones.

## 13. Reproducibilidad

Para reproducir el análisis, se deben seguir los siguientes pasos:

```bash
pip install -r requirements.txt
python src/main.py
```

Luego de ejecutar el script, los archivos generados quedan almacenados en la carpeta `outputs/`.

## 14. Conclusión técnica

La documentación técnica permite comprender el propósito del análisis, los pasos ejecutados y los resultados obtenidos. Además, facilita que el proyecto pueda ser revisado por docentes, equipos técnicos o futuras personas que necesiten reutilizar el análisis. En conjunto con GitHub, el archivo Markdown mejora la trazabilidad, la colaboración y la reproducibilidad del proyecto.
