from Color import Color

class Piece:

    def __init__(self, player, color, coords, id):
        self.color  = color
        self.coords = coords
        self.player = player
        self.id = id

    def __str__(self):
        return self.color.value + Color.BOLD.value + str(self.id) + Color.END.value

    def set_coords(self, coords):
        self.coords = coords

    def get_color(self):
        """
        Function getting the color of the piece
        """
        return self.color
    
    def copy(self):
        """
        Function that returns a copy of the piece
        """
        return Piece(self.player, self.color, self.coords, self.id)