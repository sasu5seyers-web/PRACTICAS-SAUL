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