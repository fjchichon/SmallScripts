# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 19:19:25 2024

@author: Conway
#This CODE requires csv files from ImageJ (Analyze Particles)
#Remember to set the number of SAMPLES you will have in line 45
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import scikit_posthocs as sp
from docx import Document
from docx.table import Table, _Cell
from scipy.stats import kruskal

## COLORS 
sns.set(style="whitegrid")
plt.ion()
# Create an array with the colors you want to use

# Crear paleta de colores azules, de más intenso a pastel
blues = sns.color_palette("Blues", 10)  # Paleta de 10 tonos de azul

# Crear paleta de colores naranjas, de más intenso a pastel
oranges = sns.color_palette("Oranges", 10)  # Paleta de 10 tonos de naranja

# Crear paleta nueva de 3 colores azules
#blues_palette = sns.color_palette("Blues", 3)

# %%%%%%%%% Lectura y generacion %%

#Leemos los ficheros csv
# Lista para almacenar los DataFrames
dataframes = []

# CSV Created in ImageJ
########################################################################################################################
# ,Area,X,Y,Perim.,Major,Minor,Angle,Circ.,Feret,Median,Skew,Kurt,FeretX,FeretY,FeretAngle,MinFeret,AR,Round,Solidity
#########################################################################################################################

# introducir numero de muestras ·····
ns = 6  # Cambia este valor según el número de muestras

# Bucle para cargar y añadir la columna 'Sample' a cada DataFrame
for nsample in range(1, ns + 1):
    # Leer el archivo CSV correspondiente
    file_name = f'Results_S{nsample}_dot.csv'
    df = pd.read_csv(file_name)
    

    # Calcular la nueva columna AverageFeret como el promedio de 'Feret' y 'MinFeret'
    df['AvFeret'] = (df['Feret'] + df['MinFeret']) / 2
    
    # Calcular la nueva columna GD (Geometric Diameter) como 'Perim.' / π
    df['GD'] = df['Perim.'] / np.pi  # np.pi proporciona el valor de π
    
    # Calcular la nueva columna AED (Area Equivalent Diameter) como 2 * √(Area / π)
    df['AED'] = 2 * np.sqrt(df['Area'] / np.pi)
    
    # Añadir columna identificativa para cada muestra
    df['Sample'] = f'Sample {nsample}'
    
    # Añadir el DataFrame a la lista
    dataframes.append(df)
    
# Combinar todos los DataFrames en uno solo
df_combined = pd.concat(dataframes, ignore_index=True)

# Mostrar las primeras filas del DataFrame combinado para verificar
print(df_combined.head())




# %%%%%%%%% TABLES %%
#
# CSV Created in ImageJ
########################################################################################################################
# ,Area,X,Y,Perim.,Major,Minor,Angle,Circ.,Feret,Median,Skew,Kurt,FeretX,FeretY,FeretAngle,MinFeret,AR,Round,Solidity
#########################################################################################################################
    # Calcular la nueva columna AverageFeret (AVFeret) como el promedio de 'Feret' y 'MinFeret'
    # Calcular la nueva columna GD (Geometric Diameter) como 'Perim.' / π
    # Calcular la nueva columna AED (Area Equivalent Diameter) como 2 * √(Area / π)
# Definición de nombres descriptivos para los parámetros
import pandas as pd
from docx import Document
from scipy import stats

# Definición de nombres descriptivos para los parámetros
param_names = {
    'Feret': 'MaxFeret',
    'MinFeret': 'MinFeret',
    'Area': 'Area (nm²)',  # Incluye unidades
    'GD': 'Geometric Diameter (GD)',
    'Circ.': 'Circularity',
    'Round': 'Roundness',
    'AED': 'Area Equivalent Diameter (AED)',
    'Perim.': 'Perimeter',
    'AvFeret': 'Average Feret',
    'Average': 'Average',
    'Median': 'Median',
    'Mode': 'Mode',
    'Std Dev': 'Standard Deviation',
    'Q1': '1st Quartile (Q1)',
    'Q3': '3rd Quartile (Q3)'
}

# %%%%%%%%% TABLES %%
#
# Lista de columnas para las que queremos calcular las estadísticas
columns = list(param_names.keys())  # Usar las claves del diccionario

# Diccionario para almacenar los DataFrames de estadísticas por muestra
stats_dfs = {}

# Calcular estadísticas para cada muestra
for nsample in range(1, ns + 1):
    sample_df = df_combined[df_combined['Sample'] == f'Sample {nsample}']
    
    # Verificar que las columnas existen en sample_df
    existing_columns = sample_df.columns.intersection(columns)

    stats_dict = {'Average': [], 'Median': [], 'Mode': [], 'Std Dev': [], 'Q1': [], 'Q3': []}
    
    for col in existing_columns:
        stats_dict['Average'].append(round(sample_df[col].mean(), 2))
        stats_dict['Median'].append(round(sample_df[col].median(), 2))
        stats_dict['Mode'].append(round(stats.mode(sample_df[col])[0][0], 2))
        stats_dict['Std Dev'].append(round(sample_df[col].std(), 2))
        stats_dict['Q1'].append(round(sample_df[col].quantile(0.25), 2))
        stats_dict['Q3'].append(round(sample_df[col].quantile(0.75), 2))

    # Convertir el diccionario en un DataFrame y almacenarlo en el diccionario de DataFrames
    stats_dfs[f'Sample {nsample}'] = pd.DataFrame(stats_dict, index=existing_columns)

# Mostrar las tablas de estadísticas para cada muestra
for sample, stats_df in stats_dfs.items():
    print(f"\nEstadísticas para {sample}:\n", stats_df)

# %%%%%%%%% PLOTS %%
 # %%%%%%%%% TABLES WORD%%
# DARA ERROR SI EXIXTE EL FICHERO
# Función para crear una tabla en un documento Word
def create_word_table(df, file_name):
    document = Document()
    table = document.add_table(rows=df.shape[0] + 1, cols=df.shape[1] + 1)  # +1 para la columna de parámetros

    # Agregar encabezado con nombres descriptivos
    table.cell(0, 0).text = 'Parameter'  # Nombre de la columna de parámetros
    for j, col in enumerate(df.columns):
        descriptive_name = param_names.get(col, col)  # Usar el nombre original si no está en el diccionario
        cell = table.cell(0, j + 1)  # Colocamos en j + 1 porque 0 es para la columna de parámetros
        cell.text = descriptive_name

    # Agregar filas de datos
    for i, index in enumerate(df.index):
        # Añadir el nombre del parámetro
        table.cell(i + 1, 0).text = param_names.get(index, index)  # Usar el nombre descriptivo o el original
        for j, col in enumerate(df.columns):
            cell = table.cell(i + 1, j + 1)  # Colocamos en j + 1
            cell.text = str(df.loc[index, col])

    # Ajustar el formato de las celdas
    for row in table.rows:
        for cell in row.cells:
            cell.text = cell.text.strip()  # Eliminar espacios extra

    document.save(file_name)

# Crear documentos Word para cada tabla de estadísticas
for sample, stats_df in stats_dfs.items():
    file_name = f"stats_{sample}.docx"
    create_word_table(stats_df, file_name)

#

# %%%%%%%%% Feret %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='Feret',   # Usar 'Feret' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=blues,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     
# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X

plt.ylabel('MaxFeret (nm)')    # Etiqueta del eje Y
plt.title('MaxFeret Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()


# %%%%%%%%% MinFeret %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='MinFeret',   # Usar 'Feret' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=blues,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     


# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X
plt.ylabel('MinFeret (nm)')    # Etiqueta del eje Y
plt.title('MinFeret Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()



# %%%%%%%%% Roundneess %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='Round',   # Usar 'Feret' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=oranges,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     


# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X

plt.ylabel('Roundess')    # Etiqueta del eje Y
plt.title('Roundness Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()

# %%%%%%%%% circularity %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='Circ.',   # Usar 'Feret' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=oranges,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     


# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X
plt.ylabel('Circularity')    # Etiqueta del eje Y
plt.title('Circularity Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()

# %%%%%%%%% AED %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='AED',   # Usar 'Feret' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=blues,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     


# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X
plt.ylabel('Area Equivalent Diameter (nm)')    # Etiqueta del eje Y
plt.title('Area Equivalent Diameter Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()

# %%%%%%%%% Av Feret %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='AvFeret',   # Usar 'Feret' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=blues,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     


# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X
plt.ylabel('AverageFeret')    # Etiqueta del eje Y
plt.title('Average Feret Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()

# %%%%%%%%% Geometric Diameter %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='GD',   # Usar 'Feret' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=blues,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     


# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X
plt.ylabel('Geometric Diameter')    # Etiqueta del eje Y
plt.title('Geometric Diameter Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()



# %%%%%%%%% Area %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='Area',   # Usar 'Area' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=blues,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     

# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X
plt.ylabel(r'Area ($nm^2$)')    # Etiqueta del eje Y
plt.title('NP Projection Area Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()

# %%%%%%%%% Perimeter %%
# Crear un gráfico de caja con todas las muestras
bplot = sns.boxplot(
    data=df_combined, 
    x='Sample',  # Agrupar por 'Sample' en el eje X
    y='Perim.',   # Usar 'Area' en el eje Y
    showmeans=True, 
    showfliers=False, 
    linewidth=1,
    palette=blues,  # Cambiar la paleta de colores
    meanprops={"marker":"X","markerfacecolor":"blue", "markeredgecolor":"white"}
)
     

# Etiquetas y título del gráfico
plt.xlabel('')  # Etiqueta del eje X
plt.ylabel('Perimeter (nm)')    # Etiqueta del eje Y
plt.title(' NP Projection Perimeter Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()






# %%%%%%%%% MERGED PLOT Variable%%



# Lista de parámetros que se van a graficar
params = ['Feret', 'MinFeret', 'AED', 'GD']

# Obtener el número de parámetros
num_params = len(params)

# Función para crear una paleta con un número variable de colores
def create_palette(num_colors, base_palette="Blues"):
    """
    Crea una paleta de colores con un número variable de colores basados en una paleta base.

    :param num_colors: Número de colores a generar.
    :param base_palette: Nombre de la paleta base de Seaborn. Por defecto es 'Blues'.
    :return: Paleta de colores con el número especificado de colores.
    """
    return sns.color_palette(base_palette, num_colors)

# Crear la paleta de colores basada en el número de parámetros
custom_palette = create_palette(num_params, base_palette="Blues")

# Reordenar el DataFrame en formato largo (long format)
df_melted = pd.melt(df_combined, id_vars='Sample', 
                    value_vars=params,  # Aquí se usa la lista `params`
                    var_name='Measurement', value_name='Value')

# Crear un gráfico boxplot único con todos los parámetros y muestras
plt.figure(figsize=(14, 8))  # Ajusta el tamaño del gráfico

# Crear el gráfico boxplot
sns.boxplot(x='Sample', y='Value', hue='Measurement', data=df_melted, 
            showfliers=False, palette=custom_palette)

# Ajustes del gráfico
plt.title('Parameters Distribution Across Samples')
plt.xlabel('')  # Eliminar la etiqueta del eje X
plt.ylabel('Value (nm)')  # Etiqueta del eje Y
plt.legend(title='Measurement')
plt.xticks(rotation=0)  # Rotar etiquetas si es necesario
plt.ylim(0)  # Fijar el límite inferior del eje Y a 0, si se desea

# Construir el nombre del archivo con los parámetros
params_str = '_'.join(params)  # Unir los parámetros con guiones bajos
file_name = f'Parameters_Distribution_{params_str}.png'

# Guardar el gráfico en un archivo PNG con el nombre dinámico
plt.savefig(file_name)
plt.show()  # Mostrar el gráfico

print(f"Gráfico guardado como {file_name}")



# %%%%%%%%% MERGED PLOT Variable orange%%


# Lista de parámetros que se van a graficar
params = ['Circ.', 'Round']

# Obtener el número de parámetros
num_params = len(params)

# Función para crear una paleta con un número variable de colores
def create_palette(num_colors, base_palette="Oranges"):
    """
    Crea una paleta de colores con un número variable de colores basados en una paleta base.

    :param num_colors: Número de colores a generar.
    :param base_palette: Nombre de la paleta base de Seaborn. Por defecto es 'Blues'.
    :return: Paleta de colores con el número especificado de colores.
    """
    return sns.color_palette(base_palette, num_colors)

# Crear la paleta de colores basada en el número de parámetros
custom_palette = create_palette(num_params, base_palette="Oranges")

# Reordenar el DataFrame en formato largo (long format)
df_melted = pd.melt(df_combined, id_vars='Sample', 
                    value_vars=params,  # Aquí se usa la lista `params`
                    var_name='Measurement', value_name='Value')
# Crear un gráfico boxplot único con todos los parámetros y muestras
plt.figure(figsize=(14, 8))  # Ajusta el tamaño del gráfico
# Crear el gráfico boxplot
sns.boxplot(x='Sample', y='Value', hue='Measurement', data=df_melted, 
            showfliers=False, palette=custom_palette)

# Ajustes del gráfico
plt.title('Parameters Distribution Across Samples', fontsize=25)
plt.xlabel('')  # Eliminar la etiqueta del eje X
plt.ylabel('', fontsize=20)  # Etiqueta del eje Y
plt.legend(title='Measurement')
plt.xticks(rotation=0)  # Rotar etiquetas si es necesario
plt.ylim(0)  # Fijar el límite inferior del eje Y a 0, si se desea

# Construir el nombre del archivo con los parámetros
params_str = '_'.join(params)  # Unir los parámetros con guiones bajos
file_name = f'Parameters_Distribution_{params_str}.png'

# Guardar el gráfico en un archivo PNG con el nombre dinámico
plt.savefig(file_name)
plt.show()  # Mostrar el gráfico

print(f"Gráfico guardado como {file_name}")

############################################↓


# %%%%%%%% STADISTICOS ················
######################################



# Transformar el DataFrame en formato largo
df_melted = pd.melt(df_combined, id_vars='Sample', 
                    value_vars=['Area'],  # Escoge el parámetro a comparar (e.g., 'AvFeret')
                    var_name='Measurement', value_name='Value')

print(df_melted.head())  # Verifica el DataFrame

# Agrupar los datos por muestra (Sample)
all_data = [group['Value'].values for name, group in df_melted.groupby('Sample')]

# Realizar la prueba de Kruskal-Wallis
kruskal_result = kruskal(*all_data)
print(f"Kruskal-Wallis H-Statistic: {kruskal_result.statistic}, p-value: {kruskal_result.pvalue}")

# Si el p-valor es significativo (<0.05), realizar el análisis post-hoc de Dunn
if kruskal_result.pvalue < 0.05:
    print("Prueba de Kruskal-Wallis significativa. Realizando análisis post-hoc (Dunn's test)...")
    
    # Realizar Dunn's test con corrección de Bonferroni
    dunn_result = sp.posthoc_dunn(df_melted, val_col='Value', group_col='Sample', p_adjust='bonferroni')
    print(dunn_result)
    
    # Si quieres guardar la tabla de resultados:
    dunn_result.to_csv('Dunn_posthoc_result_AvFeret.csv', index=True)  # Guardar los resultados
else:
    print("La prueba de Kruskal-Wallis no es significativa. No se realiza el análisis post-hoc.")



# %%%%%%%% STADISTICOS ·····plot····
######################################



# Crear un heatmap para visualizar los valores p
plt.figure(figsize=(10, 8))
ax = sns.heatmap(dunn_result, annot=True, fmt=".2e", cmap="coolwarm", cbar_kws={'label': 'p-value'})
plt.title('Post-hoc Dunn\'s test (p-values)')
plt.xlabel('Samples')
plt.ylabel('Samples')

# Mostrar el heatmap
plt.show()




