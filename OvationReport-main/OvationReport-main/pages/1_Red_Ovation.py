import streamlit as st
import pandas as pd
from datetime import datetime
import os
import tempfile

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

st.title('Chequeo Ovation DCS')

st.subheader("Red Ovation")

# Instrucciones con colores
st.markdown("Anote los hallazgos encontrados en el :blue-background[System Viewer] y :green-background[System Status]")


# Crear formulario para ingresar los hallazgos
form = st.form(key='my-form')

txt = form.text_area("Descripción de los hallazgos del System Viewer:")

txt2 = form.text_area("Descripción de los hallazgos del System Status:")

submit = form.form_submit_button('Submit')

# Guardar los hallazgos en un archivo CSV
if submit:
    # Obtener la fecha y hora actuales
    fecha_actual = datetime.now().strftime("%Y-%m-%d ")
    
    # Crear un DataFrame con los hallazgos
    df_hallazgos = pd.DataFrame({
        "Fecha": [fecha_actual],
        "Hallazgo System Viewer": [txt],
        "Hallazgo System Status": [txt2]
    })
    
    # Guardar el DataFrame en un archivo CSV (agregar al final si el archivo ya existe)
    try:
        if os.path.exists(csv_file):
            df_hallazgos.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            df_hallazgos.to_csv(csv_file, mode='w', header=True, index=False)
        
        # Mensaje de éxito
        st.write(f'¡Se ha registrado exitosamente la inspección de la red Ovation!')
    
    
    except PermissionError:
        st.error(f"No se puede guardar el archivo. Parece que no tienes permisos suficientes para escribir en {csv_file}.")
    except Exception as e:
        st.error(f"Error al guardar el archivo: {str(e)}")

    st.page_link("pages/page2.py", label="Siguiente", icon="➡️")
    

# Ayuda con st.expander en la barra lateral
with st.sidebar:
    with st.expander("Ayuda"):
        st.write("""
        En esta sección, puede anotar los hallazgos encontrados en el System Viewer y System Status.
        
        - **System Viewer**: Es una herramienta para monitorear los sistemas en tiempo real.
        - **System Status**: Proporciona el estado actual del sistema.
        
        Asegúrese de ingresar cualquier irregularidad o problema detectado para su posterior análisis.
        """)
st.page_link("pages/2_Controladores.py", label="Siguiente", icon="➡️")
st.page_link("Home.py", label="Volver al menú principal", icon="🏠")