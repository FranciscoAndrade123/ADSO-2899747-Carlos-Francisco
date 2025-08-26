import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV
df = pd.read_csv('youtube_data.csv')

# Contar la cantidad de videos por categoría
categoria_counts = df['category'].value_counts()

# Crear el diagrama de pastel
plt.figure(figsize=(8,8))
plt.pie(categoria_counts, labels=categoria_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribución de videos por categoría')
plt.axis('equal')  # Para que el gráfico sea circular
plt.tight_layout()
plt.show()