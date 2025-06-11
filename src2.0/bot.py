import chess
from functools import cache

SEARCH_DEPTH = 2


class Player:
    def __init__(self, is_human=False):
        self.is_human = is_human


class ChessBot(Player):
    """Bot implementing alpha beta pruning, and ordering of branches"""

    def __init__(self):
        super().__init__(is_human=False)
        self.weights = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.5,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0,  # Don't include king in material count
        }
        self.transposition_table = {}

    def mvv_lva(self, move: chess.Move, board: chess.Board):
        """priorite most valuable victim least valuable attacked (e.g. pawns attacking queens is generally a good move)"""
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            if victim and attacker:
                return (
                    10 * self.weights[victim.piece_type]
                    - self.weights[attacker.piece_type]
                )
        return 0

    def score_move(self, move, board):
        score = self.mvv_lva(move, board)

        if board.gives_check(move):
            # good move
            score += 5
        if move.promotion:
            score += self.weights[move.promotion] * 10  # prioritize queen promotions
        return score

    def get_material(self, board, my_color):
        return sum(
            self.weights[piece.piece_type]
            for square, piece in board.piece_map().items()
            if piece.color == my_color
        )

    def evaluate(self, board: chess.Board, my_color: bool) -> float:
        my_material = self.get_material(board, my_color)
        opponent_material = self.get_material(board, not my_color)
        material_balance = my_material - opponent_material

        mobility = board.legal_moves.count() * 0.1 if board.turn == my_color else 0

        return material_balance + mobility

    def ordered_legal_moves(self, board):
        moves = board.legal_moves
        scored_moves = [(self.score_move(move, board), move) for move in moves]
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        return [move for _, move in scored_moves]

    def evaluate_move(
        self, board: chess.Board, depth, alpha, beta, color_sign: int, my_color: bool
    ):
        board_key = board.fen()
        tt_key = (board_key, depth)

        # check in transposition table
        if tt_key in self.transposition_table:
            return self.transposition_table[tt_key]

        if depth == 0 or board.is_game_over():
            score = color_sign * self.evaluate(board, board.turn)
            self.transposition_table[tt_key] = score
            return score

        max_score = float("-inf")

        for move in self.ordered_legal_moves(board):
            board.push(move)
            score = -self.evaluate_move(
                board, depth - 1, -beta, -alpha, -color_sign, my_color
            )
            board.pop()
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        self.transposition_table[tt_key] = max_score
        return max_score
        """
        if board.turn == maximizing_player:
            max_eval = float("-inf")
            for move in self.ordered_legal_moves(board):
                board.push(move)
                eval = self.evaluate_move(
                    board, depth - 1, alpha, beta, maximizing_player
                )
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in self.ordered_legal_moves(board):
                board.push(move)
                eval = self.evaluate_move(
                    board, depth - 1, alpha, beta, maximizing_player
                )
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval"""

    def choose_move(self, board: chess.Board) -> chess.Move | None:
        best_move = None
        best_score = float("-inf")
        # alpha beta pruning
        alpha = float("-inf")
        beta = float("inf")
        my_color = board.turn
        color_sign = 1 if my_color == chess.WHITE else -1
        self.transposition_table.clear()

        for move in board.legal_moves:
            board.push(move)
            score = -self.evaluate_move(
                board, SEARCH_DEPTH, -beta, -alpha, -color_sign, my_color
            )
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
