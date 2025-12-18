import itertools as it
import chess

def square_color(sq):
    file = chess.square_file(sq)
    rank = chess.square_rank(sq)
    return (file + rank) % 2

def manhattan_distance(sq1, sq2):
    x1, y1 = chess.square_file(sq1), chess.square_rank(sq1)
    x2, y2 = chess.square_file(sq2), chess.square_rank(sq2)
    return abs(x1 - x2) + abs(y1 - y2)


def distance_to_target_corner(b_king, w_bishop):
    bishop_sq_color = square_color(w_bishop)
    target_corners = [chess.A1, chess.H8] if bishop_sq_color == 0 else [chess.A8, chess.H1]
    return min(chess.square_distance(b_king, corner) for corner in target_corners)

def edge_distance(b_king):
    file = chess.square_file(b_king)
    rank = chess.square_rank(b_king)
    return min(file, 7 - file, rank, 7 - rank)

def king_mobility(board, b_king):
    mobility = 0

    for move in board.legal_moves:
        if move.from_square == b_king:
            mobility += 1
    
    return mobility

def average_piece_distance(w_king, w_bishop, w_knight):

    # find manhattan distance between all three white pieces
    dists = [manhattan_distance(sq1, sq2) for sq1, sq2 in it.combinations([w_king, w_bishop, w_knight], 2)]
    return sum(dists) / len(dists)

# def draw_risk(board):
#     for mv in board.legal_moves:
#         if board.is_capture(mv):
#             return True 
#         b2 = board.copy(stack=True)
#         b2.push(mv)
#         if b2.can_claim_draw():
#             return True
        
#     return False


def evaluate(pos):
    board = pos.board

    if pos.is_terminal():
        p = pos.payoff()
        if p == 0.0:
            return -1000.0
        return p * 1000.0

    # if board.can_claim_threefold_repetition():
    #     return -1000.0
    # if board.can_claim_fifty_moves() or board.is_fifty_moves():
    #     return -1000.0
    # if draw_risk(board):
    #     return -1000.0

    key = board._transposition_key()
    count = pos.history.get(key, 0)

    if count == 3:
        return -1000.0
    if count == 2:
        return -250.0
    
    
    b_king = board.king(chess.BLACK)
    w_king = board.king(chess.WHITE)
    bishops = list(board.pieces(chess.BISHOP, chess.WHITE))
    knights = list(board.pieces(chess.KNIGHT, chess.WHITE))   
    w_bishop = bishops[0]
    w_knight = knights[0]
    
    # HEURISTICS

    # max square distance is 7 (A1 to H8 or A8 to H1)
    cornering_score = 1 - (distance_to_target_corner(b_king, w_bishop) / 7)

    # max edge distance is 3 (D4 to A4 or D4 to D1)
    ed = edge_distance(b_king)
    edge_score = 1 - (ed / 3)  

    # max square distance between kings is also 7
    kings_distance_score = 1 - (chess.square_distance(w_king, b_king) / 7)

    # max king mobility is 8
    restrictiveness_score = 1 - (king_mobility(board, b_king) / 8)

    # max average manhattan distance between pieces is 14
    coordination_score = 1 - (average_piece_distance(w_king, w_bishop, w_knight) / 14)

    urgency_penalty = board.halfmove_clock / 100.0
    # repetition_penalty = 1.0 if board.is_repetition(2) else 0.0

    corner_weight = 0.35 if ed <= 1 else 0.25
    edge_weight = 0.10 if ed <= 1 else 0.15

    score = (
        corner_weight * cornering_score + 
        edge_weight * edge_score +
        0.25 * restrictiveness_score + 
        0.10 * coordination_score + 
        0.25 * kings_distance_score -
        .15 * urgency_penalty
        )
    return score