from chess_bnk import ChessBNKGame

def play_game(
    p0,
    p1,
    seed=0, 
    max_moves=100, 
    vizualize=True,
    progress=None
):
    game = ChessBNKGame(seed=seed)
    position = game.initial_state()
    
    if vizualize:
        print("Initial Position:")
        print(position.board)
        print()

    move_count = 0
    while not position.is_terminal() and move_count <= max_moves:
        actor = position.actor()
        color = "White" if actor == 0 else "Black"
        if actor == 0:
            move = p0(position)
        else:
            move = p1(position)
        if move is None:
            raise RuntimeError(f"Policy returned None move")
        position = position.successor(move)
        b = position.board
        move_count += 1

        if vizualize:
            print(f"Move {move_count}: {color} played {move}")
            if progress:
                print(f"Wins: {progress[0]}/{progress[2]}, Draws: {progress[1]}/{progress[2]}")
            print(b)
            print()
        
    reason = None
    if position.is_terminal():
        if position.payoff() == 1.0:
            reason = "checkmate"
            print("White wins in {} moves!".format(move_count))
        else:
            if b.is_stalemate():
                reason = "stalemate"
                print("Draw by stalemate in {} moves.".format(move_count))
            elif b.is_insufficient_material():
                reason = "insufficient_material"
                print("Draw by insufficient material in {} moves.".format(move_count))
            elif b.can_claim_fifty_moves() or b.is_fifty_moves():
                reason = "fifty_move_rule"
                print("Draw by fifty-move rule in {} moves.".format(move_count))
            elif b.can_claim_threefold_repetition():
                reason = "threefold_repetition"
                print("Draw by threefold repetition in {} moves.".format(move_count))
    elif move_count >= max_moves: 
        reason = "move_limit"
        print("Draw by maximum move limit of {}.".format(max_moves))
    else:
        reason = "unknown"
        raise ValueError("Game ended for unknown reason.")

    return position.payoff(), reason, move_count
