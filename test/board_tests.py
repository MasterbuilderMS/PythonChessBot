from src.board import Board, Square

print("Running square checks")
s = Square(0, 0)
for i in range(7):
    s.column = i
    s.row = i
    assert s.column == s.file
    assert s.row == s.rank

print("Running Board checks")
b = Board()
print(b.board)


print("All checks passed successfully")