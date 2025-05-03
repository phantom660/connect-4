import sys
import tkinter
import tkinter.messagebox
from tkinter import simpledialog
import pygame
import random
import board
import minimax_ai_better
import math
import time


# Color constants
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BG = (245, 245, 245)
LIGHT_BLUE = (173, 216, 230)   
WHITE = (255, 255, 255)

performance_stats = {
    "move_times": [],
    "ai_move_count": 0
}



class Pane:
    def __init__(self, row_count, column_count, square_size):
        self.board = board.Board(row_count, column_count)
        self.square_size = square_size
        self.radius = square_size // 2 - 5
        self.width = column_count * square_size
        self.height = (row_count + 1) * square_size
        self.row_offset = square_size
        self.circle_offset = square_size // 2
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_background(self):
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                left = c * self.square_size
                top = r * self.square_size + self.row_offset
                pygame.draw.rect(self.screen, LIGHT_BLUE, (left, top, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, WHITE, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pygame.display.update()

    def fill_in_pieces(self):
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                value = self.board.grid[r, c]
                color = RED if value == 1 else YELLOW if value == 2 else LIGHT_BG
                x = c * self.square_size + self.circle_offset
                y = self.height - (r * self.square_size + self.circle_offset)
                pygame.draw.circle(self.screen, color, (x, y), self.radius)
        pygame.display.update()

    def track_mouse_motion(self, x_pos, color):
        pygame.draw.rect(self.screen, LIGHT_BG, (0, 0, self.width, self.square_size))
        pygame.draw.circle(self.screen, color, (x_pos, self.circle_offset), self.radius)
        pygame.display.update()

    def try_drop_piece(self, col, turn):
        if self.board.is_valid_location(col):
            row = self.board.get_next_open_row(col)
            self.board.drop_piece(row, col, turn)
            return True
        return False

    def reset(self):
        self.board.reset()
        self.draw_background()
        self.fill_in_pieces()


def get_random_valid_column(board_obj):
    valid_columns = [c for c in range(board_obj.column_count) if board_obj.is_valid_location(c)]
    return random.choice(valid_columns) if valid_columns else None


def prompt_players():
    root = tkinter.Tk()
    root.withdraw()

    options = {
        "1": "Human",
        "2": "RandomAI",
        "3": "MinimaxAI"
    }

    p1 = simpledialog.askstring("Player 1", "Select Player 1:\n1: Human\n2: RandomAI\n3: MinimaxAI")
    p2 = simpledialog.askstring("Player 2", "Select Player 2:\n1: Human\n2: RandomAI\n3: MinimaxAI")

    if p1 in options and p2 in options:
        return options[p1], options[p2]
    else:
        return None, None
    

def prompt_restart(winner=None):
    title = "Game Over!"
    if winner:
        message = f"Player {winner} wins! Play again?"
    else:
        message = "It's a draw! Play again?"
    return tkinter.messagebox.askyesno(title=title, message=message)


def check_game_end(pane, turn):
    if pane.board.has_four_in_a_row(turn):
        return prompt_restart(turn)
    elif pane.board.is_full():
        return prompt_restart()
    return None  # Game not over


def play_custom_game(pane, player1_type, player2_type):
    turn = 1
    color_map = {1: RED, 2: YELLOW}
    player_types = {1: player1_type, 2: player2_type}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        current_type = player_types[turn]
        current_color = color_map[turn]

        if current_type == "Human":
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    pane.track_mouse_motion(event.pos[0], current_color)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // pane.square_size
                    if pane.try_drop_piece(col, turn):
                        pane.fill_in_pieces()
                        performance_stats[turn]["moves"] += 1
                        performance_stats[turn]["times"].append(0)  # human time not timed
                        if (r := check_game_end(pane, turn)) is not None:
                            return r
                        turn = 2 if turn == 1 else 1
            continue

        elif current_type == "RandomAI":
            pygame.time.wait(300)
            start_time = time.time()
            col = get_random_valid_column(pane.board)
            duration = time.time() - start_time
        elif current_type == "MinimaxAI":
            pygame.time.wait(300)
            start_time = time.time()
            col, _ = minimax_ai_better.minimax(pane.board, depth=6, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, piece=turn)
            duration = time.time() - start_time
        else:
            print(f"Unknown player type: {current_type}")
            sys.exit()

        if col is not None and pane.try_drop_piece(col, turn):
            pane.fill_in_pieces()
            performance_stats[turn]["moves"] += 1
            performance_stats[turn]["times"].append(duration)
            print(f"[Player {turn} - {current_type}] Move took {duration:.3f} seconds")
            if (r := check_game_end(pane, turn)) is not None:
                return r
            turn = 2 if turn == 1 else 1

def report_stats():
    print("\n===== Game Performance Stats =====")
    for player in [1, 2]:
        moves = performance_stats[player]["moves"]
        times = performance_stats[player]["times"]
        if moves:
            avg_time = sum(times) / moves
            print(f"Player {player} | Type: {player_types[player]} | Moves: {moves} | Avg Time: {avg_time:.3f}s")
        else:
            print(f"Player {player} made no moves.")
    print("==================================\n")

def main():
    pygame.init()
    pygame.display.set_caption("Connect 4")

    while True:
        player1_type, player2_type = prompt_players()
        if not player1_type or not player2_type:
            print("Invalid selection. Exiting.")
            break

        pane = Pane(6, 7, 90)
        pane.draw_background()

        global performance_stats
        global player_types
        performance_stats = {1: {"times": [], "moves": 0}, 2: {"times": [], "moves": 0}}
        player_types = {1: player1_type, 2: player2_type}

        again = play_custom_game(pane, player1_type, player2_type)
        report_stats()

        if not again:
            print("Thanks for playing!")
            break
        pane.reset()


if __name__ == "__main__":
    main()
