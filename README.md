# BN-K-Checkmate

Analysis of effectiveness of alpha-beta pruning to solve the Bishop-Knight checkmate
Built on @python-chess

## Problem

The bishop knight checkmate is an obscure and difficult to execute checkmate.
Even grandmasters struggle with it under time pressure!
Goal: Find optimal AlphaBeta depth for efficient and consistent checkmate.

---

## Background

The goal for white is to win by checkmate, and the goal for black is to draw.
White must herd the black king to a corner with the same color square as the bishop.
White must avoid: stalemate, insufficient material, fifty-move rule, threefold repetition.

---

## Heuristics

- Distance of black king to target corner / edge
- Mobility of black king
- Coordination of white pieces
- Distance between the two kings

See scoring.py

---

## How to run

make - Runs demo script for overview of research
run_matches.py - Customize matchups and game counts, etc

Features: match number, seed, max moves, visuals, depth, white agent, black agent

Example: python run_matches.py --white alphabeta --black greedy_defender --depth 4 --matches 100 --viz

## Agents

### White (Bishop + Knight + King)

- Minimax
- AlphaBeta

### Black (King)

- Random
- Greedy (Escape)

Greedy defender runs away from the two target corners and makes a draw when possible.

## Conclusion

AlphaBeta at depth 4 has greatest consistency at low speeds. Depth 5 provides no significant upside over depth 4 based on heuristics and sample size.

## Results

AlphaBeta vs Random

Depth 1:
After 100 matches between AlphaBeta at depth=1 and Random:
White wins: 13 (13.00%)
Draws: 87 (87.00%)
Draw reasons: {'insufficient_material': 57, 'fifty_move_rule': 29, 'threefold_repetition': 1}
Average move count: 61.38
Total time: 6.5s
Average time/game: 0.1s

Depth 2:
After 100 matches between AlphaBeta at depth=2 and Random:
White wins: 55 (55.00%)
Draws: 45 (45.00%)
Draw reasons: {'fifty_move_rule': 44, 'stalemate': 1}
Average move count: 76.62
Total time: 2m30.7s
Average time/game: 1.5s

Depth 3:
After 100 matches between AlphaBeta at depth=3 and Random:
White wins: 80 (80.00%)
Draws: 20 (20.00%)
Draw reasons: {'fifty_move_rule': 18, 'insufficient_material': 2}
Average move count: 63.26
Total time: 2m48.8s
Average time/game: 1.7s

Depth 4:
After 100 matches between AlphaBeta at depth=4 and Random:
White wins: 97 (97.00%)
Draws: 3 (3.00%)
Draw reasons: {'fifty_move_rule': 3}
Average move count: 49.08
Total time: 4m07.2s
Average time/game: 2.5s

Depth 5:
After 100 matches between AlphaBeta at depth=5 and Random:
White wins: 97 (97.00%)
Draws: 3 (3.00%)
Draw reasons: {'fifty_move_rule': 3}
Average move count: 46.52
Total time: 45m06.7s
Average time/game: 27.1s

AlphaBeta vs Greedy

Depth 1:
After 100 matches between AlphaBeta at depth=1 and Greedy Defender:
White wins: 2 (2.00%)
Draws: 98 (98.00%)
Draw reasons: {'insufficient_material': 82, 'fifty_move_rule': 15, 'threefold_repetition': 1}
Average move count: 49.75
Total time: 5.0s
Average time/game: 0.0s

Depth 2:
After 100 matches between AlphaBeta at depth=2 and Greedy Defender:
White wins: 7 (7.00%)
Draws: 93 (93.00%)
Draw reasons: {'fifty_move_rule': 91, 'insufficient_material': 2}
Average move count: 93.96
Total time: 28.0s
Average time/game: 0.3s

Depth 3:
After 100 matches between AlphaBeta at depth=3 and Greedy Defender:
White wins: 20 (20.00%)
Draws: 80 (80.00%)
Draw reasons: {'stalemate': 2, 'fifty_move_rule': 71, 'insufficient_material': 6, 'threefold_repetition': 1}
Average move count: 87.03
Total time: 4m07.9s
Average time/game: 2.5s

Depth 4:
After 100 matches between AlphaBeta at depth=4 and Greedy Defender:
White wins: 87 (87.00%)
Draws: 13 (13.00%)
Draw reasons: {'fifty_move_rule': 12, 'stalemate': 1}
Average move count: 67.48
Total time: 6m01.0s
Average time/game: 3.6s

Depth 5
After 100 matches between AlphaBeta at depth=5 and Greedy Defender:
White wins: 82 (82.00%)
Draws: 18 (18.00%)
Draw reasons: {'fifty_move_rule': 16, 'insufficient_material': 2}
Average move count: 70.86
Total time: 1h12m38.6s
Average time/game: 43.6s
