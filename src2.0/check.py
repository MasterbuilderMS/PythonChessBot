import chess
from bot import ChessBot

board = chess.Board("8/8/8/1R6/1p6/8/8/8 w - - 0 1")
bot = ChessBot()

print(bot.choose_move(board))
