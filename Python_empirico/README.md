
# 📝 Conversor Word a PDF con extracción de números de OT

Este script en Python automatiza la conversión de archivos **Word (.docx)** a **PDF**, y extrae los **números de OT (Orden de Trabajo)** desde el nombre de cada archivo. También clasifica los archivos con nombres incorrectos y genera un archivo `.txt` con todos los números de OT extraídos, en formato lógico (`"123" OR "456" OR "789"`).

---

## 📂 Estructura general

El script realiza las siguientes tareas:

1. **Lee todos los archivos `.docx`** de una carpeta de entrada.
2. **Verifica el nombre** de cada archivo buscando el patrón `OT_<número>_INFORME`.
3. Si el nombre es válido:
   - Convierte el `.docx` a **PDF**.
   - Extrae el número de OT y lo guarda para el resumen final.
4. Si el nombre es inválido:
   - Mueve el archivo a una carpeta de errores.
5. Al final:
   - Crea un archivo `.txt` con los números de OT encontrados.
   - Imprime un **resumen del proceso**.

---

## 📌 Requisitos

- Windows
- Microsoft Word instalado
- Python 3.x
- Paquetes de Python:
  - `pywin32` (`pip install pywin32`)

---

## ⚙️ Configuración de rutas

Puedes personalizar estas rutas en la sección final del script:

```python
carpeta_entrada = r"C:\Users\CamiloAmaya\Documents\Nexxo_word"
carpeta_salida = r"C:\Users\CamiloAmaya\OneDrive - Glenfarne Companies\Documentos\Camilo\Prueba_just_pdfs"
archivo_txt_salida = r"C:\Users\CamiloAmaya\Documents\numeros_OT.txt"
carpeta_errores = r"C:\Users\CamiloAmaya\Documents\Nexxo_mal_formato"
```

---

## 📥 Formato esperado de archivo

El nombre de cada archivo `.docx` debe cumplir esta estructura:

```
OT_<número>_INFORME.docx
```

### ✅ Ejemplo válido:
```
OT_123456_INFORME.docx
```

### ❌ Ejemplo inválido:
```
123456_INFORME.docx → será movido a la carpeta de errores
```

---

## 🧠 Lógica de extracción

El script utiliza una expresión regular para buscar el número de OT en el nombre del archivo:

```python
match = re.search(r'OT_(\d+)_INFORME', archivo)
```

---

## 📤 Resultado

1. Todos los PDFs convertidos se guardan en la carpeta de salida.
2. El archivo `.txt` generado contiene los números de OT extraídos, en el siguiente formato:

```
"123456" OR "789012" OR "456789"
```

Este archivo puede ser usado para búsquedas lógicas en sistemas como SharePoint o gestores documentales.

---