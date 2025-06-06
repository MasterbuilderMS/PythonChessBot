import os
import pygame
import chess
from config import WIDTH, HEIGHT, SQUARE_SIZE
from players import HumanPlayer, RandomBot, BetterBot, AlphaBetaBot, OrderedAlphaBetaBot

BORDER_SIZE = 40  # Padding around the board

HIGHLIGHT_COLOR = (0, 255, 0, 100)  # Green for legal moves
CHECK_COLOR = (255, 0, 0, 100)  # Red for check
MOVE_COLOR = (30, 144, 255, 100)  # Dodger blue for last move


def piece_type_to_name(piece_type: int) -> str:
    mapping = {
        chess.PAWN: "pawn",
        chess.KNIGHT: "knight",
        chess.BISHOP: "bishop",
        chess.ROOK: "rook",
        chess.QUEEN: "queen",
        chess.KING: "king",
    }
    return mapping.get(piece_type, "unknown")


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece: chess.Piece, square: chess.Square):
        super().__init__()
        self.piece = piece
        self.square = square
        color = "white" if piece.color == chess.WHITE else "black"
        piece_type = piece.piece_type
        img_path = os.path.join(
            f"assets/images/imgs-80px/{color}_{piece_type_to_name(piece_type)}.png"
        )
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()

        file = chess.square_file(square)
        rank = chess.square_rank(square)
        self.rect.topleft = (file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE)


class Main:
    def __init__(self, white_player_cls, black_player_cls):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        self.board = chess.Board()
        self.clock = pygame.time.Clock()

        self.players = {
            chess.WHITE: white_player_cls(),
            chess.BLACK: black_player_cls(),
        }

        board_width = 8 * SQUARE_SIZE
        board_height = 8 * SQUARE_SIZE
        self.board_surface = pygame.Surface((board_width, board_height))
        self.board_rect = self.board_surface.get_rect(
            topleft=(BORDER_SIZE, BORDER_SIZE)
        )

        self.pieces = pygame.sprite.Group()
        self.update_pieces()

        self.selected_square = None
        self.highlight_squares = []
        self.last_move = None
        self.promotion_pending = False
        self.promotion_move = None

    def update_pieces(self):
        self.pieces.empty()
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                self.pieces.add(PieceSprite(piece, square))

    def draw_board(self):
        dark = pygame.Color("#845519")
        light = pygame.Color("#DEA361")
        for rank in range(8):
            for file in range(8):
                color = light if (rank + file) % 2 == 0 else dark
                rect = pygame.Rect(
                    file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                )
                pygame.draw.rect(self.board_surface, color, rect)

    def draw_highlights(self):
        overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        for square in self.highlight_squares:
            file = chess.square_file(square)
            rank = 7 - chess.square_rank(square)
            overlay.fill(HIGHLIGHT_COLOR)
            self.board_surface.blit(overlay, (file * SQUARE_SIZE, rank * SQUARE_SIZE))

        if self.board.is_check():
            king_square = self.board.king(self.board.turn)
            if king_square is not None:
                file = chess.square_file(king_square)
                rank = 7 - chess.square_rank(king_square)
                overlay.fill(CHECK_COLOR)
                self.board_surface.blit(
                    overlay, (file * SQUARE_SIZE, rank * SQUARE_SIZE)
                )

        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                file = chess.square_file(square)
                rank = 7 - chess.square_rank(square)
                overlay.fill(MOVE_COLOR)
                self.board_surface.blit(
                    overlay, (file * SQUARE_SIZE, rank * SQUARE_SIZE)
                )

    def get_square_under_mouse(self, pos):
        x, y = pos
        if not self.board_rect.collidepoint(pos):
            return None
        x -= self.board_rect.left
        y -= self.board_rect.top
        file = x // SQUARE_SIZE
        rank = 7 - (y // SQUARE_SIZE)
        return chess.square(file, rank)

    def handle_click(self, square):
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == self.board.turn:
                self.selected_square = square
                self.highlight_squares = [
                    move.to_square
                    for move in self.board.legal_moves
                    if move.from_square == square
                ]
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                if self.board.piece_at(
                    self.selected_square
                ).piece_type == chess.PAWN and (
                    chess.square_rank(square) == 0 or chess.square_rank(square) == 7
                ):
                    # Defer promotion
                    self.promotion_pending = True
                    self.promotion_move = move
                else:
                    self.board.push(move)
                    self.last_move = move
                    self.update_pieces()
                    self.draw_board()
                    self.draw_highlights()
                    self.pieces.draw(self.board_surface)
                    self.screen.blit(self.board_surface, self.board_rect.topleft)
                    pygame.display.flip()
                    pygame.time.delay(150)  # Optional: pause briefly to show the move
                self.selected_square = None
                self.highlight_squares = []
            else:
                self.selected_square = None
                self.highlight_squares = []

    def mainloop(self):
        running = True
        while running:
            current_player = self.players[self.board.turn]
            self.clock.tick(60)
            self.board_surface.fill((0, 0, 0))
            self.screen.fill((20, 20, 20))
            if (
                isinstance(current_player, HumanPlayer)
                and hasattr(current_player, "promotion_pending")
                and current_player.promotion_pending
            ):
                options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
                for i, piece_type in enumerate(options):
                    rect = pygame.Rect(500, 100 + i * 80, 80, 80)
                    pygame.draw.rect(self.screen, (200, 200, 200), rect)
                    img = pygame.image.load(
                        f"assets/images/imgs-80px/white_{piece_type}.png"
                    )  # Or black_ based on turn
                    self.screen.blit(img, rect.topleft)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.players[self.board.turn].is_human:
                        square = self.get_square_under_mouse(event.pos)
                        if square is not None:
                            self.handle_click(square)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        self.board.pop()
                        self.draw_board()
                        self.draw_highlights()
                        self.pieces.draw(self.board_surface)
                        self.screen.blit(self.board_surface, self.board_rect.topleft)

            if not self.players[self.board.turn].is_human:
                move = self.players[self.board.turn].choose_move(self.board)
                if move and move in self.board.legal_moves:
                    self.board.push(move)
                    self.last_move = move
                    self.update_pieces()

            # Drawing
            self.draw_board()
            self.draw_highlights()
            self.pieces.draw(self.board_surface)
            self.screen.blit(self.board_surface, self.board_rect.topleft)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Main(HumanPlayer, OrderedAlphaBetaBot).mainloop()
