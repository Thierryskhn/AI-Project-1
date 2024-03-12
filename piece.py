class Piece:

    def __init__(self, name, color, coords, id):
        self.color  = color
        self.coords = coords
        self.name = name
        self.id = id

    def __str__(self):
        return str(self.name)
    
    def get_coords(self):
        return self.coords
    
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
        return Piece(self.name, self.color, self.coords.copy(), self.id)