import chess
import random

def random_policy():
    def policy(pos):
        actions = pos.get_actions()
        return random.choice(actions)
    return policy

def greedy_policy(defender_eval):
    def policy(pos):
        best_value = float('-inf')
        best_move = None
        moves = pos.get_actions()
        for move in moves:
            child = pos.successor(move)
            value = defender_eval(child)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    return policy
