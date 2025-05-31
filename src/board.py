"""
Board represetation
"""

from piece import Piece, Pawn, Knight, Bishop, Rook, Queen, King
import copy


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

    def __eq__(self, other):
        if isinstance(other, Square):
            return self.row == other.row and self.column == other.column
        return False

    def __str__(self) -> str:
        return f"{self.piece}"

    def has_piece(self) -> bool:
        return self.piece is not None

    def empty(self) -> bool:
        return self.piece is None

    def has_enemy(self, color) -> bool:
        return self.has_piece() and self.piece.color != color

    def has_team(self, color) -> bool:
        return self.has_piece() and (self.piece.color) == color


class Move:
    def __init__(self, initial: Square, final: Square, piece: Piece = None):
        self.initial: Square = initial
        self.final: Square = final
        self.piece: Piece = piece  # optional

    def __str__(self):
        if self.piece:
            return (
                f"{self.piece.__class__} moving to {self.final.row},{self.final.column}"
            )
        else:
            return f"move to {self.final.row},{self.final.column}"

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final


class Board(object):
    def __init__(self):
        self.board = [[Square(j, i) for i in range(8)] for j in range(8)]
        self.setup_pieces()
        self.to_move = "white"

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

    def __getitem__(self, pos) -> Square:
        return self.board[pos[0]][pos[1]]

    def __setitem__(self, pos, other) -> None:
        self.board[pos[0]][pos[1]] = other

    def set_true_en_passant(self, piece):
        if isinstance(piece, Pawn):
            for row in range(8):
                for col in range(8):
                    other_piece = self.board[row][col].piece
                    if isinstance(other_piece, Pawn):
                        other_piece.has_moved_two = False
            piece.has_moved_two = True

    def move_piece(self, move: Move):
        # Remove from old square
        initial = self.board[move.initial.row][move.initial.column]
        final = self.board[move.final.row][move.final.column]

        # Capture
        if final.piece is not None:
            final.piece = None
        temp = initial.piece
        self.set_true_en_passant(temp)
        # castling
        if isinstance(temp, King):
            if abs(move.final.column - move.initial.column) == 2:
                if abs(move.final.column - move.initial.column) == 2:
                    row = move.initial.row
                    if move.final.column == 6:
                        # Kingside
                        rook_initial = self.board[row][7]
                        rook_final = self.board[row][5]
                    elif move.final.column == 2:
                        # Queenside
                        rook_initial = self.board[row][0]
                        rook_final = self.board[row][3]

                rook_piece = rook_initial.piece
                if rook_piece is not None:
                    rook_piece.column = rook_final.column
                    rook_piece.row = rook_final.row
                    rook_piece.has_moved = True
                    rook_initial.piece = None
                    rook_final.piece = rook_piece
        # en passant
        if isinstance(temp, Pawn):
            # empty and moved diagonally
            if final.empty() and initial.column - final.column != 0:
                if initial.column < final.column:
                    self.board[move.initial.row][move.initial.column + 1].piece = None
                else:
                    self.board[move.initial.row][move.initial.column - 1].piece = None

        temp.column = move.final.column
        temp.row = move.final.row
        temp.has_moved = True
        initial.piece = None

        # Place on new square
        final.piece = temp
        self.to_move = "black" if self.to_move == "white" else "white"

    def setup_pieces(self):
        pawn_rows = [6, 1]  # rows where pawns are
        for row, color in zip(pawn_rows, ["white", "black"]):
            for col in range(8):
                self.board[row][col].piece = Pawn(row, col, color)
        other_rows = [7, 0]  # rows where other pieces are (dur...)
        for row, color in zip(other_rows, ["white", "black"]):
            self.board[row][0].piece = Rook(row, 0, color)
            self.board[row][1].piece = Knight(row, 1, color)
            self.board[row][2].piece = Bishop(row, 2, color)
            self.board[row][3].piece = Queen(row, 3, color)
            self.board[row][4].piece = King(row, 4, color)
            self.board[row][5].piece = Bishop(row, 5, color)
            self.board[row][6].piece = Knight(row, 6, color)
            self.board[row][7].piece = Rook(row, 7, color)

    def calculate_straight_moves(self, row: int, column: int, directions: list[tuple[int, int]]):  # fmt: off
        moves = []
        piece = self.board[row][column].piece
        initial = Square(row, column, piece)
        for direction in directions:
            # NOTE not really sure what to put here
            for i in range(10):
                new_row: int = row + (i + 1) * direction[0]
                new_column: int = column + (i + 1) * direction[1]
                # on board
                if 0 <= new_column < 8 and 0 <= new_row < 8:
                    # piece in way
                    if self.board[new_row][new_column].has_team(piece.color):
                        break

                    moves.append(Move(initial, Square(new_row, new_column, piece)))

                    if self.board[new_row][new_column].has_enemy(piece.color):
                        break
                else:
                    break

        return moves

    def get_piece_moves(self, row: int, column: int) -> list[Move]:
        piece = self.board[row][column].piece
        moves = []
        if piece.color == self.to_move:
            # initial square of move
            initial = Square(row, column)
            moves = []
            if isinstance(piece, Pawn):
                #  move directly ahead
                for move in piece.moves:
                    if self.board[move[0]][move[1]].empty():
                        final = Square(move[0], move[1])
                        moves.append(Move(initial, final, piece))

                # captures
                for capture in [
                    (row - piece.direction, column - 1),
                    (row - piece.direction, column + 1),
                ]:
                    if (0 <= capture[0] < 8) and (0 <= capture[1] < 8):
                        if self.board[capture[0]][capture[1]].has_enemy(piece.color):
                            final = Square(capture[0], capture[1])
                            moves.append(Move(initial, final, piece))
                # en passant
                for offset in [-1, 1]:  # left, right
                    if self.board[row][column - offset].has_enemy(piece.color):
                        other_piece = self.board[row][column + offset].piece
                        if isinstance(other_piece, Pawn):
                            if other_piece.has_moved_two:
                                final = Square(row - piece.direction, column + offset)
                                moves.append(Move(initial, final, piece))

            elif isinstance(piece, Knight):
                for move in piece.moves:
                    if not self.board[move[0]][move[1]].has_team(piece.color):
                        moves.append(Move(initial, Square(move[0], move[1])))
            elif isinstance(piece, Queen):
                for move in self.calculate_straight_moves(
                    row,
                    column,
                    [
                        (1, 1),
                        (1, -1),
                        (-1, -1),
                        (-1, 1),
                        (0, 1),
                        (1, 0),
                        (-1, 0),
                        (0, -1),
                    ],
                ):
                    moves.append(move)
            elif isinstance(piece, King):
                for direction in [
                    (1, 1),
                    (1, -1),
                    (-1, -1),
                    (-1, 1),
                    (0, 1),
                    (1, 0),
                    (-1, 0),
                    (0, -1),
                ]:
                    new_row: int = row + direction[0]
                    new_column: int = column + direction[1]
                    # on board
                    if 0 <= new_column < 8 and 0 <= new_row < 8:
                        # piece in way
                        if self.board[new_row][new_column].has_team(piece.color):
                            continue

                        moves.append(Move(initial, Square(new_row, new_column, piece)))

                # castling
                if not piece.has_moved:
                    # Kingside castling:
                    kingside_rook = self.board[row][7].piece
                    if (
                        kingside_rook
                        and isinstance(kingside_rook, Rook)
                        and not kingside_rook.has_moved
                    ):
                        # Squares between king (column 4 on starting position) and rook (column 7)
                        if all(
                            self.board[row][col].empty() for col in range(column + 1, 7)
                        ):
                            # Note: In a complete implementation you should also check that the king isn't moving through check.
                            moves.append(
                                Move(initial, Square(row, column + 2, piece), piece)
                            )
                    # Queenside castling:
                    queenside_rook = self.board[row][0].piece
                    if (
                        queenside_rook
                        and isinstance(queenside_rook, Rook)
                        and not queenside_rook.has_moved
                    ):
                        if all(
                            self.board[row][col].empty() for col in range(1, column)
                        ):
                            moves.append(
                                Move(initial, Square(row, column - 2, piece), piece)
                            )
            elif isinstance(piece, Bishop):
                for move in self.calculate_straight_moves(
                    row, column, [(1, 1), (1, -1), (-1, -1), (-1, 1)]
                ):
                    moves.append(move)
            elif isinstance(piece, Rook):
                for move in self.calculate_straight_moves(
                    row, column, [(0, 1), (1, 0), (-1, 0), (0, -1)]
                ):
                    moves.append(move)
        return moves

    def valid_moves(self):
        """
        Returns a list of every possible valid move
        """
        # TODO

    @property
    def pieces(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col].has_piece():
                    yield self.board[row][col].piece


if __name__ == "__main__":
    b = Board()
    print(b)
