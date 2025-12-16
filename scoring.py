import itertools as it
import random
import chess

def distance_to_target_corner(board):
    pass

def king_mobility(board):
    pass

def piece_coordination(board):
    pass

def evaluate(pos):
    board = pos.board
    
    # HEURISTICS
    distance_score = (distance_to_target_corner(board))
    restrictiveness_score = (king_mobility(board))
    coordination_score = piece_coordination(board)

    score = (distance_score * 0.4 + restrictiveness_score * 0.3 + coordination_score * 0.3)
    return score