import chess
from scoring import distance_to_target_corner

def can_make_capture(board):
    for mv in board.legal_moves:
        if board.is_capture(mv):
            return True 
    return False

def defender_eval(pos):
    if pos.is_terminal():
        p = pos.payoff()
        if p == 0.0:
            return 1000.0
        return -1000.0
    
    b = pos.board
    key = b._transposition_key()
    count = pos.history.get(key, 0)

    if count == 3:
        return 1000.0
    
    if can_make_capture(b):
        return 1000.0
    
    b_king = b.king(chess.BLACK)
    bishops = list(b.pieces(chess.BISHOP, chess.WHITE))
    w_bishop = bishops[0]
    dist = distance_to_target_corner(b_king, w_bishop)
    return dist
    