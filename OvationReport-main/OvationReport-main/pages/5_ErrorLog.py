import streamlit as st
import pandas as pd
from annotated_text import annotated_text
from datetime import datetime
import os
import csv
import tempfile

st.title('Chequeo Ovation DCS')

# Función para probar la escritura en una carpeta
def test_write_access(folder):
    try:
        test_file = os.path.join(folder, 'test_write.txt')
        with open(test_file, 'w') as f:
            f.write('Test')
        os.remove(test_file)
        return True
    except Exception:
        return False

# Intentar usar la carpeta Documents, luego Descargas, y finalmente una carpeta temporal
documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

if test_write_access(documents_folder):
    csv_folder = documents_folder
    st.success("Usando la carpeta Documents.")
elif test_write_access(downloads_folder):
    csv_folder = downloads_folder
    st.success("Usando la carpeta Descargas.")
else:
    csv_folder = tempfile.gettempdir()
    st.warning("Usando carpeta temporal debido a problemas de permisos.")

# Definir el nombre del archivo CSV
csv_filename = 'ovation_dcs_errors.csv'
csv_file = os.path.join(csv_folder, csv_filename)

st.markdown("Ventana :red-background[Error Log] ")
form = st.form(key='my-form')

txt = form.text_area(
    "Anote las anomalías encontradas en la ventana de Error Log",
)
submit = form.form_submit_button('Submit')

if submit:
    st.balloons()
    st.write('¡Ha finalizado exitosamente el chequeo al DCS Ovation!')
    
    # Obtener la fecha y hora actual
    current_datetime = datetime.now().strftime("%Y-%m-%d")
    
    # Preparar los datos para guardar en CSV
    data = {
        'Fecha': [current_datetime],
        'Error': [txt]
    }
    
    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)
    
    # Verificar si el archivo ya existe
    file_exists = os.path.isfile(csv_file)
    
    # Guardar los datos en el archivo CSV
    df.to_csv(csv_file, mode='a', header=not file_exists, index=False)
    
    #st.success(f"Los datos se han guardado exitosamente en {csv_file}")

# Mostrar los datos guardados
with st.expander("Datos guardados"):
    if os.path.isfile(csv_file):
        st.write("Datos guardados hasta ahora:")
        st.dataframe(pd.read_csv(csv_file))
    else:
        st.error(f"No se pudo leer el archivo CSV: {csv_file}")

# Botón para descargar el CSV
if os.path.exists(csv_file):
    with open(csv_file, 'r') as file:
        st.download_button(
            label="Descargar CSV",
            data=file,
            file_name="inspeccion_est_trabajo.csv",
            mime="text/csv"
        )
else:
    st.warning("No hay archivo CSV para descargar.")

st.page_link("pages/6_Resumen.py", label="Ir al resumen", icon="📋")
st.page_link("Home.py", label="Volver al menú principal", icon="🏠")