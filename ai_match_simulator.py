import time
import math
import random
import board
import greedy_ai
import minimax_ai_H1
import mcts_ai

AI_TYPES = {
    "1": "RandomAI",
    "2": "GreedyAI",
    "3": "MinimaxAI-H1",
    "4": "MCTS"
}

def get_ai_move(ai_type, board_obj, piece):
    if ai_type == "RandomAI":
        return random.choice([c for c in range(board_obj.column_count) if board_obj.is_valid_location(c)])
    elif ai_type == "GreedyAI":
        return greedy_ai.greedy_move(board_obj, piece)
    elif ai_type == "MinimaxAI-H1":
        col, _ = minimax_ai_H1.minimax(board_obj, depth=4, alpha=-math.inf, beta=math.inf, maximizingPlayer=True, piece=piece)
        return col
    elif ai_type == "MCTS":
        return mcts_ai.mcts_move(board_obj, piece)
    else:
        raise ValueError(f"Unknown AI type: {ai_type}")

def simulate_game(p1_type, p2_type):
    game_board = board.Board(6, 7)
    turn = 1
    player_types = {1: p1_type, 2: p2_type}
    
    move_times = {1: [], 2: []}

    while True:
        current_player = turn
        ai_type = player_types[current_player]

        start_time = time.time()
        col = get_ai_move(ai_type, game_board, current_player)
        move_duration = time.time() - start_time
        move_times[current_player].append(move_duration)

        if col is not None and game_board.is_valid_location(col):
            row = game_board.get_next_open_row(col)
            game_board.drop_piece(row, col, current_player)

            if game_board.has_four_in_a_row(current_player):
                return current_player, move_times
            elif game_board.is_full():
                return 0, move_times
            turn = 2 if turn == 1 else 1
        else:
            return 3 - current_player, move_times

def run_matchup(ai1, ai2, num_games):
    stats = {
        "P1 Wins": 0,
        "P2 Wins": 0,
        "Draws": 0,
        "P1 Time": 0.0,
        "P2 Time": 0.0,
        "P1 Moves": 0,
        "P2 Moves": 0
    }

    for i in range(num_games):
        if i % 2 == 0:
            p1_type, p2_type = ai1, ai2
        else:
            p1_type, p2_type = ai2, ai1

        result, move_times = simulate_game(p1_type, p2_type)

        # Determine which AI is actually Player 1 and Player 2 in this game
        if i % 2 == 0:
            ai1_player, ai2_player = 1, 2
        else:
            ai1_player, ai2_player = 2, 1

        # Accumulate times and move counts
        stats["P1 Time"] += sum(move_times[ai1_player])
        stats["P2 Time"] += sum(move_times[ai2_player])
        stats["P1 Moves"] += len(move_times[ai1_player])
        stats["P2 Moves"] += len(move_times[ai2_player])

        if result == ai1_player:
            stats["P1 Wins"] += 1
        elif result == ai2_player:
            stats["P2 Wins"] += 1
        else:
            stats["Draws"] += 1

    return stats

def print_stats(ai1, ai2, stats, num_games):
    print(f"\n=== Matchup: {ai1} vs {ai2} ===")
    print(f"Total Games: {num_games}")
    print(f"{ai1} Wins: {stats['P1 Wins']}")
    print(f"{ai2} Wins: {stats['P2 Wins']}")
    print(f"Draws: {stats['Draws']}")

    print("\nWin Rate:")
    print(f"{ai1}: {(stats['P1 Wins'] / num_games) * 100:.2f}%")
    print(f"{ai2}: {(stats['P2 Wins'] / num_games) * 100:.2f}%")
    print(f"Draws: {(stats['Draws'] / num_games) * 100:.2f}%")

    avg_p1_time = stats["P1 Time"] / stats["P1 Moves"] if stats["P1 Moves"] > 0 else 0
    avg_p2_time = stats["P2 Time"] / stats["P2 Moves"] if stats["P2 Moves"] > 0 else 0

    print("\nAverage Move Time:")
    print(f"{ai1}: {avg_p1_time:.4f} sec/move")
    print(f"{ai2}: {avg_p2_time:.4f} sec/move")
    print("====================================\n")

def main():
    print("Available AIs:")
    for key, name in AI_TYPES.items():
        print(f"{key}: {name}")
    
    p1_choice = input("Select AI 1 (as Player 1 half the time): ")
    p2_choice = input("Select AI 2 (as Player 2 half the time): ")
    num_games = int(input("How many games to simulate? "))

    if p1_choice not in AI_TYPES or p2_choice not in AI_TYPES:
        print("Invalid AI selection.")
        return

    ai1 = AI_TYPES[p1_choice]
    ai2 = AI_TYPES[p2_choice]

    stats = run_matchup(ai1, ai2, num_games)
    print_stats(ai1, ai2, stats, num_games)

if __name__ == "__main__":
    main()
