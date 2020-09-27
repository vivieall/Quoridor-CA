# By Viviana - Team Group()

from estado import *
from sys import argv

import Tkinter
import math
import time
import threading
import random
import time 

TILE_SIZE = 50
JUGADOR_SIZE = int(.8 * TILE_SIZE)
TILE_PADDING = 10
BORDER = 10
NUM_FILAS = input("INGRESE NUMERO DE CASILLAS: ")
NUM_COLUMNAS = NUM_FILAS
CONTROL_WIDTH = 200
COLORS = {'bg': '#FFFFFF',
					  'tile': '#d0d0d0',
					  'panel': '#333333',
					  'button': '#555555',
					  'text': '#000000',
					  'jugadores': ['#00F', '#ff0000'],
					  'jugadores-shadows': ['#9999ff', '#ffbdbd']
					  }
JUGADORS = ['AZUL', 'ROJO']


class Tablero():
	def __init__(self):
		self.root = None
		self.canvas = None
		self.width = 0
		self.height = 0
		self.jugadores = [None, None]
		self.tiles = []
		self.move = None
		self.jugador_shadow = None
		self.wall_shadow = None
		self.turn = 0
		self.estado = None
		self.photo = None
		self.computadora_count = '0'
		self.current_element = None
		for _ in range(NUM_COLUMNAS):
			self.tiles.append(range(NUM_FILAS))



	def newGame(self, computadora_count):
		if self.root:
			self.root.destroy()

		self.root = Tkinter.Tk()
		self.root.title("Quoridor By Viviana, Angel & Richard")

		self.root.bind("<Escape>", lambda e: self.handleQuit())
		self.root.bind("<Enter>", lambda e: self.setMove("movePawn")) # "m"
		self.root.bind("<Motion>", lambda e: self.handleMotion(e.x, e.y))
		self.root.bind("<Button-1>", lambda e: self.handleClick(e.x, e.y))

		self.height = (NUM_FILAS*TILE_SIZE) + (NUM_FILAS*TILE_PADDING) + (2*BORDER)
		self.width = self.height + CONTROL_WIDTH
		self.canvas = Tkinter.Canvas(self.root, width=self.width, height=self.height, background=COLORS['bg'])
		self.canvas.pack()
		self.drawTiles()

		self.estado = Estado(computadora_count)
		self.computadora_count = computadora_count
		self.turn = self.estado.current
		self.drawJugadores()

		self.root.mainloop()

	

	def drawTiles(self):
		for j in range(NUM_FILAS):
			for i in range(NUM_COLUMNAS):
				x = BORDER + TILE_PADDING/2 + i*(TILE_SIZE+TILE_PADDING)
				y = BORDER + TILE_PADDING/2 + j*(TILE_SIZE+TILE_PADDING)
				tile = self.canvas.create_rectangle(x,y, x+TILE_SIZE, y+TILE_SIZE, fill=COLORS['tile'])
				self.tiles[j][i] = tile

	def drawJugadores(self, shadow=False):
		for k in range(len(JUGADORS)):
			jugador = self.estado.jugadores[k]
			fila = jugador.x
			columna = jugador.y
			self.drawJugador(fila, columna, k, jugador, shadow)

	def drawJugador(self, fila, columna, num, jugador, shadow):
		x, y = gridToCoords(fila,columna)
		if x==None or y==None:
			return
		if not shadow and self.jugadores[num]:
			self.canvas.delete(self.jugadores[num])
			self.jugadores[num] = None
		elif shadow and self.jugador_shadow:
			self.canvas.delete(self.jugador_shadow)
		color = COLORS['jugadores'][num]
		if shadow:
			color = COLORS['jugadores-shadows'][num]
		radius = JUGADOR_SIZE/2
		pawn = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, outline="")
		if not shadow:
			self.jugadores[num] = pawn
		else:
			self.jugador_shadow = pawn


	def setMove(self, move):
		self.move = move
		self.refresh()

	def handleQuit(self):
		self.root.destroy()

	def handleMotion(self, x, y):
		if self.computadora_count == '2' or (self.turn == 1 and self.computadora_count == '1'):
				return

		i, j = coordsToGrid(x,y)
		if i == None or j == None:
			return
		if self.move == 'movePawn':
			if self.estado.jugadores[self.turn].legal_move(i,j,self.estado):
				self.drawJugador(i, j, self.turn, self.estado.jugadores[self.turn], True)
			elif self.jugador_shadow != None:
				self.canvas.delete(self.jugador_shadow)
				self.jugador_shadow == None

	def handleClick(self, x, y):
		if (self.computadora_count == '2'):
			while not self.estado.jugadores[0].winning_position and not self.estado.jugadores[1].winning_position:
				self.estado.jugadores[self.turn].finalMove(self.estado)
				self.nextTurn()
				self.refresh()
				time.sleep(.1)

		else:
			i, j = coordsToGrid(x,y)
			if i == None or j == None:
				return

			if self.move == 'movePawn':
				if self.estado.jugadores[self.turn].legal_move(i,j,self.estado):
					self.estado.jugadores[self.turn].move(i,j,self.estado)
					self.nextTurn()
					self.refresh()

			if self.handleWinner():
				return

			if self.turn == 1 and self.computadora_count == '1':
				self.estado.jugadores[self.turn].finalMove(self.estado)
				self.nextTurn()
				self.refresh()
				time.sleep(.1)

	def handleWinner(self):
		winner = False
		for p in self.estado.jugadores:
			if p.winning_position:
				x = self.width - CONTROL_WIDTH/2 - BORDER
				y = self.height/2
				i = "El jugador " + JUGADORS[p.jugador_num] + " es el GANADOR!"
				self.canvas.create_text((x,y), text=i, justify='center', width=CONTROL_WIDTH, font=("Arial", 14, "bold"))
				winner = True
				break
		if winner:
			self.root.unbind("<Motion>")
			self.root.unbind("<Button-1>")
		return winner

	def refresh(self):
		self.clearShadow()
		self.drawJugadores()
		self.root.update()
		self.handleWinner()

	def nextTurn(self):
		self.estado.nextTurn()
		self.turn = self.estado.current

	def clearShadow(self):
		if self.jugador_shadow != None:
			self.canvas.delete(self.jugador_shadow)
			self.jugador_shadow = None


def gridToCoords(i, j):
	if (0<=i<=8) and (0<=j<=8):
		x = BORDER + TILE_PADDING/2 + (i)*(TILE_SIZE+TILE_PADDING)
		y = BORDER + TILE_PADDING/2 + (j)*(TILE_SIZE+TILE_PADDING)
		return (x+(TILE_SIZE/2)), (y+(TILE_SIZE/2))
	else:
		return None, None

def coordsToGrid(x, y):
	x -= BORDER
	y -= BORDER

	i = int(math.floor(float(x)/(TILE_SIZE+TILE_PADDING)))
	j = int(math.floor(float(y)/(TILE_SIZE+TILE_PADDING)))

	if (0<=i<=8) and (0<=j<=8):
		return i, j
	else:
		return None, None


if __name__ == '__main__':
	tablero = Tablero()
	if len(argv) == 2:
		if argv[1] == '1':
			tablero.newGame('1')
		elif argv[1] == '2':
			tablero.newGame('2')
	else:
		tablero.newGame('0')
