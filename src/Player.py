from abc import abstractmethod 
from Board import Board

class Player:
    # Player class is used to represent a player
    # id (int): player id
    # color (str): hex color
    def __init__(self, id: int, color: str):
        self.id = id
        self.color = color

    def get_id(self):
        return self.id
    
    def get_color(self):
        return self.color
    
    @abstractmethod
    def get_move(self, board: Board):
        pass