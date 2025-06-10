import streamlit as st
import pandas as pd
from fpdf import FPDF
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
                mime="text/csv",
                key=f"download_{section}_{filename}"  # ✅ Clave única
            )
    else:
        st.warning(f"No hay datos registrados para {section}.")

st.title("📄 Generar Reporte PDF")

# Definir carpeta donde están los CSV
documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
csv_files = {
    "Red Ovation": "inspeccion_est_trabajo.csv",
    "Controladores": "inspeccion_controladores.csv",
    "Impedancias": "impedancias.csv",
    "Estaciones": "inspeccion_est_trabajo.csv",
    "Históricos/Windows": "inspeccion_hist_windows.csv",
    "Error Log": "ovation_dcs_errors.csv"
}

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.set_title("Reporte Checklist Ovation")

for section, filename in csv_files.items():
    file_path = os.path.join(documents_folder, filename)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=section, ln=True)
    pdf.set_font("Arial", size=10)

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        for i, row in df.iterrows():
            row_text = ', '.join([f"{col}: {str(row[col])}" for col in df.columns])
            pdf.multi_cell(0, 10, txt=row_text)
        pdf.ln(5)
    else:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(200, 10, txt="Sin datos disponibles.", ln=True)
        pdf.set_text_color(0, 0, 0)

# Guardar el PDF temporalmente
pdf_path = os.path.join(documents_folder, "reporte_ovation.pdf")
pdf.output(pdf_path)

# Mostrar botón de descarga
with open(pdf_path, "rb") as f:
    st.download_button(
        label="📥 Descargar Reporte PDF",
        data=f,
        file_name="reporte_ovation.pdf",
        mime="application/pdf"
    )