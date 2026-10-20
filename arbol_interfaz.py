import tkinter as tk
from tkinter import messagebox


arbol = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': [],
    'E': ['F'],
    'F': []
}


def encontrar_rutas(arbol, inicio):
    rutas = []

    def recorrer(nodo, ruta):
        ruta.append(nodo)

        if not arbol[nodo]:
            rutas.append(ruta.copy())
        else:
            for siguiente in arbol[nodo]:
                recorrer(siguiente, ruta)

        ruta.pop()

    recorrer(inicio, [])

    return rutas


rutas = encontrar_rutas(arbol, 'A')

print("Rutas posibles:")

for ruta in rutas:
    print(" -> ".join(ruta))


# ==========================================
# INTERFAZ GRÁFICA
# ==========================================

ventana = tk.Tk()
ventana.title("Árbol y rutas")
ventana.geometry("850x750")


titulo = tk.Label(
    ventana,
    text="ÁRBOL DE RUTAS",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=15)


# ==========================================
# CAMBIAR RUTAS
# ==========================================

marco = tk.Frame(ventana)
marco.pack(pady=5)


tk.Label(
    marco,
    text="Nodo:"
).grid(
    row=0,
    column=0,
    padx=5
)


entrada_nodo = tk.Entry(
    marco,
    width=10
)

entrada_nodo.grid(
    row=0,
    column=1,
    padx=5
)


tk.Label(
    marco,
    text="Conexiones:"
).grid(
    row=0,
    column=2,
    padx=5
)


entrada_conexiones = tk.Entry(
    marco,
    width=20
)

entrada_conexiones.grid(
    row=0,
    column=3,
    padx=5
)


# ==========================================
# AGREGAR / CAMBIAR RUTA
# ==========================================

def cambiar_ruta():

    nodo = entrada_nodo.get().upper()
    conexiones = entrada_conexiones.get().upper()

    if nodo == "":
        messagebox.showwarning(
            "Aviso",
            "Escribe un nodo"
        )
        return

    if conexiones == "":
        arbol[nodo] = []

    else:

        lista = conexiones.split(",")

        arbol[nodo] = lista

        for hijo in lista:

            if hijo not in arbol:
                arbol[hijo] = []

    actualizar_inicio()

    entrada_nodo.delete(0, tk.END)
    entrada_conexiones.delete(0, tk.END)

    messagebox.showinfo(
        "Listo",
        "Ruta actualizada"
    )


# ==========================================
# ELIMINAR RUTA
# ==========================================

def eliminar_ruta():

    nodo = entrada_nodo.get().upper()
    conexion = entrada_conexiones.get().upper()

    if nodo == "":
        messagebox.showwarning(
            "Aviso",
            "Escribe el nodo"
        )
        return

    if nodo not in arbol:
        messagebox.showwarning(
            "Aviso",
            "Ese nodo no existe"
        )
        return

    # Si no se escribe una conexión,
    # se eliminan todas las conexiones del nodo

    if conexion == "":

        arbol[nodo] = []

    else:

        if conexion in arbol[nodo]:

            arbol[nodo].remove(conexion)

        else:

            messagebox.showwarning(
                "Aviso",
                "Esa conexión no existe"
            )

            return

    actualizar_inicio()

    entrada_nodo.delete(0, tk.END)
    entrada_conexiones.delete(0, tk.END)

    messagebox.showinfo(
        "Listo",
        "Ruta eliminada"
    )


# ==========================================
# BOTONES PARA MODIFICAR RUTAS
# ==========================================

boton_cambiar = tk.Button(
    marco,
    text="Agregar / Cambiar ruta",
    font=("Arial", 10),
    width=18,
    command=cambiar_ruta
)

boton_cambiar.grid(
    row=1,
    column=1,
    padx=5,
    pady=10
)


boton_eliminar = tk.Button(
    marco,
    text="Eliminar ruta",
    font=("Arial", 10),
    width=18,
    command=eliminar_ruta
)

boton_eliminar.grid(
    row=1,
    column=3,
    padx=5,
    pady=10
)


# ==========================================
# SELECCIONAR NODO DE INICIO
# ==========================================

marco_inicio = tk.Frame(ventana)
marco_inicio.pack(pady=15)


tk.Label(
    marco_inicio,
    text="Comenzar desde:"
).grid(
    row=0,
    column=0,
    padx=5
)


inicio = tk.StringVar()
inicio.set("A")


lista_inicio = tk.OptionMenu(
    marco_inicio,
    inicio,
    *arbol.keys()
)

lista_inicio.grid(
    row=0,
    column=1,
    padx=5
)


def actualizar_inicio():

    menu = lista_inicio["menu"]

    menu.delete(
        0,
        "end"
    )

    for nodo in arbol.keys():

        menu.add_command(
            label=nodo,
            command=lambda valor=nodo: inicio.set(valor)
        )

    if inicio.get() not in arbol:

        if len(arbol) > 0:

            inicio.set(
                list(arbol.keys())[0]
            )


# ==========================================
# CANVAS
# ==========================================

canvas = tk.Canvas(
    ventana,
    width=800,
    height=350,
    bg="white"
)

canvas.pack(pady=10)


# ==========================================
# DIBUJAR ÁRBOL
# ==========================================

def dibujar_arbol():

    canvas.delete("all")

    posiciones = {
        "A": (400, 50),
        "B": (250, 140),
        "C": (550, 140),
        "D": (250, 240),
        "E": (550, 240),
        "F": (550, 320)
    }

    nodos = list(arbol.keys())

    x = 100
    y = 100

    for nodo in nodos:

        if nodo not in posiciones:

            posiciones[nodo] = (x, y)

            x += 120

            if x > 700:

                x = 100
                y += 100


    # Dibujar conexiones

    for nodo in arbol:

        if nodo not in posiciones:
            continue

        x1, y1 = posiciones[nodo]

        for hijo in arbol[nodo]:

            if hijo not in posiciones:
                continue

            x2, y2 = posiciones[hijo]

            canvas.create_line(
                x1,
                y1 + 25,
                x2,
                y2 - 25,
                width=2
            )


    # Dibujar nodos

    for nodo in posiciones:

        x, y = posiciones[nodo]

        canvas.create_oval(
            x - 25,
            y - 25,
            x + 25,
            y + 25,
            fill="lightblue",
            outline="black",
            width=2
        )

        canvas.create_text(
            x,
            y,
            text=nodo,
            font=("Arial", 16, "bold")
        )


# ==========================================
# MOSTRAR RUTAS
# ==========================================

def mostrar_rutas():

    nodo_inicio = inicio.get()

    if nodo_inicio not in arbol:

        messagebox.showwarning(
            "Aviso",
            "El nodo de inicio no existe"
        )

        return

    rutas = encontrar_rutas(
        arbol,
        nodo_inicio
    )

    texto_rutas.delete(
        "1.0",
        tk.END
    )

    texto_rutas.insert(
        tk.END,
        "Rutas desde " + nodo_inicio + ":\n\n"
    )

    for ruta in rutas:

        texto_rutas.insert(
            tk.END,
            " -> ".join(ruta) + "\n"
        )


# ==========================================
# BOTONES PRINCIPALES
# ==========================================

marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=5)


boton_arbol = tk.Button(
    marco_botones,
    text="Mostrar árbol",
    font=("Arial", 11),
    width=18,
    command=dibujar_arbol
)

boton_arbol.grid(
    row=0,
    column=0,
    padx=10
)


boton_rutas = tk.Button(
    marco_botones,
    text="Mostrar rutas",
    font=("Arial", 11),
    width=18,
    command=mostrar_rutas
)

boton_rutas.grid(
    row=0,
    column=1,
    padx=10
)


# ==========================================
# RESULTADO
# ==========================================

texto_rutas = tk.Text(
    ventana,
    width=60,
    height=8,
    font=("Arial", 12)
)

texto_rutas.pack(pady=15)


# ==========================================
# EJECUTAR
# ==========================================

ventana.mainloop()