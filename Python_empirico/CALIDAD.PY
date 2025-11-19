from openpyxl import load_workbook

# Ruta del archivo Excel
ruta_excel = r"C:\Users\CamiloAmaya\OneDrive - Glenfarne Companies\CALIDAD.xlsx"

def coincidir_datos():
    print("=== INICIANDO COMPARACIÓN ENTRE HOJAS ===")

    try:
        # Cargar el archivo Excel
        wb = load_workbook(ruta_excel)
        hoja1 = wb["Tasks"]
        hoja2 = wb["Hoja2"]

        # --- Crear diccionario con los valores de Hoja2 ---
        # clave = columna A, valores = columnas H e I
        datos_hoja2 = {}
        for fila in range(2, hoja2.max_row + 1):
            clave = hoja2[f"A{fila}"].value
            if clave:
                valor_H = hoja2[f"H{fila}"].value  # columna H
                valor_I = hoja2[f"I{fila}"].value  # columna I
                datos_hoja2[str(clave)] = (valor_H, valor_I)

        print(f"📋 Datos cargados de Hoja2: {len(datos_hoja2)} registros.")

        # --- Recorrer Hoja1 y buscar coincidencias ---
        coincidencias = 0
        for fila in range(2, hoja1.max_row + 1):
            clave_hoja1 = hoja1[f"B{fila}"].value
            if clave_hoja1 and str(clave_hoja1) in datos_hoja2:
                valor_H, valor_I = datos_hoja2[str(clave_hoja1)]
                # Copiar columna I de Hoja2 → columna G de Hoja1
                hoja1[f"G{fila}"].value = valor_I
                # Copiar columna H de Hoja2 → columna I de Hoja1
                hoja1[f"I{fila}"].value = valor_H
                coincidencias += 1

        # --- Guardar cambios ---
        wb.save(ruta_excel)
        print(f"\n✅ Coincidencias encontradas: {coincidencias}")
        print(f"📘 Archivo actualizado correctamente: {ruta_excel}")

    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")

if __name__ == "__main__":
    coincidir_datos()


    ##HOLA!!!!!!!!!!!!!!!!!!
