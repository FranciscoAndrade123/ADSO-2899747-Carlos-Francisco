import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle

# Configuración para gráficos más bonitos
plt.style.use('default')
sns.set_palette("husl")

print("=== ANÁLISIS DE DATASETS DE ESTRÉS ===")
print("Cargando datasets...")

# 1. CARGAR LOS DATASETS
try:
    # Intenta cargar ambos datasets
    df1 = pd.read_csv('Stress_Dataset.csv')
    print(f"✓ Stress_Dataset.csv cargado: {df1.shape}")
    
    df2 = pd.read_csv('StressLevelDataset.csv')
    print(f"✓ StressLevelDataset.csv cargado: {df2.shape}")
    
    # Trabajaremos principalmente con el primer dataset
    df = df1.copy()
    
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Asegúrate de que los archivos CSV están en la misma carpeta que este script")
    exit()

# 2. EXPLORACIÓN INICIAL
print("\n" + "="*50)
print("EXPLORACIÓN INICIAL DEL DATASET PRINCIPAL")
print("="*50)

print(f"\n📊 DIMENSIONES: {df.shape[0]} filas, {df.shape[1]} columnas")
print(f"\n📋 COLUMNAS: {list(df.columns)}")

print(f"\n🔍 PRIMERAS 5 FILAS:")
print(df.head())

print(f"\n📈 INFORMACIÓN DE COLUMNAS:")
print(df.info())

print(f"\n📊 ESTADÍSTICAS DESCRIPTIVAS:")
print(df.describe())

# 3. ANÁLISIS DE VALORES NULOS
print(f"\n❌ VALORES NULOS POR COLUMNA:")
null_counts = df.isnull().sum()
print(null_counts[null_counts > 0] if null_counts.sum() > 0 else "¡No hay valores nulos!")

# 4. CREAR VISUALIZACIONES
print("\n" + "="*50)
print("GENERANDO GRÁFICOS...")
print("="*50)

# Figura principal con múltiples subplots
fig = plt.figure(figsize=(20, 15))
fig.suptitle('Análisis Completo del Dataset de Estrés', fontsize=20, fontweight='bold')

# Obtener columnas numéricas y categóricas
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

print(f"Columnas numéricas encontradas: {numeric_cols}")
print(f"Columnas categóricas encontradas: {categorical_cols}")

# GRÁFICO 1: Distribución de la variable objetivo (si existe 'stress_level' o similar)
ax1 = plt.subplot(3, 3, 1)
stress_columns = [col for col in df.columns if 'stress' in col.lower()]
if stress_columns:
    target_col = stress_columns[0]
    if df[target_col].dtype == 'object':
        df[target_col].value_counts().plot(kind='bar', ax=ax1, color='lightcoral')
        ax1.set_title(f'Distribución de {target_col}', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
    else:
        ax1.hist(df[target_col].dropna(), bins=20, color='lightcoral', alpha=0.7, edgecolor='black')
        ax1.set_title(f'Distribución de {target_col}', fontsize=12, fontweight='bold')
    ax1.set_xlabel(target_col)
    ax1.set_ylabel('Frecuencia')
else:
    # Si no hay columna de estrés, usar la primera categórica
    if categorical_cols:
        df[categorical_cols[0]].value_counts().head(10).plot(kind='bar', ax=ax1, color='lightcoral')
        ax1.set_title(f'Distribución de {categorical_cols[0]}', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)

# GRÁFICO 2: Boxplot de variable numérica
ax2 = plt.subplot(3, 3, 2)
if numeric_cols:
    ax2.boxplot(df[numeric_cols[0]].dropna(), patch_artist=True, 
                boxprops=dict(facecolor='skyblue', alpha=0.7))
    ax2.set_title(f'Boxplot de {numeric_cols[0]}', fontsize=12, fontweight='bold')
    ax2.set_ylabel(numeric_cols[0])

# GRÁFICO 3: Correlación entre variables numéricas
ax3 = plt.subplot(3, 3, 3)
if len(numeric_cols) >= 2:
    scatter_x = numeric_cols[0]
    scatter_y = numeric_cols[1]
    ax3.scatter(df[scatter_x], df[scatter_y], alpha=0.6, color='green', s=30)
    ax3.set_title(f'{scatter_x} vs {scatter_y}', fontsize=12, fontweight='bold')
    ax3.set_xlabel(scatter_x)
    ax3.set_ylabel(scatter_y)

# GRÁFICO 4: Histograma de otra variable numérica
ax4 = plt.subplot(3, 3, 4)
if len(numeric_cols) >= 2:
    ax4.hist(df[numeric_cols[1]].dropna(), bins=25, color='orange', alpha=0.7, edgecolor='black')
    ax4.set_title(f'Distribución de {numeric_cols[1]}', fontsize=12, fontweight='bold')
    ax4.set_xlabel(numeric_cols[1])
    ax4.set_ylabel('Frecuencia')

# GRÁFICO 5: Gráfico de barras para variable categórica
ax5 = plt.subplot(3, 3, 5)
if len(categorical_cols) >= 1:
    top_cats = df[categorical_cols[0]].value_counts().head(8)
    bars = ax5.bar(range(len(top_cats)), top_cats.values, color='purple', alpha=0.7)
    ax5.set_title(f'Top categorías: {categorical_cols[0]}', fontsize=12, fontweight='bold')
    ax5.set_xticks(range(len(top_cats)))
    ax5.set_xticklabels(top_cats.index, rotation=45, ha='right')
    ax5.set_ylabel('Frecuencia')

# GRÁFICO 6: Matriz de correlación (si hay suficientes variables numéricas)
ax6 = plt.subplot(3, 3, 6)
if len(numeric_cols) >= 3:
    corr_matrix = df[numeric_cols[:5]].corr()  # Máximo 5 variables para que se vea bien
    im = ax6.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    ax6.set_xticks(range(len(corr_matrix.columns)))
    ax6.set_yticks(range(len(corr_matrix.columns)))
    ax6.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
    ax6.set_yticklabels(corr_matrix.columns)
    ax6.set_title('Matriz de Correlación', fontsize=12, fontweight='bold')
    
    # Agregar valores de correlación
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            ax6.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                    ha='center', va='center', fontsize=8)

# GRÁFICO 7: Análisis temporal (si hay columnas de fecha)
ax7 = plt.subplot(3, 3, 7)
date_cols = df.select_dtypes(include=['datetime64']).columns
if len(date_cols) > 0 or any('date' in col.lower() or 'time' in col.lower() for col in df.columns):
    # Intentar convertir columnas que parezcan fechas
    potential_date_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
    if potential_date_cols:
        try:
            df[potential_date_cols[0]] = pd.to_datetime(df[potential_date_cols[0]])
            df.groupby(df[potential_date_cols[0]].dt.date).size().plot(ax=ax7, color='red')
            ax7.set_title('Tendencia Temporal', fontsize=12, fontweight='bold')
            ax7.tick_params(axis='x', rotation=45)
        except:
            ax7.text(0.5, 0.5, 'No se pudo procesar\nla columna temporal', 
                    ha='center', va='center', transform=ax7.transAxes)
            ax7.set_title('Análisis Temporal', fontsize=12, fontweight='bold')
else:
    if len(numeric_cols) >= 3:
        ax7.plot(df.index, df[numeric_cols[2]], color='red', linewidth=2)
        ax7.set_title(f'Tendencia: {numeric_cols[2]}', fontsize=12, fontweight='bold')
        ax7.set_xlabel('Índice')
        ax7.set_ylabel(numeric_cols[2])

# GRÁFICO 8: Comparación entre grupos (si hay variable categórica y numérica)
ax8 = plt.subplot(3, 3, 8)
if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
    # Crear boxplot agrupado
    categories = df[categorical_cols[0]].value_counts().head(5).index
    data_for_box = [df[df[categorical_cols[0]] == cat][numeric_cols[0]].dropna() for cat in categories]
    
    if all(len(data) > 0 for data in data_for_box):
        box_plot = ax8.boxplot(data_for_box, labels=categories, patch_artist=True)
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
        ax8.set_title(f'{numeric_cols[0]} por {categorical_cols[0]}', fontsize=12, fontweight='bold')
        ax8.tick_params(axis='x', rotation=45)

# GRÁFICO 9: Pie chart para variable categórica
ax9 = plt.subplot(3, 3, 9)
if len(categorical_cols) >= 1:
    pie_data = df[categorical_cols[0]].value_counts().head(6)
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(pie_data)))
    wedges, texts, autotexts = ax9.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%', 
                                      colors=colors, startangle=90)
    ax9.set_title(f'Proporción: {categorical_cols[0]}', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

# 5. ANÁLISIS ESPECÍFICO PARA DATASETS DE ESTRÉS
print("\n" + "="*50)
print("ANÁLISIS ESPECÍFICO DE ESTRÉS")
print("="*50)

# Buscar patrones específicos de estrés
stress_related_cols = [col for col in df.columns if any(keyword in col.lower() 
                      for keyword in ['stress', 'anxiety', 'sleep', 'heart', 'pressure', 'mental'])]

if stress_related_cols:
    print(f"Columnas relacionadas con estrés encontradas: {stress_related_cols}")
    
    # Crear gráfico específico para variables de estrés
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análisis Específico de Variables de Estrés', fontsize=16, fontweight='bold')
    
    for i, col in enumerate(stress_related_cols[:4]):  # Máximo 4 gráficos
        row = i // 2
        col_idx = i % 2
        
        if df[col].dtype == 'object':
            df[col].value_counts().plot(kind='bar', ax=axes[row, col_idx], color=f'C{i}')
        else:
            axes[row, col_idx].hist(df[col].dropna(), bins=20, color=f'C{i}', alpha=0.7)
        
        axes[row, col_idx].set_title(f'Distribución de {col}', fontweight='bold')
        axes[row, col_idx].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

# 6. RESUMEN Y RECOMENDACIONES
print("\n" + "="*50)
print("RESUMEN DEL ANÁLISIS")
print("="*50)

print(f"📊 Dataset principal: {df.shape[0]} filas, {df.shape[1]} columnas")
print(f"🔢 Variables numéricas: {len(numeric_cols)}")
print(f"📝 Variables categóricas: {len(categorical_cols)}")
print(f"❌ Valores nulos: {df.isnull().sum().sum()}")

if stress_related_cols:
    print(f"🧠 Variables relacionadas con estrés: {len(stress_related_cols)}")

print("\n💡 SUGERENCIAS PARA ANÁLISIS ADICIONAL:")
print("- Analizar correlaciones entre factores de estrés")
print("- Crear modelos predictivos de niveles de estrés")
print("- Segmentar usuarios por niveles de estrés")
print("- Analizar patrones temporales si hay datos de fecha")

print("\n✅ ¡Análisis completado! Revisa todos los gráficos generados.")