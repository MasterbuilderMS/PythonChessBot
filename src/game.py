"""contains the pygame implementation of the chess game"""

import os
import pygame
from board import Board, Piece


WIDTH = 800
HEIGHT = 800
SQSIZE = 80


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
        self.rect.topleft = (self.col * SQSIZE, self.row * SQSIZE)

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
        board_px = SQSIZE * 8
        self.x_offset = (WIDTH - board_px) // 2
        self.y_offset = (HEIGHT - board_px) // 2
        self.board = Board()
        self.board_surface = self.screen.subsurface(
            pygame.Rect(self.x_offset, self.y_offset, board_px, board_px)
        )
        self.board_renderer = BoardRenderer(self.board_surface, SQSIZE, origin=(self.x_offset, self.y_offset))  # fmt: off
        # subsurface, so things can omre easily be placed on the board

        self.clock = pygame.time.Clock()
        self.pieces = pygame.sprite.Group()  # all sprites on the board
        self.update_pieces()
        self.dragger = Dragger()  # dragging pieces

    def update_pieces(self):
        self.pieces.empty()
        for i in self.board.pieces:
            self.pieces.add(PieceSprite(i))

    def mainloop(self):
        running = True
        while running:
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
                                self.dragger.drag(sprite.piece, sprite)
                                break
                    else:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        file = (mouse_x - self.x_offset) // SQSIZE
                        rank = (mouse_y - self.y_offset) // SQSIZE

                        # Clamp to board boundaries
                        file = max(0, min(7, file))
                        rank = max(0, min(7, rank))

                        # Update piece position
                        self.dragger.piece.row = rank
                        self.dragger.piece.column = file
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
                    MIN_WIDTH = SQSIZE * 8 + 6
                    MIN_HEIGHT = SQSIZE * 8 + 6

                    new_width = max(event.w, MIN_WIDTH)
                    new_height = max(event.h, MIN_HEIGHT)
                    self.screen = pygame.display.set_mode(
                        (new_width, new_height), pygame.RESIZABLE
                    )

                    board_px = SQSIZE * 8
                    self.x_offset = (event.w - board_px) // 2
                    self.y_offset = (event.h - board_px) // 2

                    self.board_surface = self.screen.subsurface(
                        pygame.Rect(self.x_offset, self.y_offset, board_px, board_px)
                    )
                    self.board_renderer.surface = self.board_surface

            self.board_renderer.draw_board()
            self.pieces.draw(self.board_surface)
            if self.dragger.dragging and self.dragger.sprite:
                self.board_surface.blit(
                    self.dragger.sprite.image, self.dragger.sprite.rect
                )
            pygame.display.update()
            self.clock.tick(60)
