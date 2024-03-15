from Player import Player, Board
from AlphaBeta import AlphaBeta
from BoardEval import goal_distance_eval
from time import sleep

AI_SLEEP_TIME = 0 # Time to wait before playing once the move is found, in seconds (recommended: 2)
CUTOFF = 3 # Depth at which to cut off search (recommended: 3)

class AIPlayer(Player):
    def __init__(self, id: int, color: str, opponent: Player = None):
        """ Initialize the AIPlayer class
        Args:
            id (int): player id
            color (str): player color
        """
        super().__init__(id, color, opponent)

    def get_move(self, state: Board):
        """ Get the move from the player
        Args:
            state (Board): The current state of the game
        """
        print(f"Player {self.id} is thinking...")

        ab = AlphaBeta(CUTOFF, goal_distance_eval)
        move = ab.search(self, state, log=False)

        sleep(AI_SLEEP_TIME)

        print(f"Player {self.id} has played!")

        # main will handle this case as a forfeit
        if move == None: 
            print("AIPlayer: No move found")
            return None

        return move[1] # move[1] is the move, move[0] is the board that results from the move