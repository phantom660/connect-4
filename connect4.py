import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def get_player_input(turn):
    return int(input(f'Player {turn}: Make your selection (0-6): '))

def is_valid_location(board, column):
    pass

def drop_piece():
    pass

def get_next_open_row():
    pass

board = create_board()
game_over = False
turn = 1

while not game_over:
    print(board)
    column_selection = get_player_input(turn)
    turn = 2 if turn == 1 else 1