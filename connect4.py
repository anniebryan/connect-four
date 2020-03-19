import numpy as np
import pygame

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

HEIGHT, WIDTH = 6,7
board = create_board(HEIGHT, WIDTH)
game_over = False
turn = 1

pygame.init()

SQUARE_SIZE = 100
SCREEN_WIDTH = WIDTH * SQUARE_SIZE
SCREEN_HEIGHT = (HEIGHT+1) * SQUARE_SIZE 
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(SIZE)

while not game_over:
    board, row, col, turn = play_turn(turn)
    print(board)
    w = winner(board, row, col)
    game_over = w != 0
    if game_over:
        text = ("Player {} wins!").format(w)
        print(text)
