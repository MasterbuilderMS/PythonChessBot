import chess

SEARCH_DEPTH = 4


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

    def score_move(self, move, board: chess.Board):
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

        # king distance bonus
        king_square = board.king(not my_color)
        king_file = chess.square_file(king_square)
        king_rank = chess.square_rank(king_square)
        king_dist = (
            min(king_file, 8 - king_file) + min(king_rank, 8 - king_rank)
        ) * 0.1

        return material_balance + mobility + king_dist

    def ordered_legal_moves(self, board):
        moves = board.legal_moves
        scored_moves = [(self.score_move(move, board), move) for move in moves]
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        return [move for _, move in scored_moves]

    def quiescence(self, board, alpha, beta, my_color):
        stand_pat = self.evaluate(board, my_color)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in self.ordered_legal_moves(board):
            if board.is_capture(move) or board.gives_check(move) or move.promotion:
                board.push(move)
                score = -self.quiescence(board, -beta, -alpha, not my_color)
                board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def evaluate_move(
        self, board: chess.Board, depth, alpha, beta, maximizing_player, my_color
    ):
        board_key = board.board_fen()
        tt_key = (
            board_key,
            depth,
            maximizing_player,
            board.castling_rights,
            board.ep_square,
        )

        if tt_key in self.transposition_table:
            return self.transposition_table[tt_key]

        if depth == 0 or board.is_game_over():
            return self.quiescence(board, alpha, beta, my_color)

        if maximizing_player:
            max_eval = float("-inf")
            for move in self.ordered_legal_moves(board):
                board.push(move)
                eval = self.evaluate_move(
                    board, depth - 1, alpha, beta, False, my_color
                )
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[tt_key] = max_eval
            return max_eval
        else:
            min_eval = float("inf")
            for move in self.ordered_legal_moves(board):
                board.push(move)
                eval = self.evaluate_move(board, depth - 1, alpha, beta, True, my_color)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[tt_key] = min_eval
            return min_eval

    def choose_move(self, board: chess.Board) -> chess.Move | None:
        my_color = board.turn
        best_score = float("-inf")
        best_move = None
        alpha, beta = float("-inf"), float("inf")

        for move in board.legal_moves:
            board.push(move)
            score = self.evaluate_move(
                board, SEARCH_DEPTH - 1, alpha, beta, False, my_color
            )
            score -= board.can_claim_threefold_repetition() * 4
            score += board.is_checkmate() * 10000000
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        return best_move
