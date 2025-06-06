"Speed comparisons"

import time
from players import BetterBot, AlphaBetaBot, OrderedAlphaBetaBot
import chess

board = chess.Board("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -")
a = AlphaBetaBot()
b = BetterBot()
c = OrderedAlphaBetaBot()
print("with alpha-beta pruning")
now = time.time()
a.choose_move(board)
end = time.time()
print(f"Took {end - now}ms")
# print("without alpha-beta pruning")
# now = time.time()
# b.choose_move(board)
# end = time.time()
# print(f"Took {end - now}ms")
print("with alpha-beta pruning and ordering")
now2 = time.time()
c.choose_move(board)
end2 = time.time()
print(f"Took {end2 - now2}ms")
