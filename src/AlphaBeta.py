class AlphaBeta:

    def __init__(self, cutoff, evaluation_function):
        """ Creates a new AlphaBeta search object.
        Args:
            cutoff (int): The depth at which to cut off search
            evaluation_function (function): A function that returns a score for a given state 
        """
        self.cutoff = cutoff
        self.eval_fn = evaluation_function

    def search(self, player, state, log=False):
        """ Search the game state and return the best move
        Args:
            player (str): The current player
            state (Board): The current state of the game
            depth (int): The current depth
        """
        result = self.initial_max_value(player, state, float('-inf'), float('inf'), 0, log=log)
        
        
        if log:
            print(f"Search done for player {player.id}, found best value {result[0]}.")

        return result[1]

    def initial_max_value(self, player, state, alpha, beta, depth, log=False):
        """ Return the value of a max node, saving the first move. 
            This function exists to save the first move, as the max_value function does not
        Args:
            player (Player): The current player
            state (Board): The current state of the game
            alpha (int): The current alpha value
            beta (int): The current beta value
            depth (int): The current depth
        """
        best_value = float('-inf')
        best_move = None
        for move in state.create_all_moves_boards(player.color):
            v = self.min_value(player, move[0], alpha, beta, depth + 1, log=log)

            if v > best_value:
                best_value = v
                best_move = move

        return (best_value, best_move)
    

    def max_value(self, player, state, alpha, beta, depth, log=False):
        """ Return the value of a max node
        Args:
            player (Player): The current player
            state (Board): The current state of the game
            alpha (int): The current alpha value
            beta (int): The current beta value
            depth (int): The current depth
        """
        if self.cutoff_test(state, depth):
            return_value = self.eval_fn(player, state)
            if log:
                print(f"Searching : depth={depth}, value={return_value}", end="  \r")
            return return_value

        v = float('-inf')
        for move in state.create_all_moves_boards(player.color):

            v = max(v, self.min_value(player, move[0], alpha, beta, depth + 1, log=log))

            if v >= beta:
                return v
            
            alpha = max(alpha, v)
        
        return v

    def min_value(self, player, state, alpha, beta, depth, log=False):
        """ Return the value of a min node
        Args:
            player (Player): The current player
            state (Board): The current state of the game
            alpha (int): The current alpha value
            beta (int): The current beta value
            depth (int): The current depth
        """
        if self.cutoff_test(state, depth):
            return_value = self.eval_fn(player, state)
            if log:
                print(f"Searching : depth={depth}, value={return_value}", end="  \r")
            return return_value

        v = float('inf')
        for move in state.create_all_moves_boards(player.opponent.color): # Here the opponent is the one that is going to play
            
            v = min(v, self.max_value(player, move[0], alpha, beta, depth + 1, log=log))

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