import chess

SEARCH_DEPTH = 4

PIECE_SQUARE_TABLES = {
    chess.PAWN: (
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        78,
        83,
        86,
        73,
        102,
        82,
        85,
        90,
        7,
        29,
        21,
        44,
        40,
        31,
        44,
        7,
        -17,
        16,
        -2,
        15,
        14,
        0,
        15,
        -13,
        -26,
        3,
        10,
        9,
        6,
        1,
        0,
        -23,
        -22,
        9,
        5,
        -11,
        -10,
        -2,
        3,
        -19,
        -31,
        8,
        -7,
        -37,
        -36,
        -14,
        3,
        -31,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ),
    chess.KNIGHT: (
        -66,
        -53,
        -75,
        -75,
        -10,
        -55,
        -58,
        -70,
        -3,
        -6,
        100,
        -36,
        4,
        62,
        -4,
        -14,
        10,
        67,
        1,
        74,
        73,
        27,
        62,
        -2,
        24,
        24,
        45,
        37,
        33,
        41,
        25,
        17,
        -1,
        5,
        31,
        21,
        22,
        35,
        2,
        0,
        -18,
        10,
        13,
        22,
        18,
        15,
        11,
        -14,
        -23,
        -15,
        2,
        0,
        2,
        0,
        -23,
        -20,
        -74,
        -23,
        -26,
        -24,
        -19,
        -35,
        -22,
        -69,
    ),
    chess.BISHOP: (
        -59,
        -78,
        -82,
        -76,
        -23,
        -107,
        -37,
        -50,
        -11,
        20,
        35,
        -42,
        -39,
        31,
        2,
        -22,
        -9,
        39,
        -32,
        41,
        52,
        -10,
        28,
        -14,
        25,
        17,
        20,
        34,
        26,
        25,
        15,
        10,
        13,
        10,
        17,
        23,
        17,
        16,
        0,
        7,
        14,
        25,
        24,
        15,
        8,
        25,
        20,
        15,
        19,
        20,
        11,
        6,
        7,
        6,
        20,
        16,
        -7,
        2,
        -15,
        -12,
        -14,
        -15,
        -10,
        -10,
    ),
    chess.ROOK: (
        35,
        29,
        33,
        4,
        37,
        33,
        56,
        50,
        55,
        29,
        56,
        67,
        55,
        62,
        34,
        60,
        19,
        35,
        28,
        33,
        45,
        27,
        25,
        15,
        0,
        5,
        16,
        13,
        18,
        -4,
        -9,
        -6,
        -28,
        -35,
        -16,
        -21,
        -13,
        -29,
        -46,
        -30,
        -42,
        -28,
        -42,
        -25,
        -25,
        -35,
        -26,
        -46,
        -53,
        -38,
        -31,
        -26,
        -29,
        -43,
        -44,
        -53,
        -30,
        -24,
        -18,
        5,
        -2,
        -18,
        -31,
        -32,
    ),
    chess.QUEEN: (
        6,
        1,
        -8,
        -104,
        69,
        24,
        88,
        26,
        14,
        32,
        60,
        -10,
        20,
        76,
        57,
        24,
        -2,
        43,
        32,
        60,
        72,
        63,
        43,
        2,
        1,
        -16,
        22,
        17,
        25,
        20,
        -13,
        -6,
        -14,
        -15,
        -2,
        -5,
        -1,
        -10,
        -20,
        -22,
        -30,
        -6,
        -13,
        -11,
        -16,
        -11,
        -16,
        -27,
        -36,
        -18,
        0,
        -19,
        -15,
        -15,
        -21,
        -38,
        -39,
        -30,
        -31,
        -13,
        -31,
        -36,
        -34,
        -42,
    ),
    chess.KING: (
        4,
        54,
        47,
        -99,
        -99,
        60,
        83,
        -62,
        -32,
        10,
        55,
        56,
        56,
        55,
        10,
        3,
        -62,
        12,
        -57,
        44,
        -67,
        28,
        37,
        -31,
        -55,
        50,
        11,
        -4,
        -19,
        13,
        0,
        -49,
        -55,
        -43,
        -52,
        -28,
        -51,
        -47,
        -8,
        -50,
        -47,
        -42,
        -43,
        -79,
        -64,
        -32,
        -29,
        -32,
        -4,
        3,
        -14,
        -50,
        -57,
        -18,
        13,
        4,
        17,
        30,
        -3,
        -14,
        6,
        -1,
        40,
        18,
    ),
}


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
