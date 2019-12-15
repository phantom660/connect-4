import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def print_board(board):
    print(np.flip(board, 0))


def get_player_selection(turn):
    selection = -1
    while selection < 1 or selection > COLUMN_COUNT:
        selection = int(input(f'Player {turn}: Make your selection (1-{COLUMN_COUNT}): '))
    # Adjust user input by 1 to account for 0 based arrays
    return selection - 1 


def is_valid_location(board, column):
    # Check if last row in column is empty
    return board[ROW_COUNT - 1][column] == 0


def get_next_open_row(board, column):
    # Return first instance where row is empty
    for row in range(ROW_COUNT):
        if board[row][column] == 0:
            return row


def drop_piece(board, row, column, turn):
    board[row][column] = turn


def is_winning_move(board, turn):
    # Check horizontally
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == turn and board[r][c + 1] == turn and board[r][c + 2] == turn and board[r][c + 3] == turn:
                return True

    # Check vertically
    for r in range(ROW_COUNT - 2):
        for c in range(COLUMN_COUNT):
            if board[r][c] == turn and board[r + 1][c] == turn and board[r + 2][c] == turn and board[r + 3][c] == turn:
                return True

    # Check diagonally upward
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == turn and board[r + 1][c + 1] == turn and board[r + 2][c + 2] == turn and board[r + 3][c + 3] == turn:
                return True
    
    # Check diagonally downward
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if board[r][c] == turn and board[r - 1][c + 1] == turn and board[r - 2][c + 2] == turn and board[r - 3][c + 3] == turn:
                return True

    return False


board = create_board()
game_over = False
turn = 1

while not game_over:
    print_board(board)
    column_selection = get_player_selection(turn)
    while not is_valid_location(board, column_selection):
        print('Invalid selection. Column is full.')
        column_selection = get_player_selection(turn)
    row = get_next_open_row(board, column_selection)
    drop_piece(board, row, column_selection, turn)
    if is_winning_move(board, turn):
        game_over = True
        print_board(board)
        break
    turn = 1 if turn == 2 else 2  # Alternate turn between 1 and 2 each loop

print(f'Player {turn} wins!')