import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import silhouette_score

# --- 1. Carga y Preprocesamiento de Datos ---
# Especifica la ruta a tu archivo si es diferente
file_path = 'Datos Burnout.csv'
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: El archivo '{file_path}' no fue encontrado. Asegúrate de que el archivo está en la ubicación correcta.")
    exit()

original_row_count = len(df)
print(f"Filas originales en el dataset: {original_row_count}")

# Renombrar columnas para facilitar el manejo
# Asumiendo que la primera columna es 'Individuo' y las siguientes 22 son las preguntas del MBI
expected_num_cols = 23 # 1 para Individuo + 22 para preguntas MBI
if len(df.columns) == expected_num_cols:
    new_cols = ['Individuo'] + [f'Q{i}' for i in range(1, expected_num_cols)]
    df.columns = new_cols
    print("Columnas renombradas exitosamente.")
else:
    print(f"Advertencia: El número de columnas ({len(df.columns)}) no coincide con el esperado ({expected_num_cols}). No se renombrarán las columnas o se procederá con precaución.")

# Manejo de valores faltantes (eliminación simple)
df.dropna(inplace=True)
rows_after_na_initial = len(df)
rows_dropped_initial = original_row_count - rows_after_na_initial
print(f"Filas después de la eliminación inicial de NAs: {rows_after_na_initial} (se eliminaron {rows_dropped_initial} filas).")

# Mapeo de respuestas categóricas a numéricas
# Asegúrate de que estas respuestas coincidan exactamente con las de tu dataset
ordered_responses = [
    "Nunca",
    "Pocas veces al año o menos",
    "Unas pocas veces al año",
    "Una vez al mes o menos",
    "Una vez a la semana",
    "Pocas veces a la semana",
    "Todos los días"
]
score_mapping_ordered = {response: i for i, response in enumerate(ordered_responses)}

# Aplicar mapeo a las columnas de preguntas (Q1 a Q22)
# Solo intentar mapear si las columnas fueron renombradas y existen
question_cols_to_map = [f'Q{i}' for i in range(1, expected_num_cols)] if 'Individuo' in new_cols else []

for col in question_cols_to_map:
    if col in df.columns:
        # Convertir toda la columna a string primero para asegurar que el mapeo funcione bien con tipos mixtos
        df[col] = df[col].astype(str).map(score_mapping_ordered)
        # Verificar si quedaron NAs después del mapeo (indicando respuestas no esperadas)
        if df[col].isnull().any():
            print(f"Advertencia: La columna '{col}' contiene valores NA después del mapeo. Esto puede indicar respuestas no contempladas en 'ordered_responses'.")
            # Opcional: Imputar NAs o manejarlos de otra forma. Por ahora, se eliminarán más adelante.
    else:
        print(f"Advertencia: La columna de pregunta esperada '{col}' no fue encontrada para el mapeo.")


# Definición de las escalas del MBI (basado en los nombres renombrados Q1-Q22)
ee_items = [f'Q{i}' for i in range(1, 10)]    # Preguntas de Agotamiento Emocional (9 items)
pa_items = [f'Q{i}' for i in range(10, 18)]   # Preguntas de Realización Personal (8 items)
dp_items = [f'Q{i}' for i in range(18, 23)]   # Preguntas de Despersonalización (5 items)

# Filtrar ítems para asegurar que solo se usen columnas presentes y válidas
ee_items_present = [item for item in ee_items if item in df.columns and df[item].notna().all()]
pa_items_present = [item for item in pa_items if item in df.columns and df[item].notna().all()]
dp_items_present = [item for item in dp_items if item in df.columns and df[item].notna().all()]

# Cálculo de las puntuaciones de las escalas MBI
# Solo calcular si hay ítems presentes para cada escala
df['EE_Score'] = df[ee_items_present].sum(axis=1) if ee_items_present else pd.NA
df['PA_Score'] = df[pa_items_present].sum(axis=1) if pa_items_present else pd.NA
df['DP_Score'] = df[dp_items_present].sum(axis=1) if dp_items_present else pd.NA

# Eliminar filas donde no se pudieron calcular las puntuaciones MBI (si alguna es NA)
df.dropna(subset=['EE_Score', 'PA_Score', 'DP_Score'], inplace=True)
rows_for_clustering = len(df)
print(f"Filas finales disponibles para clustering: {rows_for_clustering}.")

if rows_for_clustering < 2: # Necesitamos al menos 2 muestras para clustering
    print("Error: No hay suficientes datos después del preprocesamiento para realizar el clustering.")
    exit()

# --- 2. Selección y Escalado de Características ---
features_for_clustering = ['EE_Score', 'PA_Score', 'DP_Score']
X = df[features_for_clustering].copy()

# Escalar las características (estandarización)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=features_for_clustering, index=X.index)

print("\n--- Primeras 5 filas de datos escalados para clustering ---")
print(X_scaled_df.head())

# --- 3. Realización del Clustering Jerárquico ---
print("\n--- Realizando Clustering Jerárquico (Método de Ward) ---")
# Se usa 'ward' para minimizar la varianza dentro de cada clúster
# Se usa 'euclidean' como métrica de distancia
linked = linkage(X_scaled_df, method='ward', metric='euclidean')

# --- 4. Visualización del Dendrograma ---
plt.figure(figsize=(18, 9)) # Aumentado el tamaño para mejor visualización
dendrogram(linked,
            orientation='top',
            distance_sort='descending',
            show_leaf_counts=True,
            truncate_mode='lastp',  # Muestra solo los últimos 'p' clústeres fusionados
            p=30,                   # Número de los últimos clústeres fusionados a mostrar
            leaf_rotation=90.,      # Rota las etiquetas de las hojas
            leaf_font_size=8.)      # Tamaño de fuente para las etiquetas
plt.title('Dendrograma del Clustering Jerárquico (Método de Ward, truncado para p=30)', fontsize=16)
plt.xlabel("Índice de la Muestra o (Tamaño del Clúster)", fontsize=12)
plt.ylabel("Distancia de Ward (Euclidiana)", fontsize=12)
# plt.axhline(y=15, color='r', linestyle='--', label='Posible corte (ej: y=15)') # Ejemplo de línea de corte
# plt.legend()
plt.tight_layout() # Ajustar layout para que no se corten las etiquetas
plt.savefig("hierarchical_clustering_dendrogram.png")
plt.close() # Cerrar la figura para liberar memoria
print("Dendrograma guardado como 'hierarchical_clustering_dendrogram.png'")
print("El dendrograma ayuda a decidir el número de clústeres. Inspecciona los saltos verticales más grandes.")

# --- 5. Determinación del Número de Clústeres y Extracción de Etiquetas ---
# Esta es una elección que puede basarse en el dendrograma o en métricas como el coeficiente de silueta.
# Como ejemplo, se elegirán 3 clústeres.
num_clusters_chosen = 3
print(f"\n--- Extrayendo {num_clusters_chosen} Clústeres del Dendrograma ---")
# 'maxclust' es el criterio para formar un número fijo de clústeres
df['Cluster_Labels_Hierarchical'] = fcluster(linked, num_clusters_chosen, criterion='maxclust')

# --- 6. Análisis e Interpretación de los Clústeres ---
print(f"\n--- Análisis de los {num_clusters_chosen} Clústeres Identificados ---")
# Calcular las medias de las puntuaciones MBI *originales* (no escaladas) para cada clúster
cluster_analysis_hierarchical = df.groupby('Cluster_Labels_Hierarchical')[features_for_clustering].mean().round(2)
cluster_analysis_hierarchical['N_Individuals'] = df['Cluster_Labels_Hierarchical'].value_counts().sort_index()
print(cluster_analysis_hierarchical)

print("\n--- Interpretación Tentativa de los Clústeres ---")
for i in range(1, num_clusters_chosen + 1):
    if i in cluster_analysis_hierarchical.index:
        cluster_data = cluster_analysis_hierarchical.loc[i]
        profile = []
        # Comparar con las medias generales para una interpretación simple
        if cluster_data['EE_Score'] > X['EE_Score'].mean() * 1.25 : profile.append("EE Alto") # Umbral ejemplo
        elif cluster_data['EE_Score'] < X['EE_Score'].mean() * 0.75: profile.append("EE Bajo")
        else: profile.append("EE Moderado")

        if cluster_data['PA_Score'] > X['PA_Score'].mean() * 1.05: profile.append("PA Alto") # PA es positivo
        elif cluster_data['PA_Score'] < X['PA_Score'].mean() * 0.95: profile.append("PA Bajo")
        else: profile.append("PA Moderado")

        if cluster_data['DP_Score'] > X['DP_Score'].mean() * 1.25: profile.append("DP Alto")
        elif cluster_data['DP_Score'] < X['DP_Score'].mean() * 0.75: profile.append("DP Bajo")
        else: profile.append("DP Moderado")

        print(f"  Clúster {i} (N={cluster_data['N_Individuals']:.0f}): "
              f"EE Medio: {cluster_data['EE_Score']}, PA Medio: {cluster_data['PA_Score']}, DP Medio: {cluster_data['DP_Score']}. "
              f"Perfil: {', '.join(profile)}")
    else:
        print(f"  Clúster {i}: No se encontraron individuos (esto no debería ocurrir si se formaron {num_clusters_chosen} clústeres).")


# --- 7. Evaluación de la Calidad de los Clústeres (Coeficiente de Silueta) ---
# Se puede calcular si 1 < num_clusters < n_samples
if 1 < num_clusters_chosen < len(X_scaled_df):
    silhouette_avg_hierarchical = silhouette_score(X_scaled_df, df['Cluster_Labels_Hierarchical'])
    print(f"\nCoeficiente de Silueta para {num_clusters_chosen} clústeres (Jerárquico): {silhouette_avg_hierarchical:.3f}")
    print(" (Valores más cercanos a 1 indican mejor definición y separación de clústeres)")
else:
    print(f"\nNo se puede calcular el coeficiente de silueta para {num_clusters_chosen} clústeres con {len(X_scaled_df)} muestras.")

# --- 8. Visualización de los Clústeres (Ejemplo: Pairplot) ---
# Asegurarse de que hay clústeres para graficar
if 'Cluster_Labels_Hierarchical' in df.columns and df['Cluster_Labels_Hierarchical'].nunique() > 0:
    cluster_plot_df = df[features_for_clustering + ['Cluster_Labels_Hierarchical']].copy()
    # Convertir etiquetas a tipo 'category' para colores discretos en seaborn
    cluster_plot_df['Cluster_Labels_Hierarchical'] = cluster_plot_df['Cluster_Labels_Hierarchical'].astype('category')

    print("\n--- Generando Pairplot de los Clústeres ---")
    plt.figure() # Crear una nueva figura para el pairplot
    pairplot_fig = sns.pairplot(cluster_plot_df, hue='Cluster_Labels_Hierarchical', palette='viridis', diag_kind='kde')
    pairplot_fig.fig.suptitle(f"Pairplot de Dimensiones MBI por Clúster Jerárquico (k={num_clusters_chosen})", y=1.02) # Ajustar título
    plt.savefig("hierarchical_clusters_pairplot.png")
    plt.close() # Cerrar la figura del pairplot
    print("Pairplot de los clústeres guardado como 'hierarchical_clusters_pairplot.png'")
else:
    print("\nNo se generó el pairplot porque no se formaron clústeres o las etiquetas no están disponibles.")


# --- 9. Guardado de Resultados ---
# Guardar el DataFrame con las etiquetas de clúster asignadas
output_filename = "datos_burnout_con_clusters_jerarquicos.csv"
df.to_csv(output_filename, index=False)
print(f"\nDataset con etiquetas de clúster jerárquico guardado como '{output_filename}'")

print("\n--- Script de Clustering Jerárquico Finalizado ---")