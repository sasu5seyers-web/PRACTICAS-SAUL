import matplotlib.pyplot as plt
import numpy as np

# Puntos
A = (1, 2)
B = (5, 5)
C = (B[0], A[1])  # Punto intermedio para formar el triángulo

# Distancias
distancia_euclidiana = int(np.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2))
distancia_manhattan = abs(B[0] - A[0]) + abs(B[1] - A[1])

print("Distancia Euclidiana:", distancia_euclidiana)
print("Distancia Manhattan:", distancia_manhattan)

# Crear cuadrícula
plt.figure(figsize=(6,6))
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xticks(range(0, 7))
plt.yticks(range(0, 7))

# Dibujar puntos
plt.scatter(A[0], A[1], color='red', label=f"A{A}")
plt.scatter(B[0], B[1], color='blue', label=f"B{B}")
plt.scatter(C[0], C[1], color='purple', label=f"C{C}")

# Dibujar triángulo
plt.plot([A[0], C[0]], [A[1], C[1]], color='green')   # Cateto horizontal
plt.plot([C[0], B[0]], [C[1], B[1]], color='green')   # Cateto vertical
plt.plot([A[0], B[0]], [A[1], B[1]], color='orange', label=f"Hipotenusa = {distancia_euclidiana}")

plt.legend()
plt.title("Triángulo entre A y B")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
