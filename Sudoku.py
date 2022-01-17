import pygame
import time
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.font.init()
pygame.display.set_caption('SUDOKU')

class Grid:

	def __init__(self,rows=9,cols=9,width=450,height=450,dirnx = 0, dirny = 0):
		self.rows = rows
		self.cols = cols
		self.width = width
		self.height = height
		self.dirnx = dirnx
		self.dirny = dirny
		self.num = ""
		self.darkmode = False
		self.fontcolor = [0,0,0]
		self.backcolor = [255,255,255]
		self.board = [
		[7,8,0,4,0,0,1,2,0],
		[6,0,0,0,7,5,0,0,9],
		[0,0,0,6,0,1,0,7,8],
		[0,0,7,0,4,0,2,6,0],
		[0,0,1,0,5,0,9,3,0],
		[9,0,4,0,6,0,0,0,5],
		[0,7,0,3,0,0,0,1,2],
		[1,2,0,0,0,7,4,0,0],
		[0,4,9,2,0,6,0,0,7]]

	#color dictionary

	def draw(self, surface, cursor):
		#display_surface = pygame.display.set_mode((50, 50 ))
		global board2
		x=25
		y=25
		font = pygame.font.Font('freesansbold.ttf', 30) 
		cursor.draw(surface)

		for m in self.highlight(cursor.pos):
			pygame.draw.rect(surface,(192,192,192),(m[1] * 50,m[0] * 50,50,50))

		for i in range(self.rows):
			for j in range(self.cols):
				if self.board[i][j] == 0:
					text = font.render("", True,self.fontcolor) 
				elif i == (cursor.pos[1]//50) and j == (cursor.pos[0]//50) and self.check_board(board2,i,j) == True and self.num != "":
					text = font.render(str(self.board[i][j]), True,[255,0,0])
				elif i == (cursor.pos[1]//50) and j == (cursor.pos[0]//50) and self.check_board(board2,i,j) == False and self.num != "":
					text = font.render(str(self.board[i][j]), True,[0,255,0])
				else:
					text = font.render(str(self.board[i][j]), True,self.fontcolor) 
				textRect = text.get_rect()
				textRect.center = (x, y) 
				surface.blit(text, textRect)
				x += 50
			x = 25
			y += 50

	def update_board(self, pos):
		global board2
		x = pos[1] // 50
		y = pos[0] // 50
		self.board[x][y] = self.num

	def end_of_game(self):
		count = 0
		for i in range(self.rows):
			for j in range(self.cols):
				if self.board[i][j] == 0:
					count += 1

		if count == 0:
			return True
		else:
			return False

	def highlight(self, pos):
		same_num = set()
		x = pos[1] // 50
		y = pos[0] // 50
		for i in range(self.rows):
			for j in range(self.cols):
				if (str(self.board[i][j]) == self.num or str(self.board[i][j]) == self.board[x][y]) and self.board[i][j] != 0:
					same_num.add((i,j))
				elif self.board[i][j] == self.board[x][y] and self.board[i][j] != 0:
					same_num.add((i,j))

		return same_num

	def check_board(self, solved_board, x, y):
		if str(solved_board[x][y]) != self.num:
			return True
		elif str(solved_board[x][y]) == self.num:
			return False
		
	def actions(self,cursor):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -50
					self.dirny = 0
				elif keys[pygame.K_RIGHT]:
					self.dirnx = 50
					self.dirny = 0
				elif keys[pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 50
				elif keys[pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -50
				elif keys[pygame.K_ESCAPE]:
					return False
				elif keys[pygame.K_1]:
					self.num = "1"
					self.update_board(cursor.pos)	
				elif keys[pygame.K_2]:
					self.num = "2"
					self.update_board(cursor.pos)
				elif keys[pygame.K_3]:
					self.num = "3"
					self.update_board(cursor.pos)
				elif keys[pygame.K_4]:
					self.num = "4"
					self.update_board(cursor.pos)
				elif keys[pygame.K_5]:
					self.num = "5"
					self.update_board(cursor.pos)
				elif keys[pygame.K_6]:
					self.num = "6"
					self.update_board(cursor.pos)
				elif keys[pygame.K_7]:
					self.num = "7"
					self.update_board(cursor.pos)
				elif keys[pygame.K_8]:
					self.num = "8"
					self.update_board(cursor.pos)
				elif keys[pygame.K_9]:
					self.num = "9"
					self.update_board(cursor.pos)
				elif keys[pygame.K_d]:
					self.fontcolor = [0,34,255]
					self.backcolor = [0,0,0]
				elif keys[pygame.K_l]:
					self.fontcolor = [0,0,0]
					self.backcolor = [255,255,255]
				else:
					self.dirnx = 0
					self.dirny = 0
					self.num = ""

				
			cursor.move(self.dirnx,self.dirny)
		return True

class Box:

	def __init__(self,pos = (225,225), dirny = 0, dirnx = 0):
		self.pos = pos
		self.dirny = dirny
		self.dirnx = dirnx

	def draw(self,surface):
		pygame.draw.rect(surface,(192,192,192),(self.pos[0]-25,self.pos[1]-25,50,50))
		#pygame.draw.rect(surface,(255, 255, 255),(self.pos[0]-20,self.pos[1]-20,40,40))

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny

		if (self.pos[0] + self.dirnx) >= 450 and (self.pos[1] + self.dirny) <= 0:
			self.dirnx = 0
			self.dirny = 0
		elif (self.pos[0] + self.dirnx) <= 0 and (self.pos[1] + self.dirny) > 0 and (self.pos[1] + self.dirny) < 450:
			self.dirnx = 0
			self.dirny = dirny
		elif (self.pos[1] + self.dirny) <= 0 and (self.pos[0] + self.dirnx) > 0 and (self.pos[0] + self.dirnx) < 450:
			self.dirny = 0
			self.dirnx = dirnx
		elif (self.pos[0] + self.dirnx) >= 450 and (self.pos[1] + self.dirny) > 0 and (self.pos[1] + self.dirny) < 450:
			self.dirnx = 0
			self.dirny = dirny
		elif (self.pos[1] + self.dirny) >= 450 and (self.pos[0] + self.dirnx) > 0 and (self.pos[0] + self.dirnx) < 450:
			self.dirny = 0
			self.dirnx = dirnx

		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

def drawGrid(w, rows, surface):
	global g
	sizeBtwn = w // rows

	x = 0
	y = 0
	for l in range(rows):		
		x += sizeBtwn
		y += sizeBtwn
		if l == 2 or l == 5:
			pygame.draw.line(surface, g.fontcolor, (x, 0), (x, w),3)
			pygame.draw.line(surface, g.fontcolor, (0, y), (w, y),3)
		else:
			pygame.draw.line(surface, g.fontcolor, (x, 0), (x, w))
			pygame.draw.line(surface, g.fontcolor, (0, y), (w, y))

def redrawWindow(surface):
	global rows, width, g, b
	width = 450
	rows = 9
	surface.fill(g.backcolor)
	g.draw(surface, b)
	drawGrid(width, rows, surface)
	pygame.display.update()

def solve(board):
	find = find_empty(board)
	if not find:
		return True
	else:
		row, col = find

	for i in range(1,10):
		if valid(board, i, (row,col)):
			board[row][col] = i

			if solve(board):
				return True

			board[row][col] = 0

	return False

def valid(board, num, pos):
	#Check row
	for i in range(len(board[0])):
		if board[pos[0]][i] == num and pos[1] != i:
			return False
	#Check col
	for j in range(len(board)):
		if board[j][pos[1]] == num and pos[0] != j:
			return False

	#Check square
	box_x = pos[1] // 3
	box_y = pos[0] // 3

	for i in range(box_y*3,box_y + 3):
		for j in range(box_x*3, box_x + 3):
			if board[i][j] == num and i != pos[0] and j!= pos[1]:
				return False
	return True	

def find_empty(board):
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				return (i,j)

	return None

def message_box(subject, content):
	global root
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass

def main():
	global width, rows, g, b, board2
	width = 450
	win = pygame.display.set_mode((width, width))
	flag = True
	g = Grid()
	b = Box()
	board2 = [
		[7,8,0,4,0,0,1,2,0],
		[6,0,0,0,7,5,0,0,9],
		[0,0,0,6,0,1,0,7,8],
		[0,0,7,0,4,0,2,6,0],
		[0,0,1,0,5,0,9,3,0],
		[9,0,4,0,6,0,0,0,5],
		[0,7,0,3,0,0,0,1,2],
		[1,2,0,0,0,7,4,0,0],
		[0,4,9,2,0,6,0,0,7]]
	solve(board2)
	clock = pygame.time.Clock()
	while flag:
		pygame.time.delay(50)
		clock.tick(10)
		flag = g.actions(b)
		if g.end_of_game():
			message_box("You Won!!", "Congratulations!")
			break
		redrawWindow(win)

#Main Program
main()