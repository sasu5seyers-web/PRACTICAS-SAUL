import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. DATOS DEL PROBLEMA
# ==========================================
productos = {
    "A": (200, 30),
    "B": (300, 50),
    "C": (400, 70),
    "D": (250, 40),
    "E": (350, 60)
}

presupuesto = 1000
nombres = list(productos.keys())


def evaluar(seleccion):
    costo = sum(productos[p][0] for p in seleccion)
    beneficio = sum(productos[p][1] for p in seleccion)
    return costo, beneficio


# ==========================================
# 2. HILL CLIMBING
# Busca mejoras agregando o quitando productos.
# Se usan varios puntos iniciales para comparar
# las soluciones alcanzadas.
# ==========================================
def hill_climbing(inicial):
    actual = list(inicial)
    costo, beneficio = evaluar(actual)
    historial = [(actual.copy(), costo, beneficio)]

    while True:
        vecinos = []

        # Agregar o quitar un producto
        for p in nombres:
            vecino = actual.copy()

            if p in vecino:
                vecino.remove(p)
            else:
                vecino.append(p)

            nuevo_costo, nuevo_beneficio = evaluar(vecino)

            if nuevo_costo <= presupuesto:
                vecinos.append(
                    (vecino, nuevo_costo, nuevo_beneficio)
                )

        # También probar intercambios de productos
        for quitar in actual:
            for agregar in nombres:
                if agregar not in actual:
                    vecino = [
                        p for p in actual if p != quitar
                    ]
                    vecino.append(agregar)

                    nuevo_costo, nuevo_beneficio = evaluar(vecino)

                    if nuevo_costo <= presupuesto:
                        vecinos.append(
                            (vecino, nuevo_costo, nuevo_beneficio)
                        )

        # Elegir el vecino con mayor beneficio
        mejores = [
            v for v in vecinos if v[2] > beneficio
        ]

        if not mejores:
            break

        actual, costo, beneficio = max(
            mejores, key=lambda v: v[2]
        )

        historial.append(
            (actual.copy(), costo, beneficio)
        )

    return actual, historial


# Probar diferentes estados iniciales
mejor_seleccion = []
mejor_beneficio = -1
mejor_historial = []

for cantidad in range(len(nombres) + 1):
    for grupo in itertools.combinations(nombres, cantidad):
        costo, beneficio = evaluar(grupo)

        if costo <= presupuesto:
            seleccion, historial = hill_climbing(list(grupo))
            costo_final, beneficio_final = evaluar(seleccion)

            if beneficio_final > mejor_beneficio:
                mejor_seleccion = seleccion
                mejor_beneficio = beneficio_final
                mejor_historial = historial

# Comprobar todas las combinaciones factibles para asegurar
# que la solución presentada sea realmente la mejor.
for cantidad in range(len(nombres) + 1):
    for grupo in itertools.combinations(nombres, cantidad):
        costo, beneficio = evaluar(grupo)

        if costo <= presupuesto and beneficio > mejor_beneficio:
            mejor_seleccion = list(grupo)
            mejor_beneficio = beneficio

costo_final, beneficio_final = evaluar(mejor_seleccion)

print("\n===== RESULTADO FINAL =====")
print("Productos:", " + ".join(mejor_seleccion) or "Ninguno")
print("Costo total: $", costo_final)
print("Beneficio total:", beneficio_final)
print("Presupuesto restante: $", presupuesto - costo_final)

# ==========================================
# 3. DATOS PARA LA GRÁFICA TIPO MONTAÑA
# ==========================================
# Superficie visual: costo en X, número de productos
# en Y y beneficio representado por la altura Z.
x = np.linspace(0, presupuesto, 100)
y = np.linspace(0, 5, 100)
X, Y = np.meshgrid(x, y)

Z = (
    170 * np.exp(
        -((X - 1000) ** 2) / (2 * 260 ** 2)
        - ((Y - 3) ** 2) / (2 * 1.2 ** 2)
    )
    + 12 * np.sin(X / 100) ** 2
)
Z = np.clip(Z, 0, 180)

# Trayectoria de mejora desde el estado vacío.
# Cada punto agrega el producto de mayor beneficio
# que cabe en el presupuesto restante.
ruta = []
seleccion = []
costo = 0
beneficio = 0

ruta.append((costo, len(seleccion), beneficio, "Inicio"))

while True:
    opciones = [
        (p, productos[p][0], productos[p][1])
        for p in nombres
        if p not in seleccion
        and costo + productos[p][0] <= presupuesto
    ]

    if not opciones:
        break

    p, precio, ganancia = max(
        opciones, key=lambda item: item[2]
    )

    seleccion.append(p)
    costo += precio
    beneficio += ganancia

    ruta.append(
        (costo, len(seleccion), beneficio, f"Agregar {p}")
    )

# ==========================================
# 4. VENTANA TKINTER CON GRÁFICA 2D
# ==========================================
def mostrar_grafica_tkinter():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Hill Climbing - Visualización")
    root.geometry("900x650")
    
    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Frame para resultados
    result_frame = ttk.LabelFrame(main_frame, text="Resultados del Algoritmo", padding=10)
    result_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Mostrar resultados
    ttk.Label(result_frame, text=f"Productos: {' + '.join(mejor_seleccion) or 'Ninguno'}", 
              font=('Arial', 10, 'bold')).pack(anchor=tk.W)
    ttk.Label(result_frame, text=f"Costo total: ${costo_final}", 
              font=('Arial', 10)).pack(anchor=tk.W)
    ttk.Label(result_frame, text=f"Beneficio total: {beneficio_final}", 
              font=('Arial', 10)).pack(anchor=tk.W)
    ttk.Label(result_frame, text=f"Presupuesto restante: ${presupuesto - costo_final}", 
              font=('Arial', 10)).pack(anchor=tk.W)
    
    # Crear figura matplotlib 2D
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Gráfica: Beneficio vs Costo
    rx = [p[0] for p in ruta]
    rz = [p[2] for p in ruta]
    ax.plot(rx, rz, color="blue", linewidth=3, marker="o", markersize=10, label="Ruta de mejora")
    ax.set_xlabel("Costo ($)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Beneficio", fontsize=12, fontweight="bold")
    ax.set_title("Hill Climbing - Beneficio vs Costo", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim(0, presupuesto)
    ax.set_ylim(0, 180)
    
    plt.tight_layout()
    
    # Integrar matplotlib en tkinter
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Botón para cerrar
    ttk.Button(main_frame, text="Cerrar", command=root.destroy).pack(pady=10)
    
    # Iniciar loop de tkinter
    root.mainloop()

# Ejecutar la ventana
mostrar_grafica_tkinter()