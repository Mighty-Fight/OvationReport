import os
import re
import shutil
import win32com.client
from collections import Counter

def convertir_docx_a_pdf_y_extraer_numeros(carpeta_entrada, carpeta_salida, archivo_txt_salida, carpeta_errores, carpeta_repetidos):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    os.makedirs(carpeta_salida, exist_ok=True)
    os.makedirs(carpeta_errores, exist_ok=True)
    os.makedirs(carpeta_repetidos, exist_ok=True)

    numeros_ot = set()
    archivos_no_validos = []
    archivos_repetidos = []
    total_archivos_docx = 0
    total_convertidos = 0

    # --- Primer barrido: contar OTs ---
    lista_ot = []
    for archivo in os.listdir(carpeta_entrada):
        if archivo.endswith(".docx") and not archivo.startswith("~$"):
            match = re.search(r'OT_(\d+)_INFORME', archivo)
            if match:
                lista_ot.append(match.group(1))

    conteo_ot = Counter(lista_ot)
    ot_repetidos = {ot for ot, count in conteo_ot.items() if count > 1}

    # --- Segundo barrido: procesar archivos ---
    for archivo in os.listdir(carpeta_entrada):
        if archivo.endswith(".docx") and not archivo.startswith("~$"):
            total_archivos_docx += 1
            origen = os.path.join(carpeta_entrada, archivo)

            match = re.search(r'OT_(\d+)_INFORME', archivo)
            if not match:
                # Formato inválido → mover a carpeta de errores
                destino = os.path.join(carpeta_errores, archivo)
                if os.path.exists(origen):
                    shutil.move(origen, destino)
                    archivos_no_validos.append(archivo)
                    print(f"❌ Formato inválido, movido: {archivo}")
                continue

            ot_num = match.group(1)

            # Si el OT está repetido → mover a carpeta REPETIDOS
            if ot_num in ot_repetidos:
                destino = os.path.join(carpeta_repetidos, archivo)
                if os.path.exists(origen):
                    shutil.move(origen, destino)
                    archivos_repetidos.append(archivo)
                    print(f"♻️ Movido a repetidos: {archivo}")
                continue

            # Si es válido y único → convertir a PDF
            ruta_pdf = os.path.join(carpeta_salida, os.path.splitext(archivo)[0] + ".pdf")
            print(f"Convirtiendo: {archivo} → {ruta_pdf}")
            try:
                doc = word.Documents.Open(origen)
                doc.SaveAs(ruta_pdf, FileFormat=17)
                doc.Close()
                total_convertidos += 1
                numeros_ot.add(ot_num)
            except Exception as e:
                print(f"❌ Error al convertir {archivo}: {e}")

    word.Quit()

    # Guardar la cadena formateada
    numeros_ordenados = sorted(numeros_ot)
    cadena_formateada = ' OR '.join(f'"{num}"' for num in numeros_ordenados)
    with open(archivo_txt_salida, 'w', encoding='utf-8') as f:
        f.write(cadena_formateada)

    # Resultados
    print("\n✅ Números de OT exportados a archivo:")
    print(archivo_txt_salida)

    if archivos_no_validos:
        print("\n⚠️ Archivos con nombre inválido movidos a carpeta de mal formato:")
        for archivo in archivos_no_validos:
            print(f" - {archivo}")

    if archivos_repetidos:
        print("\n⚠️ Archivos movidos a carpeta de repetidos:")
        for archivo in archivos_repetidos:
            print(f" - {archivo}")

    print("\n📊 RESUMEN FINAL:")
    print(f" - Total de archivos .docx encontrados: {total_archivos_docx}")
    print(f" - Archivos convertidos exitosamente: {total_convertidos}")
    print(f" - Archivos con nombre inválido: {len(archivos_no_validos)}")
    print(f" - Archivos repetidos: {len(archivos_repetidos)}")

# Rutas
carpeta_entrada = r"C:\Users\CamiloAmaya\Documents\Nexxo_word"
carpeta_salida = r"C:\Users\CamiloAmaya\Documents\PRUEBA_1"
archivo_txt_salida = r"C:\Users\CamiloAmaya\Documents\numeros_OT.txt"
carpeta_errores = r"C:\Users\CamiloAmaya\Documents\Nexxo_mal_formato"
carpeta_repetidos = r"C:\Users\CamiloAmaya\Documents\REPETIDOS"

convertir_docx_a_pdf_y_extraer_numeros(carpeta_entrada, carpeta_salida, archivo_txt_salida, carpeta_errores, carpeta_repetidos)