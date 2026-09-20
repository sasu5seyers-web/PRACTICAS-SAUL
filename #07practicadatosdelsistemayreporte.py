# ============================================
# SISTEMA EXPERTO DE DIAGNÓSTICO
# ============================================

print("SISTEMA DE DIAGNÓSTICO")

fiebre = input("¿Tiene fiebre? (s/n): ")
tos = input("¿Tiene tos? (s/n): ")
dolor = input("¿Tiene dolor de garganta? (s/n): ")

if fiebre == "s" and tos == "s":

    diagnostico = "Posible infección respiratoria"

elif tos == "s" and dolor == "s":

    diagnostico = "Posible irritación respiratoria"

elif fiebre == "s":

    diagnostico = "Se recomienda valoración profesional"

else:

    diagnostico = "No se identificó un patrón"

print("\nResultado:")
print(diagnostico)


#Implementación de mejores decisiones para un mejor resultado.