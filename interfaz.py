import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from config import mongo_uri, mongo_db, mongo_colection


# Conectar con MongoDB Atlas
client = MongoClient(mongo_uri)

# Seleccionar base de datos
db = client[mongo_db]

# Seleccionar colección
estudiantes = db[mongo_colection]


# Función para agregar alumno
def agregar_alumno():

    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    carrera = entrada_carrera.get()

    if nombre == "" or edad == "" or carrera == "":
        messagebox.showwarning("Advertencia", "Completa todos los campos")
        return

    alumno = {
        "nombre": nombre,
        "edad": int(edad),
        "carrera": carrera
    }

    estudiantes.insert_one(alumno)

    messagebox.showinfo("Éxito", "Alumno agregado correctamente")

    entrada_nombre.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_carrera.delete(0, tk.END)

    mostrar_alumnos()


# Función para mostrar alumnos
def mostrar_alumnos():

    # Limpiar tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Obtener alumnos de MongoDB
    alumnos = estudiantes.find()

    for alumno in alumnos:
        tabla.insert(
            "",
            tk.END,
            values=(
                alumno.get("nombre"),
                alumno.get("edad"),
                alumno.get("carrera")
            )
        )


# Crear ventana
ventana = tk.Tk()

ventana.title("Sistema de Alumnos")
ventana.geometry("700x500")


# Título
titulo = tk.Label(
    ventana,
    text="REGISTRO DE ALUMNOS",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=20)


# Nombre
tk.Label(
    ventana,
    text="Nombre:"
).pack()

entrada_nombre = tk.Entry(ventana, width=40)
entrada_nombre.pack(pady=5)


# Edad
tk.Label(
    ventana,
    text="Edad:"
).pack()

entrada_edad = tk.Entry(ventana, width=40)
entrada_edad.pack(pady=5)


# Carrera
tk.Label(
    ventana,
    text="Carrera:"
).pack()

entrada_carrera = tk.Entry(ventana, width=40)
entrada_carrera.pack(pady=5)


# Botones
tk.Button(
    ventana,
    text="Agregar alumno",
    command=agregar_alumno
).pack(pady=10)


tk.Button(
    ventana,
    text="Mostrar alumnos",
    command=mostrar_alumnos
).pack(pady=5)


# Tabla
tabla = ttk.Treeview(
    ventana,
    columns=("Nombre", "Edad", "Carrera"),
    show="headings"
)

tabla.heading("Nombre", text="Nombre")
tabla.heading("Edad", text="Edad")
tabla.heading("Carrera", text="Carrera")

tabla.column("Nombre", width=150)
tabla.column("Edad", width=80)
tabla.column("Carrera", width=350)

tabla.pack(pady=20)


# Ejecutar ventana
ventana.mainloop()