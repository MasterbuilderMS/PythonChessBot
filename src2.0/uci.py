import chess
import sys
from bot import ChessBot, AlphaBetaBot


def main():
    bot = ChessBot()
    board = chess.Board()

    while True:
        try:
            line = input().strip()
        except EOFError:
            break

        if line == "uci":
            print("id name MaterialBot")
            print("id author You")
            print("uciok")
        elif line == "isready":
            print("readyok")
        elif line.startswith("position"):
            board = parse_position(line, board)
        elif line.startswith("go"):
            move = bot.choose_move(board)
            if move:
                print(f"bestmove {move.uci()}")
            else:
                print("bestmove 0000")
        elif line == "ucinewgame":
            board.reset()
        elif line == "quit":
            break


def parse_position(command: str, board: chess.Board) -> chess.Board:
    tokens = command.split()
    if "startpos" in tokens:
        board.reset()
        moves_index = tokens.index("startpos") + 1
    elif "fen" in tokens:
        fen_start = tokens.index("fen") + 1
        fen_end = fen_start + 6
        fen = " ".join(tokens[fen_start:fen_end])
        board.set_fen(fen)
        moves_index = fen_end
    else:
        return board  # Invalid format

    if "moves" in tokens[moves_index:]:
        moves_start = tokens.index("moves", moves_index) + 1
        for move_str in tokens[moves_start:]:
            move = chess.Move.from_uci(move_str)
            if move in board.legal_moves:
                board.push(move)

    return board


if __name__ == "__main__":
    main()
