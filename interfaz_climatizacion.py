# ==========================================
# INTERFAZ DE ANÁLISIS DEL AGENTE
# DE CLIMATIZACIÓN
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox

from pymongo import MongoClient

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import mongo_uri, mongo_db


# ==========================================
# CONEXIÓN A MONGODB
# ==========================================

client = MongoClient(mongo_uri)

db = client[mongo_db]

coleccion = db["climatizacion"]


# ==========================================
# VENTANA PRINCIPAL
# ==========================================

ventana = tk.Tk()

ventana.title("ANÁLISIS DEL AGENTE DE CLIMATIZACIÓN")

ventana.geometry("1400x900")

ventana.resizable(True, True)


# ==========================================
# FUNCIONES
# ==========================================

def obtener_intervalo(temperatura, humedad):

    if temperatura < 18:

        return "Intervalo 1: Temperatura menor a 18 °C"

    elif temperatura >= 18 and temperatura <= 30:

        return "Intervalo 2: Temperatura entre 18 °C y 30 °C"

    elif temperatura > 30 and humedad <= 70:

        return "Intervalo 3: Temperatura mayor a 30 °C y humedad hasta 70%"

    elif temperatura > 30 and humedad > 70:

        return "Intervalo 4: Temperatura mayor a 30 °C y humedad mayor a 70%"

    return "Sin intervalo"


def obtener_accion(temperatura, humedad):

    if temperatura > 30 and humedad > 70:

        return "Encender aire acondicionado (Modo Deshumidificador)"

    elif temperatura > 30:

        return "Encender ventilador"

    elif temperatura < 18:

        return "Encender calefacción"

    else:

        return "Mantener sistema apagado"


# ==========================================
# CARGAR TEMPERATURAS
# ==========================================

def cargar_temperaturas():

    try:

        datos = list(
            coleccion.find(
                {},
                {
                    "temperatura": 1
                }
            ).sort("temperatura", 1)
        )

        temperaturas = []

        for dato in datos:

            temperatura = dato.get("temperatura")

            if temperatura is not None:

                if temperatura not in temperaturas:

                    temperaturas.append(temperatura)

        combo_temperaturas["values"] = temperaturas

        if temperaturas:

            combo_temperaturas.current(0)

            mostrar_dato_seleccionado()

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"No se pudieron cargar las temperaturas:\n{error}"
        )


# ==========================================
# MOSTRAR TEMPERATURA SELECCIONADA
# ==========================================

def mostrar_dato_seleccionado(event=None):

    try:

        temperatura_seleccionada = combo_temperaturas.get()

        if temperatura_seleccionada == "":
            return

        temperatura = float(
            temperatura_seleccionada
        )

        datos = list(
            coleccion.find(
                {
                    "temperatura": temperatura
                }
            )
        )

        if not datos:

            etiqueta_temperatura.config(
                text="Temperatura: --"
            )

            etiqueta_humedad.config(
                text="Humedad: --"
            )

            etiqueta_intervalo.config(
                text="Intervalo: --"
            )

            etiqueta_accion.config(
                text="Acción: --"
            )

            return

        # ==========================================
        # PRIMER REGISTRO
        # ==========================================

        dato = datos[0]

        humedad = dato.get(
            "humedad",
            0
        )

        accion = obtener_accion(
            temperatura,
            humedad
        )

        intervalo = obtener_intervalo(
            temperatura,
            humedad
        )

        etiqueta_temperatura.config(
            text=f"Temperatura: {temperatura} °C"
        )

        etiqueta_humedad.config(
            text=f"Humedad: {humedad} %"
        )

        etiqueta_intervalo.config(
            text=f"Intervalo: {intervalo}"
        )

        etiqueta_accion.config(
            text=f"Acción: {accion}"
        )


        # ==========================================
        # RESUMEN DE LA TEMPERATURA
        # ==========================================

        resumen_seleccionado.delete(
            "1.0",
            tk.END
        )

        resumen_seleccionado.insert(
            tk.END,
            "RESUMEN DE LA TEMPERATURA SELECCIONADA\n"
        )

        resumen_seleccionado.insert(
            tk.END,
            "============================================\n\n"
        )

        resumen_seleccionado.insert(
            tk.END,
            f"Temperatura: {temperatura} °C\n"
        )

        resumen_seleccionado.insert(
            tk.END,
            f"Cantidad de registros: {len(datos)}\n\n"
        )

        acciones = {}

        intervalos = {}

        for registro in datos:

            humedad_registro = registro.get(
                "humedad",
                0
            )

            accion_registro = obtener_accion(
                temperatura,
                humedad_registro
            )

            intervalo_registro = obtener_intervalo(
                temperatura,
                humedad_registro
            )

            # Contar acciones
            if accion_registro not in acciones:

                acciones[accion_registro] = 0

            acciones[accion_registro] += 1

            # Contar intervalos
            if intervalo_registro not in intervalos:

                intervalos[intervalo_registro] = 0

            intervalos[intervalo_registro] += 1


        resumen_seleccionado.insert(
            tk.END,
            "ACCIONES ENCONTRADAS:\n"
        )

        for accion, cantidad in acciones.items():

            resumen_seleccionado.insert(
                tk.END,
                f"- {accion}: {cantidad} caso(s)\n"
            )


        resumen_seleccionado.insert(
            tk.END,
            "\nINTERVALOS ENCONTRADOS:\n"
        )

        for intervalo, cantidad in intervalos.items():

            resumen_seleccionado.insert(
                tk.END,
                f"- {intervalo}: {cantidad} caso(s)\n"
            )


    except Exception as error:

        messagebox.showerror(
            "Error",
            f"No se pudo mostrar el dato:\n{error}"
        )


# ==========================================
# ACTUALIZAR RESUMEN GENERAL
# ==========================================

def actualizar_resumen():

    try:

        datos = list(
            coleccion.find({})
        )

        total = len(datos)

        intervalo1 = 0
        intervalo2 = 0
        intervalo3 = 0
        intervalo4 = 0


        for dato in datos:

            temperatura = float(
                dato.get(
                    "temperatura",
                    0
                )
            )

            humedad = float(
                dato.get(
                    "humedad",
                    0
                )
            )


            if temperatura < 18:

                intervalo1 += 1

            elif temperatura >= 18 and temperatura <= 30:

                intervalo2 += 1

            elif temperatura > 30 and humedad <= 70:

                intervalo3 += 1

            elif temperatura > 30 and humedad > 70:

                intervalo4 += 1


        # ==========================================
        # MOSTRAR CANTIDADES
        # ==========================================

        etiqueta_total.config(
            text=f"TOTAL DE CASOS: {total}"
        )

        etiqueta_i1.config(
            text=f"Intervalo 1 (<18 °C): {intervalo1}"
        )

        etiqueta_i2.config(
            text=f"Intervalo 2 (18-30 °C): {intervalo2}"
        )

        etiqueta_i3.config(
            text=f"Intervalo 3 (>30 °C y humedad ≤70%): {intervalo3}"
        )

        etiqueta_i4.config(
            text=f"Intervalo 4 (>30 °C y humedad >70%): {intervalo4}"
        )


        # ==========================================
        # RESUMEN EN TEXTO
        # ==========================================

        resumen_general.delete(
            "1.0",
            tk.END
        )

        resumen_general.insert(
            tk.END,
            "RESUMEN GENERAL DE LOS DATOS\n"
        )

        resumen_general.insert(
            tk.END,
            "====================================\n\n"
        )

        resumen_general.insert(
            tk.END,
            f"Total de casos registrados: {total}\n\n"
        )

        resumen_general.insert(
            tk.END,
            f"Intervalo 1: {intervalo1} caso(s)\n"
        )

        resumen_general.insert(
            tk.END,
            f"Intervalo 2: {intervalo2} caso(s)\n"
        )

        resumen_general.insert(
            tk.END,
            f"Intervalo 3: {intervalo3} caso(s)\n"
        )

        resumen_general.insert(
            tk.END,
            f"Intervalo 4: {intervalo4} caso(s)\n\n"
        )

        resumen_general.insert(
            tk.END,
            "Los datos se obtienen de la colección "
            "'climatizacion' de MongoDB."
        )


    except Exception as error:

        messagebox.showerror(
            "Error",
            f"No se pudo actualizar el resumen:\n{error}"
        )


# ==========================================
# CREAR GRÁFICA
# ==========================================

def crear_grafica():

    try:

        datos = list(
            coleccion.find({})
        )


        # ==========================================
        # LIMPIAR GRÁFICA ANTERIOR
        # ==========================================

        for widget in marco_grafica.winfo_children():

            widget.destroy()


        if not datos:

            etiqueta_sin_datos = tk.Label(
                marco_grafica,
                text="No hay datos para mostrar en la gráfica",
                font=("Arial", 16)
            )

            etiqueta_sin_datos.pack(
                expand=True
            )

            return


        temperaturas = []

        humedades = []


        # ==========================================
        # OBTENER DATOS
        # ==========================================

        for dato in datos:

            temperatura = dato.get(
                "temperatura"
            )

            humedad = dato.get(
                "humedad"
            )

            if temperatura is not None and humedad is not None:

                temperaturas.append(
                    float(temperatura)
                )

                humedades.append(
                    float(humedad)
                )


        # ==========================================
        # CREAR FIGURA
        # ==========================================

        figura = Figure(
            figsize=(12, 6),
            dpi=100
        )

        grafica = figura.add_subplot(111)


        # ==========================================
        # GRÁFICA DE PUNTOS
        # ==========================================

        grafica.scatter(
            temperaturas,
            humedades,
            s=80
        )


        # ==========================================
        # TÍTULOS
        # ==========================================

        grafica.set_xlabel(
            "Temperatura (°C)",
            fontsize=12
        )

        grafica.set_ylabel(
            "Humedad (%)",
            fontsize=12
        )

        grafica.set_title(
            "Relación entre temperatura y humedad",
            fontsize=15
        )


        # ==========================================
        # CUADRÍCULA
        # ==========================================

        grafica.grid(
            True
        )


        # ==========================================
        # AJUSTAR GRÁFICA
        # ==========================================

        figura.tight_layout()


        # ==========================================
        # MOSTRAR EN TKINTER
        # ==========================================

        canvas = FigureCanvasTkAgg(
            figura,
            master=marco_grafica
        )

        canvas.draw()


        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    except Exception as error:

        messagebox.showerror(
            "Error",
            f"No se pudo crear la gráfica:\n{error}"
        )


# ==========================================
# ACTUALIZAR TODA LA INTERFAZ
# ==========================================

def actualizar_interfaz():

    cargar_temperaturas()

    actualizar_resumen()

    crear_grafica()


# ==========================================
# PARTE SUPERIOR
# ==========================================

marco_superior = tk.Frame(
    ventana
)

marco_superior.pack(
    fill="x",
    padx=15,
    pady=10
)


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    marco_superior,
    text="ANÁLISIS DEL AGENTE DE CLIMATIZACIÓN",
    font=("Arial", 20, "bold")
)

titulo.pack(
    pady=5
)


# ==========================================
# SELECCIONAR TEMPERATURA
# ==========================================

marco_seleccion = tk.LabelFrame(
    marco_superior,
    text="Seleccionar temperatura",
    font=("Arial", 11, "bold")
)

marco_seleccion.pack(
    fill="x",
    pady=5
)


combo_temperaturas = ttk.Combobox(
    marco_seleccion,
    state="readonly",
    width=20,
    font=("Arial", 11)
)

combo_temperaturas.pack(
    side="left",
    padx=10,
    pady=10
)

combo_temperaturas.bind(
    "<<ComboboxSelected>>",
    mostrar_dato_seleccionado
)


# ==========================================
# DATOS DE TEMPERATURA
# ==========================================

marco_datos = tk.Frame(
    marco_superior
)

marco_datos.pack(
    fill="x",
    pady=5
)


etiqueta_temperatura = tk.Label(
    marco_datos,
    text="Temperatura: --",
    font=("Arial", 11)
)

etiqueta_temperatura.pack(
    side="left",
    padx=15
)


etiqueta_humedad = tk.Label(
    marco_datos,
    text="Humedad: --",
    font=("Arial", 11)
)

etiqueta_humedad.pack(
    side="left",
    padx=15
)


etiqueta_intervalo = tk.Label(
    marco_datos,
    text="Intervalo: --",
    font=("Arial", 11)
)

etiqueta_intervalo.pack(
    side="left",
    padx=15
)


etiqueta_accion = tk.Label(
    marco_datos,
    text="Acción: --",
    font=("Arial", 11)
)

etiqueta_accion.pack(
    side="left",
    padx=15
)


# ==========================================
# RESUMEN GENERAL
# ==========================================

marco_resumen = tk.LabelFrame(
    marco_superior,
    text="Resumen general",
    font=("Arial", 11, "bold")
)

marco_resumen.pack(
    fill="x",
    pady=5
)


etiqueta_total = tk.Label(
    marco_resumen,
    text="TOTAL DE CASOS: 0",
    font=("Arial", 10, "bold")
)

etiqueta_total.pack(
    side="left",
    padx=10
)


etiqueta_i1 = tk.Label(
    marco_resumen,
    text="Intervalo 1: 0"
)

etiqueta_i1.pack(
    side="left",
    padx=10
)


etiqueta_i2 = tk.Label(
    marco_resumen,
    text="Intervalo 2: 0"
)

etiqueta_i2.pack(
    side="left",
    padx=10
)


etiqueta_i3 = tk.Label(
    marco_resumen,
    text="Intervalo 3: 0"
)

etiqueta_i3.pack(
    side="left",
    padx=10
)


etiqueta_i4 = tk.Label(
    marco_resumen,
    text="Intervalo 4: 0"
)

etiqueta_i4.pack(
    side="left",
    padx=10
)


# ==========================================
# BOTÓN ACTUALIZAR
# ==========================================

boton_actualizar = tk.Button(
    marco_superior,
    text="Actualizar análisis",
    font=("Arial", 11, "bold"),
    command=actualizar_interfaz
)

boton_actualizar.pack(
    pady=5
)


# ==========================================
# CONTENIDO PRINCIPAL
# ==========================================

marco_contenido = tk.Frame(
    ventana
)

marco_contenido.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# ==========================================
# RESUMEN DE TEMPERATURA SELECCIONADA
# ==========================================

marco_seleccionado = tk.LabelFrame(
    marco_contenido,
    text="Resumen de la temperatura seleccionada",
    font=("Arial", 11, "bold")
)

marco_seleccionado.pack(
    fill="x",
    pady=5
)


resumen_seleccionado = tk.Text(
    marco_seleccionado,
    height=5,
    font=("Arial", 10)
)

resumen_seleccionado.pack(
    fill="x",
    padx=5,
    pady=5
)


# ==========================================
# INFORMACIÓN GENERAL
# ==========================================

marco_texto_general = tk.LabelFrame(
    marco_contenido,
    text="Información general",
    font=("Arial", 11, "bold")
)

marco_texto_general.pack(
    fill="x",
    pady=5
)


resumen_general = tk.Text(
    marco_texto_general,
    height=4,
    font=("Arial", 10)
)

resumen_general.pack(
    fill="x",
    padx=5,
    pady=5
)


# ==========================================
# MARCO DE LA GRÁFICA
# ==========================================

marco_grafica = tk.LabelFrame(
    marco_contenido,
    text="Gráfica de temperatura y humedad",
    font=("Arial", 12, "bold")
)

marco_grafica.pack(
    fill="both",
    expand=True,
    pady=5
)


# ==========================================
# CARGAR DATOS AL INICIAR
# ==========================================

actualizar_interfaz()


# ==========================================
# INICIAR VENTANA
# ==========================================

ventana.mainloop()