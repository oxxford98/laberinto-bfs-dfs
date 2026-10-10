# 0 = camino, 1 = muro, 2 = penalizacion, 3 = premio, 9 = meta.
LABERINTO = [
    [0, 3, 0, 0, 0, 0, 0, 1, 0],
    [2, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 3],
    [0, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 2, 9],
]
TAMANO = 9
INICIO = (0, 0)
META = (8, 8)

OPERADORES = {
    "w": (-1, 0),
    "s": (1, 0),
    "a": (0, -1),
    "d": (0, 1),
}


def es_celda_valida(laberinto, posicion):
    """Indica si una posicion esta dentro del tablero y no es un muro."""
    fila, columna = posicion
    return (
        0 <= fila < TAMANO
        and 0 <= columna < TAMANO
        and laberinto[fila][columna] != 1
    )


def construir_grafo(laberinto):
    """Crea el grafo: estado actual -> movimientos y estados siguientes."""
    grafo = {}

    # ESTADOS: cada celda que no es muro se representa como (fila, columna).
    for fila in range(TAMANO):
        for columna in range(TAMANO):
            if laberinto[fila][columna] == 1:
                continue

            estado = (fila, columna)
            vecinos = {}
            # OPERADORES: se agregan solo los movimientos hacia celdas validas.
            for movimiento, cambio in OPERADORES.items():
                siguiente = (fila + cambio[0], columna + cambio[1])
                if es_celda_valida(laberinto, siguiente):
                    vecinos[movimiento] = siguiente
            grafo[estado] = vecinos

    return grafo


def reconstruir_camino(predecesor, nodo):
    camino = []
    while nodo is not None:
        camino.append(nodo)
        nodo = predecesor[nodo]
    return list(reversed(camino))


def bfs_camino(grafo, inicio, objetivo):
    """Busca el camino con menos movimientos mediante una cola."""
    cola = [inicio]
    visitados = {inicio}
    predecesor = {inicio: None}

    while cola:
        nodo = cola.pop(0)
        if nodo == objetivo:
            return reconstruir_camino(predecesor, nodo)

        for vecino in grafo[nodo].values():
            if vecino not in visitados:
                visitados.add(vecino)
                predecesor[vecino] = nodo
                cola.append(vecino)
    return None


def dfs_camino(grafo, inicio, objetivo):
    """Busca un camino mediante una pila, como en el ejemplo DFS."""
    pila = [inicio]
    visitados = {inicio}
    predecesor = {inicio: None}

    while pila:
        nodo = pila.pop(-1)
        if nodo == objetivo:
            return reconstruir_camino(predecesor, nodo)

        for vecino in grafo[nodo].values():
            if vecino not in visitados:
                visitados.add(vecino)
                predecesor[vecino] = nodo
                pila.append(vecino)
    return None


def mostrar_camino(camino):
    posiciones = set(camino)
    print("\nS = inicio | * = camino | 1 = muro | 9 = meta")
    for fila, celdas in enumerate(LABERINTO):
        vista = []
        for columna, valor in enumerate(celdas):
            posicion = (fila, columna)
            if posicion == INICIO:
                vista.append("S")
            elif posicion == META:
                vista.append("9")
            elif posicion in posiciones:
                vista.append("*")
            else:
                vista.append(str(valor))
        print(" ".join(vista))


def main():
    print("Busqueda de un camino en el laberinto")
    print("1. BFS (anchura): camino con menos movimientos")
    print("2. DFS (profundidad): primer camino encontrado")
    print("Los premios y penalizaciones son transitables; no se optimizan coins.")

    while True:
        opcion = input("Que algoritmo deseas usar (1/BFS o 2/DFS): ").strip().lower()
        if opcion in ("1", "bfs"):
            algoritmo = bfs_camino
            nombre = "BFS"
            break
        if opcion in ("2", "dfs"):
            algoritmo = dfs_camino
            nombre = "DFS"
            break
        print("Opcion invalida. Escribe 1, BFS, 2 o DFS.")

    grafo = construir_grafo(LABERINTO)
    camino = algoritmo(grafo, INICIO, META)
    if camino is None:
        print(f"{nombre}: no se encontro un camino hasta la meta.")
        return

    print(f"\nCamino encontrado con {nombre} (fila, columna):")
    print(camino)
    print(f"Cantidad de movimientos: {len(camino) - 1}")
    mostrar_camino(camino)


if __name__ == "__main__":
    main()
