import chess


class Player:
    def __init__(self, is_human=False):
        self.is_human = is_human


class OrderedAlphaBetaBot(Player):
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

    def get_material(self, board: chess.Board, color: bool) -> float:
        return sum(
            len(board.pieces(pt, color)) * val for pt, val in self.weights.items()
        )

    def evaluate(self, board: chess.Board, my_color: bool) -> float:
        material = self.get_material(board, my_color) - self.get_material(
            board, not my_color
        )

        # Add positional considerations
        mobility = len(list(board.legal_moves)) * 0.1  # bonus for mobility
        score = 0

        # for piece_type in range(1, 6):
        #    for color in [chess.WHITE, chess.BLACK]:
        #        table = PIECE_SQUARE_TABLES[(piece_type, color)]
        #        for square in board.pieces(piece_type, color):
        #            value = table[square]
        ##            if color == chess.WHITE:
        #                score += value
        #            else:
        #                score -= value

        # Penalize repeated moves (basic repetition detector)
        if board.can_claim_threefold_repetition():
            material -= 1

        return material + mobility + (score * 0.1)

    def ordered_legal_moves(self, board):
        moves = list(board.legal_moves)
        scored_moves = [(self.score_move(move, board), move) for move in moves]
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        return [move for _, move in scored_moves]

    def evaluate_move(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            # quiescne search
            # if board.is_check() or any(board.is_capture(m) for m in board.legal_moves):
            #    depth += 1
            return self.evaluate(board, maximizing_player)

        if board.turn == maximizing_player:
            max_eval = float("-inf")
            for move in board.legal_moves:
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
            for move in board.legal_moves:
                board.push(move)
                eval = self.evaluate_move(
                    board, depth - 1, alpha, beta, maximizing_player
                )
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def choose_move(self, board: chess.Board) -> chess.Move:
        best_move = None
        best_score = float("-inf")
        # alpha beta pruning
        alpha = float("-inf")
        beta = float("inf")
        my_color = board.turn

        for move in board.legal_moves:
            board.push(move)
            score = self.evaluate_move(board, SEARCH_DEPTH, alpha, beta, my_color)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
