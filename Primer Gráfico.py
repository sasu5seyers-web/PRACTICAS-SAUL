"""
==============================================================
Primer Gráfico con Matplotlib
==============================================================
# Materia: Extracción de Conocimiento en Bases de Datos
# Objetivo: Aprender a construir una gráfica utilizando
# Matplotlib.
==============================================================
"""
# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Configurar estilo profesional
plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams['font.family'] = 'DejaVu Sans'
mpl.rcParams['font.size'] = 11

# ==========================================================
# DATOS
# ==========================================================
# Meses del año
meses = [
    "Ene", "Feb", "Mar", "Abr",
    "May", "Jun", "Jul", "Ago",
    "Sep", "Oct", "Nov", "Dic"
]
# Ventas simuladas (miles de pesos)
ventas = [85, 90, 96, 105, 120, 135,
          150, 148, 160, 172, 181, 195]

# ==========================================================
# CONFIGURACIÓN GENERAL ESTABLECE EL TAMAÑO DE LA FIGURA
# ==========================================================
plt.figure(figsize=(14, 8), facecolor='#f8f9fa')
ax = plt.gca()
ax.set_facecolor('#ffffff')

# ==========================================================
# GRÁFICA PRINCIPAL DIBUJA LA LINEA CON COLOR, GROSOR Y MARCADORES PERSONALIZADOS
# ==========================================================
# Crear gradiente para el relleno
colors = ['#1f77b4', '#1f77b4']
n_bins = 100
cmap_name = 'blue_gradient'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

plt.plot(
    meses,
    ventas,
    color="#2563eb",
    linewidth=3,
    marker="o",
    markersize=9,
    markerfacecolor="white",
    markeredgecolor="#2563eb",
    markeredgewidth=2.5,
    label="Ventas mensuales",
    zorder=5,
    solid_capstyle='round'
)
plt.fill_between(
    meses,
    ventas,
    alpha=0.25,
    color="#2563eb",
    zorder=3
)

# ==========================================================
# TÍTULO PRINCIPAL
# ==========================================================
plt.suptitle(
    "Ventas Mensuales de la Empresa EcoMart",
    fontsize=22,
    fontweight="bold",
    y=0.98
)

# ==========================================================
# SUBTÍTULO CON CONTEXTO
# ==========================================================
plt.title(
    "Periodo Enero - Diciembre 2026",
    fontsize=14,
    color="gray",
    pad=10
)

# ==========================================================
# ETIQUETAS EN LOS EJES INDICANDO LA VARIABLE Y SUS UNIDADES
# ==========================================================
plt.xlabel(
    "Mes",
    fontsize=14,
    fontweight="semibold",
    color='#374151'
)
plt.ylabel(
    "Ventas (Miles de pesos)",
    fontsize=14,
    fontweight="semibold",
    color='#374151'
)

# ==========================================================
# CUADRÍCULA FACILITA LA LECTURA DE LOS VALORES
# ==========================================================
plt.grid(
    linestyle='-',
    linewidth=0.8,
    alpha=0.4,
    color='#e5e7eb',
    zorder=1
)

# ==========================================================
# LEYENDA IDENTIFICA LOS ELEMENTOS REPRESENTADOS
# ==========================================================
plt.legend(
    fontsize=11,
    loc='upper left',
    framealpha=0.95,
    shadow=True,
    facecolor='white',
    edgecolor='#e5e7eb',
    frameon=True
)

# ==========================================================
# ANOTACIONES MUESTRA EL VALOR EXACTO DE CADA OBSERVACIÓN
# ==========================================================
for x, y in zip(meses, ventas):
    plt.text(
        x,
        y + 4,
        str(y),
        fontsize=9.5,
        ha="center",
        va="bottom",
        fontweight="bold",
        color="#1f2937",
        bbox=dict(
            boxstyle='round,pad=0.3',
            facecolor='white',
            edgecolor='#e5e7eb',
            alpha=0.9,
            linewidth=1
        ),
        zorder=6
    )

# ==========================================================
# LÍNEA DE PROMEDIO COMPARA CADA DATO CON EL PROMEDIO ANUAL
# ==========================================================
promedio = np.mean(ventas)
plt.axhline(
    promedio,
    color="#f59e0b",
    linestyle='--',
    linewidth=2.5,
    alpha=0.8,
    label="Promedio",
    zorder=4
)
plt.text(
    10.5,
    promedio + 5,
    f"Promedio = {promedio:.1f} miles de pesos",
    color="#f59e0b",
    fontsize=11,
    fontweight="bold",
    backgroundcolor='white',
    bbox=dict(
        boxstyle='round,pad=0.4',
        facecolor='white',
        edgecolor='#f59e0b',
        alpha=0.95,
        linewidth=1.5
    ),
    zorder=6
)

# ==========================================================
# DESTACAR EL MÁXIMO DESTACA EL PUNTO DE MAYOR VENTA MEDIANTE UN MARCADOR Y UNA FLECHA
# ==========================================================
indice_max = np.argmax(ventas)
plt.scatter(
    meses[indice_max],
    ventas[indice_max],
    color="#ef4444",
    s=220,
    zorder=10,
    edgecolor="white",
    linewidth=2.5,
    label="Máximo",
    alpha=0.9
)
plt.annotate(
    "Mayor venta del año",
    xy=(meses[indice_max], ventas[indice_max]),
    xytext=(8, 205),
    arrowprops=dict(
        arrowstyle="->",
        color="#ef4444",
        lw=2.5,
        connectionstyle="arc3,rad=0.2"
    ),
    fontsize=12,
    fontweight="bold",
    color="#ef4444",
    backgroundcolor='white',
    bbox=dict(
        boxstyle='round,pad=0.5',
        facecolor='white',
        edgecolor='#ef4444',
        alpha=0.95,
        linewidth=1.5
    ),
    zorder=11
)

# ==========================================================
# PIE DE FIGURA INDICA LA FUENTE DE LOS DATOS Y EL AUTOR
# ==========================================================
plt.figtext(
    0.01,
    0.01,
    "Conclusión: Estimado de las ventas | Elaboración propia | UTVT",
    fontsize=10,
    color="gray"
)

# ==========================================================
# QUITAR MARCO SUPERIOR Y DERECHO
# ==========================================================
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color('#9ca3af')
ax.spines["bottom"].set_color('#9ca3af')
ax.spines["left"].set_linewidth(1.2)
ax.spines["bottom"].set_linewidth(1.2)
ax.tick_params(axis='both', colors='#6b7280', labelsize=10)

# ==========================================================
# AJUSTAR ESPACIOS
# ==========================================================
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# ==========================================================
# MOSTRAR
# ==========================================================
plt.show()