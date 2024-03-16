from Player import Player, Board
from AlphaBeta import AlphaBeta
from BoardEval import eval
from time import sleep

AI_SLEEP_TIME = 0 # Time to wait before playing once the move is found, in seconds (recommended: 2)
CUTOFF = 2 # Depth at which to cut off search (recommended: 3)
RECENTLY_PLAYED_SIZE = 3 # Number of moves to remember

class AIPlayer(Player):
    def __init__(self, id: int, color: str, opponent: Player = None):
        """ Initialize the AIPlayer class
        Args:
            id (int): player id
            color (str): player color
        """
        super().__init__(id, color, opponent=opponent, saves_moves=True)
        self.recently_played = []

    def get_move(self, state: Board):
        """ Get the move from the player
        Args:
            state (Board): The current state of the game
        """
        print(f"Player {self.id} is thinking...")

        ab = AlphaBeta(CUTOFF, eval)
        move = ab.search(self, state, log=False)

        while len(self.recently_played) > RECENTLY_PLAYED_SIZE:
            self.recently_played.pop(0)
        to_append = self.build_recently_played_elem(move[0])
        self.recently_played.append(to_append)

        sleep(AI_SLEEP_TIME)

        print(f"Player {self.id} has played!")

        # main will handle this case as a forfeit
        if move == None: 
            print("AIPlayer: No move found")
            return None

        return move[1] # move[1] is the move, move[0] is the board that results from the move
    
    def build_recently_played_elem(self, board):
        """ Build the set to add to the recently_played list 
            The set contains the coordinates of the player's pieces, not saving the opponent's pieces
            or what piece is in each position
        """
        return set(p.coords for p in board.pieces if p.color == self.color)
        