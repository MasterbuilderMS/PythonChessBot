"""
Board represetation
"""

class Square:
    def __init__(self, file: int, rank: int, piece: str|None = None):
        self.file: int = file
        self.rank: int = rank
        self.piece: str|None = piece # TODO: will be type piece later
    
    def __str__(self) -> str:
        return f"{self.piece}"

    @property
    def column(self) -> int:
        """Vertical index"""
        return self.file

    @column.setter
    def column(self, value) -> None:
        self.file = value
    
    @property
    def row(self) -> int:
        """Horizontal index"""
        return self.rank
    
    @row.setter
    def row(self, value) -> None:
        self.rank = value
    
    @property
    def has_piece(self) -> bool:
        return self.piece is not None
    
    @property
    def empty(self) -> bool:
        return self.piece is None
    
    def has_enemy(self,color):
        # TODO when we have enemies and piece classes
        pass 

    def has_team(self,color):
        # TODO
        pass




class Board(object):
    def __init__(self):
        self.board = [[Square(i,j) for i in range(8)] for j in range(8)]

    
s = Square(0,0,None)


