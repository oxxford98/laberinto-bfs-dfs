# 0 = camino, 1 = muro, 2 = penalizacion, 3 = premio, 9 = meta.
# Busqueda A* con tres heuristicas: Manhattan, Euclidiana y Chebyshev.
# El programa verifica si cada heuristica es admisible, si es monotona
# (consistente) y cual domina a las otras.
import heapq
import math


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


# ----------------------------------------------------------------------
# ESTADOS, OPERADORES Y COSTOS (se conservan del codigo original)
# ----------------------------------------------------------------------
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
    for fila in range(TAMANO):
        for columna in range(TAMANO):
            if laberinto[fila][columna] == 1:
                continue
            estado = (fila, columna)
            vecinos = {}
            for movimiento, cambio in OPERADORES.items():
                siguiente = (fila + cambio[0], columna + cambio[1])
                if es_celda_valida(laberinto, siguiente):
                    vecinos[movimiento] = siguiente
            grafo[estado] = vecinos
    return grafo


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


def reconstruir_camino(predecesor, nodo):
    camino = []
    while nodo is not None:
        camino.append(nodo)
        nodo = predecesor[nodo]
    return list(reversed(camino))


# ----------------------------------------------------------------------
# HEURISTICAS
# ----------------------------------------------------------------------
def h_manhattan(posicion, meta):
    """h1: suma de las diferencias en filas y columnas."""
    return abs(posicion[0] - meta[0]) + abs(posicion[1] - meta[1])


def h_euclidiana(posicion, meta):
    """h2: distancia en linea recta."""
    return math.sqrt((posicion[0] - meta[0]) ** 2 + (posicion[1] - meta[1]) ** 2)


def h_chebyshev(posicion, meta):
    """h3: la mayor de las diferencias en filas o columnas."""
    return max(abs(posicion[0] - meta[0]), abs(posicion[1] - meta[1]))


HEURISTICAS = {
    "h1 Manhattan": h_manhattan,
    "h2 Euclidiana": h_euclidiana,
    "h3 Chebyshev": h_chebyshev,
}


# ----------------------------------------------------------------------
# ALGORITMO A*
# ----------------------------------------------------------------------
def a_estrella(grafo, inicio, objetivo, laberinto, heuristica, mostrar=True):
    """
    A*: f(n) = g(n) + h(n).
    g(n) = costo real acumulado desde el inicio.
    h(n) = estimacion de lo que falta hasta la meta.
    Devuelve el camino y la cantidad de nodos expandidos.
    """
    h_inicio = heuristica(inicio, objetivo)
    frontera = [(h_inicio, 0, 0, inicio)]   # (f, desempate, g, nodo)
    costos = {inicio: 0}
    predecesor = {inicio: None}
    contador = 1
    expandidos = 0

    if mostrar:
        print("\n--- PRUEBA DE ESCRITORIO A* ---")
        print(f"Inicio {inicio}: g = 0, h = {h_inicio:.2f}, f = {h_inicio:.2f}")

    while frontera:
        f_actual, _, g_actual, nodo = heapq.heappop(frontera)
        if g_actual != costos[nodo]:
            continue   # entrada vieja de la frontera, ya hay un camino mejor

        expandidos += 1
        h_actual = heuristica(nodo, objetivo)
        if mostrar:
            print(
                f"\nPaso {expandidos}: expande {nodo} | "
                f"g = {g_actual:.2f}, h = {h_actual:.2f}, f = {f_actual:.2f}"
            )

        if nodo == objetivo:
            if mostrar:
                print(">> Se llego a la META.")
            return reconstruir_camino(predecesor, nodo), expandidos

        for movimiento, vecino in grafo[nodo].items():
            nuevo_g = g_actual + costo_de_celda(laberinto, vecino)
            if nuevo_g < costos.get(vecino, float("inf")):
                costos[vecino] = nuevo_g
                predecesor[vecino] = nodo
                h_vecino = heuristica(vecino, objetivo)
                f_vecino = nuevo_g + h_vecino
                heapq.heappush(frontera, (f_vecino, contador, nuevo_g, vecino))
                contador += 1
                if mostrar:
                    print(
                        f"   {movimiento} -> {vecino}: g = {nuevo_g:.2f}, "
                        f"h = {h_vecino:.2f}, f = {f_vecino:.2f}"
                    )

        if mostrar:
            vista = sorted((f, n) for f, _, g, n in frontera if g == costos[n])
            texto = ", ".join(f"{n} f={f:.2f}" for f, n in vista)
            print(f"   Frontera: [{texto}]")

    return None, expandidos


# ----------------------------------------------------------------------
# VERIFICACIONES: ADMISIBLE, MONOTONA Y DOMINANTE
# ----------------------------------------------------------------------
def costos_reales_a_meta(grafo, laberinto, meta):
    """
    Calcula h*(n): el costo real minimo desde cada celda hasta la meta.
    Se hace una busqueda de costo uniforme "al reves", partiendo de la meta.
    Ir de v a u cuesta lo que cuesta entrar en u.
    """
    reales = {meta: 0}
    frontera = [(0, meta)]
    while frontera:
        costo_u, u = heapq.heappop(frontera)
        if costo_u != reales[u]:
            continue
        for v in grafo[u].values():
            nuevo = costo_u + costo_de_celda(laberinto, u)
            if nuevo < reales.get(v, float("inf")):
                reales[v] = nuevo
                heapq.heappush(frontera, (nuevo, v))
    return reales


def verificar_admisible(nombre, heuristica, reales, meta):
    """Admisible si h(n) <= h*(n) en TODAS las celdas."""
    print(f"\n=== ADMISIBILIDAD de {nombre}: h(n) <= h*(n) ===")
    print(f"{'Celda':<10}{'h(n)':>8}{'h*(n)':>9}   Cumple")
    fallas = 0
    for celda in sorted(reales):
        h = heuristica(celda, meta)
        real = reales[celda]
        cumple = h <= real + 1e-9
        if not cumple:
            fallas += 1
        print(f"{str(celda):<10}{h:>8.2f}{real:>9.2f}   {'SI' if cumple else 'NO  <-- sobreestima'}")
    es_admisible = fallas == 0
    print(
        f"Resultado: {nombre} "
        f"{'ES admisible' if es_admisible else f'NO es admisible ({fallas} celdas sobreestiman)'}"
    )
    return es_admisible


def verificar_monotona(nombre, heuristica, grafo, laberinto, meta):
    """Monotona si h(n) <= c(n, n') + h(n') para TODO par de vecinos."""
    print(f"\n=== MONOTONIA de {nombre}: h(n) <= c(n,n') + h(n') ===")
    revisados = 0
    fallas = 0
    for nodo, vecinos in grafo.items():
        for vecino in vecinos.values():
            revisados += 1
            h_n = heuristica(nodo, meta)
            c = costo_de_celda(laberinto, vecino)
            h_v = heuristica(vecino, meta)
            if h_n > c + h_v + 1e-9:
                fallas += 1
                print(
                    f"   Falla {nodo} -> {vecino}: "
                    f"{h_n:.2f} > {c:.2f} + {h_v:.2f} = {c + h_v:.2f}"
                )
    es_monotona = fallas == 0
    print(f"Pares revisados: {revisados} | Pares que fallan: {fallas}")
    print(
        f"Resultado: {nombre} "
        f"{'ES monotona' if es_monotona else 'NO es monotona'}"
    )
    return es_monotona


def verificar_dominancia(reales, meta, admisibles):
    """
    h_a domina a h_b si h_a(n) >= h_b(n) en todas las celdas.
    Formalmente la dominancia solo tiene sentido entre heuristicas ADMISIBLES.
    """
    print("\n=== DOMINANCIA: h_a(n) >= h_b(n) en todas las celdas ===")
    nombres = list(HEURISTICAS)
    for i, a in enumerate(nombres):
        for b in nombres[i + 1:]:
            a_sobre_b = all(HEURISTICAS[a](c, meta) >= HEURISTICAS[b](c, meta) for c in reales)
            b_sobre_a = all(HEURISTICAS[b](c, meta) >= HEURISTICAS[a](c, meta) for c in reales)
            if a_sobre_b and not b_sobre_a:
                texto = f"{a} domina a {b}"
            elif b_sobre_a and not a_sobre_b:
                texto = f"{b} domina a {a}"
            elif a_sobre_b and b_sobre_a:
                texto = f"{a} y {b} son iguales"
            else:
                texto = f"ninguna domina entre {a} y {b}"
            print(f"   {texto}")

    validas = [n for n in nombres if admisibles[n]]
    if len(validas) < 2:
        print(
            "Nota: la dominancia se define entre heuristicas ADMISIBLES. "
            f"Admisibles en este laberinto: {validas if validas else 'ninguna'}."
        )
        print(
            "La comparacion anterior muestra cual estima valores mas altos, "
            "pero como no son admisibles no se puede concluir que una sea mejor guia."
        )


# ----------------------------------------------------------------------
# PRESENTACION
# ----------------------------------------------------------------------
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
    print("Busqueda A* en el laberinto")
    print("f(n) = g(n) + h(n)")
    print("Costo: celda normal = 1, penalizacion = 3, premio = 0.25")
    print("1. h1 Manhattan:  |fila - fila_meta| + |col - col_meta|")
    print("2. h2 Euclidiana: raiz((fila - fila_meta)^2 + (col - col_meta)^2)")
    print("3. h3 Chebyshev:  max(|fila - fila_meta|, |col - col_meta|)")

    nombres = list(HEURISTICAS)
    while True:
        opcion = input("Que heuristica deseas usar (1, 2 o 3): ").strip()
        if opcion in ("1", "2", "3"):
            nombre = nombres[int(opcion) - 1]
            break
        print("Opcion invalida. Escribe 1, 2 o 3.")

    grafo = construir_grafo(LABERINTO)
    camino, expandidos = a_estrella(
        grafo, INICIO, META, LABERINTO, HEURISTICAS[nombre]
    )
    if camino is None:
        print(f"{nombre}: no se encontro un camino hasta la meta.")
        return

    print(f"\nCamino encontrado con A* + {nombre} (fila, columna):")
    print(camino)
    print(f"Cantidad de movimientos: {len(camino) - 1}")
    print(f"Costo acumulado: {costo_camino(LABERINTO, camino)}")
    print(f"Nodos expandidos: {expandidos}")
    mostrar_camino(camino)

    # Verificaciones de las tres heuristicas
    reales = costos_reales_a_meta(grafo, LABERINTO, META)
    print(f"\nCosto real optimo desde el inicio h*(S) = {reales[INICIO]:.2f}")

    admisibles = {}
    monotonas = {}
    for n, h in HEURISTICAS.items():
        admisibles[n] = verificar_admisible(n, h, reales, META)
        monotonas[n] = verificar_monotona(n, h, grafo, LABERINTO, META)
    verificar_dominancia(reales, META, admisibles)

    # Tabla comparativa
    print("\nComparacion de resultados")
    print(
        f"{'Heuristica':<16}{'Movim.':<8}{'Costo':<8}{'Expandidos':<12}"
        f"{'Admisible':<11}{'Monotona'}"
    )
    for n, h in HEURISTICAS.items():
        c, e = a_estrella(grafo, INICIO, META, LABERINTO, h, mostrar=False)
        print(
            f"{n:<16}{len(c) - 1:<8}{costo_camino(LABERINTO, c):<8.2f}{e:<12}"
            f"{'SI' if admisibles[n] else 'NO':<11}{'SI' if monotonas[n] else 'NO'}"
        )


if __name__ == "__main__":
    main()