# -*- coding: utf-8 -*-
"""
NP Statistics Analysis - Single Sample
Adapted from Conway/JCH scripts for single-sample TEM nanoparticle characterization.

Input:  NP_medidas_individuales.csv  (output de la macro ImageJ)
Output: - Histogramas PNG por parámetro
        - Boxplots PNG por parámetro
        - combined_stats.docx con tabla estadística formateada

Columnas del CSV de ImageJ:
Area, Perim., Circ., Feret, FeretX, FeretY, FeretAngle, MinFeret, AR, Round, Solidity
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# ============================================================
# CONFIGURACION
# ============================================================

INPUT_CSV  = 'NP_medidas_individuales.csv'
SAMPLE_NAME = 'Sample_1'          # Nombre de la muestra para los graficos
OUTPUT_DIR  = './'                 # Carpeta de salida (misma carpeta por defecto)

# ============================================================
# COLORES
# ============================================================
sns.set(style="whitegrid")
blues   = sns.color_palette("Blues",   10)
oranges = sns.color_palette("Oranges", 10)

# ============================================================
# LECTURA Y CALCULO DE PARAMETROS DERIVADOS
# ============================================================
df = pd.read_csv(INPUT_CSV, index_col=0)

# Columnas derivadas (igual que en tus scripts anteriores)
df['AvFeret'] = (df['Feret'] + df['MinFeret']) / 2
df['GD']      = df['Perim.'] / np.pi
df['AED']     = 2 * np.sqrt(df['Area'] / np.pi)

print(f"Particulas cargadas: {len(df)}")
print(df.head())

# ============================================================
# DEFINICION DE PARAMETROS Y NOMBRES
# ============================================================
param_names = {
    'Feret'    : 'MaxFeret (nm)',
    'MinFeret' : 'MinFeret (nm)',
    'AvFeret'  : 'Average Feret (nm)',
    'Area'     : 'Area (nm²)',
    'GD'       : 'GD (nm)',
    'AED'      : 'AED (nm)',
    'Circ.'    : 'Circularity',
    'Round'    : 'Roundness',
    'Perim.'   : 'Perimeter (nm)',
    'Solidity' : 'Solidity',
    # Para cabeceras de tabla estadística
    'Average'  : 'Average',
    'Median'   : 'Median',
    'Mode'     : 'Mode',
    'Std Dev'  : 'StdDev',
    'Q1'       : 'Q1',
    'Q3'       : 'Q3'
}

# Parámetros a analizar y graficar
params = ['Feret', 'AvFeret', 'MinFeret', 'AED', 'GD', 'Area', 'Circ.', 'Round', 'Solidity']

# Parámetros de forma (van en naranja)
shape_params = ['Circ.', 'Round', 'Solidity']

# ============================================================
# ESTADISTICAS
# ============================================================
stats_dict = {
    'Average' : [],
    'Median'  : [],
    'Mode'    : [],
    'Std Dev' : [],
    'Q1'      : [],
    'Q3'      : []
}

for col in params:
    stats_dict['Average'].append(round(df[col].mean(), 3))
    stats_dict['Median'].append(round(df[col].median(), 3))
    try:
        mode_val = stats.mode(df[col], keepdims=True)[0][0]
    except Exception:
        mode_val = np.nan
    stats_dict['Mode'].append(round(float(mode_val), 3))
    stats_dict['Std Dev'].append(round(df[col].std(), 3))
    stats_dict['Q1'].append(round(df[col].quantile(0.25), 3))
    stats_dict['Q3'].append(round(df[col].quantile(0.75), 3))

stats_df = pd.DataFrame(stats_dict, index=params)
print(f"\nEstadísticas para {SAMPLE_NAME}:\n", stats_df)

# ============================================================
# HISTOGRAMAS
# ============================================================
for param in params:
    color = oranges[5] if param in shape_params else blues[5]
    long_name = param_names[param]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df[param].dropna(), bins=20, color=color, edgecolor='white', linewidth=0.8)

    # Líneas de media y mediana
    mean_val   = df[param].mean()
    median_val = df[param].median()
    ax.axvline(mean_val,   color='black',  linestyle='--', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
    ax.axvline(median_val, color='dimgray', linestyle=':',  linewidth=1.5, label=f'Median: {median_val:.2f}')

    ax.set_title(f'{long_name} Distribution — {SAMPLE_NAME}', fontsize=14)
    ax.set_xlabel(long_name, fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.legend(fontsize=11)

    fname = os.path.join(OUTPUT_DIR, f'Hist_{param.replace(".", "")}.png')
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Guardado: {fname}")

# ============================================================
# BOXPLOTS (uno por parámetro, muestra única)
# ============================================================
for param in params:
    color = oranges[5] if param in shape_params else blues[5]
    long_name = param_names[param]

    fig, ax = plt.subplots(figsize=(5, 7))
    bp = ax.boxplot(
        df[param].dropna(),
        patch_artist=True,
        showfliers=False,
        showmeans=True,
        meanprops={"marker": "X", "markerfacecolor": "black",
                   "markeredgecolor": "white", "markersize": 10},
        medianprops={"color": "black", "linewidth": 2}
    )
    bp['boxes'][0].set_facecolor(color)

    ax.set_title(f'{long_name}\n{SAMPLE_NAME}', fontsize=13)
    ax.set_ylabel(long_name, fontsize=12)
    ax.set_xticks([])

    # Anotar Q1, Q3, media, mediana
    q1   = df[param].quantile(0.25)
    q3   = df[param].quantile(0.75)
    mean = df[param].mean()
    med  = df[param].median()
    ax.text(1.35, q1,   f'Q1={q1:.2f}',   va='center', fontsize=9, color='gray')
    ax.text(1.35, q3,   f'Q3={q3:.2f}',   va='center', fontsize=9, color='gray')
    ax.text(1.35, mean, f'μ={mean:.2f}',   va='center', fontsize=9)
    ax.text(1.35, med,  f'M={med:.2f}',    va='center', fontsize=9, color='dimgray')

    fname = os.path.join(OUTPUT_DIR, f'Box_{param.replace(".", "")}.png')
    plt.savefig(fname, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Guardado: {fname}")

# ============================================================
# PLOT COMBINADO — Diámetros
# ============================================================
diam_params = ['Feret', 'MinFeret', 'AvFeret', 'AED', 'GD']
df_melted_diam = pd.melt(df, value_vars=diam_params,
                          var_name='Measurement', value_name='Value (nm)')

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='Measurement', y='Value (nm)', data=df_melted_diam,
            showfliers=False, palette=blues[:len(diam_params)],
            showmeans=True,
            meanprops={"marker": "X", "markerfacecolor": "black",
                       "markeredgecolor": "white", "markersize": 10},
            ax=ax)
ax.set_title(f'Diameter Parameters — {SAMPLE_NAME}', fontsize=14)
ax.set_xlabel('')
ax.set_ylabel('Size (nm)', fontsize=12)
ax.set_ylim(0)
fname = os.path.join(OUTPUT_DIR, 'Combined_Diameters.png')
plt.savefig(fname, dpi=150, bbox_inches='tight')
plt.show()
print(f"Guardado: {fname}")

# ============================================================
# PLOT COMBINADO — Parámetros de forma
# ============================================================
df_melted_shape = pd.melt(df, value_vars=shape_params,
                           var_name='Measurement', value_name='Value')

fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x='Measurement', y='Value', data=df_melted_shape,
            showfliers=False, palette=oranges[:len(shape_params)],
            showmeans=True,
            meanprops={"marker": "X", "markerfacecolor": "black",
                       "markeredgecolor": "white", "markersize": 10},
            ax=ax)
ax.set_title(f'Shape Parameters — {SAMPLE_NAME}', fontsize=14)
ax.set_xlabel('')
ax.set_ylabel('Value (0–1)', fontsize=12)
ax.set_ylim(0, 1.05)
fname = os.path.join(OUTPUT_DIR, 'Combined_Shape.png')
plt.savefig(fname, dpi=150, bbox_inches='tight')
plt.show()
print(f"Guardado: {fname}")

# ============================================================
# TABLA WORD FORMATEADA
# ============================================================
def set_cell_color(cell, color):
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    tcPr.append(shd)

def create_word_table(df_stats, sample_name, document):
    title = document.add_paragraph(f"{sample_name}: Statistical Descriptors")
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = title.runs[0]
    run.font.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(31, 73, 125)

    stat_cols = ['Average', 'Median', 'Mode', 'Std Dev', 'Q1', 'Q3']
    table = document.add_table(rows=len(params) + 1, cols=len(stat_cols) + 1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Cabecera
    header_cell = table.cell(0, 0)
    header_cell.text = 'Parameter'
    header_cell.paragraphs[0].runs[0].font.bold = True
    header_cell.paragraphs[0].runs[0].font.size = Pt(11)
    header_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    header_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cell_color(header_cell, '4472C4')

    for j, col in enumerate(stat_cols):
        hc = table.cell(0, j + 1)
        hc.text = param_names.get(col, col)
        hc.paragraphs[0].runs[0].font.bold = True
        hc.paragraphs[0].runs[0].font.size = Pt(11)
        hc.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        hc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_color(hc, '4472C4')

    # Filas de datos
    for i, param in enumerate(params):
        if param not in df_stats.index:
            continue
        row_color = 'D9E1F2' if i % 2 == 0 else 'FFFFFF'

        pc = table.cell(i + 1, 0)
        pc.text = param_names.get(param, param)
        pc.paragraphs[0].runs[0].font.bold = True
        pc.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_color(pc, row_color)

        for j, col in enumerate(stat_cols):
            cell = table.cell(i + 1, j + 1)
            cell.text = str(df_stats.loc[param, col])
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.paragraphs[0].runs[0].font.size = Pt(10)
            set_cell_color(cell, row_color)

    document.add_paragraph("")

# Generar documento Word
document = Document()
create_word_table(stats_df, SAMPLE_NAME, document)
docx_path = os.path.join(OUTPUT_DIR, 'NP_stats_table.docx')
document.save(docx_path)
print(f"\nDocumento Word guardado: {docx_path}")
print("\n=== ANALISIS COMPLETADO ===")
print(f"N partículas analizadas: {len(df)}")
print(stats_df.to_string())
