import numpy as np
import sys
import pygame
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0, 0, 102)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,51)

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece
	return

def is_valid_loc(board,col):
	return board[ROW_COUNT-1][col] == 0

def get_nxt_openrow(board,col):
	for row in range(ROW_COUNT):
		if(board[row][col] == 0):
			return row

def print_board(board):
	print(np.flip(board,0))
	return

def winning_move(board,piece):
	#horizontal win check
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if(board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece):
				return True

	#vertical win check
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if(board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece):
				return True

	#+ve sloped diagonal win check
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if(board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece):
				return True

	#-ve sloped diagonal win check
	for c in range(COLUMN_COUNT-3):
		for r in range(3,ROW_COUNT):
			if(board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece):
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE ,SQUARESIZE , SQUARESIZE))
			#empty cell color black
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS) 

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if(board[r][c] == 1): #plyer1 
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif(board[r][c] == 2): #plyer2
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

	pygame.display.update()

board = create_board()
game_over = False
turn = 0

######## GUI
pygame.init()
SQUARESIZE = 100   #100px
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT*SQUARESIZE
height = (ROW_COUNT+1)*SQUARESIZE
size = (width,height)

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace" , 50)
draw_board(board)



while(not game_over):

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if(event.type == pygame.MOUSEMOTION):
			pygame.draw.rect(screen, BLACK , (0,0,width,SQUARESIZE))
			posx = event.pos[0]
			if(turn == 0):
				pygame.draw.circle(screen, RED, (posx,int(SQUARESIZE/2)), RADIUS)
			else:
				pygame.draw.circle(screen, YELLOW, (posx,int(SQUARESIZE/2)), RADIUS)
			pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK , (0,0,width,SQUARESIZE))
			#plyer 1 turn
			if turn == 0:
				posx = event.pos[0]
				col = int(posx/SQUARESIZE)

				if(is_valid_loc(board,col)):
					row = get_nxt_openrow(board,col)
					drop_piece(board,row,col,1)
					if(winning_move(board,1)):
						print("player 1 wins !!")
						label = myfont.render(">>  Player 1 Wins  <<" , 1, RED)
						screen.blit(label, (40,10))
						game_over = True
						#break

			
			#plyer 2 turn 
			else:
				posx = event.pos[0]
				col = int(posx/SQUARESIZE)
				if(is_valid_loc(board,col)):
					row = get_nxt_openrow(board,col)
					drop_piece(board,row,col,2)
					if(winning_move(board,2)):
						print("player 2 wins !!")
						label = myfont.render(">>  Player 2 Wins  <<" , 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True
						#break

			draw_board(board)
			turn = turn ^ 1

			if(game_over):
				pygame.time.wait(5000)