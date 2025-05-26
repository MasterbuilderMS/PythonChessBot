"""
Board represetation
"""


class Piece:
    """
    Internal class for pieces
    Do not confuse with game.PieceSprite ( the class used by pygame)
    """

    def __init__(self, piece: str, row: int, column: int, color: str):
        self.piece: str = piece  # name of piece
        self.row: int = row
        self.column: int = column
        self.color: str = color


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
        self.setup_pieces()

    def __str__(self):
        text = ""
        for i in range(8):
            for j in range(8):
                cell = self.board[i][j]
                if cell is None or cell.piece is None:
                    text += "|" + " ".ljust(10) + "|"
                else:
                    text += "|" + cell.piece.piece.ljust(10) + "|"
                # text += "|" + self.board[i][j].piece.piece.ljust(10) + "|"
            text += "\n"
        return text

    def setup_pieces(self):
        pawn_rows = [1, 6]  # rows where pawns are
        for row, color in zip(pawn_rows, ["white", "black"]):
            for col in range(8):
                self.board[row][col].piece = Piece("pawn", row, col, color)
        other_rows = [0, 7]  # rows where other pieces are (dur...)
        for row, color in zip(other_rows, ["white", "black"]):
            for col, piece in enumerate(
                [
                    "rook",
                    "knight",
                    "bishop",
                    "queen",
                    "king",
                    "bishop",
                    "knight",
                    "rook",
                ]
            ):
                self.board[row][col].piece = Piece(piece, row, col, color)

    @property
    def pieces(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col].has_piece():
                    yield self.board[row][col].piece


if __name__ == "__main__":
    b = Board()
    print(b)
