from Board import Board

class CCBoard(Board):
    def __init__(self, size: int):
        super().__init__(size)

    def is_valid_position(self, x: int, y: int):
        return x >= 0 and x < self.size and y >= 0 and y < self.size
    
    def is_valid_move(self, playerId: int, origin: tuple, dest: tuple):
        return origin != dest