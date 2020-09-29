# By Viviana - Team Group()

from busqueda import bfs

class Jugador(object):

    def __init__(self, jugador_num):
        self.walls = 10
        self.jugador_num = jugador_num
        self.winning_position = False

        if (jugador_num == 0):
            self.x = 4
            self.y = 0
            self.opp = 1
        elif (jugador_num == 1):
            self.x = 4
            self.y = 8
            self.opp = 0

        for i in range(8):
            for j in range(8):
                for k in ["horizontal", "vertical"]:
                    top_l = Casilla(i,j)
                    top_r = Casilla(i+1,j)
                    bot_l = Casilla(i,j+1)
                    bot_r = Casilla(i+1,j+1)

#DEFINIMOS LOS MOVIMIENTOS EN LAS CASILLAS
    def move(self, x, y, tablero):

        if self.legal_move(x, y, tablero):
            self.x = x
            self.y = y
            if self.jugador_num == 0 and self.y == 8:
                self.winning_position = True
            elif self.jugador_num == 1 and self.y == 0:
                self.winning_position = True
        else:
            raise ("Movimiento NO PERMITIDO")


  #DEFINIMOS LAS REGLAS DEL JUEGO (MOVERSE SOLO UP, DOWN, LEFT, RIGHT)
    def legal_move(self, x, y, tablero):
        if (x<0 or x>8 or y<0 or y>8):
            return False
        # SI NO ESTA DENTRO DE LA MISMA FILA
        if (self.x == x and self.y == y):
            return False

        if (not self.legal_jump(x,y,tablero) and (abs(self.y-y) > 1 or abs(self.x - x) > 1 or (abs(self.y-y) == 1 and abs(self.x - x) == 1))):
            return False

        if self.occupied(x,y,tablero):
            return False

        return True

    def occupied(self,x,y,b):

        if (self.jugador_num == 0 and b.jugadores[1].x == x and b.jugadores[1].y == y):
            return True
        if (self.jugador_num == 1 and b.jugadores[0].x == x and b.jugadores[0].y == y):
            return True
        return False

    def legal_jump(self,x,y,b):

        if self.jugador_num == 0:
            opp_num = 1
        else:
            opp_num = 0

        oppx = b.jugadores[opp_num].x
        oppy = b.jugadores[opp_num].y

        if (self.adjacent(self.x,self.y,oppx,oppy) and self.adjacent(oppx,oppy,x,y) and (not self.blocked(oppx,oppy,x,y,b))):
            if (not self.blocked(self.x,self.y,oppx,oppy,b)):
                logicalx = self.x
                logicaly = self.y
                if self.x < oppx:
                    logicalx = oppx + 1
                elif self.x > oppx:
                    logicalx = oppx - 1

                if self.y < oppy:
                    logicaly = oppy  + 1
                elif self.y > oppy:
                    logicaly = oppy - 1

                if self.blocked(oppx, oppy,logicalx,logicaly,b) or (logicaly < 0) or (logicaly > 8) or (logicalx < 0) or (logicalx > 8):
                    return True
                if x == logicalx and y == logicaly:
                    return True

        return False

    def blocked(self, x1, y1, x2, y2, tablero):
        return False

    def adjacent(self,x1,y1,x2,y2):
        if ((abs(x1-x2) == 1 and abs(y1-y2) == 0) or (abs(y1-y2) == 1 and abs(x1-x2) == 0)):
            return True
        return False

    def legal_placement(self, tablero):
        return True

    def path_exists(self, b): #, w):
        p1_path = False
        p2_path = False
        win_fila1 = [(0,8),(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8)]
        win_fila2 = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]

        for casilla in win_fila1:
            if bfs((b.jugadores[0].x,b.jugadores[0].y), casilla, b):
                p1_path = True
        for casilla in win_fila2:
            if bfs((b.jugadores[1].x,b.jugadores[1].y), casilla, b):
                p2_path = True

        return (p1_path and p2_path)

    def possibleMoves(self, estado, opponent=False):
        movimientos = []
        if not opponent:
            movimientos.append(Casilla(self.x, self.y-1))
            movimientos.append(Casilla(self.x, self.y+1))
            movimientos.append(Casilla(self.x+1, self.y))
            movimientos.append(Casilla(self.x-1, self.y))

            movimientos.append(Casilla(self.x, self.y-2))
            movimientos.append(Casilla(self.x, self.y+2))
            movimientos.append(Casilla(self.x-2, self.y))
            movimientos.append(Casilla(self.x+2, self.y))
            movimientos.append(Casilla(self.x-1, self.y-1))
            movimientos.append(Casilla(self.x+1, self.y+1))
            movimientos.append(Casilla(self.x+1, self.y-1))
            movimientos.append(Casilla(self.x-1, self.y+1))

            result = []
            for m in movimientos:
                if self.legal_move(m.x, m.y, estado):
                    result.append(m)
        else:
            opp = estado.jugadores[self.opp]
            movimientos.append(Casilla(opp.x, opp.y-1))
            movimientos.append(Casilla(opp.x, opp.y+1))
            movimientos.append(Casilla(opp.x+1, opp.y))
            movimientos.append(Casilla(opp.x-1, opp.y))

            movimientos.append(Casilla(opp.x, opp.y-2))
            movimientos.append(Casilla(opp.x, opp.y+2))
            movimientos.append(Casilla(opp.x-2, opp.y))
            movimientos.append(Casilla(opp.x+2, opp.y))
            movimientos.append(Casilla(opp.x-1, opp.y-1))
            movimientos.append(Casilla(opp.x+1, opp.y+1))
            movimientos.append(Casilla(opp.x+1, opp.y-1))
            movimientos.append(Casilla(opp.x-1, opp.y+1))

            result = []
            for m in movimientos:
                if opp.legal_move(m.x, m.y, estado):
                    result.append(m)

        return result


class Casilla:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_casilla(self):
        return "Lugar en la casilla: (%d, %d)" % (self.x, self.y)

class Estado:

    def __init__(self, computadora_count='0'):
        import computadora
        if  computadora_count == '1':
            self.jugadores =[Jugador(0), computadora.Minimax(1)]
        elif computadora_count == '2':
            self.jugadores =[computadora.Minimax(0), computadora.Minimax(1)]
        else:
            self.jugadores = [Jugador(0), Jugador(1)]

        self.casillas = [ [],[],[],[],[],[],[],[],[] ]
        self.current = 0

        for i in range(0,8):
            for j in range(0,8):
                self.casillas[i].append(Casilla(i,j))

    def printTablero(self):
        print self.casillas

    def nextTurn(self):
        if self.current == 0:
            self.current = 1
        else:
            self.current = 0