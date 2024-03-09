from Player import Player, Board
from AlphaBeta import AlphaBeta
from BoardEval import eval

class AIPlayer(Player):
    def __init__(self, id: int, color: str):
        """ Initialize the AIPlayer class
        Args:
            id (int): player id
            color (str): player color
        """
        super().__init__(id, color)

    def get_move(self, state: Board):
        """ Get the move from the player
        Args:
            state (Board): The current state of the game
        """
        ab = AlphaBeta(3, eval)
        move = ab.search(self, state)

        return move[1] # move[1] is the move, move[0] is the board that results from the move