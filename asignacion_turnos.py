import itertools
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. DATOS DEL PROBLEMA
# ==========================================
empleados = {
    "Ana": {"preferencia": "mañana", "guardia_fin_semana": False},
    "Luis": {"preferencia": "tarde", "guardia_fin_semana": True},
    "Carlos": {"preferencia": "noche", "guardia_fin_semana": False},
    "María": {"preferencia": "mañana", "guardia_fin_semana": True}
}

turnos = ["mañana", "tarde", "noche", "mixto"]
nombres_empleados = list(empleados.keys())

# Requerimiento: al menos 2 empleados deben hacer guardia fines de semana
guardias_requeridas = 2

# Puntuación de satisfacción según preferencia
def calcular_satisfaccion(empleado, turno):
    preferencia = empleados[empleado]["preferencia"]
    if turno == preferencia:
        return 10  # Máxima satisfacción
    elif turno == "mixto":
        return 5   # Satisfacción media
    else:
        return 1   # Mínima satisfacción


def evaluar_asignacion(asignacion):
    """Calcula la satisfacción total de una asignación"""
    satisfaccion_total = 0
    detalles = []
    guardias_asignadas = 0
    
    for empleado, turno in asignacion:
        sat = calcular_satisfaccion(empleado, turno)
        hace_guardia = empleados[empleado]["guardia_fin_semana"]
        
        if hace_guardia:
            guardias_asignadas += 1
            sat += 2  # Bonificación por hacer guardia
        
        satisfaccion_total += sat
        detalles.append((empleado, turno, sat, hace_guardia))
    
    # Penalización si no se cumplen las guardias requeridas
    if guardias_asignadas < guardias_requeridas:
        satisfaccion_total -= 50  # Penalización severa
    
    return satisfaccion_total, detalles, guardias_asignadas


# ==========================================
# 2. BÚSQUEDA EXHAUSTIVA (FUERZA BRUTA)
# ==========================================
print("\n===== BÚSQUEDA DE LA MEJOR ASIGNACIÓN =====")

mejor_asignacion = []
mejor_satisfaccion = -1
mejor_detalles = []
mejor_guardias = 0

# Probar todas las permutaciones de asignaciones
for permutacion in itertools.permutations(turnos):
    asignacion = list(zip(nombres_empleados, permutacion))
    satisfaccion, detalles, guardias = evaluar_asignacion(asignacion)
    
    if satisfaccion > mejor_satisfaccion:
        mejor_satisfaccion = satisfaccion
        mejor_asignacion = asignacion
        mejor_detalles = detalles
        mejor_guardias = guardias

# ==========================================
# 3. MOSTRAR RESULTADOS
# ==========================================
print("\n===== MEJOR ASIGNACIÓN ENCONTRADA =====")
for empleado, turno, sat, hace_guardia in mejor_detalles:
    guardia_text = " (Guardia fin de semana)" if hace_guardia else ""
    print(f"{empleado}: {turno} (Satisfacción: {sat}){guardia_text}")

print(f"\nGuardias asignadas: {mejor_guardias}/{guardias_requeridas}")
print(f"Satisfacción total: {mejor_satisfaccion}")
print(f"Requisito de guardias: {'CUMPLIDO' if mejor_guardias >= guardias_requeridas else 'NO CUMPLIDO'}")

# ==========================================
# 4. VENTANA TKINTER CON DIAGRAMA DE PASTEL
# ==========================================
import math

def dibujar_pie_chart(canvas, centro_x, centro_y, radio, datos):
    """Dibuja un diagrama de pastel en un canvas de tkinter"""
    total = sum(d[1] for d in datos)
    angulo_inicio = 0
    segmentos = []  # Guardar información de cada segmento
    
    for etiqueta, valor, color in datos:
        angulo = (valor / total) * 360
        angulo_fin = angulo_inicio + angulo
        porcentaje = (valor / total) * 100
        
        # Dibujar el segmento
        segmento_id = canvas.create_arc(
            centro_x - radio, centro_y - radio,
            centro_x + radio, centro_y + radio,
            start=angulo_inicio, extent=angulo,
            fill=color, outline="white", width=2
        )
        
        # Guardar información del segmento
        segmentos.append({
            'id': segmento_id,
            'angulo_inicio': angulo_inicio,
            'angulo_fin': angulo_fin,
            'etiqueta': etiqueta,
            'valor': valor,
            'porcentaje': porcentaje,
            'color': color
        })
        
        # Calcular posición para la etiqueta (fuera del pastel)
        medio_rad = math.radians(angulo_inicio + angulo/2)
        etiqueta_x = centro_x + (radio * 1.25) * math.cos(medio_rad)
        etiqueta_y = centro_y - (radio * 1.25) * math.sin(medio_rad)
        
        # Etiqueta fuera del pastel con letra negra
        canvas.create_text(etiqueta_x, etiqueta_y, text=etiqueta, 
                         font=('Arial', 11, 'bold'), fill="black")
        
        angulo_inicio = angulo_fin
    
    return segmentos, total

def mostrar_resultados_tkinter():
    # Crear ventana principal
    root = tk.Tk()
    root.title("Asignación de Turnos - Diagrama de Pastel")
    root.geometry("900x650")
    
    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Título
    ttk.Label(main_frame, text="Distribución de Satisfacción por Empleado", 
              font=('Arial', 14, 'bold')).pack(pady=(0, 15))
    
    # Frame superior: pastel y tabla
    top_frame = ttk.Frame(main_frame)
    top_frame.pack(fill=tk.BOTH, expand=True)
    
    # Frame para el canvas del pastel
    canvas_frame = ttk.Frame(top_frame)
    canvas_frame.pack(side=tk.LEFT, padx=10)
    
    canvas = tk.Canvas(canvas_frame, width=400, height=300, bg="white")
    canvas.pack()
    
    # Etiqueta para mostrar porcentaje al pasar el mouse
    porcentaje_label = tk.Label(canvas_frame, text="Pasa el cursor sobre un segmento", 
                               font=('Arial', 10), bg="white")
    porcentaje_label.pack(pady=5)
    
    # Datos para el pastel (satisfacción de cada empleado)
    datos_pastel = []
    colores = ["#2ecc71", "#3498db", "#9b59b6", "#e67e22"]
    
    for i, (empleado, turno, sat, hace_guardia) in enumerate(mejor_detalles):
        datos_pastel.append((empleado, sat, colores[i % len(colores)]))
    
    # Dibujar el pastel y obtener segmentos
    segmentos, total = dibujar_pie_chart(canvas, 200, 150, 120, datos_pastel)
    
    # Función para detectar el segmento bajo el cursor
    def on_mouse_move(event):
        x, y = event.x, event.y
        centro_x, centro_y = 200, 150
        radio = 120
        
        # Calcular distancia desde el centro
        dx = x - centro_x
        dy = y - centro_y
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia > radio:
            porcentaje_label.config(text="Pasa el cursor sobre un segmento")
            return
        
        # Calcular ángulo del cursor
        angulo = math.degrees(math.atan2(dy, dx))
        if angulo < 0:
            angulo += 360
        
        # Encontrar el segmento correspondiente
        for seg in segmentos:
            if seg['angulo_inicio'] <= angulo <= seg['angulo_fin']:
                porcentaje_label.config(
                    text=f"{seg['etiqueta']}: {seg['porcentaje']:.1f}% (Sat: {seg['valor']})",
                    fg=seg['color']
                )
                return
        
        porcentaje_label.config(text="Pasa el cursor sobre un segmento")
    
    canvas.bind('<Motion>', on_mouse_move)
    
    # Frame para la tabla
    table_frame = ttk.LabelFrame(top_frame, text="Tabla de Asignación", padding=10)
    table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
    
    # Crear tabla con Treeview
    tree = ttk.Treeview(table_frame, columns=('Empleado', 'Turno', 'Satisfacción', 'Guardia'), show='headings', height=6)
    tree.heading('Empleado', text='Empleado')
    tree.heading('Turno', text='Turno')
    tree.heading('Satisfacción', text='Satisfacción')
    tree.heading('Guardia', text='Guardia')
    
    tree.column('Empleado', width=100)
    tree.column('Turno', width=100)
    tree.column('Satisfacción', width=80)
    tree.column('Guardia', width=80)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Llenar la tabla
    for empleado, turno, sat, hace_guardia in mejor_detalles:
        guardia_text = "Sí" if hace_guardia else "No"
        tree.insert('', 'end', values=(empleado, turno, sat, guardia_text))
    
    # Frame para resumen
    summary_frame = ttk.LabelFrame(main_frame, text="Resumen", padding=10)
    summary_frame.pack(fill=tk.X, pady=(15, 0))
    
    ttk.Label(summary_frame, text=f"Guardias asignadas: {mejor_guardias}/{guardias_requeridas}", 
              font=('Arial', 10)).pack(anchor=tk.W)
    ttk.Label(summary_frame, text=f"Satisfacción total: {mejor_satisfaccion}", 
              font=('Arial', 10)).pack(anchor=tk.W)
    
    estado = "CUMPLIDO ✓" if mejor_guardias >= guardias_requeridas else "NO CUMPLIDO ✗"
    estado_color = "green" if mejor_guardias >= guardias_requeridas else "red"
    tk.Label(summary_frame, text=f"Requisito de guardias: {estado}", 
             font=('Arial', 10, 'bold'), fg=estado_color).pack(anchor=tk.W, pady=(5, 0))
    
    # Botón para cerrar
    ttk.Button(main_frame, text="Cerrar", command=root.destroy).pack(pady=10)
    
    # Iniciar loop de tkinter
    root.mainloop()

# Ejecutar la ventana
mostrar_resultados_tkinter()
