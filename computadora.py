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

    def finalMove(self, estado):
        moves = self.possibleMoves(estado)
        choice = random.randint(0, len(moves))
        self.move(moves[choice].x, moves[choice].y, estado)


# Heuristic nos ayuda a definir la minima distancia de caminos.
# Se verifica la distancia del jugador y del oponente para
# tomar una mejor decision en base a las menores distancias.
class Heuristic(Computadora):
    def __init__(self, num):
        super(Heuristic, self).__init__(num)

    def finalMove(self, estado):
        oponente = estado.jugador[self.oponente]

        minOppPath = minPathLen(oponente.x, oponente.y, self.fila_oponente, estado)
        minMovePath = minPathLen(self.x, self.y, self.fila_triunfo, estado)

        min_diff = maxint
        minPath = maxint
        minMove = None
        moves = self.possibleMoves(estado)

        for m in moves:
            minMovePath = minPathLen(m.x, m.y, self.win_fila, estado)
            rand = random.randint(0, 7)
        min_diff = minPath - minOppPath

        if minMove == None:
            self.finalMove(estado)

        minOppPath = minPathLen(oponente.x, oponente.y, self.opp_fila, estado)
        minMovePath = minPathLen(self.x, self.y, self.win_fila, estado)


class Minimax(Computadora):
    def __init__(self, num):
        super(Minimax, self).__init__(num)

    def finalMove(self, estado):
        moves = {}
        possible_moves = self.possibleMoves(estado)

        for m in possible_moves:
            node = Node(self.jugador_num, estado, "move", m.x, m.y)
            moves[node] = self.alphabeta(node, 0, minint, maxint, True)

        move = max(moves, key=moves.get)

        if move.move_type == "move":
            self.move(move.moveX, move.moveY, estado)

    def miniMax(self, node, depth, maximizingJugador):
        if depth == 0 or self.winningMove(node):
            return self.heuristic(node, node.estado)

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
        if depth == 0 or self.winningMove(node):
            return self.heuristic(node, node.estado)

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

    def winningMove(self, node):
        if node.move_type == "move":
            if (node.moveX, node.moveY) in self.win_fila:
                return True
        return False

    def heuristic(self, node, estado):
        opp = estado.jugadores[self.opp]
        if node.move_type == "move":
            minMovePath = minPathLen(node.moveX, node.moveY, self.win_fila, estado)
            minOppPath = minPathLen(opp.x, opp.y, self.opp_fila, estado)
            return minOppPath - minMovePath
        else:

            minWinPath = minPathLen(self.x, self.y, self.win_fila, estado)
            minOppPath = minPathLen(opp.x, opp.y, self.opp_fila, estado)

            return minOppPath - minWinPath


class Node():
    def __init__(self, jugador_num, estado, move_type, moveX=None, moveY=None):
        self.move_type = move_type

        self.moveX = moveX
        self.moveY = moveY
        self.jugador_num = jugador_num
        new_estado = copy.deepcopy(estado)
        if self.move_type == "move":
            new_estado.jugadores[self.jugador_num].x = self.moveX
            new_estado.jugadores[self.jugador_num].y = self.moveY

        self.estado = new_estado
        self.opp_num = new_estado.jugadores[self.jugador_num].opp

    def children(self):
        children = []
        opponent_possible_moves = self.estado.jugadores[self.opp_num].possibleMoves(self.estado, True)

        for m in opponent_possible_moves:
            node = Node(self.opp_num, self.estado, "move", None, m.x, m.y)
            children.append(node)
        return children


def minPathLen(x, y, win_fila, estado):
    minPath = maxint
    for end in win_fila:
        path_len = busqueda.path((x, y), end, estado)
        if path_len < minPath:
            minPath = path_len
    return minPath
