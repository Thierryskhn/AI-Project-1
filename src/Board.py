from abc import abstractmethod 

class Board:
    def __init__(self, size: int):
        self.size = size
        self.player = []
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def create_player(self, playerId: int):
        self.player.append(playerId)

    @abstractmethod
    def is_valid_position(self, x: int, y: int):
        pass
    
    @abstractmethod
    def is_valid_move(self, playerId: int, piece: tuple, dest: tuple):
        pass 