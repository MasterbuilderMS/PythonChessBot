from src.board import Board, Square

print("Running square checks")
s = Square(0, 0)
assert s.column == 0
assert s.row == 0
assert s.file == "A"
assert s.rank == 1
s.column = 5
s.row = 5
assert s.column == 5
assert s.row == 5
assert s.file == "F"
assert s.rank == 6

print("Running Board checks")
b = Board()


print("All checks passed successfully")
