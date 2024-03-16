from abc import abstractmethod 
from Board import Board

class Player:
    def __init__(self, id: int, color: str, opponent=None, saves_moves=False):
        """ Initialize the Player class
        Args:
            id (int): player id
            color (str): player color
        """
        self.id = id
        self.color = color
        self.opponent = opponent
        self.saves_moves = saves_moves

    def get_id(self):
        """ Get the player id """
        return self.id
    
    def get_color(self):
        """ Get the player color """
        return self.color
    
    @abstractmethod
    def get_move(self, board: Board):
        """ Get the move from the player
        Args:
            board (Board): The current state of the game
        """
        pass