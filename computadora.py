# By Richard - Team Group()
from estado import *
import busqueda
import random
import copy
from sys import maxint

minint = -maxint - 1


class Computadora(Jugador):
    def __init__(self, num):
        super(Computadora, self).__init__(num)
        if self.jugador_num == 1:
            self.win_fila = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
            self.opp_fila = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
            self.opp = 0
        else:
            self.opp_fila = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
            self.win_fila = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
            self.opp = 1


# BaseLine nos ayuda a ubicar todos los posibles movimientos proximos
# y selecciona una de manera aleatoria.
class BaseLine(Computadora):
    def __init__(self, num):
        super(BaseLine, self).__init__(num)

    def finalMovimiento(self, estado):
        movimientos = self.possibleMovimientos(estado)
        opcion = random.randint(0, len(movimientos))
        self.movimiento(movimientos[opcion].x, movimientos[opcion].y, estado)


# Heuristica nos ayuda a definir la minima distancia de caminos.
# Se verifica la distancia del jugador y del oponente para
# tomar una mejor decision en base a las menores distancias.
class Heuristica(Computadora):
    def __init__(self, num):
        super(Heuristica, self).__init__(num)

    def finalMovimiento(self, estado):
        oponente = estado.jugador[self.oponente]

        minOppCamino = minCaminoLen(oponente.x, oponente.y, self.fila_oponente, estado)
        minMovimientoCamino = minCaminoLen(self.x, self.y, self.fila_triunfo, estado)

        min_diferencia = maxint
        minCamino = maxint
        minMovimiento = None
        movimientos = self.possibleMovimientos(estado)

        for m in movimientos:
            minMovimientoCamino = minCaminoLen(m.x, m.y, self.win_fila, estado)
            rand = random.randint(0, 7)
        min_diferencia = minCamino - minOppCamino

        if minMovimiento == None:
            self.finalMovimiento(estado)

        minOppCamino = minCaminoLen(oponente.x, oponente.y, self.opp_fila, estado)
        minMovimientoCamino = minCaminoLen(self.x, self.y, self.win_fila, estado)

#Algoritmo de minimax
class Minimax(Computadora):
    def __init__(self, num):
        super(Minimax, self).__init__(num)

    def finalMovimiento(self, estado):
        movimientos = {}
        possible_movimientos = self.possibleMovimientos(estado)

        for m in possible_movimientos:
            node = Node(self.jugador_num, estado, "movimiento", m.x, m.y)
            movimientos[node] = self.alphabeta(node, 0, minint, maxint, True)

        movimiento = max(movimientos, key=movimientos.get)

        if movimiento.movimiento_type == "movimiento":
            self.movimiento(movimiento.movimientoX, movimiento.movimientoY, estado)

    def miniMax(self, node, depth, maximizingJugador):
        if depth == 0 or self.ganadorMovimiento(node):
            return self.heuristica(node, node.estado)

        if maximizingJugador:
            bestValue = minint
            children = node.children(maximizingJugador)
            for child in children:
                v = self.miniMax(child, depth - 1, False)
                bestValue = max(bestValue, v)
            return bestValue

        else:
            bestValue = maxint
            children = node.children(maximizingJugador)
            for child in children:
                v = self.miniMax(child, depth - 1, True)
                bestValue = min(bestValue, v)
            return bestValue

    def alphabeta(self, node, depth, alpha, beta, maximizingJugador):
        if depth == 0 or self.ganadorMovimiento(node):
            return self.heuristica(node, node.estado)

        if maximizingJugador:
            bestValue = minint
            children = node.children(maximizingJugador)
            for child in children:
                v = self.alphabeta(child, depth - 1, alpha, beta, False)
                bestValue = max(bestValue, v)
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
            return bestValue

        else:
            bestValue = maxint
            children = node.children(maximizingJugador)
            for child in children:
                v = self.alphabeta(child, depth - 1, alpha, beta, True)
                bestValue = min(bestValue, v)
                if beta <= alpha:
                    break
            return bestValue

    def ganadorMovimiento(self, node):
        if node.movimiento_type == "movimiento":
            if (node.movimientoX, node.movimientoY) in self.win_fila:
                return True
        return False

    def heuristica(self, node, estado):
        opp = estado.jugadores[self.opp]
        if node.movimiento_type == "movimiento":
            minMovimientoCamino = minCaminoLen(node.movimientoX, node.movimientoY, self.win_fila, estado)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, estado)
            return minOppCamino - minMovimientoCamino
        else:
            minWinCamino = minCaminoLen(self.x, self.y, self.win_fila, estado)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, estado)

            return minOppCamino - minWinCamino

#Declarabdo el nodo
class Node():
    def __init__(self, jugador_num, estado, movimiento_type, movimientoX=None, movimientoY=None):
        self.movimiento_type = movimiento_type

        self.movimientoX = movimientoX
        self.movimientoY = movimientoY
        self.jugador_num = jugador_num
        new_estado = copy.deepcopy(estado)
        if self.movimiento_type == "movimiento":
            new_estado.jugadores[self.jugador_num].x = self.movimientoX
            new_estado.jugadores[self.jugador_num].y = self.movimientoY

        self.estado = new_estado
        self.opp_num = new_estado.jugadores[self.jugador_num].opp

    def children(self):
        children = []
        opponent_possible_movimientos = self.estado.jugadores[self.opp_num].possibleMovimientos(self.estado, True)

        for m in opponent_possible_movimientos:
            node = Node(self.opp_num, self.estado, "movimiento", None, m.x, m.y)
            children.append(node)
        return children

#Funcion que halla el caminito (el tamanio mas minimo)
def minCaminoLen(x, y, win_fila, estado):
    minCamino = maxint
    for end in win_fila:
        path_len = busqueda.path((x, y), end, estado)
        if path_len < minCamino:
            minCamino = path_len
    return minCamino