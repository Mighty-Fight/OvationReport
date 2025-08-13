import os
import re
import shutil
import win32com.client

def convertir_docx_a_pdf_y_extraer_numeros(carpeta_entrada, carpeta_salida, archivo_txt_salida, carpeta_errores):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    os.makedirs(carpeta_salida, exist_ok=True)
    os.makedirs(carpeta_errores, exist_ok=True)

    numeros_ot = set()
    archivos_no_validos = []
    total_archivos_docx = 0
    total_convertidos = 0

    for archivo in os.listdir(carpeta_entrada):
        if archivo.endswith(".docx") and not archivo.startswith("~$"):
            total_archivos_docx += 1
            ruta_docx = os.path.join(carpeta_entrada, archivo)
            nombre_sin_ext = os.path.splitext(archivo)[0]
            ruta_pdf = os.path.join(carpeta_salida, nombre_sin_ext + ".pdf")

            # Buscar número de OT válido
            match_ot = re.search(r'OT_(\d{6})_INFORME', archivo)
            match_simple = re.search(r'C_(\d{6})_INFORME', archivo)
            match_w = re.search(r'W_(\d{6})_INFORME', archivo)
            numero_ot = match_ot.group(1) if match_ot else (match_simple.group(1) if match_simple else (match_w.group(1) if match_w else None))

            if not numero_ot:
                # Mover archivo a carpeta de errores
                destino_error = os.path.join(carpeta_errores, archivo)
                try:
                    shutil.move(ruta_docx, destino_error)
                    archivos_no_validos.append(archivo)
                    print(f"❌ Formato inválido, movido: {archivo}")
                except Exception as e:
                    print(f"❌ Error al mover {archivo}: {e}")
                continue

            # Convertir a PDF
            print(f"✅ Convirtiendo: {archivo} → {ruta_pdf}")
            try:
                doc = word.Documents.Open(ruta_docx)
                doc.SaveAs(ruta_pdf, FileFormat=17)
                doc.Close()
                total_convertidos += 1
                numeros_ot.add(numero_ot)
            except Exception as e:
                print(f"❌ Error al convertir {archivo}: {e}")

    word.Quit()

    # Guardar cadena de números OT
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
    else:
        print("\n✅ Todos los archivos tenían el formato correcto.")

    print("\n📊 RESUMEN:")
    print(f" - Total de archivos .docx encontrados: {total_archivos_docx}")
    print(f" - Archivos convertidos exitosamente: {total_convertidos}")
    print(f" - Archivos con nombre inválido y movidos: {len(archivos_no_validos)}")

# Rutas
carpeta_entrada = r"C:\Users\CamiloAmaya\Documents\Nexxo_word_prueba"
carpeta_salida = r"C:\Users\CamiloAmaya\Documents\Camilo\Prueba_flujo_nexxo_prueba"
archivo_txt_salida = r"C:\Users\CamiloAmaya\Documents\numeros_OT.txt_prueba"
carpeta_errores = r"C:\Users\CamiloAmaya\Documents\Nexxo_mal_formato"

convertir_docx_a_pdf_y_extraer_numeros(carpeta_entrada, carpeta_salida, archivo_txt_salida, carpeta_errores)
