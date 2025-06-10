import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Chequeo DCS Ovation",
    page_icon="🎛️",
    layout="wide"
)

# Título principal con estilo
st.title('Sistema de Inspección y Reportes DCS Ovation')

# Descripción general del sistema
st.markdown("""
### Sistema de Control Distribuido (DCS)
El DCS Ovation es fundamental para nuestra operación, controlando y supervisando procesos industriales críticos 
en tiempo real. Este sistema de inspección está diseñado para mantener su óptimo funcionamiento.
""")

# Crear tres columnas para los objetivos principales
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    ### Digitalización
    - Formularios digitales
    - Registro automático
    - Eliminación de papel
    """)

with col2:
    st.success("""
    ### Eficiencia
    - Proceso optimizado
    - Checklist interactivo
    - Reportes automáticos
    """)

with col3:
    st.warning("""
    ### Seguimiento
    - Histórico de datos
    - Análisis de tendencias
    - Detección temprana
    """)

# Sección de proceso de inspección
st.markdown("---")
st.header("Proceso de Inspección")

# Crear columnas para el proceso (ahora 4 en lugar de 5)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 1. Red Ovation
    #### System Viewer
    - Verificación de estado
    - Monitoreo de alarmas
    - Revisión de eventos
    
    #### System Status
    - Estado del sistema
    - Indicadores críticos
    - Parámetros operativos
    """)

with col2:
    st.markdown("""
    ### 2. Controladores
    #### Verificaciones
    - Estado de LEDs
    - Conexiones de red
    - Fibra óptica
    
    #### Mediciones
    - Impedancias
    - Alimentación
    - Diagnósticos
    """)

with col3:
    st.markdown("""
    ### 3. Estaciones
    #### Hardware
    - Estado del equipo
    - Conexiones físicas
    - Funcionamiento general
    
    #### Software
    - Sincronización
    - Comunicaciones
    - Estado operativo
    """)

with col4:
    st.markdown("""
    ### 4. Históricos
    #### Drops
    - Drop 160
    - Drop 164
    - Verificación de datos
    
    #### Scanners
    - Scanner 233
    - Scanner 166
    - Rendimiento
    """)

# Sección de instrucciones
st.markdown("---")
st.header("Instrucciones de Uso")

with st.expander("Ver instrucciones detalladas"):
    st.markdown("""
    1. **Inicio de Inspección**
        - Seleccione "Iniciar" para comenzar el proceso
        - Siga el orden establecido de inspección
        - Complete todos los campos requeridos
    
    2. **Durante la Inspección**
        - Verifique cada punto del checklist cuidadosamente
        - Documente cualquier anomalía encontrada
        - Registre las mediciones con precisión
    
    3. **Finalización**
        - Revise la información ingresada
        - Guarde los cambios en cada sección
        - Verifique la completitud del proceso
    """)

# Información adicional
st.markdown("---")
st.subheader("Información Importante")
col1, col2 = st.columns(2)

with col1:
    st.error("""
    ### Contacto de Soporte
    En caso de encontrar problemas críticos durante la inspección:
    - Notifique inmediatamente al supervisor
    - Registre el incidente en el sistema
    - Documente detalladamente la situación
    """)

with col2:
    st.success("""
    ### Mejores Prácticas
    Para obtener mejores resultados:
    - Siga la secuencia establecida
    - Complete todos los campos requeridos
    - Verifique la información antes de enviar
    - Mantenga registros precisos y detallados
    """)

# Botón de inicio grande y llamativo
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <div style='text-align: center'>
            <h2>¿Listo para comenzar la inspección?</h2>
        </div>
        """, 
        unsafe_allow_html=True
        )
    st.page_link("pages/1_Red_Ovation.py", label="Iniciar inspección", icon="🔧", help="Comenzar el proceso de inspección")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: grey;'>
        Sistema de Inspección y Reportes DCS Ovation | Desarrollado por Instrumentación y Control
    </div>
    """, 
    unsafe_allow_html=True
)
