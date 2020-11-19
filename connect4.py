import sys
import tkinter
import tkinter.messagebox

import pygame

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
    # Setup game
    tkinter.Tk().wm_withdraw()  # Hide tkinter main application window, only using messagebox
    pygame.init()
    pygame.display.set_caption('Connect 4')
    pane = Pane(6, 7, 90)
    pane.draw_background()
    continue_playing = True
    turn = 1
    current_color = RED

    # Begin gameplay
    while continue_playing:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pane.track_mouse_motion(event.pos[0], current_color)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pane.try_drop_piece(event.pos[0], turn):
                    pane.fill_in_pieces()
                    if pane.board.has_four_in_a_row(turn):  # Check if the current player won
                        continue_playing = prompt_player(turn)
                        pane.reset()
                    elif pane.board.is_full():  # Check if there is a draw
                        continue_playing = prompt_player()
                        pane.reset()
                    else:  # Prepare next turn
                        turn = 1 if turn == 2 else 2  # Alternate turn between 1 and 2 after each valid selection
                        current_color = RED if turn == 1 else YELLOW  # Player 1 color is red, player 2 is yellow
                        pane.track_mouse_motion(event.pos[0], current_color)  # Switch the next piece color


if __name__ == "__main__":
    main()
