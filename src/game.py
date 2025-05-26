"""contains the pygame implementation of the chess game"""

import os
import pygame
from board import Board, Piece

WIDTH = 800
HEIGHT = 800
SQSIZE = 80


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece: Piece, origin):
        super().__init__()
        self.piece = piece
        image_path = os.path.join(
            f"assets/images/imgs-80px/{self.piece.color}_{self.piece.piece}.png"
        )
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.origin = origin
        self.update_position()

    def update_position(self):
        self.rect.topleft = (
            self.col * 80 + self.origin[0],
            self.row * 80 + self.origin[0],
        )  # Assuming 80px squares

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
                x = file * self.sqsize + self.origin[0]
                y = rank * self.sqsize + self.origin[1]
                rect = pygame.Rect(x, y, self.sqsize, self.sqsize)

                pygame.draw.rect(self.surface, color, rect)

    def draw_coordinates(self):
        for rank in range(8):
            text = self.font.render(str(8 - rank), True, (0, 0, 0))
            self.surface.blit(text, (2, rank * self.sqsize + 2))

        for file in range(8):
            text = self.font.render(chr(ord("a") + file), True, (0, 0, 0))
            self.surface.blit(text, (file * self.sqsize + 2, self.sqsize * 7 + 60))


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        board_px = SQSIZE * 8
        self.x_offset = (WIDTH - board_px) // 2
        self.y_offset = (HEIGHT - board_px) // 2
        self.board = Board()
        self.board_renderer = BoardRenderer(self.screen, SQSIZE, origin=(self.x_offset, self.y_offset))  # fmt: off
        self.clock = pygame.time.Clock()
        self.pieces = pygame.sprite.Group()
        self.update_pieces()

    def update_pieces(self):
        for i in self.board.pieces:
            self.pieces.add(PieceSprite(i, (self.x_offset, self.y_offset)))

    def mainloop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.board_renderer.draw_board()
            self.pieces.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)
