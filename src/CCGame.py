from Game import Game, Player
from CCBoard import CCBoard

class CCGame(Game):
    def __init__(self, board: CCBoard, players: list, initial_state):
        super().__init__(board, players, initial_state)

    def player(self, state):
        #TODO
        pass

    def actions(self, state):
        #TODO
        pass

    def result(self, state, action):
        #TODO
        pass

    def terminal_test(self, state):
        #TODO
        pass

    def utility(self, state, player):
        #TODO
        pass