import tkinter as tk
from tkinter import ttk

# --- Función para convertir el color a inglés ---
def traducir_color(color_es):
    colores = {
        "Rojo": "red",
        "Amarillo": "yellow",
        "Azul": "blue"
    }
    return colores.get(color_es, "black")

# --- Función para dibujar las figuras ---
def dibujar():
    canvas.delete("all")
    figura1 = figura1_var.get()  # Figura trasera (más grande)
    figura2 = figura2_var.get()  # Figura delantera (más pequeña)
    color1 = traducir_color(color1_var.get())
    color2 = traducir_color(color2_var.get())

    # Centro del canvas
    cx, cy = 175, 150

    # Tamaños relativos
    size1 = 120  # tamaño figura trasera
    size2 = 80   # tamaño figura delantera

    # --- Dibujar figura trasera ---
    if figura1 == "Cuadrado":
        canvas.create_rectangle(cx - size1, cy - size1, cx + size1, cy + size1, fill=color1, outline="")
    elif figura1 == "Círculo":
        canvas.create_oval(cx - size1, cy - size1, cx + size1, cy + size1, fill=color1, outline="")
    elif figura1 == "Triángulo":
        canvas.create_polygon(
            cx, cy - size1,
            cx - size1, cy + size1,
            cx + size1, cy + size1,
            fill=color1, outline=""
        )

    # --- Dibujar figura delantera ---
    if figura2 == "Cuadrado":
        canvas.create_rectangle(cx - size2, cy - size2, cx + size2, cy + size2, fill=color2, outline="")
    elif figura2 == "Círculo":
        canvas.create_oval(cx - size2, cy - size2, cx + size2, cy + size2, fill=color2, outline="")
    elif figura2 == "Triángulo":
        canvas.create_polygon(
            cx, cy - size2,
            cx - size2, cy + size2,
            cx + size2, cy + size2,
            fill=color2, outline=""
        )

# --- Ventana principal ---
root = tk.Tk()
root.title("Combinador de Figuras y Colores")
root.geometry("400x500")
root.config(bg="#f5f5f5")

# --- Variables ---
figura1_var = tk.StringVar(value="Cuadrado")
figura2_var = tk.StringVar(value="Círculo")
color1_var = tk.StringVar(value="Rojo")
color2_var = tk.StringVar(value="Azul")

# --- Opciones ---
figuras = ["Cuadrado", "Círculo", "Triángulo"]
colores = ["Rojo", "Amarillo", "Azul"]

# --- Interfaz ---
ttk.Label(root, text="Figura trasera:").pack(pady=5)
ttk.OptionMenu(root, figura1_var, figuras[0], *figuras).pack()

ttk.Label(root, text="Color trasero:").pack(pady=5)
ttk.OptionMenu(root, color1_var, colores[0], *colores).pack()

ttk.Label(root, text="Figura delantera:").pack(pady=5)
ttk.OptionMenu(root, figura2_var, figuras[1], *figuras).pack()

ttk.Label(root, text="Color delantero:").pack(pady=5)
ttk.OptionMenu(root, color2_var, colores[2], *colores).pack()

ttk.Button(root, text="Dibujar combinación", command=dibujar).pack(pady=10)

# --- Área de dibujo ---
canvas = tk.Canvas(root, width=350, height=300, bg="white")
canvas.pack(pady=10)

# --- Inicial ---
dibujar()

root.mainloop()
