# SmallScripts

Scripts para caracterizar nanopartículas (NPs) a partir de imágenes de TEM:
segmentación en ImageJ/Fiji y análisis estadístico de tamaño y forma en Python.

## Flujo de trabajo

```
Stack TIF de TEM ──► NP_Analysis_Macro.ijm (Fiji) ──► CSV con medidas por partícula
                                                          │
                     ┌────────────────────────────────────┤
                     ▼                                    ▼
          una muestra: NP_stats_analysis.py     varias muestras: Nanomegas_Statistics*.py
                                                                 Plot_IJPArticles.py
```

## Scripts

| Script | Qué hace | Entrada | Salida |
|---|---|---|---|
| `NP_Analysis_Macro.ijm` | Macro de Fiji: 8-bit + autocontraste, bandpass FFT para quitar el carbono, umbral Otsu, *fill holes* + dilatación y *Analyze Particles*. | Stack TIF abierto en Fiji | `NP_medidas_individuales.csv`, `NP_resumen_por_imagen.csv`, `Overlay_Stack.tif` con las ROIs |
| `NP_stats_analysis.py` | Estadística de **una muestra**: histogramas y boxplots por parámetro. | `NP_medidas_individuales.csv` | PNG por parámetro y `combined_stats.docx` con la tabla |
| `Nanomegas_Statistics_simple.py` | Compara **varias muestras**: boxplots por parámetro, test de Kruskal-Wallis y post-hoc de Dunn (mapa de calor de similitud). | `S1_CLASS_1.csv`, `S2_CLASS_1.csv`… | PNG por parámetro y tablas resumen en Word |
| `Nanomegas_Statistics.py` | Como el anterior, y además dendrograma de agrupamiento jerárquico a partir del test de Dunn. | `S{n}_CLASS_1.csv` | PNG (distribuciones, heatmaps, dendrogramas) y Word |
| `Nanomegas_Statistics_Separated.py` | Variante del análisis multimuestra, con cada gráfico y test en una sección aparte. | CSV de *Analyze Particles* | PNG, CSV del test de Dunn y Word |
| `Plot_IJPArticles.py` | Boxplots para figuras de artículo: MaxFeret, MinFeret, AvFeret, AED, GD, área, perímetro, redondez, circularidad y un gráfico combinado de diámetros. | `Results_S{n}_dot.csv` | Gráficos en pantalla |

## Parámetros calculados

Además de las columnas de ImageJ (`Area`, `Perim.`, `Feret`, `MinFeret`, `Circ.`, `Round`…),
los scripts de Python añaden:

- **AvFeret**: media de `Feret` y `MinFeret`.
- **GD** (diámetro geométrico): `Perim. / π`.
- **AED** (diámetro de área equivalente): `2·√(Area / π)`.

## Uso

1. Fiji: abre el stack TIF y ejecuta `NP_Analysis_Macro.ijm`. Revisa antes la configuración al
   principio de la macro (tamaño de píxel, por defecto 0.3 nm/px; área mínima; circularidad).
2. Python: copia el script a la carpeta de los CSV, ajusta el número de muestras (`ns`) o el
   nombre del CSV en la sección de configuración y ejecútalo.

Dependencias de Python:

```
pip install pandas numpy matplotlib seaborn scipy scikit-posthocs python-docx
```

## Notas

- El Feret que mide la macro puede quedarse 1–2 nm corto por el suavizado del bandpass.
  Conviene validarlo midiendo a mano unas 20–30 NPs.
