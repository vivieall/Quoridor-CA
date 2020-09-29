# By Angel - Team Group()
import estado
from sys import maxint


def starLength(start, end, estado):
    path = star(start, end, estado)
    return len(path)


def pathExists(start, end, estado):
    path = star(start, end, estado)
    if path == []:
        return False
    return True


def star(start, end, estado):
    visitado = set()
    frontera = list()
    frontera.append(start)
    origen = {}

    gScore = {}
    for i in range(0, 9):
        for j in range(0, 9):
            gScore[(i, j)] = maxint
    gScore[start] = 0

    fScore = {}
    fScore = {}
    for i in range(0, 9):
        for j in range(0, 9):
            fScore[(i, j)] = maxint

    fScore[start] = heuristica(start, end)

    while len(frontera) != 0:
        current = smallest(frontera, fScore)
        if current == end:
            return make_path(origen, current)

        frontera.remove(current)
        visitado.add(current)

        children = get_successors(current)
        for child in children:
            if not (child in visitado):
                if not blocked(child[0], child[1], current[0], current[1], estado):
                    frontera.append(child)

            tent_gScore = gScore[current] + 1
            if tent_gScore >= gScore[child]:
                continue

            origen[child] = current
            gScore[child] = tent_gScore
            fScore[child] = gScore[child] + heuristica(child, end)
    return []


def make_path(origen, current):
    tot_path = [current]
    while current in origen.keys():
        current = origen[current]
        tot_path.append(current)
    return tot_path


def blocked(x1, y1, x2, y2, tablero):
    return False


def smallest(frontera, fScore):
    smallest = frontera[0]
    for node in frontera:
        if fScore[node] < fScore[smallest]:
            smallest = node
    return smallest


def heuristica(start, end):
    return abs(start[1] - end[1])


def bfs(start, end, tablero):
    frontera = []
    visitado = set()
    frontera.append(start)
    visitado.add(start)
    while frontera != []:
        parent = frontera.pop(0)
        if (parent == end):
            return True

        children = get_successors(parent)
        for child in children:
            if not (child in visitado):
                if not blocked(child[0], child[1], parent[0], parent[1], tablero):
                    frontera.append(child)
                    visitado.add(child)
    return False


def path(start, end, tablero):
    frontera = []
    visitado = set()
    frontera.append(start)
    visitado.add(start)
    distancia = {}
    distancia[start] = 0
    while frontera != []:
        parent = frontera.pop(0)
        if (parent == end):
            return distancia[end]

        children = get_successors(parent)
        for child in children:
            if not (child in visitado):
                if not blocked(child[0], child[1], parent[0], parent[1], tablero):
                    frontera.append(child)
                    distancia[child] = distancia[parent] + 1
                    visitado.add(child)

    return maxint


def get_successors(parent):
    children = set()
    p0 = parent[0]
    p1 = parent[1]
    x1 = parent[0] - 1
    x2 = parent[0] + 1
    y1 = parent[1] - 1
    y2 = parent[1] + 1
    if (x1 >= 0):
        children.add((x1, p1))
    if (y1 >= 0):
        children.add((p0, y1))
    if (x2 <= 8):
        children.add((x2, p1))
    if (y2 <= 8):
        children.add((p0, y2))
    return children