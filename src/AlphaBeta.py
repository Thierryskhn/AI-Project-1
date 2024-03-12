class AlphaBeta:

    def __init__(self, cutoff, evaluation_function):
        """ Creates a new AlphaBeta search object.
        Args:
            cutoff (int): The depth at which to cut off search
            evaluation_function (function): A function that returns a score for a given state 
        """
        self.cutoff = cutoff
        self.eval_fn = evaluation_function

    def search(self, player, state):
        """ Search the game state and return the best move
        Args:
            player (str): The current player
            state (Board): The current state of the game
            depth (int): The current depth
        """
        v = self.max_value(player, state, float('-inf'), float('inf'), 0)

        all_moves = state.create_all_moves_boards(player.color)
        for move in all_moves:
            if self.eval_fn(player, move[0]) == v:
                return move

        print("AlphaBeta: No move found")
        return None

    def max_value(self, player, state, alpha, beta, depth):
        """ Return the value of a max node
        Args:
            player (str): The current player
            state (Board): The current state of the game
            alpha (int): The current alpha value
            beta (int): The current beta value
            depth (int): The current depth
        """
        if self.cutoff_test(state, depth):
            return self.eval_fn(player, state)

        v = float('-inf')
        for move in state.create_all_moves_boards(player.color):
            v = max(v, self.min_value(player, move[0], alpha, beta, depth + 1))

            if v >= beta:
                return v
            
            alpha = max(alpha, v)
        
        return v

    def min_value(self, player, state, alpha, beta, depth):
        """ Return the value of a min node
        Args:
            player (str): The current player
            state (Board): The current state of the game
            alpha (int): The current alpha value
            beta (int): The current beta value
            depth (int): The current depth
        """
        if self.cutoff_test(state, depth):
            return self.eval_fn(player, state)

        v = float('inf')
        for move in state.create_all_moves_boards(player.color):
            v = min(v, self.max_value(player, move[0], alpha, beta, depth + 1))

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
        if depth >= self.cutoff or state.game_finished(state.list_players):
            return True
        
        return False