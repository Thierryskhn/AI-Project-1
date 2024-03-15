from Player import Player, Board

class RealPlayer(Player):
    def __init__(self, id: int, color: str, opponent: Player = None):
        """ Initialize the RealPlayer class
        Args:
            id (int): player id
            color (str): player color
        """
        super().__init__(id, color, opponent)

    def get_coordinates_input(self, board: Board, message: str):
        """ Get the coordinates input from the player
        Args:
            board (Board): The current state of the game
            message (str): The message to display to the player
        """
        coordinates = None
        while coordinates == None:
            move = input(message).strip().split(' ')
            if len(move) != 3 or not all(coord.isnumeric() for coord in move):
                print("Invalid input, try again")
                continue

            if not board.coords_in_boards((int(move[0]), int(move[1]), int(move[2]))):
                print("Invalid position, try again")
                continue

            coordinates = (int(move[0]), int(move[1]), int(move[2]))

        return coordinates
    
    def get_id_input(self, board: Board, message: str):
        """ Get the id input from the player
        Args:
            board (Board): The current state of the game
            message (str): The message to display to the player
        """
        piece_id = None
        while piece_id == None:
            piece_id = input(message).strip()
            if not piece_id.isnumeric():
                print("Invalid input, try again")
                piece_id = None
                continue
            piece_id = int(piece_id)
            if not piece_id in [p.id for p in board.pieces if p.color == self.color]:
                print("Invalid piece id, try again")
                piece_id = None

        return piece_id

    def get_move(self, board: Board):
        """ Get the move from the player
        Args:
            board (Board): The current state of the game
        """
        valid = False

        while not valid:
            piece = self.get_id_input(board, f"Player {self.id}: Enter the piece you want to move : ")
            dest = self.get_coordinates_input(board, f"Player {self.id}: Enter the place you want to move the piece to ('q r s', see src/Board.png): ")

            piece = [p for p in board.pieces if p.id == piece and p.color == self.color][0]

            valid = dest in board.legal_moves(piece) and board.coords_in_boards(dest)

            if not valid:
                print("Invalid move, try again")

        print(f"Player {self.id} has played!")

        return (piece, dest)