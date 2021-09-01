import numpy as np 
import pygame
import sys
import math
import random

# Size of the grid.
ROW_COUNT=6
COL_COUNT=7

# Defined the colours in RGB
BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
NEON=(0,200,0)

PLAYER=0
AI=1
PLAYER_PIECE=1
AI_PIECE=2

def create_board():
	board=np.zeros((ROW_COUNT,COL_COUNT))
	return board

# Drops the piece at board[row][col]
def drop_piece(board,row,col,piece):      
	board[row][col] = piece

# Checks whether the column has at least an empty space 
def is_valid(board,col):                   
	return board[ROW_COUNT-1][col] == 0

 # Gives the next open row in that particular column
def get_next_open_row(board,col):         
	for i in range(ROW_COUNT):
		if(board[i][col] == 0):
			return i

# Prints the matrix on the console 
def print_board(board):                   
	print(np.flip(board,0))

 # Checks whether the player/AI has won the game
def winning_move(board,piece,call):          
	
	#Checks whether there are four pieces in horizontal fashion
	for c in range(COL_COUNT-3):          
		for r in range (ROW_COUNT):
			if(board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece):
				if call:
					board[r][c] =board[r][c+1] =board[r][c+2] =board[r][c+3] =3
				return True
	
	#Checks whether there are four pieces in vertical fashion
	for r in range(ROW_COUNT-3):
		for c in range (COL_COUNT):
			if(board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece):
				if(call):
					board[r][c] =board[r+1][c] =board[r+2][c] =board[r+3][c] =3
				return True

	#Checks whether there are four pieces in positive sloped diagonals
	for r in range (ROW_COUNT-3):
		for c in range(COL_COUNT-3):
			if(board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece):
				if(call):
					board[r][c] =board[r+1][c+1] =board[r+2][c+2] =board[r+3][c+3] =3
				return True

	#Checks whether there are four pieces in negative sloped diagonals
	for c in range (COL_COUNT-3):
		for r in range(3,ROW_COUNT):
			if(board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece):
				if(call):
					board[r][c] =board[r-1][c+1] =board[r-2][c+2] =board[r-3][c+3] =3
				return True

# Evaluates the score(effectiveness of the move) for a particular window frame 
def evaluate_window(window,piece):       
	score=0
	
	opp_piece=PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece=AI_PIECE
	

	if window.count(piece) == 4:
		score+=100
	elif window.count(piece) == 3 and window.count(0) == 1:
		score+=5
	elif window.count(piece) == 2 and window.count(0) == 2:
		score+=2

	
	if window.count(opp_piece) == 3 and window.count(0) == 1:
		score-=4
	
	return score
	
# Evaluates all the possible window and returns their score
def score_position(board,piece):       
	score=0

	center_array= [int(i) for i in list(board[:,COL_COUNT//2])]
	center_count=center_array.count(piece)
	score+=center_count*3

	#For Horizontal
	for r in range(ROW_COUNT):
		row_array=[int(i) for i in list(board[r,:])]
		for c in range (COL_COUNT-3):
			window=row_array[c:c+4]
			score+=evaluate_window(window,piece)

	#For Vertical
	for c in range (COL_COUNT):
		col_array=[int(i) for i in list(board[:,c])]
		for r in range (ROW_COUNT-3):
			window=col_array[r:r+4]
			score+=evaluate_window(window,piece)
			

	#For Positive Sloped
	for r in range(ROW_COUNT-3):
		for c in range(COL_COUNT-3):
			window=[board[r+i][c+i] for i in range(4)]
			score+=evaluate_window(window,piece)


	#For Negative Sloped
	for c in range (COL_COUNT-3):
		for r in range(ROW_COUNT-3):
			window=[board[r+3-i][c+i] for i in range(4)]
			score+=evaluate_window(window,piece)
			

	return score

# Checks whether someone has won or the board is filled
def is_terminal(board):      
	return winning_move(board,PLAYER_PIECE,0) or winning_move(board,AI_PIECE,0) or len(get_valid_location(board)) == 0

def minimax(board,depth,alpha,beta,maxi):
	valid_loc=get_valid_location(board)
	terminal_node=is_terminal(board)

	 # Base Case where the algorithm returns from further execution
	if depth == 0 or terminal_node:           
		if terminal_node:
			# If AI wins the returning a very high score 
			if winning_move(board,AI_PIECE,0):       
				return None,math.inf
			elif winning_move(board,PLAYER_PIECE,0):  
				# If Player wins the returning a very low score    
				return None,-math.inf
			else:        #All cells filled
				return None,0
		else:      # Depth becomes 0 hence returning the default score
			return None,score_position(board,AI_PIECE)

	if maxi:                                           
		value=-math.inf
		column=random.choice(valid_loc)
		for col in valid_loc:                           
			row=get_next_open_row(board,col)
			temp_board=board.copy()
			drop_piece(temp_board,row,col,AI_PIECE)
			new_score=minimax(temp_board,depth-1,alpha,beta,False)
			if new_score[1] == math.inf:
				if new_score[0] == None:
					return col,new_score[1]
				else:
					return new_score
			if new_score[1]>value:
				value=new_score[1]
				column=col

			alpha=max(alpha,value)
			if alpha>beta:
				break
		return column,value
	else:
		value=math.inf
		column=random.choice(valid_loc)
		for col in valid_loc:
			row=get_next_open_row(board,col)
			temp_board=board.copy()
			drop_piece(temp_board,row,col,PLAYER+1)
			new_score=minimax(temp_board,depth-1,alpha,beta,True)
			if new_score[1] == -math.inf:
				if new_score[0] == None:
					return col,new_score[1]
				else:
					return new_score

			if new_score[1]<value:
				value=new_score[1]
				column=col

			beta=min(beta,value)
			if alpha>beta:
				break
		return column,value

# Returns a list of all possible valid location where a piece can be drop
def get_valid_location(board):              
	valid_loc=[]
	for col in range (COL_COUNT):
		if is_valid(board,col):
			valid_loc.append(col)

	return valid_loc


def pick_best(board,piece):
	valid_loc=get_valid_location(board)

	best_score=-800000
	best_col=random.choice(valid_loc)

	for col in valid_loc:
		row=get_next_open_row(board,col)
		temp_board=board.copy()
		drop_piece(temp_board,row,col,piece)
		score=score_position(temp_board,piece)

		if score>best_score:
			best_score=score
			best_col=col
	
	return best_col

# Draws the board on the screen.
def draw_board(board):                      
	for r in range (ROW_COUNT):
		for c in range (COL_COUNT):
			pygame.draw.rect(screen,BLUE,(c*SQUARE_SIZE,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
			pygame.draw.circle(screen,BLACK,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),int(RADIUS))
		pygame.display.update()

	for r in range (ROW_COUNT):
		for c in range (COL_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen,RED,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),int(RADIUS))
			elif board[r][c] == 2:
				pygame.draw.circle(screen,YELLOW,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),int(RADIUS))
			elif board[r][c] == 3:
				pygame.draw.circle(screen,NEON,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),int(RADIUS))
		pygame.display.update()


board =create_board()
game_over=False

pygame.init()

# Defined the width and height of screen.
SQUARE_SIZE=100
width=COL_COUNT*SQUARE_SIZE
height=(ROW_COUNT+1)*SQUARE_SIZE

size=(width,height)

# Displays the screen 
screen=pygame.display.set_mode(size)

RADIUS=int((SQUARE_SIZE/2)-5)


print_board(board)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace" , 50)

turn=random.randint(PLAYER,AI)
level=3

while not game_over:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		# Displays the Red circle wherever we point the cursor.
		if event.type == pygame.MOUSEMOTION:    
			posx=event.pos[0]
			pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
			if(turn == PLAYER):
				pygame.draw.circle(screen,RED,(posx,int(SQUARE_SIZE/2)),RADIUS)
			else:
				pygame.time.wait(200)
		pygame.display.update()

		# Drops the circle according to the position of the mouse click
		if event.type == pygame.MOUSEBUTTONDOWN:     
			# Player Move
			if turn == PLAYER:
				col = int(math.floor(event.pos[0]/SQUARE_SIZE))
				
				 # If the col is not empty returns true    
				if is_valid(board,col):                
					pygame.time.wait(500)
					# Gives the next open row in that particular column
					row=get_next_open_row(board,col)          
					drop_piece(board,row,col,PLAYER_PIECE)
					
					# After droping the piece checking whether player wins
					if winning_move(board,PLAYER_PIECE,1):     
						print_board(board)
						pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
						label=myfont.render(">>  Player wins <<",1,RED)
						screen.blit(label,(40,10))
						print("Player Wins")
						game_over=True

					turn = turn ^ 1     # Switches turn

					print_board(board)
					draw_board(board)


	# AI 
	if turn == AI and not game_over:         
		if level == 1:
			col=random.randint(0,COL_COUNT-1)
		elif level == 2:
			col=pick_best(board,AI+1)
		elif level==3:
			# Selects the best move using minimax algorithm
			col,minimum_score=minimax(board,5,-math.inf,math.inf,True)        
			print(col,minimum_score)

		# If the col is not empty returns true  
		if is_valid(board,col):                                    
			row=get_next_open_row(board,col)
			drop_piece(board,row,col,AI_PIECE)

			# Gives the next open row in that particular column
			if winning_move(board,AI_PIECE,1):                      
				#print_board(board)
				pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
				label=myfont.render("    >> AI wins <<",1,BLUE)
				screen.blit(label,(40,10))
				print("AI Wins")
				game_over=True
			
			turn = turn ^ 1                      # Switches turn
			print_board(board)
			draw_board(board)

	if game_over:
		pygame.time.wait(5000)								
			

			

	

