import sys
import tkinter
import tkinter.messagebox
from tkinter import simpledialog

import pygame
import random
import board

# Color constants
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


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
                pygame.draw.rect(self.screen, BLUE, (left, top, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, BLACK, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pygame.display.update()

    def fill_in_pieces(self):
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                value = self.board.grid[r, c]
                if value == 1:
                    color = RED
                elif value == 2:
                    color = YELLOW
                else:
                    color = BLACK
                x = c * self.square_size + self.circle_offset
                y = self.height - (r * self.square_size + self.circle_offset)
                pygame.draw.circle(self.screen, color, (x, y), self.radius)
        pygame.display.update()

    def track_mouse_motion(self, x_pos, color):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
        pygame.draw.circle(self.screen, color, (x_pos, self.circle_offset), self.radius)
        pygame.display.update()

    def try_drop_piece(self, x_pos, turn):
        col = x_pos // self.square_size
        if self.board.is_valid_location(col):
            row = self.board.get_next_open_row(col)
            self.board.drop_piece(row, col, turn)
            return True
        return False

    def reset(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.board.reset()
        self.draw_background()
        self.fill_in_pieces()


def get_random_valid_column(board_obj):
    valid_columns = [c for c in range(board_obj.column_count) if board_obj.is_valid_location(c)]
    return random.choice(valid_columns) if valid_columns else None


def prompt_mode():
    root = tkinter.Tk()
    root.withdraw()
    mode = simpledialog.askstring("Select Mode", "Choose game mode:\n1: Player vs Player\n2: Player vs AI\n3: AI vs AI")
    return mode


def prompt_player(winner=False):
    title = 'Game Over!'
    message = f'Player {winner} wins! Play again?' if winner else 'It was a draw. Play again?'
    return tkinter.messagebox.askyesno(title=title, message=message)


def main():
    pygame.init()
    pygame.display.set_caption('Connect 4')

    mode = prompt_mode()
    if mode not in ['1', '2', '3']:
        print("Invalid mode selected.")
        return

    pane = Pane(6, 7, 90)
    font = pygame.font.SysFont("monospace", 30)

    continue_playing = True
    turn = 1
    current_color = RED
    game_mode = int(mode)

    pane.draw_background()

    while continue_playing:
        if game_mode == 1:  # Player vs Player
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    pane.track_mouse_motion(event.pos[0], current_color)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pane.try_drop_piece(event.pos[0], turn):
                        pane.fill_in_pieces()
                        if pane.board.has_four_in_a_row(turn):
                            continue_playing = prompt_player(turn)
                            pane.reset()
                        elif pane.board.is_full():
                            continue_playing = prompt_player()
                            pane.reset()
                        else:
                            turn = 2 if turn == 1 else 1
                            current_color = RED if turn == 1 else YELLOW

        elif game_mode == 2:  # Player vs AI
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION and turn == 1:
                    pane.track_mouse_motion(event.pos[0], current_color)
                elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1:
                    if pane.try_drop_piece(event.pos[0], turn):
                        pane.fill_in_pieces()
                        if pane.board.has_four_in_a_row(turn):
                            continue_playing = prompt_player(turn)
                            pane.reset()
                        elif pane.board.is_full():
                            continue_playing = prompt_player()
                            pane.reset()
                        else:
                            turn = 2
                            current_color = YELLOW

            if turn == 2:
                pygame.time.wait(500)
                col = get_random_valid_column(pane.board)
                if col is not None:
                    row = pane.board.get_next_open_row(col)
                    pane.board.drop_piece(row, col, turn)
                    pane.fill_in_pieces()
                    if pane.board.has_four_in_a_row(turn):
                        continue_playing = prompt_player(turn)
                        pane.reset()
                    elif pane.board.is_full():
                        continue_playing = prompt_player()
                        pane.reset()
                    else:
                        turn = 1
                        current_color = RED

        elif game_mode == 3:  # AI vs AI
            pygame.time.wait(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            col = get_random_valid_column(pane.board)
            if col is not None:
                row = pane.board.get_next_open_row(col)
                pane.board.drop_piece(row, col, turn)
                pane.fill_in_pieces()
                if pane.board.has_four_in_a_row(turn):
                    continue_playing = prompt_player(turn)
                    pane.reset()
                elif pane.board.is_full():
                    continue_playing = prompt_player()
                    pane.reset()
                else:
                    turn = 2 if turn == 1 else 1
                    current_color = RED if turn == 1 else YELLOW


if __name__ == "__main__":
    main()
