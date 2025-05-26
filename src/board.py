"""
Board represetation
"""


class Piece:
    """
    Internal class for pieces
    Do not confuse with game.PieceSprite ( the class used by pygame)
    """

    def __init__(self, piece: str, row: int, column: int):
        self.piece: str = piece  # name of piece
        self.row: int = row
        self.column: int = column


class Square:
    def __init__(self, row: int, column: int, piece: Piece | None = None):
        if row < 0 or row > 7:
            raise ValueError(f"Not a valid row: expected int 0-7, got: {row}")
        self.row: int = row
        if column < 0 or column > 7:
            raise ValueError(f"Not a valid col: expected int 0-7, got: {row}")
        self.column: int = column
        self.piece: Piece | None = piece
        self._alphacols = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
            7: "H",
        }
        self.rank = self._alphacols[column]
        self.file = self.row + 1
        self.col = column  # ease of use

    def __str__(self) -> str:
        return f"{self.piece}"

    def has_piece(self) -> bool:
        return self.piece is not None

    def empty(self) -> bool:
        return self.piece is None

    def has_enemy(self, color) -> bool:
        # TODO when we have enemies and piece classes
        return False

    def has_team(self, color) -> bool:
        # TODO
        return False


class Board(object):
    def __init__(self):
        self.board = [[Square(i, j) for i in range(8)] for j in range(8)]

    def __str__(self):
        #
        pass
