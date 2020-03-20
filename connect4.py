import numpy as np
import pygame
import sys

BLUE = (14,54,134)
RED = (157, 44, 32)
YELLOW = (236,222,80)
WHITE = (255, 25, 255)
BLACK = (0,0,0)

HEIGHT, WIDTH = 6,7

def create_board(height, width):
    board = np.zeros((height, width))
    return board

def get_user_input(user):
    text = ("Player {}, make your selection (0-6): ").format(user)
    col = input(text)
    
    try: col = int(col)
    except:
        print("You must enter a number")
        return get_user_input(user)
    
    if col < 0 or col > 6:
        print("The number must be between 0 and 6")
        return get_user_input(user)
    
    if not is_valid_col(board, col):
        print("That column is full")
        return get_user_input(user)
    
    return int(col)

def is_valid_col(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    if not is_valid_col:
        return -1
    height, width = board.shape
    for row in reversed(range(height)):
        if board[row][col] == 0:
            return row
        
def drop_piece(board, row, col, turn):
    board[row][col] = turn

def play_turn(turn):
    col = get_user_input(turn)
    row = get_next_open_row(board, col)
    drop_piece(board, row, col, turn)
    return board, row, col, (turn%2)+1
    
def winner(board, row, col):
    """ 
    row, col represents indices of most recent move
    returns 0 if the game is still in progress,
    returns 1 if player 1 has won,
    returns 2 if player 2 has won
    """
    height, width = board.shape
    
    # search horizontal
    for c in range(max(col-3, 0), col+1):
        if c + 3 < width:
            set_vals = set()
            for i in range(4):
                val = board[row][c+i]
                set_vals.add(val)
            if len(set_vals) == 1: 
                w = int(next(iter(set_vals)))
                return w
    
    # search vertical
    for r in range(max(row-3, 0), row+1):
        if r + 3 < height:
            set_vals = set()
            for i in range(4):
                val = board[r+i][col]
                set_vals.add(val)
            if len(set_vals) == 1:
                w = int(next(iter(set_vals)))
                return w
    
    # search positively sloped diagonal
    for i in range(0, min(row, width - col - 1) + 1):
        if row + 3 - i < height and col - 3 + i >= 0:
            set_vals = set()
            for j in range(4):
                val = board[row-i+j][col+i-j]
                set_vals.add(val)
            if len(set_vals) == 1:
                w = int(next(iter(set_vals)))
                return w
        
    # search negatively sloped diagonal
    for i in range(0, min(row, col)+1):
        if row + 3 - i < height and col + 3 - i < width:
            set_vals = set()
            for j in range(4):
                val = board[row-i+j][col-i+j]
                set_vals.add(val)
            if len(set_vals) == 1:
                w = int(next(iter(set_vals)))
                return w
            
    return 0

def draw_board(board):
    for c in range(WIDTH):
        for r in range(HEIGHT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, (r+1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[r][c] == 1:  color = RED
            elif board[r][c] == 2: color = YELLOW
            else: color = BLACK
            
            pygame.draw.circle(screen, color, (int((c + 0.5) * SQUARE_SIZE), int((r+1.5) * SQUARE_SIZE)), RADIUS)
            
board = create_board(HEIGHT, WIDTH)
game_over = False
turn = 1

pygame.init()

SQUARE_SIZE = 100
SCREEN_WIDTH = WIDTH * SQUARE_SIZE
SCREEN_HEIGHT = (HEIGHT+1) * SQUARE_SIZE 
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

RADIUS = int(0.8 * SQUARE_SIZE / 2)

screen = pygame.display.set_mode(SIZE)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while True:
    for event in pygame.event.get():
        if not game_over:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SQUARE_SIZE))
                x, y = event.pos
                if turn == 1: color = RED
                else: color = YELLOW
                pygame.draw.circle(screen, color, (x, int(SQUARE_SIZE/2)), RADIUS)
            pygame.display.update()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = int(x / SQUARE_SIZE)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, turn)
                draw_board(board)
                turn = (turn%2)+1
                w = winner(board, row, col)
                game_over = w != 0   
            pygame.display.update()
        
        else:
            draw_board(board)
            pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SQUARE_SIZE))
            pygame.display.update()
            if w == 1:
                label = myfont.render("Player 1 wins!", 1, RED)
            elif w == 2:
                label = myfont.render("Player 2 wins!", 1, YELLOW)
            else:
                label = myfont.render("Tie game", 1, WHITE)
            screen.blit(label, (40,10))
            pygame.time.wait(3000)
            pygame.display.update()
