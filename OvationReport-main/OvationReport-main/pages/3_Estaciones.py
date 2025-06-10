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

csv_file = os.path.join(csv_folder, 'inspeccion_est_trabajo.csv')

# Mostrar información de depuración
#st.write(f"Ruta del archivo CSV: {csv_file}")
#st.write(f"La carpeta existe: {os.path.exists(os.path.dirname(csv_file))}")
#st.write(f"El archivo CSV existe: {os.path.exists(csv_file)}")

with st.sidebar:
    # Selección de estación de trabajo
    option = st.selectbox(
        "Inspección de estaciones de trabajo",
        ("160", "164", "166", "200", "212", "213", "214", "230", "233", "234"),
    )

# Texto anotado
annotated_text("Inspección de la estación de trabajo ", (f" {option} ", "", "#bf6b6b"))

# Formulario para editar los datos
form = st.form(key='my-form')

# DataFrame para la inspección
df = pd.DataFrame(
    [
       {"Item": "El equipo está encendido", "Estado": False},
       {"Item": "Los dos cables de red se encuentran encendidos y funcionales", "Estado": False},
       {"Item": "El cableado del equipo se encuentra en buenas condiciones", "Estado": False},
       {"Item": "La sincronización horaria es la correcta con el GPS", "Estado": False},
    ]
)

# Editor de datos
edited_df = form.data_editor(df)

# Campo de texto para observaciones
observaciones = form.text_area("Observaciones")

# Botón de envío
submit = form.form_submit_button('Submit')

# Si se envía el formulario, guardar el DataFrame y las observaciones en un archivo CSV
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
    
# Mostrar los datos guardados
with st.expander("Datos guardados"):
    # Mostrar el contenido del archivo CSV
    if os.path.isfile(csv_file):
        st.write("Datos guardados hasta ahora:")
        st.dataframe(pd.read_csv(csv_file))
    else:
        st.error(f"No se pudo leer el archivo CSV: {csv_file}")

# Navegación condicional para la estación 234
if option == "234":
    st.page_link("pages/page4.py", label="Siguiente", icon="➡️")

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

st.page_link("pages/4_Historicos.py", label="Siguiente", icon="➡️")
st.page_link("Home.py", label="Volver al menú principal", icon="🏠")