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

            # Verificar si cumple el patrón correcto
            match = re.search(r'OT_(\d+)_INFORME', archivo)
            if not match:
                # Si no cumple, moverlo y continuar
                origen = os.path.join(carpeta_entrada, archivo)
                destino = os.path.join(carpeta_errores, archivo)
                try:
                    shutil.move(origen, destino)
                    archivos_no_validos.append(archivo)
                    print(f"❌ Formato inválido, movido: {archivo}")
                except Exception as e:
                    print(f"❌ Error al mover {archivo}: {e}")
                continue

            # Si cumple, proceder a convertir
            ruta_docx = os.path.join(carpeta_entrada, archivo)
            nombre_sin_ext = os.path.splitext(archivo)[0]
            ruta_pdf = os.path.join(carpeta_salida, nombre_sin_ext + ".pdf")

            print(f"Convirtiendo: {archivo} → {ruta_pdf}")
            try:
                doc = word.Documents.Open(ruta_docx)
                doc.SaveAs(ruta_pdf, FileFormat=17)
                doc.Close()
                total_convertidos += 1
                numeros_ot.add(match.group(1))
            except Exception as e:
                print(f"❌ Error al convertir los  {archivo}: {e}")

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
    else:
        print("\n✅ Todos los archivos tenían el formato correcto.")

    print("\n📊 RESUMEN:")
    print(f" - Total de archivos .docx encontrados: {total_archivos_docx}")
    print(f" - Archivos convertidos exitosamente: {total_convertidos}")
    print(f" - Archivos con nombre inválido y movidos: {len(archivos_no_validos)}")

# Rutas
carpeta_entrada = r"C:\Users\CamiloAmaya\Documents\Nexxo_word" #CARPETA DONDE SUBIR LOS DOCUMENTOS EN FORMATO WORD
carpeta_salida = r"C:\Users\CamiloAmaya\OneDrive - Glenfarne Companies\Documentos\Camilo\Prueba_just_pdfs" #CARPETA DONDE APARECERAN LOS DOCUMENTOS COMPARTIDOS EN PDF
archivo_txt_salida = r"C:\Users\CamiloAmaya\Documents\numeros_OT.txt" #ARCHIVO .TXT QUE SE MODIFICARA CON LA LISTA DE LOS TASK
carpeta_errores = r"C:\Users\CamiloAmaya\Documents\Nexxo_mal_formato" #CARPETA DONDE MOVERA TODOS LOS ARCHIVOS MAL NOMBRADOS Y DEBERAS CORREGIRLOS PARA PASARALOS DE NUEVO POR EL PROGRAMA

convertir_docx_a_pdf_y_extraer_numeros(carpeta_entrada, carpeta_salida, archivo_txt_salida, carpeta_errores)
