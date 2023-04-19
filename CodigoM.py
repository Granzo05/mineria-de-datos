import pandas as pd

# Crear un DataFrame con los datos de los empleados
data = {'Empleado': ['Empleado1', 'Empleado2', 'Empleado3', 'Empleado4', 'Empleado5'],
        'Horas de trabajo': [40, 35, 38, 42, 37],
        'Asistencia': [5, 4, 5, 3, 5],
        'Productos vendidos': [10, 8, 12, 6, 11]}
df = pd.DataFrame(data)

# Calcular el rendimiento laboral
df['Rendimiento'] = df['Horas de trabajo'] * 0.5 + df['Asistencia'] * 1.5 + df['Productos vendidos'] * 2

# Ordenar los resultados en orden ascendente por rendimiento
df = df.sort_values(by='Rendimiento', ascending=True)

# Mostrar los resultados
print(df)