import itertools as it
import random
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

def evaluate(pos):
    if pos.is_terminal():
        return pos.payoff() * 1000
    
    board = pos.board

    if board.is_repetition(3):
        return -5.0
    
    b_king = board.king(chess.BLACK)
    w_king = board.king(chess.WHITE)
    w_bishop = next(iter(board.pieces(chess.BISHOP, chess.WHITE)))
    w_knight = next(iter(board.pieces(chess.KNIGHT, chess.WHITE)))

    
    # HEURISTICS

    # max square distance is 7 (A1 to H8 or A8 to H1)
    cornering_score = 1 - (distance_to_target_corner(b_king, w_bishop) / 7)

    # max manhattan distance between kings is also 14
    kings_distance_score = 1 - (manhattan_distance(w_king, b_king) / 14)

    # max king mobility is 8
    restrictiveness_score = 1 - (king_mobility(board, b_king) / 8)

    # max average manhattan distance between pieces is also 14
    coordination_score = 1 - (average_piece_distance(w_king, w_bishop, w_knight) / 14)

    urgency_penalty = board.halfmove_clock / 100.0
    repetition_penalty = 1.0 if board.is_repetition(2) else 0.0

    score = (
        0.3 * cornering_score + 
        0.25 * restrictiveness_score + 
        0.15 * coordination_score + 
        0.2 * kings_distance_score -
        0.15 * urgency_penalty -
        0.5 * repetition_penalty
        )
    return score