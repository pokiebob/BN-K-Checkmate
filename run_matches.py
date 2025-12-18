import argparse
import time

from agents import random_policy, greedy_policy
from minimax import Heuristic, minimax_policy
from alphabeta import alphabeta_policy
from scoring import evaluate, defender_eval

from play_game import play_game


def make_policy(policy: str, depth: int):

    # BLACK POLICIES
    if policy == "random":
        return random_policy(), "Random"
    
    if policy == "greedy_defender":
        return greedy_policy(defender_eval), "Greedy Defender"

    # WHITE POLICIES
    if policy == "minimax":
        h = Heuristic(evaluate)
        return minimax_policy(depth, h), f"Minimax at depth={depth}"

    if policy == "alphabeta":
        h = Heuristic(evaluate)
        return alphabeta_policy(depth, h), f"AlphaBeta at depth={depth}"

    raise ValueError(f"Unknown policy: {policy}. Please select from: random, minimax, alphabeta")


def time_pretty(s: float):
    if s < 60:
        return f"{s:.1f}s"

    m, sec = divmod(s, 60)
    sec = round(sec, 1)

    if m < 60:
        return f"{int(m)}m{sec:04.1f}s"

    h, rem = divmod(m, 60)
    return f"{int(h)}h{int(rem):02d}m{sec:04.1f}s"



def main():
    parser = argparse.ArgumentParser(description="Run BNK endgame matches between two agents.")
    parser.add_argument("--matches", type=int, default=1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-moves", type=int, default=100)
    parser.add_argument("--viz", action="store_true")
    parser.add_argument("--depth", type=int, default=3, help="Agent depth")

    parser.add_argument("--white", type=str, default="random", help="random | minimax | alphabeta")
    parser.add_argument("--black", type=str, default="random", help="random | minimax | alphabeta")

    args = parser.parse_args()

    p0, label0 = make_policy(args.white, args.depth)
    p1, label1 = make_policy(args.black, args.depth)

    total_wins = 0
    total_draws = 0
    total_move_count = 0
    draw_reasons = {}

    match_times = []
    t0_total = time.perf_counter()

    for i in range(args.matches):
        print("======= Match {} =======".format(i + 1))

        t0_match = time.perf_counter()
        payoff, reason, move_count = play_game(
            p0,
            p1,
            seed=args.seed + i,
            max_moves=args.max_moves,
            vizualize=args.viz,
            progress=(total_wins, total_draws, i)
        )
        t1_match = time.perf_counter()

        dt_match = t1_match - t0_match
        match_times.append(dt_match)

        if payoff == 1.0:
            total_wins += 1
        elif payoff == -1.0:
            raise ValueError("Black wins, which should not happen in BNK endgames.")
        else:
            assert payoff == 0.0
            total_draws += 1
            draw_reasons[reason] = draw_reasons.get(reason, 0) + 1

        total_move_count += move_count

        elapsed_total = time.perf_counter() - t0_total
        avg_time_so_far = elapsed_total / (i + 1)

        print(f"Match time: {time_pretty(dt_match)}")
        print(f"Total time: {time_pretty(elapsed_total)} | Avg/match so far: {time_pretty(avg_time_so_far)}")
        print()

    average_move_count = total_move_count / args.matches
    total_elapsed = time.perf_counter() - t0_total
    avg_time = total_elapsed / args.matches

    print(f"After {args.matches} matches between {label0} and {label1}:")
    print(f"White wins: {total_wins} ({(total_wins / args.matches) * 100:.2f}%)")
    print(f"Draws: {total_draws} ({(total_draws / args.matches) * 100:.2f}%)")
    print(f"Draw reasons: {draw_reasons}")
    print(f"Average move count: {average_move_count:.2f}")
    print(f"Total time: {time_pretty(total_elapsed)}")
    print(f"Average time/game: {time_pretty(avg_time)}")


if __name__ == "__main__":
    main()
