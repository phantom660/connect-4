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
                color = RED if value == 1 else YELLOW if value == 2 else BLACK
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


def prompt_mode():
    root = tkinter.Tk()
    root.withdraw()
    return simpledialog.askstring("Select Mode", "Choose game mode:\n1: Player vs Player\n2: Player vs RandomAI\n3: RandomAI vs RandomAI\n4: Player vs MinimaxAI\n5: MinimaxAI vs MinimaxAI")


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


def play_pvp(pane):
    turn = 1
    current_color = RED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                pane.track_mouse_motion(event.pos[0], current_color)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // pane.square_size
                if pane.try_drop_piece(col, turn):
                    pane.fill_in_pieces()
                    game_continue = check_game_end(pane, turn)
                    if game_continue is not None:
                        return game_continue
                    turn = 2 if turn == 1 else 1
                    current_color = RED if turn == 1 else YELLOW


def play_pvrandomai(pane):
    turn = 1
    current_color = RED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION and turn == 1:
                pane.track_mouse_motion(event.pos[0], current_color)
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1:
                col = event.pos[0] // pane.square_size
                if pane.try_drop_piece(col, turn):
                    pane.fill_in_pieces()
                    game_continue = check_game_end(pane, turn)
                    if game_continue is not None:
                        return game_continue
                    turn = 2
                    current_color = YELLOW

        if turn == 2:
            pygame.time.wait(500)
            col = get_random_valid_column(pane.board)
            if col is not None and pane.try_drop_piece(col, turn):
                pane.fill_in_pieces()
                game_continue = check_game_end(pane, turn)
                if game_continue is not None:
                    return game_continue
                turn = 1
                current_color = RED


def play_randomaivsrandomai(pane):
    turn = 1
    current_color = RED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.time.wait(500)
        col = get_random_valid_column(pane.board)
        if col is not None and pane.try_drop_piece(col, turn):
            pane.fill_in_pieces()
            game_continue = check_game_end(pane, turn)
            if game_continue is not None:
                return game_continue
            turn = 2 if turn == 1 else 1
            current_color = RED if turn == 1 else YELLOW

def play_pvminimaxai(pane):
    turn = 1
    current_color = RED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION and turn == 1:
                pane.track_mouse_motion(event.pos[0], current_color)
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1:
                col = event.pos[0] // pane.square_size
                if pane.try_drop_piece(col, turn):
                    pane.fill_in_pieces()
                    game_continue = check_game_end(pane, turn)
                    if game_continue is not None:
                        return game_continue
                    turn = 2
                    current_color = YELLOW

        if turn == 2:

            start_time = time.time()

            col, _ = minimax_ai_better.minimax(pane.board, depth=6, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, piece=2)
            if col is not None and pane.try_drop_piece(col, turn):
                pane.fill_in_pieces()
                game_continue = check_game_end(pane, turn)
                if game_continue is not None:
                    return game_continue
                turn = 1
                current_color = RED

            duration = time.time() - start_time
            performance_stats["move_times"].append(duration)
            performance_stats["ai_move_count"] += 1
            print(f"[AI Move] Took {duration:.3f} seconds")

def play_minimax_vs_minimaxai(pane):
    turn = 1
    current_color = RED

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        start_time = time.time()

        col, _ = minimax_ai_better.minimax(pane.board, depth=6, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, piece=turn)
        if col is not None and pane.try_drop_piece(col, turn):
            pane.fill_in_pieces()
            game_continue = check_game_end(pane, turn)
            if game_continue is not None:
                return game_continue
            turn = 2 if turn == 1 else 1
            current_color = RED if turn == 1 else YELLOW

        duration = time.time() - start_time
        performance_stats["move_times"].append(duration)
        performance_stats["ai_move_count"] += 1
        print(f"[AI Move] Took {duration:.3f} seconds")


def main():
    pygame.init()
    pygame.display.set_caption("Connect 4")

    while True:
        mode = prompt_mode()
        if mode not in {'1', '2', '3', '4', '5'}:
            print("Invalid or no mode selected. Exiting.")
            break

        pane = Pane(6, 7, 90)
        pane.draw_background()

        if mode == '1':
            again = play_pvp(pane)
        elif mode == '2':
            again = play_pvrandomai(pane)
        elif mode == '3':
            again = play_randomaivsrandomai(pane)
        elif mode == '4':
            again = play_pvminimaxai(pane)
        elif mode == '5':
            again = play_minimax_vs_minimaxai(pane)

        if performance_stats["move_times"]:
            avg_time = sum(performance_stats["move_times"]) / len(performance_stats["move_times"])
            print(f"Total AI Moves: {performance_stats['ai_move_count']}")
            print(f"Average AI Move Time: {avg_time:.3f} seconds")

        if not again:
            print("Thanks for playing!")
            break
        pane.reset()


if __name__ == "__main__":
    main()
