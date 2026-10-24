# 0 = camino, 1 = muro, 2 = penalizacion, 3 = premio, 9 = meta.
import heapq


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

#
def costo_de_celda(laberinto, posicion):
    """Devuelve el costo de entrar a una celda."""
    valor = laberinto[posicion[0]][posicion[1]]
    if valor == 2:
        return 3
    if valor == 3:
        return 0.25
    return 1


def costo_camino(laberinto, camino):
    """Calcula el costo acumulado de un camino, sin contar la celda inicial."""
    if not camino:
        return None
    return sum(costo_de_celda(laberinto, posicion) for posicion in camino[1:])


def costo_uniforme_camino(grafo, inicio, objetivo, laberinto):
    """Busca el camino de menor costo acumulado usando una cola de prioridad."""
    frontera = [(0, 0, inicio)]
    costos = {inicio: 0}
    predecesor = {inicio: None}
    contador = 1

    while frontera:
        costo_actual, _, nodo = heapq.heappop(frontera)
        if costo_actual != costos[nodo]:
            continue
        if nodo == objetivo:
            return reconstruir_camino(predecesor, nodo)

        for vecino in grafo[nodo].values():
            nuevo_costo = costo_actual + costo_de_celda(laberinto, vecino)
            if nuevo_costo < costos.get(vecino, float("inf")):
                costos[vecino] = nuevo_costo
                predecesor[vecino] = nodo
                heapq.heappush(
                    frontera, (nuevo_costo, contador, vecino)
                )
                contador += 1
    return None


def comparar_algoritmos(grafo, laberinto, inicio, objetivo):
    """Ejecuta los tres métodos y devuelve sus métricas principales."""
    algoritmos = {
        "BFS": lambda: bfs_camino(grafo, inicio, objetivo),
        "DFS": lambda: dfs_camino(grafo, inicio, objetivo),
        "Costo uniforme": lambda: costo_uniforme_camino(
            grafo, inicio, objetivo, laberinto
        ),
    }
    resultados = {}
    for nombre, algoritmo in algoritmos.items():
        camino = algoritmo()
        resultados[nombre] = {
            "camino": camino,
            "movimientos": len(camino) - 1 if camino else None,
            "costo": costo_camino(laberinto, camino),
        }
    return resultados


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
    print("3. Costo uniforme: camino con menor costo acumulado")
    print("Costo: cada movimiento vale 1 y entrar en una penalizacion vale 3.")

    while True:
        opcion = input(
            "Que algoritmo deseas usar (1/BFS, 2/DFS o 3/UCS): "
        ).strip().lower()
        if opcion in ("1", "bfs"):
            algoritmo = bfs_camino
            nombre = "BFS"
            break
        if opcion in ("2", "dfs"):
            algoritmo = dfs_camino
            nombre = "DFS"
            break
        if opcion in ("3", "ucs", "costo uniforme", "costo_uniforme"):
            algoritmo = lambda grafo, inicio, meta: costo_uniforme_camino(
                grafo, inicio, meta, LABERINTO
            )
            nombre = "Costo uniforme"
            break
        print("Opcion invalida. Escribe 1/BFS, 2/DFS o 3/UCS.")

    grafo = construir_grafo(LABERINTO)
    camino = algoritmo(grafo, INICIO, META)
    if camino is None:
        print(f"{nombre}: no se encontro un camino hasta la meta.")
        return

    print(f"\nCamino encontrado con {nombre} (fila, columna):")
    print(camino)
    print(f"Cantidad de movimientos: {len(camino) - 1}")
    print(f"Costo acumulado: {costo_camino(LABERINTO, camino)}")
    mostrar_camino(camino)

    print("\nComparacion de resultados")
    print(f"{'Metodo':<18}{'Movimientos':<14}{'Costo acumulado'}")
    for metodo, resultado in comparar_algoritmos(
        grafo, LABERINTO, INICIO, META
    ).items():
        print(
            f"{metodo:<18}{resultado['movimientos']:<14}"
            f"{resultado['costo']:.2f}"
        )


if __name__ == "__main__":
    main()
