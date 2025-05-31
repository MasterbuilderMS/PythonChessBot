"""contains the pygame implementation of the chess game"""

import os
import pygame
from board import Board, Piece, Move, Square


WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = 80


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece: Piece):
        super().__init__()
        self.piece = piece
        image_path = os.path.join(
            f"assets/images/imgs-80px/{self.piece.color}_{self.piece.piece}.png"
        )
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.update_position()

    def update_position(self):
        self.rect.topleft = (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE)

    @property
    def row(self):
        return self.piece.row

    @property
    def col(self):
        return self.piece.column


class BoardRenderer:
    def __init__(self, surface, sqsize, origin=(0, 0)):
        self.surface = surface
        self.sqsize = sqsize
        #  NOTE - replace with theme class later
        self.dark_color = "#845519"
        self.light_color = "#DEA361"
        self.font = pygame.font.SysFont(None, 24)
        self.origin = origin  # (x-y offset)

    def draw_board(self):
        for rank in range(8):
            for file in range(8):
                color = self.light_color if (rank + file) % 2 == 0 else self.dark_color
                x = file * self.sqsize
                y = rank * self.sqsize
                rect = pygame.Rect(x, y, self.sqsize, self.sqsize)

                pygame.draw.rect(self.surface, color, rect)

    def draw_coordinates(self):
        for rank in range(8):
            text = self.font.render(str(8 - rank), True, (0, 0, 0))
            self.surface.blit(text, (2, rank * self.sqsize + 2))

        for file in range(8):
            text = self.font.render(chr(ord("a") + file), True, (0, 0, 0))
            self.surface.blit(text, (file * self.sqsize + 2, self.sqsize * 7 + 60))


class Dragger:
    def __init__(self):
        self.dragging = False
        self.piece: None | Piece = None
        self.sprite: None | PieceSprite = None
        self.mouse_pos = (0, 0)

    def drag(self, piece: Piece, sprite: PieceSprite):
        self.dragging = True
        self.piece = piece
        self.sprite = sprite

    def undrag(self):
        self.dragging = False
        self.piece = None
        self.sprite = None


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        board_px = SQUARE_SIZE * 8
        self.x_offset = (WIDTH - board_px) // 2
        self.y_offset = (HEIGHT - board_px) // 2
        self.board = Board()
        self.board_surface = self.screen.subsurface(
            pygame.Rect(self.x_offset, self.y_offset, board_px, board_px)
        )
        self.board_renderer = BoardRenderer(self.board_surface, SQUARE_SIZE, origin=(self.x_offset, self.y_offset))  # fmt: off
        # subsurface, so things can more easily be placed on the board

        self.clock = pygame.time.Clock()
        self.pieces: pygame.sprite.Group = (
            pygame.sprite.Group()
        )  # all sprites on the board
        self.update_pieces()
        self.dragger = Dragger()  # dragging pieces

    # board display methods
    def update_pieces(self):
        self.pieces.empty()
        for i in self.board.pieces:
            self.pieces.add(PieceSprite(i))

    def show_moves(self, row, col):
        piece = self.board[row, col].piece
        if piece is not None:
            surface = self.board_surface
            for move in self.board.get_piece_moves(row, col):
                row, col = move.final.row, move.final.column
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill((0, 255, 0, 100))  # TODO replace later with theme
                surface.blit(highlight, (x, y))

    def mainloop(self):
        running = True
        while running:
            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # dragging

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.dragger.dragging:
                        mx, my = pygame.mouse.get_pos()
                        local_x = mx - self.x_offset
                        local_y = my - self.y_offset
                        for sprite in self.pieces:
                            if sprite.rect.collidepoint((local_x, local_y)):
                                # print(sprite.piece.moves)
                                self.dragger.drag(sprite.piece, sprite)
                                self.show_moves(sprite.piece.row, sprite.piece.column)
                                break
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        file = (mouse_x - self.x_offset) // SQUARE_SIZE
                        rank = (mouse_y - self.y_offset) // SQUARE_SIZE

                        # Clamp to board boundaries
                        file = max(0, min(7, file))
                        rank = max(0, min(7, rank))

                        # Update piece position
                        initial = Square(
                            self.dragger.piece.row, self.dragger.piece.column
                        )
                        final = Square(rank, file)
                        # valid move:
                        move = Move(initial, final, self.dragger.piece)
                        if move in self.board.get_piece_moves(self.dragger.piece.row, self.dragger.piece.column):  # fmt: off
                            self.board.move_piece(Move(initial, final))
                            self.update_pieces()
                        self.dragger.sprite.update_position()
                        self.dragger.undrag()

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragger.dragging and self.dragger.sprite:
                        mx, my = pygame.mouse.get_pos()
                        local_x = mx - self.x_offset
                        local_y = my - self.y_offset
                        self.dragger.sprite.rect.center = (local_x, local_y)

                # display events
                if event.type == pygame.VIDEORESIZE:
                    # TODO fix screen resizing
                    MIN_WIDTH = SQUARE_SIZE * 8 + 6
                    MIN_HEIGHT = SQUARE_SIZE * 8 + 6

                    new_width = max(event.w, MIN_WIDTH)
                    new_height = max(event.h, MIN_HEIGHT)
                    self.screen = pygame.display.set_mode(
                        (new_width, new_height), pygame.RESIZABLE
                    )

                    board_px = SQUARE_SIZE * 8
                    self.x_offset = (event.w - board_px) // 2
                    self.y_offset = (event.h - board_px) // 2

                    self.board_surface = self.screen.subsurface(
                        pygame.Rect(self.x_offset, self.y_offset, board_px, board_px)
                    )
                    self.board_renderer.surface = self.board_surface

            self.board_renderer.draw_board()
            self.board_renderer.draw_coordinates()
            self.pieces.draw(self.board_surface)
            if self.dragger.piece is not None:
                self.show_moves(self.dragger.piece.row, self.dragger.piece.column)

            if self.dragger.dragging and self.dragger.sprite:
                self.board_surface.blit(
                    self.dragger.sprite.image, self.dragger.sprite.rect
                )
            pygame.display.update()
            self.clock.tick(60)
