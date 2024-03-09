class AlphaBeta:

    def __init__(self, cutoff, evaluation_function):
        """ Creates a new AlphaBeta search object.
        Args:
            cutoff (int): The depth at which to cut off search
            evaluation_function (function): A function that returns a score for a given state 
        """
        self.cutoff = cutoff
        self.eval_fn = evaluation_function

    def search(self, color, state):
        """ Search the game state and return the best move
        Args:
            color (str): The color of the player to move
            state (Board): The current state of the game
            depth (int): The current depth
        """
        v = self.max_value(state, color, float('-inf'), float('inf'), 0)

        for move in state[0].create_all_moves_boards(color):
            if self.eval_fn(move, color) == v:
                return move

        print("AI Error: No move found")
        return None

    def max_value(self, color, state, alpha, beta, depth):
        """ Return the value of a max node
        Args:
            color (str): The color of the player to move
            state (Board): The current state of the game
            alpha (int): The current alpha value
            beta (int): The current beta value
            depth (int): The current depth
        """
        if self.cutoff_test(state, depth):
            return self.eval_fn(state, color)

        v = float('-inf')
        for move in state[0].create_all_moves_boards(color):
            v = max(v, self.min_value(color, move, alpha, beta, depth + 1))

            if v >= beta:
                return v
            
            alpha = max(alpha, v)
        
        return v

    def min_value(self, color, state, alpha, beta, depth):
        """ Return the value of a min node
        Args:
            color (str): The color of the player to move
            state (Board): The current state of the game
            alpha (int): The current alpha value
            beta (int): The current beta value
            depth (int): The current depth
        """
        if self.cutoff_test(state, depth):
            return self.eval_fn(state, color)

        v = float('inf')
        for move in state[0].create_all_moves_boards(color):
            v = min(v, self.max_value(color, move, alpha, beta, depth + 1))

            if v <= alpha:
                return v
            
            beta = min(beta, v)
        
        return v

    def cutoff_test(self, state, depth):
        """ Check if the search should be cut off
        Args:
            state (Board): The current state of the game
            depth (int): The current depth
        """
        if depth >= self.cutoff or state[0].game_finished()[0]:
            return True
        
        return False