# ==========================================================
# SISTEMA DE REVISIÓN DE EQUIPO DE CÓMPUTO
# ==========================================================

print("==============================================")
print("       REVISIÓN DE EQUIPO DE CÓMPUTO")
print("==============================================")

# ----------------------------------------------------------
# 1. ENTRADA DE DATOS
# ----------------------------------------------------------

electricidad = input("¿El equipo tiene electricidad? (si/no): ").lower()
enciende = input("¿El equipo enciende? (si/no): ").lower()
imagen = input("¿El equipo muestra imagen? (si/no): ").lower()
teclado = input("¿El teclado funciona? (si/no): ").lower()
mouse = input("¿El mouse funciona? (si/no): ").lower()
monitor = input("¿El monitor está conectado? (si/no): ").lower()
internet = input("¿El equipo tiene conexión a Internet? (si/no): ").lower()
sistema = input("¿El sistema operativo inicia correctamente? (si/no): ").lower()
sonido = input("¿El equipo tiene sonido? (si/no): ").lower()


# ----------------------------------------------------------
# 2. PROPOSICIONES
# ----------------------------------------------------------

P = electricidad == "si"
Q = enciende == "si"
R = imagen == "si"
S = teclado == "si"
T = mouse == "si"
U = monitor == "si"
V = internet == "si"
W = sistema == "si"
X = sonido == "si"


# ----------------------------------------------------------
# 3. MOSTRAR PROPOSICIONES
# ----------------------------------------------------------

print("\n" + "=" * 55)
print("              PROPOSICIONES")
print("=" * 55)

print("P - Tiene electricidad :", P)
print("Q - Enciende           :", Q)
print("R - Muestra imagen     :", R)
print("S - Teclado funciona   :", S)
print("T - Mouse funciona     :", T)
print("U - Monitor conectado  :", U)
print("V - Tiene Internet     :", V)
print("W - Sistema inicia     :", W)
print("X - Tiene sonido       :", X)


# ----------------------------------------------------------
# 4. OPERACIONES LÓGICAS
# ----------------------------------------------------------

print("\n" + "=" * 55)
print("             OPERACIONES LÓGICAS")
print("=" * 55)

print("Teclado Y mouse funcionan:", S and T)
print("Monitor conectado Y tiene Internet:", U and V)
print("Sistema inicia Y tiene sonido:", W and X)
print("Teclado O mouse funciona:", S or T)
print(" Monitor conectado O tiene Internet:", U or V)

print("Si el monitor está conectado, entonces tiene Internet:", (not U) or V)
print("Si el sistema inicia, entonces tiene sonido:", (not W) or X)

print("Teclado si y solo si mouse funciona:", S == T)
print("Sistema inicia si y solo si tiene sonido:", W == X)


# ----------------------------------------------------------
# 5. DECISIÓN FINAL
# ----------------------------------------------------------

print("\n" + "=" * 55)
print("                RESULTADO")
print("=" * 55)

if not P:
    print("El equipo NO puede ser revisado, no tiene electricidad.")
elif not Q:
    print("El equipo NO puede ser revisado, no enciende.")
elif not R:
    print("El equipo NO puede ser revisado, no muestra imagen.")
else:
    print("El equipo puede ser revisado.")

