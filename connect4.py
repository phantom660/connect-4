import sys
import tkinter
import tkinter.messagebox

import pygame

import board

import random


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
        self.height = (row_count + 1) * square_size  # Additional row for next piece at top
        self.row_offset = square_size  # Used to account for additional row at top
        self.circle_offset = square_size // 2  # Used to center circle inside each grid square
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_background(self):
        # Draws a grid of blue rectangles with black circles superimposed at the center of each rectangle
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                left = c * self.square_size
                top = r * self.square_size + self.row_offset
                pygame.draw.rect(self.screen, BLUE, (left, top, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, BLACK, (left + self.circle_offset, top + self.circle_offset), self.radius)
        pygame.display.update()

    def fill_in_pieces(self):
        # Fills each spot on the board with the color of the piece at said spot
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                if self.board.grid[r, c] == 1:
                    current_color = RED
                elif self.board.grid[r, c] == 2:
                    current_color = YELLOW
                else:
                    current_color = BLACK
                x_position = c * self.square_size + self.circle_offset
                y_position = self.height - (r * self.square_size + self.circle_offset)  # Invert because pieces need to come from bottom up
                pygame.draw.circle(self.screen, current_color, (x_position, y_position), self.radius)
        pygame.display.update()

    def track_mouse_motion(self, x_position, current_color):
        # Moves next piece x position along the top of the pane as user moves mouse
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))  # Resets top of pane to black
        pygame.draw.circle(self.screen, current_color, (x_position, self.circle_offset), self.radius)
        pygame.display.update()

    def try_drop_piece(self, x_position, turn):
        # Converts user's mouse position into a column selection
        # Fills said column if column isn't full
        # Returns whether or not operation was completed
        column_selection = x_position // self.square_size
        if self.board.is_valid_location(column_selection):
            row = self.board.get_next_open_row(column_selection)
            self.board.drop_piece(row, column_selection, turn)
            return True
        return False

    def reset(self):
        # Prepares the Pane for another game
        self.screen = pygame.display.set_mode((self.width, self.height))  # Gives Pygame focus again
        self.board.reset()
        self.draw_background()
        self.fill_in_pieces()


def get_random_valid_column(board_obj):
    valid_columns = [c for c in range(board_obj.column_count) if board_obj.is_valid_location(c)]
    if valid_columns:
        return random.choice(valid_columns)
    return None

def prompt_player(winner = False):
    # Launches tkinter messagebox showing game end result
    # Asks user to play again and returns user's choice
    title = 'Game Over!'
    if winner:
        message = f'Player {winner} wins! Would you like to play again?'
    else:
        message = 'It was a draw. Would you like to play again?'
    return tkinter.messagebox.askyesno(title=title, message=message)

def main():
    tkinter.Tk().wm_withdraw()
    pygame.init()
    pygame.display.set_caption('Connect 4')
    pane = Pane(6, 7, 90)
    pane.draw_background()

    # New state variables
    play_vs_ai = False  # Default: Player vs Player

    font = pygame.font.SysFont("monospace", 30)
    ai_text = font.render("Press A to toggle AI Mode", True, (255, 255, 255))
    ai_status = lambda status: font.render(f"AI Mode: {'ON' if status else 'OFF'}", True, (255, 255, 255))

    pane.screen.blit(ai_text, (10, 10))
    pane.screen.blit(ai_status(play_vs_ai), (10, 40))
    pygame.display.update()

    continue_playing = True
    turn = 1
    current_color = RED

    while continue_playing:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    play_vs_ai = not play_vs_ai
                    pane.draw_background()
                    pane.fill_in_pieces()
                    pane.screen.blit(ai_text, (10, 10))
                    pane.screen.blit(ai_status(play_vs_ai), (10, 40))
                    pygame.display.update()

            elif event.type == pygame.MOUSEMOTION and (not play_vs_ai or turn == 1):
                pane.track_mouse_motion(event.pos[0], current_color)

            elif event.type == pygame.MOUSEBUTTONDOWN and (not play_vs_ai or turn == 1):
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

        # AI's turn
        if play_vs_ai and turn == 2:
            pygame.time.wait(500)  # Add a small delay for realism
            ai_column = get_random_valid_column(pane.board)
            if ai_column is not None:
                row = pane.board.get_next_open_row(ai_column)
                pane.board.drop_piece(row, ai_column, turn)
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


if __name__ == "__main__":
    main()
