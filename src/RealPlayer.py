from Player import Player, Board

class RealPlayer(Player):
    def __init__(self, id: int, color: str):
        """ Initialize the RealPlayer class
        Args:
            id (int): player id
            color (str): player color
        """
        super().__init__(id, color)

    def get_coordinates_input(self, board: Board, message: str):
        """ Get the coordinates input from the player
        Args:
            board (Board): The current state of the game
            message (str): The message to display to the player
        """
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

    def get_move(self, board: Board):
        """ Get the move from the player
        Args:
            board (Board): The current state of the game
        """
        valid = False

        while not valid:
            piece = self.get_coordinates_input(board, f"Player {self.id}: Enter the piece you want to move ('x y'): ")
            dest = self.get_coordinates_input(board, f"Player {self.id}: Enter the place you want to move the piece to ('x y'): ")

            valid = board.is_valid_move(self.id, piece, dest)

        return (piece, dest)