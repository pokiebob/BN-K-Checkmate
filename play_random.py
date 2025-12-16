import chess
from chess_bnk import ChessBNKGame, ChessBNKState
from agents import random_policy

def play_random_game(seed=0, max_moves=100, vizualize=True):
    game = ChessBNKGame(seed=seed)
    position = game.initial_state()
    p0 = random_policy()
    p1 = random_policy()
    
    if vizualize:
        print("Initial Position:")
        print(position.board)
        print()

    move_count = 0
    while not position.is_terminal() and move_count < max_moves:
        actor = position.actor()
        color = "White" if actor == 0 else "Black"
        b = position.board
        if actor == 0:
            move = p0(position)
        else:
            move = p1(position)
        position = position.successor(move)
        move_count += 1

        if vizualize:
            print(f"Move count: {move_count} | {color} played {move}")
            print(b)
            print()
        
    if position.is_terminal():
        if position.payoff() == 1.0:
            print("White wins in {} moves!".format(move_count))
        elif position.payoff() == -1.0:
            print("Black wins in {} moves!".format(move_count))
        else:
            if b.is_stalemate():
                print("Draw by stalemate in {} moves.".format(move_count))
            elif b.is_insufficient_material():
                print("Draw by insufficient material in {} moves.".format(move_count))
            elif b.can_claim_fifty_moves() or b.is_fifty_moves():
                print("Draw by fifty-move rule in {} moves.".format(move_count))
            elif b.can_claim_threefold_repetition():
                print("Draw by threefold repetition in {} moves.".format(move_count))
            else:
                print("Draw by maximum move limit of {}.".format(max_moves))

    return position.payoff()

if __name__ == "__main__":
    play_random_game(seed=42, max_moves=100, vizualize=True)