import busqueda
import random
import copy

from estado import *
from sys import maxsize

minint = -maxsize - 1

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

class Minimax(Computadora):
    def __init__(self, num):
        super(Minimax, self).__init__(num)

    def finalMovimiento(self, estado):
        movimientos = {}
        possible_movimientos = self.possibleMovimientos(estado)

        for m in possible_movimientos:
            node = Node(self.jugador_num, estado, "movimiento", m.x, m.y)
            movimientos[node] = self.alfabeta(node, 0, minint, maxsize, True)

        movimiento = max(movimientos, key=movimientos.get)

        if movimiento.movimiento_type == "movimiento":
            self.movimiento(movimiento.movimientoX, movimiento.movimientoY, estado)

    def miniMax(self, node, depth, maximizingJugador):
        if depth == 0 or self.ganadorMovimiento(node):
            return self.sfs(node, node.estado)

        if maximizingJugador:
            mejorPosicion = minint
            hijos = node.hijos(maximizingJugador)
            for hijo in hijos:
                v = self.miniMax(hijo, depth - 1, False)
                mejorPosicion = max(mejorPosicion, v)
            return mejorPosicion
        else:
            mejorPosicion = maxsize
            hijos = node.hijos(maximizingJugador)
            for hijo in hijos:
                v = self.miniMax(hijo, depth - 1, True)
                mejorPosicion = min(mejorPosicion, v)
            return mejorPosicion

    #Algoritmo que reduce el numero de nodos evaluados en un arbol
    #SE HACE USO DEL ALGORITMO MINIMAX
    def alfabeta(self, node, depth, alfa, beta, maximizingJugador):
        if depth == 0 or self.ganadorMovimiento(node):
            return self.sfs(node, node.estado)
        if maximizingJugador:
            mejorPosicion = minint
            hijos = node.hijos(maximizingJugador)
            for hijo in hijos:
                v = self.alfabeta(hijo, depth - 1, alfa, beta, False)
                mejorPosicion = max(mejorPosicion, v)
                alfa = max(alfa, mejorPosicion)
                if beta <= alfa:
                    break
            return mejorPosicion
        else:
            mejorPosicion = maxsize
            hijos = node.hijos(maximizingJugador)
            for hijo in hijos:
                v = self.alfabeta(hijo, depth - 1, alfa, beta, True)
                mejorPosicion = min(mejorPosicion, v)
                if beta <= alfa:
                    break
            return mejorPosicion

    def ganadorMovimiento(self, node):
        if node.movimiento_type == "movimiento":
            if (node.movimientoX, node.movimientoY) in self.win_fila:
                return True
        return False

    def sfs(self, node, estado):
        opp = estado.jugadores[self.opp]
        if node.movimiento_type == "movimiento":
            minMovimientoCamino = minCaminoLen(node.movimientoX, node.movimientoY, self.win_fila, estado)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, estado)
            return minOppCamino - minMovimientoCamino
        else:
            minWinCamino = minCaminoLen(self.x, self.y, self.win_fila, estado)
            minOppCamino = minCaminoLen(opp.x, opp.y, self.opp_fila, estado)
            return minOppCamino - minWinCamino

#Declarando el nodo
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

    def hijos(self):
        hijos = []
        opponent_possible_movimientos = self.estado.jugadores[self.opp_num].possibleMovimientos(self.estado, True)
        for m in opponent_possible_movimientos:
            node = Node(self.opp_num, self.estado, "movimiento", None, m.x, m.y)
            hijos.append(node)
        return hijos

#Funcion que halla el caminito (el tamanio mas minimo)
def minCaminoLen(x, y, win_fila, estado):
    minCamino = maxsize
    for end in win_fila:
        camino_len = busqueda.camino((x, y), end, estado)
        if camino_len < minCamino:
            minCamino = camino_len
    return minCamino