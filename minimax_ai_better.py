import math
import random
import numpy as np

def evaluate_window(window, piece):
    score = 0
    opp_piece = 3 - piece

    if window.count(piece) == 4:
        score += 1000000
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 1

    if window.count(opp_piece) == 4:
        score -= 10000
    elif window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 100

    return score

def score_position(board, piece):
    score = 0
    ROW_COUNT = board.shape[0]
    COLUMN_COUNT = board.shape[1]

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = list(board[r, :])
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = list(board[:, c])
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board_obj):
    return board_obj.has_four_in_a_row(1) or board_obj.has_four_in_a_row(2) or board_obj.is_full()

def get_valid_locations(board_obj):
    return [col for col in range(board_obj.column_count) if board_obj.is_valid_location(col)]


def minimax(board_obj, depth, alpha, beta, maximizingPlayer, piece):
    valid_locations = get_valid_locations(board_obj)
    terminal = is_terminal_node(board_obj)
    if depth == 0 or terminal:
        if terminal:
            if board_obj.has_four_in_a_row(piece):
                return (None, 100000000000000)
            elif board_obj.has_four_in_a_row(3 - piece):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board_obj.grid, piece))
    
    if maximizingPlayer:
        value = -math.inf
        best_column = valid_locations[0]
        for col in valid_locations:
            row = board_obj.get_next_open_row(col)
            temp_board = np.copy(board_obj.grid)
            board_obj.drop_piece(row, col, piece)
            new_score = minimax(board_obj, depth-1, alpha, beta, False, piece)[1]
            board_obj.grid = temp_board
            if new_score > value:
                value = new_score
                best_column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_column, value
    else:
        value = math.inf
        best_column = random.choice(valid_locations)
        for col in valid_locations:
            row = board_obj.get_next_open_row(col)
            temp_board = np.copy(board_obj.grid)
            board_obj.drop_piece(row, col, 3 - piece)
            new_score = minimax(board_obj, depth-1, alpha, beta, True, piece)[1]
            board_obj.grid = temp_board
            if new_score < value:
                value = new_score
                best_column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_column, value