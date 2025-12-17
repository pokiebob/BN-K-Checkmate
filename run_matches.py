import argparse

from agents import random_policy
from minimax import Heuristic, minimax_policy
from alphabeta import alphabeta_policy
from scoring import evaluate

from play_game import play_game


def make_policy(policy: str, depth: int):
    if policy == "random":
        return random_policy(), f"Random"

    if policy == "minimax":
        h = Heuristic(evaluate)
        return minimax_policy(depth, h), f"Minimax at depth={depth}"
    
    if policy == "alphabeta":
        h = Heuristic(evaluate)
        return alphabeta_policy(depth, h), f"AlphaBeta at depth={depth}"

    raise ValueError(f"Unknown policy: {policy}. Please select from: random, minimax")


def main():
    parser = argparse.ArgumentParser(description="Run BNK endgame matches between two agents.")
    parser.add_argument("--matches", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-moves", type=int, default=100)
    parser.add_argument("--viz", action="store_true")
    parser.add_argument("--depth", type=int, default=3, help="Agent depth")

    parser.add_argument("--white", type=str, default="random", help="random | minimax")
    parser.add_argument("--black", type=str, default="random", help="random | minimax")

    args = parser.parse_args()

    p0, label0 = make_policy(args.white, args.depth)
    p1, label1 = make_policy(args.black, args.depth)

    total_wins = 0
    total_draws = 0
    total_move_count = 0
    draw_reasons = {}
    for i in range(args.matches):
        print("======= Match {} =======".format(i + 1))
        payoff, reason, move_count = play_game(
            p0,
            p1,
            seed=args.seed + i,
            max_moves=args.max_moves,
            vizualize=args.viz,
        )

        if payoff == 1.0:
            total_wins += 1

        elif payoff == -1.0:
            raise ValueError("Black wins, which should not happen in BNK endgames.")

        else:
            assert payoff == 0.0
            total_draws += 1
            draw_reasons[reason] = draw_reasons.get(reason, 0) + 1
        
        total_move_count += move_count
        print('\n')

    average_move_count = total_move_count / args.matches

    print(f"After {args.matches} matches between {label0} and {label1}:")
    print(f"White wins: {total_wins} ({(total_wins / args.matches) * 100:.2f}%)")
    print(f"Draws: {total_draws} ({(total_draws / args.matches) * 100:.2f}%)")
    print(f"Draw reasons: {draw_reasons}")
    print(f"Average move count: {average_move_count:.2f}")



if __name__ == "__main__":
    main()
