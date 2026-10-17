# Laberinto: BFS, DFS y costo uniforme

Solucion de un laberinto con tres estrategias de busqueda:

- **BFS (anchura):** encuentra un camino con el menor numero de movimientos
  cuando todos los movimientos tienen el mismo costo.
- **DFS (profundidad):** devuelve el primer camino que encuentra; no garantiza
  que sea el mas corto ni el de menor costo.
- **Costo uniforme (UCS):** siempre expande el estado de menor costo acumulado
  y encuentra el camino de menor costo cuando los costos son no negativos.

## Modelo de costos

Entrar en una celda normal o en la meta cuesta **1**. Entrar en una celda de
penalizacion (`2`) cuesta **3**. Entrar en un premio (`3`) cuesta **0.25**,
es decir, una cuarta parte del costo normal. La celda inicial no suma costo.

El programa se ejecuta con:

```text
python laberinto.py
```

Se puede elegir `1/BFS`, `2/DFS` o `3/UCS`. Al terminar se muestra el camino
seleccionado, sus movimientos, su costo acumulado y una tabla comparativa de
los tres metodos.

## Analisis final y comparacion

Los tres algoritmos pueden llegar a la misma meta, pero optimizan criterios
distintos:

| Metodo | Criterio que optimiza | Garantia | Uso de memoria |
| --- | --- | --- | --- |
| BFS | Cantidad de movimientos | Camino mas corto si los movimientos cuestan igual | Alta |
| DFS | Ninguno; depende del orden de vecinos | No garantiza optimalidad | Menor que BFS en muchos casos |
| Costo uniforme | Costo acumulado | Camino de menor costo | Alta |

En este laberinto, BFS es la referencia para medir la distancia en
movimientos. DFS puede producir un recorrido mas largo porque toma decisiones
en profundidad antes de explorar alternativas. UCS puede elegir mas
movimientos que BFS si con ello evita la penalizacion; por eso es la opcion
adecuada cuando las celdas tienen costos diferentes. Si todas las celdas
tuvieran el mismo costo, UCS y BFS encontrarian caminos optimos equivalentes
(salvo empates por el orden de exploracion). En este caso, los premios hacen
que UCS pueda preferir un camino que atraviese una celda `3`, aunque tenga mas
movimientos, porque su costo acumulado puede ser menor.

La comparacion que imprime el programa permite verificar directamente esta
diferencia: **movimientos** mide la longitud del recorrido y **costo
acumulado** mide el esfuerzo real definido por el problema. No debe
considerarse automaticamente mejor el camino con menos movimientos; la
decision depende de la metrica solicitada.
