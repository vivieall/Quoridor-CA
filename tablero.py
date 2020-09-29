# By Viviana - Team Group()

from estado import *
from sys import argv

import Tkinter
import math
import time
import threading
import random
import time 

CASILLA_SIZE = 50
JUGADOR_SIZE = int(.8 * CASILLA_SIZE)
CASILLA_PADDING = 10
BORDER = 10
NUM_FILAS = input("INGRESE NUMERO DE CASILLAS: ")
NUM_COLUMNAS = NUM_FILAS
CONTROL_WIDTH = 200
COLORS = {'bg': '#FFFFFF',
					  'casilla': '#d0d0d0',
					  'panel': '#333333',
					  'button': '#555555',
					  'text': '#000000',
					  'jugadores': ['#00F', '#ff0000'],
					  'jugadores-sombras': ['#9999ff', '#ffbdbd']
					  }
JUGADORES = ['AZUL', 'ROJO']


class Tablero():
	def __init__(self):
		self.root = None
		self.canvas = None
		self.width = 0
		self.height = 0
		self.jugadores = [None, None]
		self.casillas = []
		self.movimiento = None
		self.jugador_sombra = None
		self.wall_sombra = None
		self.turn = 0
		self.estado = None
		self.computadora_count = '0'
		self.current_element = None
		for _ in range(NUM_COLUMNAS):
			self.casillas.append(range(NUM_FILAS))

	def nuevoJuego(self, computadora_count):
		if self.root:
			self.root.destroy()

		self.root = Tkinter.Tk()
		self.root.title("Quoridor By Viviana, Angel & Richard")

		self.root.bind("<Escape>", lambda e: self.handleQuit())
		self.root.bind("<Enter>", lambda e: self.setMovimiento("movimientoPawn")) # "m"
		self.root.bind("<Motion>", lambda e: self.handleMotion(e.x, e.y))
		self.root.bind("<Button-1>", lambda e: self.handleClick(e.x, e.y))

		self.height = (NUM_FILAS*CASILLA_SIZE) + (NUM_FILAS*CASILLA_PADDING) + (2*BORDER)
		self.width = self.height + CONTROL_WIDTH
		self.canvas = Tkinter.Canvas(self.root, width=self.width, height=self.height, background=COLORS['bg'])
		self.canvas.pack()
		self.dibujarCasillas()

		self.estado = Estado(computadora_count)
		self.computadora_count = computadora_count
		self.turn = self.estado.current
		self.dibujarJugadores()

		self.root.mainloop()

	

	def dibujarCasillas(self):
		for j in range(NUM_FILAS):
			for i in range(NUM_COLUMNAS):
				x = BORDER + CASILLA_PADDING/2 + i*(CASILLA_SIZE+CASILLA_PADDING)
				y = BORDER + CASILLA_PADDING/2 + j*(CASILLA_SIZE+CASILLA_PADDING)
				casilla = self.canvas.create_rectangle(x,y, x+CASILLA_SIZE, y+CASILLA_SIZE, fill=COLORS['casilla'])
				self.casillas[j][i] = casilla

	def dibujarJugadores(self, sombra=False):
		for k in range(len(JUGADORES)):
			jugador = self.estado.jugadores[k]
			fila = jugador.x
			columna = jugador.y
			self.dibujarJugador(fila, columna, k, jugador, sombra)

	def dibujarJugador(self, fila, columna, num, jugador, sombra):
		x, y = gridToCoords(fila,columna)
		if x==None or y==None:
			return
		if not sombra and self.jugadores[num]:
			self.canvas.delete(self.jugadores[num])
			self.jugadores[num] = None
		elif sombra and self.jugador_sombra:
			self.canvas.delete(self.jugador_sombra)
		color = COLORS['jugadores'][num]
		if sombra:
			color = COLORS['jugadores-sombras'][num]
		radius = JUGADOR_SIZE/2
		pawn = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="")
		if not sombra:
			self.jugadores[num] = pawn
		else:
			self.jugador_sombra = pawn


	def setMovimiento(self, movimiento):
		self.movimiento = movimiento
		self.refresh()

	def handleQuit(self):
		self.root.destroy()

	def handleMotion(self, x, y):
		if self.computadora_count == '2' or (self.turn == 1 and self.computadora_count == '1'):
				return

		i, j = coordsToGrid(x,y)
		if i == None or j == None:
			return
		if self.movimiento == 'movimientoPawn':
			if self.estado.jugadores[self.turn].legal_movimiento(i,j,self.estado):
				self.dibujarJugador(i, j, self.turn, self.estado.jugadores[self.turn], True)
			elif self.jugador_sombra != None:
				self.canvas.delete(self.jugador_sombra)
				self.jugador_sombra == None

	def handleClick(self, x, y):
		if (self.computadora_count == '2'):
			while not self.estado.jugadores[0].winning_position and not self.estado.jugadores[1].winning_position:
				self.estado.jugadores[self.turn].finalMovimiento(self.estado)
				self.sigTurno()
				self.refresh()
				time.sleep(.1)

		else:
			i, j = coordsToGrid(x,y)
			if i == None or j == None:
				return

			if self.movimiento == 'movimientoPawn':
				if self.estado.jugadores[self.turn].legal_movimiento(i,j,self.estado):
					self.estado.jugadores[self.turn].movimiento(i,j,self.estado)
					self.sigTurno()
					self.refresh()

			if self.handleGanador():
				return

			if self.turn == 1 and self.computadora_count == '1':
				self.estado.jugadores[self.turn].finalMovimiento(self.estado)
				self.sigTurno()
				self.refresh()
				time.sleep(.1)

	def handleGanador(self):
		ganador = False
		for p in self.estado.jugadores:
			if p.winning_position:
				x = self.width - CONTROL_WIDTH/2 - BORDER
				y = self.height/2
				i = "El jugador " + JUGADORES[p.jugador_num] + " es el GANADOR!"
				self.canvas.create_text((x,y), text=i, justify='center', width=CONTROL_WIDTH, font=("Arial", 14, "bold"))
				ganador = True
				break
		if ganador:
			self.root.unbind("<Motion>")
			self.root.unbind("<Button-1>")
		return ganador

	def refresh(self):
		self.clearSombra()
		self.dibujarJugadores()
		self.root.update()
		self.handleGanador()

	def sigTurno(self):
		self.estado.sigTurno()
		self.turn = self.estado.current

	def clearSombra(self):
		if self.jugador_sombra != None:
			self.canvas.delete(self.jugador_sombra)
			self.jugador_sombra = None


def gridToCoords(i, j):
	if (0<=i<=8) and (0<=j<=8):
		x = BORDER + CASILLA_PADDING/2 + (i)*(CASILLA_SIZE+CASILLA_PADDING)
		y = BORDER + CASILLA_PADDING/2 + (j)*(CASILLA_SIZE+CASILLA_PADDING)
		return (x+(CASILLA_SIZE/2)), (y+(CASILLA_SIZE/2))
	else:
		return None, None

def coordsToGrid(x, y):
	x -= BORDER
	y -= BORDER

	i = int(math.floor(float(x)/(CASILLA_SIZE+CASILLA_PADDING)))
	j = int(math.floor(float(y)/(CASILLA_SIZE+CASILLA_PADDING)))

	if (0<=i<=8) and (0<=j<=8):
		return i, j
	else:
		return None, None


if __name__ == '__main__':
	tablero = Tablero()
	if len(argv) == 2:
		if argv[1] == '1':
			tablero.nuevoJuego('1')
		elif argv[1] == '2':
			tablero.nuevoJuego('2')
	else:
		tablero.nuevoJuego('0')
