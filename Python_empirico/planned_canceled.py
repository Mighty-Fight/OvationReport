import pandas as pd

# Ruta del archivo Excel (el que tiene ambas hojas)
archivo = r"C:\Users\CamiloAmaya\Downloads\ArchivoComparacion.xlsx"

# Cargar ambas hojas
hoja1 = pd.read_excel(archivo, sheet_name="Hoja1")
hoja2 = pd.read_excel(archivo, sheet_name="Hoja2")

# Tomar columnas de comparación
columna_hoja1 = hoja1.iloc[:, 3]  # Columna D (índice 3)
columna_hoja2 = hoja2.iloc[:, 0]  # Columna A (índice 0)

# Convertir a texto y limpiar espacios (importante para coincidencias reales)
columna_hoja1 = columna_hoja1.astype(str).str.strip()
columna_hoja2 = columna_hoja2.astype(str).str.strip()

# Filtrar las filas de Hoja2 cuya columna A esté presente en la columna D de Hoja1
coincidencias = hoja2[hoja2.iloc[:, 0].isin(columna_hoja1)]

# Mostrar cantidad de coincidencias encontradas
print(f"🔍 Se encontraron {len(coincidencias)} coincidencias.")

# Guardar las coincidencias en una nueva hoja del mismo archivo
with pd.ExcelWriter(archivo, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    coincidencias.to_excel(writer, sheet_name="Coincidencias", index=False)

print("✅ Coincidencias guardadas en la hoja 'Coincidencias'.")
