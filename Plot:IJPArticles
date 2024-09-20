# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 19:19:25 2024

@author: JCH
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
sns.set(style="whitegrid")
plt.ion()
# Create an array with the colors you want to use


# Crear paleta de colores azules, de más intenso a pastel
blues = sns.color_palette("Blues", 10)  # Paleta de 10 tonos de azul

# Crear paleta de colores naranjas, de más intenso a pastel
oranges = sns.color_palette("Oranges", 10)  # Paleta de 10 tonos de naranja



# %%%%%%%%% Lectura y generacion %%

#Leemos los ficheros csv
# Lista para almacenar los DataFrames
dataframes = []


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
#
# Lista de columnas para las que queremos calcular las estadísticas
columns = ['AvFeret', 'Feret', 'MinFeret', 'GD', 'AED', 'Area', 'Perim.', 'Round', 'Circ.']

# Diccionario para almacenar los DataFrames de estadísticas por muestra
stats_dfs = {}

# Calcular estadísticas para cada muestra
for nsample in range(1, ns + 1):
    sample_df = df_combined[df_combined['Sample'] == f'Sample {nsample}']
    stats_dict = {'Average': [], 'Median': [], 'Mode': [], 'Std Dev': [], 'Q1': [], 'Q3': []}
    
    for col in columns:
        stats_dict['Average'].append(round(sample_df[col].mean(), 2))
        stats_dict['Median'].append(round(sample_df[col].median(), 2))
        stats_dict['Mode'].append(round(stats.mode(sample_df[col])[0][0], 2))
        stats_dict['Std Dev'].append(round(sample_df[col].std(), 2))
        stats_dict['Q1'].append(round(sample_df[col].quantile(0.25), 2))
        stats_dict['Q3'].append(round(sample_df[col].quantile(0.75), 2))
    
    # Convertir el diccionario en un DataFrame y almacenarlo en el diccionario de DataFrames
    stats_dfs[f'Sample {nsample}'] = pd.DataFrame(stats_dict, index=columns)

# Mostrar las tablas de estadísticas para cada muestra
for sample, stats_df in stats_dfs.items():
    print(f"\nEstadísticas para {sample}:\n", stats_df)


# %%%%%%%%% PLOTS %%

#
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
plt.ylabel('Perimeter (nm)')    # Etiqueta del eje Y
plt.title(' NP Projection Perimeter Distribution')  # Título del gráfico

# Forzar el eje Y a comenzar en 0
plt.ylim(0, None)

# Mostrar gráfico
plt.show()



# %%%%%%%%% MERGED PLOT %%
plt.figure(figsize=(14, 8))  # Ajusta el tamaño del gráfico

# Reordenar el DataFrame en formato largo (long format)
df_melted = pd.melt(df_combined, id_vars='Sample', 
                    value_vars=['AvFeret', 'AED', 'GD'], 
                    var_name='Measurement', value_name='Value')

# Crear un boxplot para las variables
sns.boxplot(x='Sample', y='Value', hue='Measurement', data=df_melted, showfliers=False, palette="Set3")

# Ajustes del gráfico
plt.title('Diameters Distribution')
plt.xlabel('')  # Eliminar la etiqueta del eje X
plt.ylabel('Diameters (nm)')  # Usar LaTeX para formato del eje Y

plt.legend(title='Distributions')
plt.xticks(rotation=45)  # Rotar etiquetas si es necesario
plt.ylim(0)  # Fijar el límite inferior del eje Y a 0, si se desea

plt.show()

