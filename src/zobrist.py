import random
from collections import namedtuple
import chess


def init_zobrist():
    random.seed(2025)
    zobrist_table = {
        "pieces": [
            [[random.getrandbits(64) for _ in range(64)] for _ in range(2)]
            for _ in range(6)
        ],
        "castling": [
            random.getrandbits(64) for _ in range(16)
        ],  # 4 bits of castling rights
        "ep": [random.getrandbits(64) for _ in range(8)],  # files a-h
        "turn": random.getrandbits(64),
    }
    return zobrist_table


def zobrist_hash(board: chess.Board, zobrist_table) -> int:
    h = 0

    # Pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            pt = piece.piece_type - 1  # 0-indexed: 0 for PAWN ... 5 for KING
            color = int(piece.color)
            h ^= zobrist_table["pieces"][pt][color][square]

    # Castling rights
    cr = 0
    if board.has_kingside_castling_rights(chess.WHITE):
        cr |= 1
    if board.has_queenside_castling_rights(chess.WHITE):
        cr |= 2
    if board.has_kingside_castling_rights(chess.BLACK):
        cr |= 4
    if board.has_queenside_castling_rights(chess.BLACK):
        cr |= 8
    h ^= zobrist_table["castling"][cr]

    # En passant file (if applicable)
    if board.ep_square:
        h ^= zobrist_table["ep"][chess.square_file(board.ep_square)]

    # Turn
    if board.turn == chess.BLACK:
        h ^= zobrist_table["turn"]

    return h


TTEntry = namedtuple("TTEntry", ["depth", "value", "flag"])
EXACT, LOWEBOUND, UPPERBOUND = 0, 1, 2
