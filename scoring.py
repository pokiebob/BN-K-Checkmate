import itertools as it
import random
import chess

def distance_to_target_corner(board, b_king, w_bishop):
    bishop_color = board.color_at(w_bishop)

    target_corners = [chess.A8, chess.H8] if bishop_color == chess.BLACK else [chess.A1, chess.H1]

    min_distance = min(chess.square_distance(b_king, corner) for corner in target_corners)

    return min_distance

def king_mobility(board, b_king):
    b_king = board.king(chess.BLACK)
    mobility = 0

    for move in board.legal_moves:
        if move.from_square == b_king:
            mobility += 1
    
    return mobility

def average_piece_distance(w_king, w_bishop, w_knight):

    # find manhattan distance between all three white pieces
    def manhattan_distance(sq1, sq2):
        x1, y1 = chess.square_file(sq1), chess.square_rank(sq1)
        x2, y2 = chess.square_file(sq2), chess.square_rank(sq2)
        return abs(x1 - x2) + abs(y1 - y2)
    
    dists = [manhattan_distance(sq1, sq2) for sq1, sq2 in it.combinations([w_king, w_bishop, w_knight], 2)]
    return sum(dists) / len(dists)

def evaluate(pos):
    if pos.is_terminal():
        return pos.payoff() * 1000
    
    board = pos.board
    b_king = board.king(chess.BLACK)
    w_king = board.king(chess.WHITE)
    w_bishop = board.pieces(chess.BISHOP, chess.WHITE).pop()
    w_knight = board.pieces(chess.KNIGHT, chess.WHITE).pop()
    
    # HEURISTICS

    # max manhattan distance is 14 (A1 to H8 or A8 to H1)
    distance_score = 1 - (distance_to_target_corner(board, b_king, w_bishop) / 14)

    # max king mobility is 8
    restrictiveness_score = 1 - (king_mobility(board, b_king) / 8)

    # max average manhattan distance between pieces is also 14
    coordination_score = 1 - (average_piece_distance(w_king, w_bishop, w_knight) / 14)

    score = (
        distance_score * 0.4 + 
        restrictiveness_score * 0.3 + 
        coordination_score * 0.3
        )
    return score