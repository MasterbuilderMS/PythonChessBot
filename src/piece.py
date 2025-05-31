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
        self.moves: list
        self.has_moved: bool = False  # whether or not the piece has already moved

    def generate_line_moves(
        self, directions: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        moves = []
        for dr, dc in directions:
            r, c = self.row + dr, self.column + dc
            while 0 <= r < 8 and 0 <= c < 8:
                moves.append((r, c))
                r += dr
                c += dc
        return moves

    @staticmethod
    def filter_in_range(positions: list[tuple[int, int]]) -> list[tuple[int, int]]:
        return [i for i in positions if 0 <= i[0] < 8 and 0 <= i[1] < 8]


class Pawn(Piece):
    def __init__(self, row, column, color):
        super().__init__("pawn", row, column, color)
        self.direction = 1 if color == "white" else -1
        self.has_moved_two = False  # whether the pawn has just moved 2

    @property
    def moves(self):
        # Diagonal captures
        row, column = self.row, self.column
        captures = [
            (row - self.direction, column - 1),
            (row - self.direction, column + 1),
        ]
        moves = [(row - self.direction, column)]
        if not self.has_moved:
            moves.append((row - (2 * self.direction), column))
        moves = self.filter_in_range(moves)
        return moves


class Knight(Piece):
    def __init__(self, row, column, color):
        super().__init__("knight", row, column, color)

    @property
    def moves(self):
        row, column = self.row, self.column
        moves = [
            (row + 2, column + 1),
            (row + 2, column - 1),
            (row - 2, column + 1),
            (row - 2, column - 1),
            (row + 1, column + 2),
            (row + 1, column - 2),
            (row - 1, column + 2),
            (row - 1, column - 2),
        ]
        return self.filter_in_range(moves)


class Bishop(Piece):
    def __init__(self, row, column, color):
        super().__init__("bishop", row, column, color)

    @property
    def moves(self):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        moves = self.generate_line_moves(directions)
        return moves


class Rook(Piece):
    def __init__(self, row, column, color):
        super().__init__("rook", row, column, color)

    @property
    def moves(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        moves = self.generate_line_moves(directions)
        return moves


class King(Piece):
    def __init__(self, row, column, color):
        super().__init__("king", row, column, color)

    @property
    def moves(self):
        row, column = self.row, self.column
        moves = [
            (row + 1, column),
            (row - 1, column),
            (row, column + 1),
            (row, column - 1),
            (row + 1, column + 1),
            (row + 1, column - 1),
            (row - 1, column + 1),
            (row - 1, column - 1),
        ]
        return self.filter_in_range(moves)


class Queen(Piece):
    def __init__(self, row, column, color):
        super().__init__("queen", row, column, color)

    @property
    def moves(self):
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        return self.generate_line_moves(directions)
