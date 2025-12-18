import chess
from game import Game, State
import random

class ChessBNKState(State):
    def __init__(self, board: chess.Board, history=None):
        self.board = board
        if history is None:
            self.history = {}
            k = board._transposition_key()
            self.history[k] = 1
        else:
            self.history = history

    def is_terminal(self):
        if self.board.is_checkmate() or self.board.is_stalemate():
            return True
        
        if self.board.can_claim_fifty_moves() or self.board.is_fifty_moves():
            return True
        
        if self.board.is_insufficient_material() or self.board.can_claim_threefold_repetition():
            return True
        
        return False

    def payoff(self):
        if self.board.is_checkmate():
            return 1.0 if self.board.turn == chess.BLACK else -1.0
        
        return 0.0

    def actor(self):
        return 0 if self.board.turn == chess.WHITE else 1

    def get_actions(self):
        return list(self.board.legal_moves)

    def successor(self, action):
        b2 = self.board.copy(stack=True)
        b2.push(action)

        k2 = b2._transposition_key()
        history2 = self.history.copy()
        history2[k2] = history2.get(k2, 0) + 1
        return ChessBNKState(b2, history2)

class ChessBNKGame(Game):
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def _random_bnk_position(self):
        for _ in range(1000):
            board = chess.Board()
            board.clear_board()
            wk, bk, wb, wn = self.rng.sample(list(chess.SQUARES), 4)

            # check if kings are adjacent
            if chess.square_distance(wk, bk) <= 1:
                continue

            # place pieces
            board.set_piece_at(wk, chess.Piece(chess.KING, chess.WHITE))
            board.set_piece_at(bk, chess.Piece(chess.KING, chess.BLACK))
            board.set_piece_at(wb, chess.Piece(chess.BISHOP, chess.WHITE))
            board.set_piece_at(wn, chess.Piece(chess.KNIGHT, chess.WHITE))
            board.turn = chess.WHITE
            board.castling_rights = 0
            board.ep_square = None
            board.halfmove_clock = 0
            board.fullmove_number = 1

            if board.is_checkmate() or board.is_stalemate():
                continue
            if not board.is_valid():
                continue
            
            return board

        raise RuntimeError("Failed to generate a valid position.")

    def initial_state(self):
        board = self._random_bnk_position()
        return ChessBNKState(board)

    