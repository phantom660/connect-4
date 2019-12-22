import sys

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
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_background(self):
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                pygame.draw.rect(self.screen, BLUE, (c * self.square_size, r * self.square_size + self.square_size, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, BLACK, (c * self.square_size + self.square_size // 2, r * self.square_size + self.square_size + self.square_size // 2), self.radius)
        pygame.display.update()

    def fill_in_pieces(self):
        for r in range(self.board.row_count):
            for c in range(self.board.column_count):
                current_color = BLACK
                if self.board.grid[r][c] == 1:
                    current_color = RED
                elif self.board.grid[r][c] == 2:
                    current_color = YELLOW
                pygame.draw.circle(self.screen, current_color, (c * self.square_size + self.square_size // 2, self.height - (r * self.square_size + self.square_size // 2)), self.radius)
        pygame.display.update()

    def track_mouse_motion(self, x_position, current_color):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
        pygame.draw.circle(self.screen, current_color, (x_position, self.square_size // 2), self.radius)
        pygame.display.update()

    def try_drop_piece(self, x_position, turn):
        column_selection = x_position // self.square_size
        if self.board.is_valid_location(column_selection):
            row = self.board.get_next_open_row(column_selection)
            self.board.drop_piece(row, column_selection, turn)
            return True
        return False
        

pygame.init()
pane = Pane(6, 7, 90)
pane.draw_background()
game_over = False
turn = 1

while not game_over:

    for event in pygame.event.get():

        current_color = RED if turn == 1 else YELLOW  # Player 1 color is red, player 2 is yellow

        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.MOUSEMOTION:
            pane.track_mouse_motion(event.pos[0], current_color)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pane.try_drop_piece(event.pos[0], turn):
                pane.fill_in_pieces()
                if pane.board.has_four_in_a_row(turn):
                    game_over = True
                    pane.board.print_grid()
                    break
                turn = 1 if turn == 2 else 2  # Alternate turn between 1 and 2 after each valid selection

print(f'Player {turn} wins!')