from Player import Player, Board
from AlphaBeta import AlphaBeta
from BoardEval import eval

class AIPlayer(Player):

    def __init__(self, color, name, pieces_array, goal_states):
        self.name  = name
        self.color = color
        #Adding this array to just handle the pieces on the board 

        
    def __str__(self):
        return self.name

    def get_move(self, state: Board):
        """ Get the move from the player
        Args:
            state (Board): The current state of the game
        """
        ab = AlphaBeta(3, eval)
        move = ab.search(self, state)

        return move[1] # move[1] is the move, move[0] is the board that results from the move