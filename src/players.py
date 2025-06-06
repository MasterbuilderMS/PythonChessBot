import chess
import pygame
import random
import copy
from config import SEARCH_DEPTH
import time
from zobrist import init_zobrist, zobrist_hash, TTEntry

PAWN_PST = [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    4.0,
    4.0,
    4.0,
    4.0,
    4.0,
    4.0,
    4.0,
    4.0,
    1.0,
    1.0,
    2.0,
    2.0,
    2.0,
    2.0,
    1.0,
    1.0,
    0.5,
    0.5,
    1.0,
    1.5,
    1.5,
    1.0,
    0.5,
    0.5,
    0.0,
    0.0,
    0.0,
    2.0,
    2.0,
    0.0,
    0.0,
    0.0,
    0.5,
    -0.5,
    -1.0,
    0.0,
    0.0,
    -1.0,
    -0.5,
    0.5,
    0.5,
    1.0,
    1.0,
    -2.0,
    -2.0,
    1.0,
    1.0,
    0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
]
KNIGHT_PST = [
    -5.0,
    -4.0,
    -3.0,
    -3.0,
    -3.0,
    -3.0,
    -4.0,
    -5.0,
    -4.0,
    -2.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.0,
    -4.0,
    -3.0,
    0.0,
    1.0,
    1.5,
    1.5,
    1.0,
    0.0,
    -3.0,
    -3.0,
    0.5,
    1.5,
    2.0,
    2.0,
    1.5,
    0.5,
    -3.0,
    -3.0,
    0.0,
    1.5,
    2.0,
    2.0,
    1.5,
    0.0,
    -3.0,
    -3.0,
    0.5,
    1.0,
    1.5,
    1.5,
    1.0,
    0.5,
    -3.0,
    -4.0,
    -2.0,
    0.0,
    0.5,
    0.5,
    0.0,
    -2.0,
    -4.0,
    -5.0,
    -4.0,
    -3.0,
    -3.0,
    -3.0,
    -3.0,
    -4.0,
    -5.0,
]
BISHOP_PST = [
    -2.0,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -2.0,
    -1.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -1.0,
    -1.0,
    0.0,
    0.5,
    1.0,
    1.0,
    0.5,
    0.0,
    -1.0,
    -1.0,
    0.5,
    0.5,
    1.0,
    1.0,
    0.5,
    0.5,
    -1.0,
    -1.0,
    0.0,
    1.0,
    1.0,
    1.0,
    1.0,
    0.0,
    -1.0,
    -1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    -1.0,
    -1.0,
    0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.5,
    -1.0,
    -2.0,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -1.0,
    -2.0,
]
ROOK_PST = [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.5,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    0.5,
    -0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -0.5,
    -0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -0.5,
    -0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -0.5,
    -0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -0.5,
    -0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -0.5,
    0.0,
    0.0,
    0.0,
    0.5,
    0.5,
    0.0,
    0.0,
    0.0,
]
QUEEN_PST = [
    -2.0,
    -1.0,
    -1.0,
    -0.5,
    -0.5,
    -1.0,
    -1.0,
    -2.0,
    -1.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -1.0,
    -1.0,
    0.0,
    0.5,
    0.5,
    0.5,
    0.5,
    0.0,
    -1.0,
    -0.5,
    0.0,
    0.5,
    0.5,
    0.5,
    0.5,
    0.0,
    -0.5,
    0.0,
    0.0,
    0.5,
    0.5,
    0.5,
    0.5,
    0.0,
    -0.5,
    -1.0,
    0.5,
    0.5,
    0.5,
    0.5,
    0.5,
    0.0,
    -1.0,
    -1.0,
    0.0,
    0.5,
    0.0,
    0.0,
    0.0,
    0.0,
    -1.0,
    -2.0,
    -1.0,
    -1.0,
    -0.5,
    -0.5,
    -1.0,
    -1.0,
    -2.0,
]


def mirror_table(pst):
    return pst[::-1]


PIECE_SQUARE_TABLES = {
    (chess.PAWN, chess.WHITE): PAWN_PST,
    (chess.PAWN, chess.BLACK): mirror_table(PAWN_PST),
    (chess.KNIGHT, chess.WHITE): KNIGHT_PST,
    (chess.KNIGHT, chess.BLACK): mirror_table(KNIGHT_PST),
    (chess.BISHOP, chess.WHITE): BISHOP_PST,
    (chess.BISHOP, chess.BLACK): mirror_table(BISHOP_PST),
    (chess.ROOK, chess.WHITE): ROOK_PST,
    (chess.ROOK, chess.BLACK): mirror_table(ROOK_PST),
    (chess.QUEEN, chess.WHITE): QUEEN_PST,
    (chess.QUEEN, chess.BLACK): mirror_table(QUEEN_PST),
}


class Player:
    def __init__(self, is_human=False):
        self.is_human = is_human


class HumanPlayer(Player):
    def __init__(self):
        super().__init__(is_human=True)
        self.selected_square = None
        self.selected_move = None

    def handle_events(self, event, board, game_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            file = (x - 40) // 80  # adjust for BORDER_SIZE and SQUARE_SIZE
            rank = 7 - ((y - 40) // 80)
            if not (0 <= file <= 7 and 0 <= rank <= 7):
                return
            square = chess.square(file, rank)

            if self.selected_square is None:
                if board.piece_at(square) and board.color_at(square) == board.turn:
                    self.selected_square = square
            else:
                move = chess.Move(self.selected_square, square)

                # Check for promotion
                if board.piece_at(self.selected_square).piece_type == chess.PAWN and (
                    chess.square_rank(square) == 0 or chess.square_rank(square) == 7
                ):
                    # Show promotion selection overlay
                    self.promotion_pending = (self.selected_square, square)
                    return  # Wait for GUI to call self.promote()

                # Normal move
                if move in board.legal_moves:
                    game_manager.make_move(move)

                self.selected_square = None

    def promote(self, board, game_manager, piece_type):
        from_sq, to_sq = self.promotion_pending
        move = chess.Move(from_sq, to_sq, promotion=piece_type)

        if move in board.legal_moves:
            game_manager.make_move(move)

        self.promotion_pending = None
        self.selected_square = None

    def choose_move(self, board: chess.Board):
        return self.selected_move  # For now, not used with handle_events

    def clear_move(self):
        self.selected_move = None
        self.selected_square = None


class RandomBot(Player):
    def __init__(self):
        super().__init__(is_human=False)

    def choose_move(self, board: chess.Board):
        time.sleep(0.5)
        return random.choice(list(board.legal_moves))


class BetterBot(Player):
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

    def get_material(self, board: chess.Board, color: bool) -> float:
        return sum(
            len(board.pieces(pt, color)) * val for pt, val in self.weights.items()
        )

    def evaluate(self, board: chess.Board, my_color: bool) -> float:
        """Simple evaluation: material difference"""
        return self.get_material(board, my_color) - self.get_material(
            board, not my_color
        )

    def minimax(
        self, board: chess.Board, depth: int, is_maximizing: bool, my_color: bool
    ) -> float:
        # set
        if depth == 0 or board.is_game_over():
            return self.evaluate(board, my_color)

        if is_maximizing:
            max_eval = float("-inf")
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, False, my_color)
                board.pop()
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, True, my_color)
                board.pop()
                min_eval = min(min_eval, eval)
            return min_eval

    def choose_move(self, board: chess.Board) -> chess.Move:
        best_move = None
        best_score = float("-inf")
        my_color = board.turn

        for move in board.legal_moves:
            board.push(move)
            score = self.minimax(
                board, depth=SEARCH_DEPTH, is_maximizing=False, my_color=my_color
            )
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move


class AlphaBetaBot(Player):
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

    def get_material(self, board: chess.Board, color: bool) -> float:
        return sum(
            len(board.pieces(pt, color)) * val for pt, val in self.weights.items()
        )

    def evaluate(self, board: chess.Board, my_color: bool) -> float:
        """Simple evaluation: material difference"""
        return self.get_material(board, my_color) - self.get_material(
            board, not my_color
        )

    def minimax(
        self,
        board: chess.Board,
        depth: int,
        alpha,
        beta,
        is_maximizing: bool,
        my_color: bool,
    ) -> float:
        # set fixed depth
        if depth == 0 or board.is_game_over():
            return self.evaluate(board, my_color)

        if is_maximizing:
            eval = float("-inf")
            for move in board.legal_moves:
                board.push(move)
                eval = max(
                    eval, self.minimax(board, depth - 1, alpha, beta, False, my_color)
                )
                board.pop()
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return eval
        else:
            eval = float("inf")
            for move in board.legal_moves:
                board.push(move)
                eval = max(
                    eval, self.minimax(board, depth - 1, alpha, beta, True, my_color)
                )
                board.pop()
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return eval

    def choose_move(self, board: chess.Board) -> chess.Move:
        best_move = None
        best_score = float("-inf")
        # alpha beta pruning
        alpha = float("-inf")
        beta = float("inf")
        my_color = board.turn

        for move in board.legal_moves:
            board.push(move)
            score = self.minimax(
                board,
                depth=SEARCH_DEPTH,
                alpha=alpha,
                beta=beta,
                is_maximizing=False,
                my_color=my_color,
            )
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move

        return best_move


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
