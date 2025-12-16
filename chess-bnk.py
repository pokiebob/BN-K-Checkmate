import chess
from game import Game, State

class ChessBNKState(State):
    def __init__(self, board: chess.Board):
        self.board = board

    def is_terminal(self):
        if self.board.is_checkmate() or self.board.is_stalemate():
            return True
        
        if self.board.can_claim_fifty_moves() or self.board.is_fifty_moves():
            return True
        
        if self.board.is_insufficient_material() or self.board.can_claim_threefold_repetition():
            return True
        
        return False

    def payoff(self):
        # simplification for now
        if self.board.is_checkmate():
            return 1.0 if self.board.turn == chess.BLACK else -1.0
        
        return 0.0

    def actor(self):
        return 0 if self.board.turn == chess.WHITE else 1

    def get_actions(self):
        return list(self.board.legal_moves)

    def successor(self, action):
        b2 = self.board.copy(stack=False)
        b2.push(action)
        return ChessBNKState(b2)

class ChessBNKGame(Game):
    def __init__(self):
        pass

    