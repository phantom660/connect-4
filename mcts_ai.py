import copy
import math
import random
import time

SIMULATION_TIME = 0.25  # seconds to simulate

class Node:
    def __init__(self, board_obj, parent=None, move=None, player=1):
        self.board = copy.deepcopy(board_obj)
        self.parent = parent
        self.move = move
        self.player = player
        self.children = []
        self.visits = 0
        self.wins = 0

    def expand(self):
        valid_moves = [c for c in range(self.board.column_count) if self.board.is_valid_location(c)]
        for col in valid_moves:
            new_board = copy.deepcopy(self.board)
            row = new_board.get_next_open_row(col)
            new_board.drop_piece(row, col, self.player)
            child = Node(new_board, parent=self, move=col, player=3 - self.player)
            self.children.append(child)

    def is_fully_expanded(self):
        return len(self.children) > 0

    def best_child(self, c_param=1.41):
        unvisited = [child for child in self.children if child.visits == 0]
        if unvisited:
            return random.choice(unvisited)

        return max(self.children, key=lambda node:
            node.wins / node.visits + c_param * math.sqrt(math.log(self.visits) / node.visits))


def simulate_game(board_obj, player):
    temp_board = copy.deepcopy(board_obj)
    current_player = player
    while not temp_board.is_full():
        if temp_board.has_four_in_a_row(1):
            return 1
        elif temp_board.has_four_in_a_row(2):
            return 2
        valid_cols = [c for c in range(temp_board.column_count) if temp_board.is_valid_location(c)]
        col = random.choice(valid_cols)
        row = temp_board.get_next_open_row(col)
        temp_board.drop_piece(row, col, current_player)
        current_player = 3 - current_player
    return 0  # Draw

def mcts_move(board_obj, piece):
    root = Node(board_obj, player=piece)
    start_time = time.time()

    while time.time() - start_time < SIMULATION_TIME:
        node = root
        # Selection
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # Expansion
        if not node.is_fully_expanded():
            node.expand()

        # Simulation
        if node.children:
            node = random.choice(node.children)

        result = simulate_game(node.board, node.player)

        # Backpropagation
        while node is not None:
            node.visits += 1
            if result == piece:
                node.wins += 1
            elif result == 3 - piece:
                node.wins -= 1
            node = node.parent

    best = max(root.children, key=lambda n: n.visits)
    return best.move
