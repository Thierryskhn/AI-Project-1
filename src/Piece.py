class Piece:

    def __init__(self, name, color, coords):
        self.color  = color
        self.coords = coords
        self.name = name


    def __str__(self):
        return self.name
    
    def get_coords(self):
        return self.coords
    
    def set_coords(self, coords):
        self.coords = coords

    