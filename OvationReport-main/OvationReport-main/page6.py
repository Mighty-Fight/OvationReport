import streamlit as st
import pandas as pd
import os

st.title("📊 Resumen de Inspecciones Ovation DCS")

# Definir rutas
documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
csv_files = {
    "Red Ovation": "inspeccion_est_trabajo.csv",
    "Controladores": "inspeccion_controladores.csv",
    "Impedancias": "impedancias.csv",
    "Estaciones": "inspeccion_est_trabajo.csv",
    "Históricos/Windows": "inspeccion_hist_windows.csv",
    "Error Log": "ovation_dcs_errors.csv"
}

for section, filename in csv_files.items():
    file_path = os.path.join(documents_folder, filename)
    st.subheader(section)
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        st.dataframe(df)
        with open(file_path, 'r') as file:
            st.download_button(
                label=f"Descargar {filename}",
                data=file,
                file_name=filename,
                mime="text/csv"
            )
    else:
        st.warning(f"No hay datos registrados para {section}.")