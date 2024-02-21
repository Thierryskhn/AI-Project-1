
# --------------------- Whole Chinese Checkers game class -------------------- #
class ChineseCheckers:

    def __init__(self, num_players):
        self.board = Board()
        self.num_players = num_players


# -------------------------------- Board Class ------------------------------- #
class Board:

    def __init__(self):
        self.width = 25
        self.height = 17 


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
