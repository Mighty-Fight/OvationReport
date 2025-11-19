import os
import win32com.client

def convertir_word_a_pdf(carpeta):
    # Inicializar Word
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    # Recorrer archivos en la carpeta
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".docx") and not archivo.startswith("~$"):
            ruta_docx = os.path.join(carpeta, archivo)
            ruta_pdf = os.path.splitext(ruta_docx)[0] + ".pdf"

            try:
                print(f"Convirtiendo: {ruta_docx} → {ruta_pdf}")
                doc = word.Documents.Open(ruta_docx)
                doc.SaveAs(ruta_pdf, FileFormat=17)  # 17 = PDF
                doc.Close()
            except Exception as e:
                print(f"❌ Error al convertir {archivo}: {e}")

    # Cerrar Word
    word.Quit()
    print("✅ Conversión finalizada.")

# Ruta de la carpeta
carpeta_repetidos = r"C:\Users\CamiloAmaya\Documents\Nexxo_mal_formato"

convertir_word_a_pdf(carpeta_repetidos)
