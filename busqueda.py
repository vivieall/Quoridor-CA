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

    fScore[start] = heuristic(start, end)

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
            fScore[child] = gScore[child] + heuristic(child, end)
    return []


def make_path(origen, current):
    tot_path = [current]
    while current in origen.keys():
        current = origen[current]
        tot_path.append(current)
    return tot_path


def blocked(x1, y1, x2, y2, tablero):
    return False
