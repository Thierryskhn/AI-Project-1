import numpy as np


# --------------------- Whole Chinese Checkers game class -------------------- #
class ChineseCheckers:

    def __init__(self, num_players):
        self.board = Board()
        self.num_players = num_players


# -------------------------------- Board Class ------------------------------- #
class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height


# ------------------------------- Vertex class ------------------------------- #
class Piece:

    def __init__(self, player, x, y):
        self.x = x
        self.y = y 
        self.player = player 

    def getplayer(self):
        return self.player
    
    def getCoords(self):
        return (self.x, self.y)
    
    def setCoords(self, newX, newY):
        self.x = newX
        self.y = newY

# ------------------------------- Player Class ------------------------------- #

class Player:
    
    def __init__(self, id, score, moves):
        self.id = id
        self.moves = moves
        self.score = score

    def __str__(self) -> str:
        return f"Player {self.id} has {self.score} points and {self.moves} moves left"
    
    def get_score(self):
        return self.score
    
    def add_score(self):
        self.score += 1 


"""
_BOARD_STR = \
222200000
222000000
220000000
200000000
000000000
000000001
000000011
000000111
000001111

FULL_BOARD = np.array([[ int(c) for c in r] for r in _BOARD_STR.splitlines()], dtype=np.int8)

print(FULL_BOARD)"""