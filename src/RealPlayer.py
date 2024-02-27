from Player import Player
from CCBoard import CCBoard, Board

class RealPlayer(Player):
    # RealPlayer class is used to represent a real player
    # id (int): player id
    # color (str): hex color
    def __init__(self, id: int, color: str):
        super().__init__(id, color)


    # Gets the coordinates input from the player
    def get_coordinates_input(self, board: Board, message: str):
        coordinates = None
        while coordinates == None:
            move = input(message).strip().split(' ')
            if len(move) != 2 or not move[0].isnumeric() or not move[1].isnumeric():
                print("Invalid input, try again")
                continue

            if not board.is_valid_position(int(move[0]), int(move[1])):
                print("Invalid position, try again")
                continue

            coordinates = (int(move[0]), int(move[1]))

        return coordinates

    # Gets the move from the player
    def get_move(self, board: Board):
        valid = False

        while not valid:
            piece = self.get_coordinates_input(board, f"Player {self.id}: Enter the piece you want to move ('x y'): ")
            dest = self.get_coordinates_input(board, f"Player {self.id}: Enter the place you want to move the piece to ('x y'): ")

            valid = board.is_valid_move(self.id, piece, dest)

        return (piece, dest)