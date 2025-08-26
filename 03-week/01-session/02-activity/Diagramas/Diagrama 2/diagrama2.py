import pandas as pd
import matplotlib.pyplot as plt

# Cargar el CSV
df = pd.read_csv('Hearing well-being Survey Report.csv')

# Ejemplo: Diagrama de barras de la cantidad de respuestas por grupo de edad
plt.figure(figsize=(10,6))
df['Age_group'].value_counts().plot(kind='bar')
plt.title('Cantidad de respuestas por grupo de edad')
plt.xlabel('Grupo de edad')
plt.ylabel('Cantidad')

plt.show()