
import math
import random
import numpy as np

def evaluate_window(window, piece):
    score = 0
    opp_piece = 3 - piece

    if window.count(piece) == 4:
        score += 1000  # immediate win
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 50   # setup for win
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 5    # decent setup

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 80   # block opponent's win
    elif window.count(opp_piece) == 4:
        score -= 1000  # urgent block (theoretically already terminal)

    return score

def score_position(board, piece):
    score = 0
    ROW_COUNT = board.shape[0]
    COLUMN_COUNT = board.shape[1]

    # Score center column a bit (encourages middle play)
    center_col = COLUMN_COUNT // 2
    center_array = list(board[:, center_col])
    center_count = center_array.count(piece)
    score += center_count * 2

    # Score horizontal
    for r in range(ROW_COUNT):
        row_array = list(board[r, :])
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN_COUNT):
        col_array = list(board[:, c])
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score positive diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board_obj):
    return board_obj.has_four_in_a_row(1) or board_obj.has_four_in_a_row(2) or board_obj.is_full()

def get_valid_locations(board_obj):
    return [col for col in range(board_obj.column_count) if board_obj.is_valid_location(col)]

def greedy_move(board_obj, piece):
    valid_locations = get_valid_locations(board_obj)
    best_score = -math.inf
    best_col = random.choice(valid_locations)  # fallback

    for col in valid_locations:
        row = board_obj.get_next_open_row(col)
        temp_board = np.copy(board_obj.grid)
        board_obj.drop_piece(row, col, piece)
        score = score_position(board_obj.grid, piece)
        board_obj.grid = temp_board  # restore original state

        if score > best_score:
            best_score = score
            best_col = col

    return best_col
