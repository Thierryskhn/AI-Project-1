class State:
    def __init__(self, board, players, current_player):
        self.board = board
        self.players = players
        self.current_player = current_player

    def get_board(self):
        return self.board
    
    def get_players(self):
        return self.players
    
    def get_current_player(self):
        return self.current_player