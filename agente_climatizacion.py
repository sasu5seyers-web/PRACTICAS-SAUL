import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from config import mongo_uri, mongo_db


# ==========================================
# CONEXIÓN CON MONGODB ATLAS
# ==========================================

client = MongoClient(mongo_uri)

db = client[mongo_db]

agentes = db["climatizacion"]


# ==========================================
# AGENTE DE CLIMATIZACIÓN
# ==========================================

class AgenteClimatizacion:

    def __init__(self):
        self.temperatura = 0.0
        self.humedad = 0.0
        self.accion = ""

    # Percibir los datos del entorno
    def percibir(self, temperatura, humedad):
        self.temperatura = float(temperatura)
        self.humedad = float(humedad)

    # Tomar una decisión
    def tomar_decision(self):

        if self.temperatura > 30 and self.humedad > 70:
            self.accion = "Encender aire acondicionado (Modo Deshumidificador)"

        elif self.temperatura > 30:
            self.accion = "Encender ventilador"

        elif self.temperatura < 18:
            self.accion = "Encender calefacción"

        else:
            self.accion = "Mantener sistema apagado"

    # Guardar los datos en MongoDB
    def guardar_datos(self):

        datos = {
            "temperatura": self.temperatura,
            "humedad": self.humedad,
            "accion": self.accion
        }

        agentes.insert_one(datos)


# ==========================================
# EJECUTAR AGENTE
# ==========================================

def ejecutar_agente():

    temperatura = entrada_temperatura.get()
    humedad = entrada_humedad.get()

    if temperatura == "" or humedad == "":
        messagebox.showwarning(
            "Advertencia",
            "Completa todos los campos"
        )
        return

    try:

        agente.percibir(temperatura, humedad)

        agente.tomar_decision()

        agente.guardar_datos()

        resultado_temperatura.config(
            text=f"Temperatura: {agente.temperatura} °C"
        )

        resultado_humedad.config(
            text=f"Humedad: {agente.humedad} %"
        )

        resultado_accion.config(
            text=f"Acción: {agente.accion}"
        )

        messagebox.showinfo(
            "Agente",
            "Datos procesados y guardados en MongoDB Atlas"
        )

        entrada_temperatura.delete(0, tk.END)
        entrada_humedad.delete(0, tk.END)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Ingresa números válidos"
        )


# ==========================================
# CREAR INTERFAZ
# ==========================================

ventana = tk.Tk()

ventana.title("Agente de Climatización")

ventana.geometry("600x500")


# Título

titulo = tk.Label(
    ventana,
    text="AGENTE DE CLIMATIZACIÓN",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=20)


# Temperatura

tk.Label(
    ventana,
    text="Temperatura actual (°C):",
    font=("Arial", 12)
).pack()

entrada_temperatura = tk.Entry(
    ventana,
    width=30
)

entrada_temperatura.pack(pady=10)


# Humedad

tk.Label(
    ventana,
    text="Humedad actual (%):",
    font=("Arial", 12)
).pack()

entrada_humedad = tk.Entry(
    ventana,
    width=30
)

entrada_humedad.pack(pady=10)


# Botón ejecutar

tk.Button(
    ventana,
    text="Ejecutar agente",
    command=ejecutar_agente,
    width=25
).pack(pady=20)


# Resultados

tk.Label(
    ventana,
    text="--- RESULTADO DEL AGENTE ---",
    font=("Arial", 14, "bold")
).pack(pady=10)


resultado_temperatura = tk.Label(
    ventana,
    text="Temperatura: -",
    font=("Arial", 11)
)

resultado_temperatura.pack(pady=5)


resultado_humedad = tk.Label(
    ventana,
    text="Humedad: -",
    font=("Arial", 11)
)

resultado_humedad.pack(pady=5)


resultado_accion = tk.Label(
    ventana,
    text="Acción: -",
    font=("Arial", 11)
)

resultado_accion.pack(pady=10)


# ==========================================
# INICIAR AGENTE
# ==========================================

agente = AgenteClimatizacion()

ventana.mainloop()