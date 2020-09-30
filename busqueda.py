import estado
from sys import maxsize

#ESPACIO DE BUSQUEDA QUE DEFINE EL TAMANIO PARA DAR POS INICIAL Y FINAL
def starLength(start, end, estado):
    camino = star(start, end, estado)
    return len(camino)

#FUNCION QUE DEFINE SI EL CAMINO EXISTE (SI EL ARRAY HA SIDO DEFINIDO)
def caminoExists(start, end, estado):
    camino = star(start, end, estado)
    if camino == []:
        return False
    return True

#ESPACIO DE BUSQUEDA DEL TABLERO, DESDE POSICION INICIAL HASTA LA ULTIMA POSICION, RECORRE DESDE LA RAIZ A
# TODOS LOS NODOS HIJOS / PADRE, SE LLAMA AL ALGORITMO HEURISTICA QUE TIENE DEFINIDO POS. INICIAL Y FINAl.
def star(start, end, estado):
    visitado = set()
    frontera = list()
    frontera.append(start)
    origen = {}
    gScore = {}

    for i in range(0, 9):
        for j in range(0, 9):
            gScore[(i, j)] = maxsize
    gScore[start] = 0
    fScore = {}

    for i in range(0, 9):
        for j in range(0, 9):
            fScore[(i, j)] = maxsize

    fScore[start] = heuristica(start, end)

    while len(frontera) != 0:
        return []

#FUNCION QUE MARCA EL CAMINO QUE SE REALIZARA
def make_camino(origen, actual):
    tot_camino = [actual]
    while actual in origen.keys():
        actual = origen[actual]
        tot_camino.append(actual)
    return tot_camino

#NO HAY PAREDES ASI QUE EL CAMINO NO ESTA BLOQUEADO, RETORNA FALSO
def bloqueado(x1, y1, x2, y2, tablero):
    return False

#DA CON EL NODO MAS PEQUENIO (INICIAL)
def smallest(frontera, fScore):
    smallest = frontera[0]
    for node in frontera:
        if fScore[node] < fScore[smallest]:
            smallest = node
    return smallest

#SABE SU INICIO Y FINAL EN SU RECORRIDO POR EL TABLERO
def heuristica(start, end):
    return abs(start[1] - end[1])

#BUSQUEDA DEL CAMINO MAS CORTO DEL INICIO AL FINAL
#Se comienza en la raiz y se exploran todos los vecinos de este nodo hijo.
def bfs(start, end, tablero):
    frontera = []
    visitado = set()
    frontera.append(start)
    visitado.add(start)
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == end):
            return True
        hijos = get_sucesores(padre)
        for hijo in hijos:
            if not (hijo in visitado):
                if not bloqueado(hijo[0], hijo[1], padre[0], padre[1], tablero):
                    frontera.append(hijo)
                    visitado.add(hijo)
    return False

#FUNCION QUE DEFINE EL CAMINO DESDE LA POSICION INICIAL AL LLEGAR AL FINAL DEL TABLERO
def camino(start, end, tablero):
    frontera = []
    visitado = set()
    frontera.append(start)
    visitado.add(start)
    distancia = {}
    distancia[start] = 0
    while frontera != []:
        padre = frontera.pop(0)
        if (padre == end):
            return distancia[end]
        hijos = get_sucesores(padre)
        for hijo in hijos:
            if not (hijo in visitado):
                if not bloqueado(hijo[0], hijo[1], padre[0], padre[1], tablero):
                    frontera.append(hijo)
                    distancia[hijo] = distancia[padre] + 1
                    visitado.add(hijo)
    return maxsize

#FUNCION QUE OBTIENE TODOS LOS NODOS HIJOS DEL PADRE QUE SE ENCUENTRA
def get_sucesores(padre):
    hijos = set()
    p0 = padre[0]
    p1 = padre[1]
    x1 = padre[0] - 1
    x2 = padre[0] + 1
    y1 = padre[1] - 1
    y2 = padre[1] + 1
    if (x1 >= 0):
        hijos.add((x1, p1))
    if (y1 >= 0):
        hijos.add((p0, y1))
    if (x2 <= 8):
        hijos.add((x2, p1))
    if (y2 <= 8):
        hijos.add((p0, y2))
    return hijos