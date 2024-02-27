from abc import abstractmethod

from src.Board import Board
from src.Player import Player
from src.State import State

class Game:
    def __init__(self, board: Board, players: list[Player], initial_state: State):
        self.board = board
        self.players = players
        self.state = initial_state

    @abstractmethod
    def player(self, state: State):
        pass

    @abstractmethod
    def actions(self, state: State):
        pass

    @abstractmethod
    def result(self, state: State, action: tuple):
        pass

    @abstractmethod
    def terminal_test(self, state: State):
        pass

    @abstractmethod
    def utility(self, state: State, player: Player):
        pass