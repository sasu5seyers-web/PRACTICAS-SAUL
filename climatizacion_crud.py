# ==========================================
# CRUD DEL AGENTE DE CLIMATIZACIÓN
# ==========================================

import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from bson.objectid import ObjectId

from config import mongo_uri, mongo_db
from agente_climatizacion import AgenteClimatizacion


# ==========================================
# CONEXIÓN CON MONGODB ATLAS
# ==========================================

client = MongoClient(mongo_uri)

db = client[mongo_db]

coleccion = db["climatizacion"]


# ==========================================
# CREAR AGENTE
# ==========================================

agente = AgenteClimatizacion()


# ==========================================
# GUARDAR DATOS
# ==========================================

def guardar_datos():

    temperatura = entrada_temperatura.get()
    humedad = entrada_humedad.get()

    if temperatura == "" or humedad == "":
        messagebox.showwarning(
            "Advertencia",
            "Completa todos los campos"
        )
        return

    try:

        # El agente percibe los datos
        agente.percibir(
            temperatura,
            humedad
        )

        # El agente toma una decisión
        agente.tomar_decision()

        # Datos que se guardarán
        datos = {
            "temperatura": agente.temperatura,
            "humedad": agente.humedad,
            "accion": agente.accion
        }

        # Guardar en MongoDB
        coleccion.insert_one(datos)

        messagebox.showinfo(
            "Éxito",
            "Datos guardados correctamente"
        )

        limpiar_campos()

        consultar_datos()

    except ValueError:

        messagebox.showerror(
            "Error",
            "La temperatura y la humedad deben ser números"
        )


# ==========================================
# CONSULTAR TODOS LOS DATOS
# ==========================================

def consultar_datos():

    # Limpiar la tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Buscar todos los registros
    datos = coleccion.find()

    # Mostrar registros
    for dato in datos:

        tabla.insert(
            "",
            tk.END,
            iid=str(dato["_id"]),
            values=(
                dato.get("temperatura"),
                dato.get("humedad"),
                dato.get("accion")
            )
        )


# ==========================================
# SELECCIONAR DATO
# ==========================================

def seleccionar_dato(event):

    seleccionado = tabla.selection()

    if not seleccionado:
        return

    # Obtener información de la fila
    fila = tabla.item(
        seleccionado[0]
    )

    valores = fila["values"]

    # Colocar temperatura
    entrada_temperatura.delete(
        0,
        tk.END
    )

    entrada_temperatura.insert(
        0,
        valores[0]
    )

    # Colocar humedad
    entrada_humedad.delete(
        0,
        tk.END
    )

    entrada_humedad.insert(
        0,
        valores[1]
    )


# ==========================================
# CONSULTAR DATO SELECCIONADO
# ==========================================

def consultar_seleccionado():

    seleccionado = tabla.selection()

    if not seleccionado:

        messagebox.showwarning(
            "Advertencia",
            "Selecciona un registro de la tabla"
        )

        return

    # Obtener el ID del registro seleccionado
    id_registro = seleccionado[0]

    # Buscar ese registro en MongoDB
    dato = coleccion.find_one(
        {
            "_id": ObjectId(id_registro)
        }
    )

    if dato:

        messagebox.showinfo(
            "Consulta del registro",
            f"Temperatura: {dato.get('temperatura')} °C\n"
            f"Humedad: {dato.get('humedad')} %\n"
            f"Acción: {dato.get('accion')}"
        )


# ==========================================
# ACTUALIZAR DATO
# ==========================================

def actualizar_datos():

    seleccionado = tabla.selection()

    if not seleccionado:

        messagebox.showwarning(
            "Advertencia",
            "Selecciona un registro para actualizar"
        )

        return

    temperatura = entrada_temperatura.get()
    humedad = entrada_humedad.get()

    if temperatura == "" or humedad == "":

        messagebox.showwarning(
            "Advertencia",
            "Completa todos los campos"
        )

        return

    try:

        # El agente recibe los nuevos datos
        agente.percibir(
            temperatura,
            humedad
        )

        # El agente vuelve a tomar una decisión
        agente.tomar_decision()

        # Nuevos datos
        datos_actualizados = {
            "temperatura": agente.temperatura,
            "humedad": agente.humedad,
            "accion": agente.accion
        }

        # Obtener ID del registro
        id_registro = seleccionado[0]

        # Actualizar en MongoDB
        coleccion.update_one(
            {
                "_id": ObjectId(id_registro)
            },
            {
                "$set": datos_actualizados
            }
        )

        messagebox.showinfo(
            "Éxito",
            "Registro actualizado correctamente"
        )

        limpiar_campos()

        consultar_datos()

    except ValueError:

        messagebox.showerror(
            "Error",
            "Ingresa números válidos"
        )


# ==========================================
# ELIMINAR DATO
# ==========================================

def eliminar_datos():

    seleccionado = tabla.selection()

    if not seleccionado:

        messagebox.showwarning(
            "Advertencia",
            "Selecciona un registro para eliminar"
        )

        return

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        "¿Deseas eliminar este registro?"
    )

    if confirmar:

        # Obtener ID
        id_registro = seleccionado[0]

        # Eliminar de MongoDB
        coleccion.delete_one(
            {
                "_id": ObjectId(id_registro)
            }
        )

        messagebox.showinfo(
            "Éxito",
            "Registro eliminado correctamente"
        )

        limpiar_campos()

        consultar_datos()


# ==========================================
# LIMPIAR CAMPOS
# ==========================================

def limpiar_campos():

    entrada_temperatura.delete(
        0,
        tk.END
    )

    entrada_humedad.delete(
        0,
        tk.END
    )

    entrada_temperatura.focus()


# ==========================================
# CREAR VENTANA
# ==========================================

ventana = tk.Tk()

ventana.title(
    "Agente de Climatización"
)

ventana.geometry(
    "1100x700"
)


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    ventana,
    text="AGENTE DE CLIMATIZACIÓN",
    font=("Arial", 20, "bold")
)

titulo.pack(
    pady=20
)


# ==========================================
# TEMPERATURA
# ==========================================

tk.Label(
    ventana,
    text="Temperatura actual (°C):",
    font=("Arial", 11)
).pack()

entrada_temperatura = tk.Entry(
    ventana,
    width=30
)

entrada_temperatura.pack(
    pady=5
)


# ==========================================
# HUMEDAD
# ==========================================

tk.Label(
    ventana,
    text="Humedad actual (%):",
    font=("Arial", 11)
).pack()

entrada_humedad = tk.Entry(
    ventana,
    width=30
)

entrada_humedad.pack(
    pady=5
)


# ==========================================
# BOTONES
# ==========================================

marco_botones = tk.Frame(
    ventana
)

marco_botones.pack(
    pady=15
)


# BOTÓN GUARDAR

tk.Button(
    marco_botones,
    text="Guardar",
    width=15,
    command=guardar_datos
).grid(
    row=0,
    column=0,
    padx=5
)


# BOTÓN CONSULTAR

tk.Button(
    marco_botones,
    text="Consultar",
    width=15,
    command=consultar_datos
).grid(
    row=0,
    column=1,
    padx=5
)


# BOTÓN CONSULTAR SELECCIONADO

tk.Button(
    marco_botones,
    text="Consultar seleccionado",
    width=20,
    command=consultar_seleccionado
).grid(
    row=0,
    column=2,
    padx=5
)


# BOTÓN ACTUALIZAR

tk.Button(
    marco_botones,
    text="Actualizar",
    width=15,
    command=actualizar_datos
).grid(
    row=0,
    column=3,
    padx=5
)


# BOTÓN ELIMINAR

tk.Button(
    marco_botones,
    text="Eliminar",
    width=15,
    command=eliminar_datos
).grid(
    row=0,
    column=4,
    padx=5
)


# BOTÓN LIMPIAR

tk.Button(
    marco_botones,
    text="Limpiar",
    width=15,
    command=limpiar_campos
).grid(
    row=0,
    column=5,
    padx=5
)


# ==========================================
# TÍTULO DE LA TABLA
# ==========================================

tk.Label(
    ventana,
    text="Registros de climatización",
    font=("Arial", 14, "bold")
).pack(
    pady=10
)


# ==========================================
# TABLA
# ==========================================

tabla = ttk.Treeview(
    ventana,
    columns=(
        "Temperatura",
        "Humedad",
        "Accion"
    ),
    show="headings",
    height=15
)


# Encabezado temperatura

tabla.heading(
    "Temperatura",
    text="Temperatura °C"
)


# Encabezado humedad

tabla.heading(
    "Humedad",
    text="Humedad %"
)


# Encabezado acción

tabla.heading(
    "Accion",
    text="Acción del agente"
)


# Tamaño de columnas

tabla.column(
    "Temperatura",
    width=180
)

tabla.column(
    "Humedad",
    width=180
)

tabla.column(
    "Accion",
    width=550
)


tabla.pack(
    pady=10
)


# ==========================================
# SELECCIONAR REGISTRO DE LA TABLA
# ==========================================

tabla.bind(
    "<ButtonRelease-1>",
    seleccionar_dato
)


# ==========================================
# MOSTRAR DATOS AL INICIAR
# ==========================================

consultar_datos()


# ==========================================
# INICIAR PROGRAMA
# ==========================================

ventana.mainloop()