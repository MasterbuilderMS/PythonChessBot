"""Speed tests"""

import time
from bot import ChessBot
import chess
import cProfile


def get_bot_time():
    c = ChessBot()
    times = []
    # loop to get average
    print("starting...")
    for i in range(100):
        print(i)
        start = time.time()
        c.choose_move(chess.Board())
        end = time.time()
        times.append(end - start)
    average = sum(times) / 100

    print(f"average = {average}")


# get_bot_time()
bot = ChessBot()
board = chess.Board()
cProfile.run("bot.choose_move(board)", sort=-1)
