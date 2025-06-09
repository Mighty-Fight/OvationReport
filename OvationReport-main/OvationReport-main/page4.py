import streamlit as st
import pandas as pd
from annotated_text import annotated_text
from datetime import datetime
import os
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

csv_file = os.path.join(csv_folder, 'inspeccion_hist_windows.csv')

# Mostrar información de depuración
#st.write(f"Ruta del archivo CSV: {csv_file}")
#st.write(f"La carpeta existe: {os.path.exists(os.path.dirname(csv_file))}")
#st.write(f"El archivo CSV existe: {os.path.exists(csv_file)}")

with st.sidebar:

    option = st.selectbox(
    "Drops y servidores",
    ("Drop 160", "Drop 164", "Scanner 233", "Scanner 166"),)
    # Ayuda con st.expander
    with st.expander("Ayuda"):
        st.write("""
        Para confirmar el rendimiento del sistema abra el Administrador de tareas de Windows:
                
                Ctrl + Alt + Supr -> Administrador de tareas de Windows
        
                
        - Revise la utilización de espacio en disco.
        - Revise el uso, configuración y ubicación de la memoria física y virtual.
        - Compruebe el monitor de rendimiento     
        
        Asegúrese de ingresar cualquier irregularidad o problema detectado para su posterior análisis.
        """)

annotated_text("Revisión de históticos y eventos de Windows " ,(f"{option}", "", "#7029ff"),)
form = st.form(key='my-form')

df = pd.DataFrame(
    [
       {"Item": "Compruebe el Historian Status Monitor ¿Todo se encuentra en orden?", "Estado": False, },
       {"Item": "Rendimiento óptimo del sistema", "Estado": False},
       {"Item": "El cableado del equipo se encuentra en buenas condiciones", "Estado": False},
       {"Item": "La sincronización horaria es la correcta con el GPS", "Estado": False},
    ]
)
edited_df = form.data_editor(df)

observaciones = form.text_area(
    "Observaciones",
)
submit = form.form_submit_button('Submit')

if submit:
    try:
        # Obtener la fecha y hora actuales
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        
        # Agregar columnas adicionales al DataFrame
        edited_df['Estación'] = option
        edited_df['Fecha'] = fecha_actual
        
        # Crear una nueva fila para las observaciones
        observaciones_row = pd.DataFrame({
            'Item': ['Observaciones'],
            'Estado': [observaciones],
            'Estación': [option],
            'Fecha': [fecha_actual]
        })
        
        # Concatenar el DataFrame original con la fila de observaciones
        final_df = pd.concat([edited_df, observaciones_row], ignore_index=True)
        
        # Guardar el DataFrame en el archivo CSV (agregar al final si el archivo ya existe)
        if os.path.exists(csv_file):
            # Si el archivo existe, agregar sin encabezado
            final_df.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            # Si el archivo no existe, crear uno nuevo con encabezado
            final_df.to_csv(csv_file, mode='w', header=True, index=False)
        
        # Mensaje de éxito
        st.success(f'¡Se ha registrado exitosamente la inspección de la estación de trabajo {option}!')

    except Exception as e:
        st.error(f"Error al guardar el archivo: {str(e)}")
        st.error(f"Tipo de error: {type(e).__name__}")
        st.error(f"Detalles adicionales: {e.args}")

    # Navegación condicional para la estación 234
    if option == "Scanner 166":
        st.page_link("pages/page5.py", label="Siguiente", icon="➡️")
        
# Mostrar los datos guardados
with st.expander("Datos guardados"):
    # Mostrar el contenido del archivo CSV
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
            file_name="inspeccion_hist_windows.csv",
            mime="text/csv"
        )
else:
    st.warning("No hay archivo CSV para descargar.")

st.page_link("pages/page5.py", label="Siguiente", icon="➡️")
st.page_link("pages/page9.py", label="Volver al menú principal", icon="🏠")
