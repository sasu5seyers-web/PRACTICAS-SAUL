import itertools
import math
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. DATOS DEL PROBLEMA
# ==========================================
# Puntos: almacén y clientes
puntos = {
    "Almacén": (0, 0),
    "A": (2, 6),
    "B": (5, 3),
    "C": (6, 8),
    "D": (8, 2),
    "E": (1, 1)
}

nombres_puntos = list(puntos.keys())
clientes = ["A", "B", "C", "D", "E"]  # Sin incluir el almacén

# ==========================================
# 2. CÁLCULO DE DISTANCIAS
# ==========================================
def calcular_distancia(punto1, punto2):
    """Calcula la distancia euclidiana entre dos puntos"""
    x1, y1 = punto1
    x2, y2 = punto2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def crear_matriz_distancias():
    """Crea la matriz de distancias entre todos los puntos"""
    matriz = {}
    for p1 in nombres_puntos:
        matriz[p1] = {}
        for p2 in nombres_puntos:
            if p1 == p2:
                matriz[p1][p2] = 0
            else:
                matriz[p1][p2] = calcular_distancia(puntos[p1], puntos[p2])
    return matriz


# ==========================================
# 3. BÚSQUEDA DE LA MEJOR RUTA (FUERZA BRUTA)
# ==========================================
def evaluar_ruta(ruta, matriz):
    """Calcula la distancia total de una ruta"""
    distancia_total = 0
    ruta_completa = ["Almacén"] + list(ruta) + ["Almacén"]  # Empieza y termina en almacén
    
    for i in range(len(ruta_completa) - 1):
        origen = ruta_completa[i]
        destino = ruta_completa[i + 1]
        distancia_total += matriz[origen][destino]
    
    return distancia_total, ruta_completa


print("\n===== OPTIMIZACIÓN DE RUTA DE ROBOT REPARTIDOR =====")
print(f"Puntos: {nombres_puntos}")
print(f"Total de permutaciones: {math.factorial(5)} = 120")

# Crear matriz de distancias
matriz = crear_matriz_distancias()

print("\n===== MATRIZ DE DISTANCIAS =====")
# Imprimir encabezados
print(f"{'Punto':<10}", end="")
for p in nombres_puntos:
    print(f"{p:<10}", end="")
print()

# Imprimir filas
for p1 in nombres_puntos:
    print(f"{p1:<10}", end="")
    for p2 in nombres_puntos:
        print(f"{matriz[p1][p2]:<10.2f}", end="")
    print()

# Buscar la mejor ruta y guardar todas las rutas
mejor_ruta = []
mejor_distancia = float('inf')
mejor_ruta_completa = []
todas_las_rutas = []
contador = 0

print("\n===== BUSCANDO LA MEJOR RUTA =====")

for permutacion in itertools.permutations(clientes):
    contador += 1
    distancia, ruta_completa = evaluar_ruta(permutacion, matriz)
    todas_las_rutas.append((ruta_completa, distancia))
    
    if distancia < mejor_distancia:
        mejor_distancia = distancia
        mejor_ruta = permutacion
        mejor_ruta_completa = ruta_completa

print(f"Total de combinaciones evaluadas: {contador}")
print(f"\n===== MEJOR RUTA ENCONTRADA =====")
print("Ruta:", " -> ".join(mejor_ruta_completa))
print(f"Distancia total: {mejor_distancia:.2f}")

# ==========================================
# 4. VENTANA TKINTER CON GRÁFICA Y TABLA
# ==========================================
def dibujar_grafica(canvas, ruta_optima, todas_rutas):
    """Dibuja la gráfica con los puntos, todas las rutas y la ruta óptima"""
    # Escala para dibujar
    escala = 40
    offset_x = 50
    offset_y = 350
    
    # Dibujar ejes
    canvas.create_line(offset_x, offset_y, offset_x + 400, offset_y, arrow=tk.LAST, width=2)
    canvas.create_line(offset_x, offset_y, offset_x, offset_y - 350, arrow=tk.LAST, width=2)
    canvas.create_text(offset_x + 420, offset_y, text="X", font=('Arial', 12, 'bold'))
    canvas.create_text(offset_x, offset_y - 370, text="Y", font=('Arial', 12, 'bold'))
    
    # Dibujar todas las rutas (en gris muy tenue)
    print("Dibujando todas las rutas...")
    for idx, (ruta, distancia) in enumerate(todas_rutas):
        for i in range(len(ruta) - 1):
            origen = puntos[ruta[i]]
            destino = puntos[ruta[i + 1]]
            
            x1 = offset_x + origen[0] * escala
            y1 = offset_y - origen[1] * escala
            x2 = offset_x + destino[0] * escala
            y2 = offset_y - destino[1] * escala
            
            canvas.create_line(x1, y1, x2, y2, fill="#e0e0e0", width=1)
    
    # Dibujar puntos
    for nombre, (x, y) in puntos.items():
        px = offset_x + x * escala
        py = offset_y - y * escala
        
        color = "red" if nombre == "Almacén" else "blue"
        canvas.create_oval(px - 8, py - 8, px + 8, py + 8, fill=color, outline="black", width=2)
        canvas.create_text(px, py - 20, text=nombre, font=('Arial', 10, 'bold'))
        canvas.create_text(px, py + 20, text=f"({x},{y})", font=('Arial', 8))
    
    # Dibujar ruta óptima (en verde más grueso)
    for i in range(len(ruta_optima) - 1):
        origen = puntos[ruta_optima[i]]
        destino = puntos[ruta_optima[i + 1]]
        
        x1 = offset_x + origen[0] * escala
        y1 = offset_y - origen[1] * escala
        x2 = offset_x + destino[0] * escala
        y2 = offset_y - destino[1] * escala
        
        canvas.create_line(x1, y1, x2, y2, fill="green", width=4, arrow=tk.LAST)
    
    # Dibujar números de orden en la ruta óptima
    for i, nombre in enumerate(ruta_optima):
        x, y = puntos[nombre]
        px = offset_x + x * escala
        py = offset_y - y * escala
        canvas.create_text(px + 15, py + 15, text=str(i), font=('Arial', 10, 'bold'), fill="green")


def mostrar_resultados_tkinter():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Optimización de Ruta - Robot Repartidor")
    root.geometry("1200x900")
    
    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Título
    ttk.Label(main_frame, text="Optimización de Ruta de Robot Repartidor", 
              font=('Arial', 16, 'bold')).pack(pady=(0, 15))
    
    # Frame superior: gráfica y tabla
    top_frame = ttk.Frame(main_frame)
    top_frame.pack(fill=tk.BOTH, expand=True)
    
    # Frame para la gráfica
    graph_frame = ttk.LabelFrame(top_frame, text="Gráfica de Ruta Óptima", padding=10)
    graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
    canvas = tk.Canvas(graph_frame, width=500, height=400, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Dibujar la gráfica con todas las rutas
    dibujar_grafica(canvas, mejor_ruta_completa, todas_las_rutas)
    
    # Frame para la tabla de distancias
    table_frame = ttk.LabelFrame(top_frame, text="Matriz de Distancias", padding=10)
    table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
    
    # Crear tabla con Treeview
    tree = ttk.Treeview(table_frame, columns=nombres_puntos, show='headings', height=7)
    
    for nombre in nombres_puntos:
        tree.heading(nombre, text=nombre)
        tree.column(nombre, width=70, anchor=tk.CENTER)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Llenar la tabla
    for p1 in nombres_puntos:
        fila = [p1]
        for p2 in nombres_puntos:
            fila.append(f"{matriz[p1][p2]:.2f}")
        tree.insert('', 'end', values=fila)
    
    # Frame inferior para tabla de todas las combinaciones
    bottom_frame = ttk.LabelFrame(main_frame, text="Las 120 Combinaciones", padding=10)
    bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
    
    # Crear tabla scrollable para todas las combinaciones
    combo_tree = ttk.Treeview(bottom_frame, columns=('Ruta', 'Distancia'), show='headings', height=15)
    combo_tree.heading('Ruta', text='Ruta')
    combo_tree.heading('Distancia', text='Distancia')
    combo_tree.column('Ruta', width=400)
    combo_tree.column('Distancia', width=100, anchor=tk.CENTER)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=combo_tree.yview)
    combo_tree.configure(yscrollcommand=scrollbar.set)
    
    combo_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Llenar tabla con todas las combinaciones
    for idx, (ruta, distancia) in enumerate(todas_las_rutas, 1):
        ruta_str = " -> ".join(ruta)
        combo_tree.insert('', 'end', values=(f"{idx}. {ruta_str}", f"{distancia:.2f}"))
    
    # Frame para resultados
    result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=15)
    result_frame.pack(fill=tk.X, pady=(15, 0))
    
    ttk.Label(result_frame, text=f"Ruta óptima: {' -> '.join(mejor_ruta_completa)}", 
              font=('Arial', 12, 'bold')).pack(anchor=tk.W)
    ttk.Label(result_frame, text=f"Distancia total: {mejor_distancia:.2f} unidades", 
              font=('Arial', 12, 'bold')).pack(anchor=tk.W)
    ttk.Label(result_frame, text=f"Total de combinaciones evaluadas: {contador}", 
              font=('Arial', 10)).pack(anchor=tk.W)
    
    # Botón para cerrar
    ttk.Button(main_frame, text="Cerrar", command=root.destroy).pack(pady=10)
    
    # Iniciar loop de tkinter
    root.mainloop()

# Ejecutar la ventana
mostrar_resultados_tkinter()
