import streamlit as st
import pandas as pd
from annotated_text import annotated_text
from datetime import datetime
import os
import tempfile

# Título de la aplicación
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

csv_file = os.path.join(csv_folder, 'inspeccion_controladores.csv')

# Mostrar información de depuración
#st.write(f"Ruta del archivo CSV: {csv_file}")
#st.write(f"La carpeta existe: {os.path.exists(os.path.dirname(csv_file))}")
#st.write(f"El archivo CSV existe: {os.path.exists(csv_file)}")

# Resto del código...

# Barra lateral para seleccionar el controlador
with st.sidebar:
    option = st.selectbox(
        "Inspección de controladores",
        ("118/168", "113/163", "117/167", "121/171", "122/172", "23/73", "33/83", "41/91", "42/92", "44/94", "43/93"), )
    
    # Ayuda con st.expander
    with st.expander("Ayuda"):
        st.image('OCR1100.png', caption="OCR 1100")


# Texto anotado con el controlador seleccionado
annotated_text("Inspección del controlador ",(f"{option}", "", "#ffbd59"),)

# Formulario para la inspección
form = st.form(key='my-form')

# Definir el checklist de inspección como DataFrame
df = pd.DataFrame(
    [
       {"Item": "Led Power (P) en verde", "Estado": False},
       {"Item": "Led Communicaction (Cm) en verde", "Estado": False},
       {"Item": "Led Control (Ct) en verde", "Estado": False},
       {"Item": "Led Alive (A) en verde", "Estado": False},
       {"Item": "Led Error (E) en rojo", "Estado": False},
       {"Item": "Enlaces de fibra óptica en buen estado", "Estado": False},
       {"Item": "Fuente de alimentación del controlador en buenas condiciones", "Estado": False},
   ]
)

# Editor de datos para que el usuario pueda interactuar con el checklist
edited_df = form.data_editor(df)
number=form.number_input("Impedancia de la tierra del gabinete")
number2=form.number_input("Impedancia de la tierra del gabinete de expansión")
submit = form.form_submit_button('Submit')

# Condición al hacer submit
if submit:
    try:
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        # Agregar una columna de controlador al DataFrame editado
        edited_df['Controlador'] = option
        edited_df['Fecha'] = fecha_actual

        # Definir la ruta para el archivo de impedancias
        impedancia_file = os.path.join(csv_folder, 'impedancias.csv')

        # Si el archivo CSV de checklist no existe, crearlo con los encabezados
        if not os.path.isfile(csv_file):
            edited_df.to_csv(csv_file, index=False)
        else:
            # Si ya existe, agregar los datos sin sobrescribir
            edited_df.to_csv(csv_file, mode='a', header=False, index=False)

        # Crear filas para las mediciones de impedancia
        impedancia_row = pd.DataFrame({
            'Item': ['Impedancia'],
            'Valor': [number],
            'Controlador': [option],
            'Fecha': [fecha_actual]
        })
        impedancia2_row = pd.DataFrame({
            'Item': ['Impedancia2'],
            'Valor': [number2],
            'Controlador': [option],
            'Fecha': [fecha_actual]
        })
        
        # Concatenar las filas de impedancia y guardar en el archivo separado
        impedancia_final_df = pd.concat([impedancia_row, impedancia2_row], ignore_index=True)
        
        if not os.path.isfile(impedancia_file):
            impedancia_final_df.to_csv(impedancia_file, index=False)
            st.success(f"Se ha creado el archivo CSV de impedancias en: {impedancia_file}")
        else:
            impedancia_final_df.to_csv(impedancia_file, mode='a', header=False, index=False)
        
        st.success(f'¡Se ha registrado exitosamente la inspección del controlador {option} y las impedancias!')

        with st.expander("Datos guardados"):
            # Mostrar el contenido del archivo CSV de checklist
            if os.path.isfile(csv_file):
                st.write("Datos del checklist guardados hasta ahora:")
                st.dataframe(pd.read_csv(csv_file))
            else:
                st.error(f"No se pudo leer el archivo CSV del checklist: {csv_file}")

            # Mostrar el contenido del archivo CSV de impedancias
            if os.path.isfile(impedancia_file):
                st.write("Datos de impedancias guardados hasta ahora:")
                st.dataframe(pd.read_csv(impedancia_file))
            else:
                st.error(f"No se pudo leer el archivo CSV de impedancias: {impedancia_file}")

    except Exception as e:
        st.error(f"Ocurrió un error al guardar los datos: {str(e)}")
        st.error(f"Tipo de error: {type(e).__name__}")
        st.error(f"Detalles adicionales: {e.args}")


# Botón para descargar el CSV
if os.path.exists(csv_file):
    with open(csv_file, 'r') as file:
        st.download_button(
            label="Descargar CSV",
            data=file,
            file_name="inspeccion_controladores.csv",
            mime="text/csv"
        )
else:
    st.warning("No hay archivo CSV para descargar.")
    
st.page_link("pages/page3.py", label="Siguiente", icon="➡️")
st.page_link("pages/page9.py", label="Volver al menú principal", icon="🏠")
