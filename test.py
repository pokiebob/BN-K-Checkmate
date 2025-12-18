"""
INTERACTIVE TEST SCRIPT

Quick start:
    make
or  python test.py

Press Enter to proceed through each section.
"""

import time
from play_game import play_game
from run_matches import make_policy, time_pretty


PRECOMPUTED_STATS = {
    ("random", 2): "WIN RATE: 55%, AVG MOVE COUNT: 76.62, AVG TIME: 1.5s",
    ("random", 3): "WIN RATE: 80%, AVG MOVE COUNT: 63.26, AVG TIME: 1.7s",
    ("random", 4): "WIN RATE: 97%, AVG MOVE COUNT: 49.08, AVG TIME: 2.5s",
    ("random", 5): "WIN RATE: 97%, AVG MOVE COUNT: 46.52, AVG TIME: 27.1s",

    ("greedy_defender", 2): "WIN RATE: 7%, AVG MOVE COUNT: 93.96, AVG TIME: 0.3s",
    ("greedy_defender", 3): "WIN RATE: 20%, AVG MOVE COUNT: 87.03, AVG TIME: 2.5s",
    ("greedy_defender", 4): "WIN RATE: 87%, AVG MOVE COUNT: 67.48, AVG TIME: 3.6s",
    ("greedy_defender", 5): "WIN RATE: 82%, AVG MOVE COUNT: 70.86, AVG TIME: 43.6s",
}

MATCHUP_ANALYSIS = {
    ("random", 2): "At depth 2, AlphaBeta manages to win just over half the time against a random defender",
    ("random", 3): "Increasing to depth 3 significantly improves the agent's ability to herd and checkmate",
    ("random", 4): "Depth 4 sees a nearly solved win rate without sacrificing much time",
    ("random", 5): "Depth 5 doesn't seem to improve win rate but it does sacrifice significant time",
    ("greedy_defender", 2): "Greedy defender easy beats AlphaBeta at depth 2",
    ("greedy_defender", 3): "While AlphaBeta at depth 3 could beat the random defender, it struggles with greedy",
    ("greedy_defender", 4): "Depth 4 sees a huge jump in win rate, and still at a rapid time",
    ("greedy_defender", 5): "Surprisingly, depth 5 drops in win rate slightly while increasing time drastically",
}



def hr():
    print("\n" + "-" * 80 + "\n")

def clear_screen():
    print("\033[2J", end="")

def banner(title):
    clear_screen()
    width = max(80, len(title) + 8)
    print("=" * width)
    print(title.center(width))
    print("=" * width)
    print()


def prompt_play_or_skip():
    while True:
        ans = input("--- Type p or enter to play demo! Type s to skip :( ---").strip().lower()
        if ans in ("", "p", "play"):
            return True
        if ans in ("s", "skip"):
            return False
        print("Invalid input")

def intro_page():
    print("\nThe Bishop and Knight Checkmate")
    print("Analysis of AlphaBeta pruning performance in BNK endgames\n")
    print("CREATED BY: Cyrus Cursetjee")
    hr()
    print("PROBLEM:")
    print("The bishop knight checkmate is an obscure and difficult to execute checkmate.")
    print("Even grandmasters struggle with it under time pressure!")
    print("You don't need stockfish to figure it out, but you may need AlphaBeta pruning...")
    print("This demo will walk you through the optimal depth for AlphaBeta to solve BNK endgames.")
    hr()
    print("BACKGROUND:")
    print("The goal for white is to win by checkmate, and the goal for black is to draw.")
    print("White must herd the black king to a corner with the same color square as the bishop.")
    print("White must avoid: stalemate, insufficient material, fifty-move rule, threefold repetition.")
    hr()
    print("HEURISTICS (see scoring.py):")
    print(" - Distance of black king to target corner / edge")
    print(" - Mobility of black king")
    print(" - Coordination of white pieces")
    print(" - Distance between the two kings")
    hr()
    print("INSTRUCTIONS:")
    print(" - This interactive script will walk you through AlphaBeta performance vs random and greedy defenders.")
    print(" - For each matchup, you can choose to play out the demo, or skip to the precomputed stats over 100 games.")
    print(" - There will also be some analysis along the way!")
    hr()
    print("Expand your terminal window for best visualization experience.")
    hr()


def matchup_intro(defender_label, depth):

    hr()
    if depth < 5:
        print("Demo: 10 games with random setups vs {}.".format(defender_label))
    else:
        print("Depth 5 is slower, so just 1 game vs {}!".format(defender_label))
    hr()


def run_demo_games(p0, p1, label0, label1, demo_n, seed0, depth):
    total_wins = 0
    total_draws = 0
    total_move_count = 0
    draw_reasons = {}

    t0_total = time.perf_counter()

    for i in range(demo_n):
        print("======= Match {} =======".format(i + 1))

        t0_match = time.perf_counter()
        payoff, reason, move_count = play_game(
            p0,
            p1,
            seed=seed0 + i,
            max_moves=100,
            vizualize=depth > 3,
            progress=(total_wins, total_draws, i),
        )
        t1_match = time.perf_counter()

        dt_match = t1_match - t0_match

        if payoff == 1.0:
            total_wins += 1
        elif payoff == -1.0:
            raise ValueError("Black wins, which should not happen in BNK endgames.")
        else:
            total_draws += 1
            draw_reasons[reason] = draw_reasons.get(reason, 0) + 1

        total_move_count += move_count

        elapsed_total = time.perf_counter() - t0_total
        avg_time_so_far = elapsed_total / (i + 1)

        print(f"Match time: {time_pretty(dt_match)}")
        print(f"Total time: {time_pretty(elapsed_total)} | Avg/match so far: {time_pretty(avg_time_so_far)}")
        print()

    average_move_count = total_move_count / demo_n if demo_n else 0.0
    total_elapsed = time.perf_counter() - t0_total
    avg_time = total_elapsed / demo_n if demo_n else 0.0

    print(f"After {demo_n} matches between {label0} and {label1}:")
    print(f"White wins: {total_wins} ({(total_wins / demo_n) * 100:.2f}%)")
    print(f"Draws: {total_draws} ({(total_draws / demo_n) * 100:.2f}%)")
    print(f"Draw reasons: {draw_reasons}")
    print(f"Average move count: {average_move_count:.2f}")
    print(f"Total time: {time_pretty(total_elapsed)}")
    print(f"Average time/game: {time_pretty(avg_time)}")


def run_section(defender_name):
    p1, label1 = make_policy(defender_name, None)
    SEED = 42

    banner(f"ALPHABETA vs {label1.upper()}")


    for depth in [2, 3, 4, 5]:
        banner(f"DEPTH {depth}  —  ALPHABETA vs {label1.upper()}")
        p0, label0 = make_policy("alphabeta", depth)
        demo_n = 10 if depth < 5 else 1

        matchup_intro(label1, depth)

        if prompt_play_or_skip():
            seed0 = SEED + 10000 * (depth + (0 if defender_name == "random" else 1))
            run_demo_games(p0, p1, label0, label1, demo_n, seed0, depth)
        else:
            print("\nSkipping demos :(")

        hr()

        print("\nPRECOMPUTED STATISTICS:")
        key = (defender_name, depth)
        stats_text = PRECOMPUTED_STATS.get(key)
        print(f"  {label0} vs {label1} over 100 matches")
        print(f"  {stats_text}")
        analysis_text = MATCHUP_ANALYSIS.get(key)
        print("\nANALYSIS:")
        print(f"  {analysis_text}")
        hr()
        if depth < 5:
            input("Press Enter to continue to the next depth!")


def outro():
    hr()
    print("Thanks for running this demo!")
    hr()
    print("You can run_matches.py to recreate higher quantity matchups. For example:\n")
    print("  python run_matches.py --white alphabeta --black greedy_defender --depth 4 --matches 100 --viz")
    hr()


def main():

    intro_page()
    input("Press Enter to begin the first section...")
    banner("ALPHABETA vs. RANDOM AGENT")

    run_section("random")
    clear_screen()
    print("Greedy defender runs away from the two target corners and makes a draw when possible.")
    input("Press Enter to continue to the Greedy section.")

    run_section("greedy_defender")

    clear_screen()
    outro()

if __name__ == "__main__":
    main()
