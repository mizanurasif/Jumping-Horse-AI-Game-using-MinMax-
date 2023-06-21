import pygame
import sys
import numpy as np

# initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer
click_sound = pygame.mixer.Sound("arcade-game-jump.wav")
# click_sound = pygame.mixer.Sound("mixkit-shotgun-hard-pump-1665.wav")

# CONSTANTS
WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 10
BOARD_ROWS = 5
BOARD_COLS = BOARD_ROWS
SQUARE_SIZE = WIDTH/BOARD_ROWS
SCORE_AREA_HEIGHT = 200
font = pygame.font.Font('NotoMono-Regular.ttf', 25)

# # Colors
BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# GRAY = (128, 128, 128)
WHITE = (238,238,210)
GRAY = (118,150,86)
# # WHITE = "#e2e2e2"
# # GRAY = "#00695C"

OFFWHITE = (238,238,225)
GREEN = (0, 255, 0)

AI=1
HU=1


WHITE_HORSE = pygame.image.load(r"white_horse.png")
WHITE_HORSE = pygame.transform.scale(WHITE_HORSE, (120,120))

BLACK_HORSE = pygame.image.load(r"black_horse.png")
BLACK_HORSE = pygame.transform.scale(BLACK_HORSE, (120,120))

RED_HORSE = pygame.image.load(r"red_horse.png")
RED_HORSE = pygame.transform.scale(RED_HORSE, (120,120))

RED_CROSS = pygame.image.load(r"red_cross.png")
RED_CROSS = pygame.transform.scale(RED_CROSS, (125,125))

GAME_OVER = pygame.image.load(r"green_horse.png")
GAME_OVER = pygame.transform.scale(GAME_OVER, (100,100))

LOSE = pygame.image.load(r"lose.png")
LOSE = pygame.transform.scale(LOSE, (100,100))

WIN = pygame.image.load(r"win.png")
WIN = pygame.transform.scale(WIN, (110,100))

ai_turn_surf = font.render('AI Turn',True,'Black')
ai_turn_rect = ai_turn_surf.get_rect(midleft=(120,665))
hu_turn_surf = font.render('Human Turn',True,'Black')
hu_turn_rect = hu_turn_surf.get_rect(midleft=(120,725))

reset_surf = font.render('Press R to Restart',True,'Black')
reset_rect = reset_surf.get_rect(midleft=(300,725))

quit_surf = font.render('Press Q to Quit',True,'Black')
quit_rect = quit_surf.get_rect(midleft=(300,750))

loading_surf = pygame.image.load(r"knight.jpg")
loading_surf = pygame.transform.rotozoom(loading_surf, 0,0.4)
loading_rect = loading_surf.get_rect(topleft=(0,0))


# VARIABLES
player = 1
game_over = False
losePlayer = 0


# SCREEN
screen = pygame.display.set_mode( (WIDTH, HEIGHT + SCORE_AREA_HEIGHT) )
pygame.display.set_caption( 'Horse Jump' )

# CONSOLE BOARD
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )


# Player Current Possition
playerOneCurrentRow = -1
playerOneCurrentCol = -1
playerTwoCurrentRow = -1
playerTwoCurrentCol = -1

def clear_area(color,top,left,w,h):
    pygame.draw.rect(screen, color, (top, left, w, h))

# Draw the chessboard
def draw_chessboard():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_ROWS):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

def draw_score_area():
    pygame.draw.rect(screen, OFFWHITE, (0, HEIGHT, WIDTH, SCORE_AREA_HEIGHT))

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                if (row == playerOneCurrentRow and col == playerOneCurrentCol and losePlayer == 1 ):    #player1 lost UI
                    screen.blit(RED_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                    # if (row + col) % 2 == 0:
                    #     pygame.draw.rect(screen, WHITE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE ), SQUARE_SIZE, SQUARE_SIZE))
                    # else:
                    #     pygame.draw.rect(screen, GRAY, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE ), SQUARE_SIZE, SQUARE_SIZE))
                         
                    screen.blit(GAME_OVER, (460,620))
                    screen.blit(LOSE, (300,620))
                elif (row == playerOneCurrentRow and col == playerOneCurrentCol):
                    # screen.blit(ai_turn_surf,hu_turn_rect)
                    screen.blit(BLACK_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                else:
                    screen.blit(RED_CROSS, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
            elif board[row][col] == 2:
                if (row == playerTwoCurrentRow and col == playerTwoCurrentCol and losePlayer == 2 ):    #player2 lost UI
                    if (row + col) % 2 == 0:
                        pygame.draw.rect(screen, WHITE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE ), SQUARE_SIZE, SQUARE_SIZE))
                    else:
                        pygame.draw.rect(screen, GRAY, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE ), SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(RED_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                    
                    screen.blit(GAME_OVER, (460,620))
                    screen.blit(WIN, (300,620))
                elif (row == playerTwoCurrentRow and col == playerTwoCurrentCol):
                    screen.blit(WHITE_HORSE, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
                else:
                    screen.blit(RED_CROSS, (int( col * SQUARE_SIZE ), int( row * SQUARE_SIZE )))
    pygame.display.update()


def mark_square(row, col, player):
    board[row][col] = player
    print ("----------------------------------------------------")
    print("Player " + str(player) + " marked square : (" + str(row) + "," + str(col) + ")")
    print(board)
    print ("----------------------------------------------------")


def available_square(row, col, player):
    if(player == 1): 
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
        sp_move=HU
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol
        sp_move = AI
    #check my current movie is empty or is it valid directional move
    return (board[row][col] == 0 and ( 
        (currentRow == -1 and currentCol==-1) or
        (currentRow-1 == row and currentCol-1 == col) or
        (currentRow-1 == row and currentCol+1 == col) or
        (currentRow+1 == row and currentCol-1 == col) or
        (currentRow+1 == row and currentCol+1 == col) or

        (currentRow-1 == row and currentCol == col and sp_move>0) or
        (currentRow+1 == row and currentCol == col and sp_move>0) or
        (currentRow == row and currentCol-1 == col and sp_move>0) or
        (currentRow == row and currentCol+1 == col and sp_move>0)
    ))				

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False

    return True

def check_lose(currentRow,currentCol,player,sp_hu,sp_ai):
    """
    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol
    """
    global AI
    global HU
    if(player==1):
         sp_move=sp_hu
    else:
         sp_move=sp_ai

    if(currentRow == -1 or currentCol == -1):
        return False

    return not (
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ) or
        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ) or

        (-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow-1][currentCol] == 0 and sp_move>0) or
        (-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and board[currentRow+1][currentCol] == 0 and sp_move>0) or
        (-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow][currentCol-1] == 0 and sp_move>0) or
        (-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow][currentCol+1] == 0 and sp_move>0) 
    )

def check_special(row ,col,player):
    global HU
    global AI
    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol

    if((currentRow-1 == row and currentCol == col) or
        (currentRow+1 == row and currentCol == col) or
        (currentRow == row and currentCol-1 == col) or
        (currentRow == row and currentCol+1 == col)):
        if player==1:
            HU=HU-1
            print("---------------------->>>>>>change HU value")
        else:
            AI=AI-1
            print("-------------------->>>>>>>>change AI value")







def restart():
    # screen.fill( BG_COLOR )
    draw_chessboard()
    draw_score_area()
    global AI
    global HU
    AI=1
    HU=1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0



#Find out AI best move
def bestMove(player = 2):
    bestScore = -100000
    move = (-1,-1)

    global playerTwoCurrentCol
    global playerTwoCurrentRow

    global AI
    global HU
    depth=6


    #never used for player 1
    if(player == 1):
        currentRow = playerOneCurrentRow
        currentCol = playerOneCurrentCol
        sp_move=HU
    else:
        currentRow = playerTwoCurrentRow
        currentCol = playerTwoCurrentCol
        sp_move=AI


    if(currentRow == -1 or currentCol == -1):
        #first move for AI but not using minmax complexity and first move easily calculate
        #print("playeroneCurrentrow",playerOneCurrentRow)
        #print("playerOneCurrentCol",playerOneCurrentCol)
        row=playerOneCurrentRow-1
        col=playerOneCurrentCol-1
        if -1 < row and row < BOARD_ROWS and -1 < col and col < BOARD_COLS :
            available=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,row,col,False)
            if(available>bestScore):
                    bestScore = available
                    move = (row,col)
            
             
        row=playerOneCurrentRow-1
        col=playerOneCurrentCol+1
        if -1 < row and row < BOARD_ROWS and -1 < col and col < BOARD_COLS :
             available=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,row,col,False)
             if(available>bestScore):
                    bestScore = available
                    move = (row,col)
    
        row=playerOneCurrentRow+1
        col=playerOneCurrentCol-1
        if -1 < row and row < BOARD_ROWS and -1 < col and col < BOARD_COLS :
             available=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,row,col,False)
             if(available>bestScore):
                    bestScore = available
                    move = (row,col)

        row=playerOneCurrentRow+1
        col=playerOneCurrentCol+1
        if -1 < row and row < BOARD_ROWS and -1 < col and col < BOARD_COLS :
             available=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,row,col,False)
             if(available>bestScore):
                    bestScore = available
                    move = (row,col)
        
#Frist move end

#Rest of move (check best move using minmax and next available move possible by AI)  
    else:
        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
            board[currentRow-1][currentCol-1] = 2
            print("-----------------minmax start1("+str(currentRow-1) +","+str(currentCol-1)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol-1,depth-1,HU,AI)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol-1,False)
            print("score",score)
            board[currentRow-1][currentCol-1] = 0
            print("-----------------minmax end----------------")
            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow-1 , currentCol-1)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
            board[currentRow-1][currentCol+1] = 2
            print("-----------------minmax start2("+str(currentRow-1) +","+str(currentCol+1)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol+1,depth-1,HU,AI)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol+1,False)
            print("score",score)
            board[currentRow-1][currentCol+1] = 0
            print("-----------------minmax end---------------")

            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow-1,currentCol+1)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
            board[currentRow+1][currentCol-1] = 2
            print("-----------------minmax start3("+str(currentRow+1) +","+str(currentCol-1)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol-1,depth-1,HU,AI)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow+1 , currentCol-1,False)
            print("score",score)
            board[currentRow+1][currentCol-1] = 0
            print("-----------------minmax end-------------")


            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow+1,currentCol-1)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
            board[currentRow+1][currentCol+1] = 2
            print("-----------------minmax start4("+str(currentRow+1) +","+str(currentCol+1)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol+1,depth-1,HU,AI)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow+1 , currentCol+1,False)
            print("score",score)
            board[currentRow+1][currentCol+1] = 0
            print("-----------------minmax end-------------")

            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow+1,currentCol+1)


        #Special move
        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and sp_move>0 and board[currentRow-1][currentCol] == 0 ):
            board[currentRow-1][currentCol] = 2
            print("-----------------minmax start sp 1("+str(currentRow-1) +","+str(currentCol)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow-1,currentCol,depth-1,HU,AI-1)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow-1 , currentCol,False)
            print("score",score)
            board[currentRow-1][currentCol] = 0
            print("-----------------minmax end-------------")

            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow-1,currentCol)
        
        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and sp_move>0 and board[currentRow+1][currentCol] == 0 ):
            board[currentRow+1][currentCol] = 2
            print("-----------------minmax start sp 2("+str(currentRow+1) +","+str(currentCol)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow+1,currentCol,depth-1,HU,AI-1)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow+1 , currentCol,False)
            print("score",score)
            board[currentRow+1][currentCol] = 0
            print("-----------------minmax end-------------")

            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow+1,currentCol)
        
        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and sp_move>0 and board[currentRow][currentCol-1] == 0 ):
            board[currentRow][currentCol-1] = 2
            print("-----------------minmax start sp 3("+str(currentRow) +","+str(currentCol-1)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol-1,depth-1,HU,AI-1)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow , currentCol-1,False)
            print("score",score)
            board[currentRow][currentCol-1] = 0
            print("-----------------minmax end-------------")

            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow,currentCol-1)
        
        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and sp_move>0 and board[currentRow][currentCol+1] == 0 ):
            board[currentRow][currentCol+1] = 2
            print("-----------------minmax start sp 4("+str(currentRow) +","+str(currentCol+1)+")-------------")
            score = minimax(board,1,playerOneCurrentRow,playerOneCurrentCol,currentRow,currentCol+1,depth-1,HU,AI-1)
            free_cell=max_valid_turn(board,player,playerOneCurrentRow,playerOneCurrentCol,currentRow , currentCol+1,False)
            print("score",score)
            board[currentRow][currentCol+1] = 0
            print("-----------------minmax end-------------")

            if((free_cell+score)>bestScore):
                bestScore = score+free_cell
                move = (currentRow,currentCol+1)
        
        

    print("-------bestmove---------")
    print("AI move",move)
    print("AI bestScore",bestScore)
    print("-------bestmove---------")

    if(move!=(-1,-1)):
        check_special(move[0],move[1],player)
        playerTwoCurrentRow = move[0]
        playerTwoCurrentCol = move[1]
        
        mark_square( move[0], move[1], 2)
    else:
        print("not valid move in bestmove")
    


def max_valid_turn(board,player,playerOneCurrent_Row, playerOneCurrent_Col, playerTwoCurrent_Row, playerTwoCurrent_Col,isprint):
    if isprint == True:
        print(board)
    if player==1:
         currentRow=playerOneCurrent_Row
         currentCol=playerOneCurrent_Col
    else:
         currentRow=playerTwoCurrent_Row
         currentCol=playerTwoCurrent_Col

    cur_max=0

    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
                    cur_max=cur_max+1
    if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
                     cur_max=cur_max+1
    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
                     cur_max=cur_max+1
    if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
                     cur_max=cur_max+1
            
    return cur_max
       


# depth 6

def minimax(board, player, playerOneCurrent_Row, playerOneCurrent_Col, playerTwoCurrent_Row, playerTwoCurrent_Col , depth, sp_hu,sp_ai):
    #check is there any available move for AI
    if(player==1 and check_lose(playerOneCurrent_Row,playerOneCurrent_Col,player,sp_hu,sp_ai)):
            return 100
    if(player==2 and check_lose(playerTwoCurrent_Row,playerTwoCurrent_Col,player,sp_hu,sp_ai)):
            return -100
    
    if(depth==0):
        return max_valid_turn(board,player,playerOneCurrent_Row, playerOneCurrent_Col, playerTwoCurrent_Row, playerTwoCurrent_Col,False)

    




    if(player == 1):
        currentRow = playerOneCurrent_Row
        currentCol = playerOneCurrent_Col
    else:
        currentRow = playerTwoCurrent_Row
        currentCol = playerTwoCurrent_Col
#AI maximizing
    if player==2:
        bestScore = -100000


        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
            board[currentRow-1][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow-1 , currentCol-1, depth-1,sp_hu,sp_ai)
            board[currentRow-1][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
            board[currentRow-1][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow-1,currentCol+1,depth-1,sp_hu,sp_ai)
            board[currentRow-1][currentCol+1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
            board[currentRow+1][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow+1,currentCol-1,depth-1,sp_hu,sp_ai)
            board[currentRow+1][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
            board[currentRow+1][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow+1,currentCol+1,depth-1,sp_hu,sp_ai)
            board[currentRow+1][currentCol+1] = 0

            bestScore = max(score,bestScore)
        #special move
        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and sp_ai>0 and board[currentRow-1][currentCol] == 0 ):
            board[currentRow-1][currentCol] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow-1 , currentCol, depth-1,sp_hu,sp_ai-1)
            board[currentRow-1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and sp_ai>0 and board[currentRow+1][currentCol] == 0 ):
            board[currentRow+1][currentCol] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow+1, currentCol, depth-1,sp_hu,sp_ai-1)
            board[currentRow+1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and sp_ai>0 and board[currentRow][currentCol-1] == 0 ):
            board[currentRow][currentCol-1] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow , currentCol-1, depth-1,sp_hu,sp_ai-1)
            board[currentRow][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and sp_ai>0 and board[currentRow][currentCol+1] == 0 ):
            board[currentRow][currentCol+1] = 2
            score = minimax(board,1,playerOneCurrent_Row,playerOneCurrent_Col,currentRow , currentCol+1, depth-1,sp_hu,sp_ai-1)
            board[currentRow][currentCol+1] = 0

            bestScore = max(score,bestScore)
        
        #print("BEST SCORE max AI = ",bestScore)
        return bestScore

    else:
        #HU minimizing
        bestScore = 10000
        
        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow-1][currentCol-1] == 0 ):
            board[currentRow-1][currentCol-1] = 1
            score = minimax(board,2,currentRow-1,currentCol-1,playerTwoCurrent_Row,playerTwoCurrent_Col ,depth-1,sp_hu,sp_ai)
            board[currentRow-1][currentCol-1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow-1][currentCol+1] == 0 ):
            board[currentRow-1][currentCol+1] = 1
            score = minimax(board,2,currentRow-1,currentCol+1,playerTwoCurrent_Row,playerTwoCurrent_Col ,depth-1,sp_hu,sp_ai)
            board[currentRow-1][currentCol+1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and board[currentRow+1][currentCol-1] == 0 ):
            board[currentRow+1][currentCol-1] = 1
            score = minimax(board,2,currentRow+1,currentCol-1,playerTwoCurrent_Row,playerTwoCurrent_Col ,depth-1,sp_hu,sp_ai)
            board[currentRow+1][currentCol-1] = 0

            bestScore = min(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and board[currentRow+1][currentCol+1] == 0 ):
            board[currentRow+1][currentCol+1] = 1
            score = minimax(board,2,currentRow+1,currentCol+1,playerTwoCurrent_Row,playerTwoCurrent_Col ,depth-1,sp_hu,sp_ai)
            board[currentRow+1][currentCol+1] = 0

            bestScore = min(score,bestScore)
        
        #special move
        if(-1 < currentRow-1 and currentRow-1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and sp_hu>0 and board[currentRow-1][currentCol] == 0 ):
            board[currentRow-1][currentCol] = 1
            score = minimax(board,2,currentRow-1,currentCol,playerTwoCurrent_Row,playerTwoCurrent_Col , depth-1,sp_hu-1,sp_ai)
            board[currentRow-1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow+1 and currentRow+1 < BOARD_ROWS and -1 < currentCol and currentCol < BOARD_COLS and sp_hu>0 and board[currentRow+1][currentCol] == 0 ):
            board[currentRow+1][currentCol] = 1
            score = minimax(board,2,currentRow+1,currentCol,playerTwoCurrent_Row,playerTwoCurrent_Col , depth-1,sp_hu-1,sp_ai)
            board[currentRow+1][currentCol] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol-1 and currentCol-1 < BOARD_COLS and sp_hu>0 and board[currentRow][currentCol-1] == 0 ):
            board[currentRow][currentCol-1] = 1
            score = minimax(board,2,currentRow,currentCol-1,playerTwoCurrent_Row,playerTwoCurrent_Col , depth-1,sp_hu-1,sp_ai)
            board[currentRow][currentCol-1] = 0

            bestScore = max(score,bestScore)

        if(-1 < currentRow and currentRow < BOARD_ROWS and -1 < currentCol+1 and currentCol+1 < BOARD_COLS and sp_hu>0 and board[currentRow][currentCol+1] == 0 ):
            board[currentRow][currentCol+1] = 1
            score = minimax(board,2,currentRow,currentCol+1,playerTwoCurrent_Row,playerTwoCurrent_Col , depth-1,sp_hu-1,sp_ai)
            board[currentRow][currentCol+1] = 0

            bestScore = max(score,bestScore)

        
        
        

        #print("BEST SCORE min HU= ",bestScore)
        return bestScore



# Get the cell indices based on mouse position
def get_cell_indices(mouse_pos):
    x, y = mouse_pos
    row = y // SQUARE_SIZE  
    col = x // SQUARE_SIZE
    return row, col

draw_chessboard()
draw_score_area()

# MAINLOOP---------
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)
            #print('Mouse X position: ' + str(mouseX))
            #print('Mouse Y position: ' + str(mouseY))
            print('Clicked row: ' + str(clicked_row))
            print('Clicked col: ' + str(clicked_col))

            if clicked_row >= 5:
                continue
            
            if available_square( clicked_row, clicked_col, 1 ):
                player = 1
                click_sound.play()
                #check this move is special move or not
                check_special(clicked_row,clicked_col,player)
                mark_square( clicked_row, clicked_col, player )

                playerOneCurrentRow = clicked_row
                playerOneCurrentCol = clicked_col
                print('Player One Current Row and Col: (',str(playerOneCurrentRow)+','+str(playerOneCurrentCol)+')')

                #check for player 2(AI)
                if check_lose(playerTwoCurrentRow,playerTwoCurrentCol ,2,HU,AI ):
                    losePlayer = 2
                    game_over = True
                    draw_figures()
                    print("AI lost")

                else:
                    player = 2
                    bestMove(player)
                    #Check for player 1(HU)
                    if check_lose(playerOneCurrentRow,playerOneCurrentCol,1 ,HU,AI):
                        losePlayer = 1
                        game_over = True
                        print("Human  lost")
                        print("********************************************************")
                        print("Player 1 lost.\nRestarting game : Press -> R")
                        print("Quit game : Press -> Q")
                        print("********************************************************")
                    
                    draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False
                losePlayer = 0
                playerOneCurrentRow = -1
                playerOneCurrentCol = -1
                playerTwoCurrentRow = -1
                playerTwoCurrentCol = -1
            
            elif event.key == pygame.K_q:
                pygame.display.quit()
                sys.exit()  
    

    ai_sp_surf = font.render('AI SP Move: ' + str(AI),True,'Black')
    ai_sp_rect = ai_sp_surf.get_rect(midleft=(10,725))
    hu_sp_surf = font.render('Human SP Move: ' + str(HU),True,'Black')
    hu_sp_rect = hu_sp_surf.get_rect(midleft=(10,750))
    
    screen.blit(ai_sp_surf,ai_sp_rect)
    screen.blit(hu_sp_surf,hu_sp_rect)
    screen.blit(reset_surf,reset_rect)
    screen.blit(quit_surf,quit_rect)

    # screen.blit(loading_surf,loading_rect)


    # ai_turn_surf = font.render('AI Turn',True,'Black')
    # ai_turn_rect = ai_turn_surf.get_rect(midleft=(320,865))
    # hu_turn_surf = font.render('Human Turn',True,'Black')
    # hu_turn_rect = hu_turn_surf.get_rect(midleft=(320,925))
    
    # screen.blit(ai_turn_surf,ai_turn_rect)
    # screen.blit(hu_turn_surf,hu_turn_rect)
    # clear_area(OFFWHITE,0,160,160,160)
    
    pygame.display.update()
