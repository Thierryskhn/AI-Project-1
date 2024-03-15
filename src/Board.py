from Piece import Piece
from Color import Color

class Board:

    def __init__(self, list_players, *args, **kwargs):
        self.num_players = 2
        self.pieces = []
        self.list_players = list_players.copy()

        # if we want to copy the board, avoid creating what we already have that does not change
        test_args = ['copy', 'zones', 'coordinates', 'start_zones', 'end_zones', 'pieces']
        if all(arg in kwargs for arg in test_args) and kwargs['copy'] == True:
            self.pieces = kwargs['pieces']
            self.zones = kwargs['zones']
            self.coordinates = kwargs['coordinates']
            self.start_zones = kwargs['start_zones']
            self.end_zones = kwargs['end_zones']
        else :
            self.zones = self.create_zones(self.num_players)
            self.coordinates = [self.zones[0],self.zones[1],self.zones[2],self.zones[3],self.zones[4],self.zones[5],self.zones[6]]
            self.start_zones = {list_players[0]:self.zones[1],list_players[1]:self.zones[4]}
            self.end_zones = {list_players[0]:self.zones[4], list_players[1]:self.zones[1]}

    #create each zones with the correct coordinates
    def create_zones(self,num_players):
        side_size = 4
        zones = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

        #start and end zones player 1
        for q in range(-side_size, 0):
            for r in range(side_size+1, side_size -q + 1):
                    zones[1].append((q,r,-q-r))
                    self.add_piece(0, (q,r,-q-r))
                    zones[4].append((-q,-r,q+r))
                    if num_players == 2 : 
                        self.add_piece(1, (-q,-r,q+r))
        
        for q in range(0, side_size + 1):
            for r in range(side_size - q+ 1, side_size + 1):
                zones[2].append((q,r,-q-r))
                zones[5].append((-q,-r,q+r))
                if num_players == 3 : 
                    self.add_piece(2, (-q,-r,q+r))
                

        # start and end zone player 3
        for q in range(side_size+1, 2*side_size+1):
            for r in range(-side_size, side_size -q + 1):
                zones[3].append((q,r,-q-r))
                if num_players == 3 : 
                    self.add_piece(1, (q,r,-q-r))
                zones[6].append((-q,-r,q+r))

        #neutral zone ie zone 0
        for q in range(-side_size, side_size + 1):
            r1 = max(-side_size, -q - side_size)
            r2 = min(side_size, -q + side_size)
            for r in range(r1, r2 + 1):
                zones[0].append((q,r,-q-r))

        return zones

    def coords_in_boards(self,coords):
        return any(coords in zone for zone in self.coordinates)

    def is_adjacent_piece(self, piece_coords, coords_to_check):
        return abs(piece_coords[0] - coords_to_check[0]) + abs(piece_coords[1] - coords_to_check[1]) + abs(piece_coords[2] - coords_to_check[2]) == 2

    def legal_moves(self, piece):
        """
        Computes a list of legal moves for a given piece
        
        Args:
            Piece (Piece): the piece for which we want to compute the legal moves
        """
        # List containing the legal moves for a specific piece
        legal_moves = []

        # First get the piece's coordinates
        piece_x, piece_y, piece_z = piece.coords

        # Then we have to search if there is any adjacent piece blocking the current piece
        neighbour_pieces = self.get_neighbours(piece.coords[0], piece.coords[1], piece.coords[2])

        # Adding the neighbouring spaces that are not filled up by the adjacent pieces
        coords_to_check = [(piece_x+1, piece_y-1, piece_z), (piece_x+1, piece_y, piece_z-1), (piece_x, piece_y+1, piece_z-1),
                        (piece_x-1, piece_y+1, piece_z), (piece_x-1, piece_y, piece_z+1), (piece_x, piece_y-1, piece_z+1)]
        for coords in coords_to_check:
            if self.coords_in_boards(coords) and coords not in [(p.coords) for p in neighbour_pieces]:
                legal_moves.append(coords)

        # Now we have to append the spaces that can be added with jumps   
        places_to_jump_from = [(piece.coords)]

        # Iterate while there are places that have not been expanded
        while len(places_to_jump_from) > 0:
            # Get the first element of the list
            current_place = places_to_jump_from.pop(0)

            neighbour_pieces = self.get_neighbours(current_place[0], current_place[1], current_place[2])
            for neighbour_piece in neighbour_pieces:
                # If the space after the piece is empty, then we can jump over it
                # Substract to get the perfect aligned space 
                x = neighbour_piece.coords[0] - current_place[0]
                y = neighbour_piece.coords[1] - current_place[1] 
                z = neighbour_piece.coords[2] - current_place[2]
                
                piece_coords_to_check = (neighbour_piece.coords[0] + x, neighbour_piece.coords[1] + y, neighbour_piece.coords[2] + z)

                in_board = self.coords_in_boards(piece_coords_to_check)
                dest_free = piece_coords_to_check not in [(p.coords) for p in self.pieces]
                not_expanded = piece_coords_to_check not in legal_moves

                if in_board == True and dest_free == True and not_expanded == True:
                    legal_moves.append(piece_coords_to_check)
                    places_to_jump_from.append(piece_coords_to_check)
                    
        return legal_moves

    def get_neighbours(self, piece_x, piece_y, piece_z):
        neighbour_pieces = []
        for p in self.pieces:
            #compute the euclidean distance of the piece to the current piece 
            if self.is_adjacent_piece((piece_x, piece_y, piece_z), p.coords):
                neighbour_pieces.append(p)

        return neighbour_pieces

    def game_finished(self, list_players):
        """
        Function that checks if the game is finished and returns a boolean
        Args:
            list_players (list(Player)): list of players in the game
        """
        return self.get_winner(list_players) != None
        
    def get_winner(self, list_players):
        """
        Function that returns the winner of the game, or None if the game is not finished
        Args:
            list_players (list(Player)): list of players in the game
        """
        for player in list_players:
            # Initially we assume that the goal is reached
            goal_reached = True
            # Iterating through the pieces of each player, we check if they are in the goal state
            for piece in [p for p in self.pieces if p.color == player.color]:
                # If one piece does not satisfy the goal, the game is not finished
                if piece.coords not in self.end_zones[player]:
                    goal_reached = False
                    break
            # Otherwise a player satisified the goal states ! 
            if goal_reached:
                return player
        # If no player satisfied the goal states, the game is not finished
        return None

    def create_all_moves_boards(self, color):
        """
        Function that creates boards for all possible moves from a given state, for a specific player (color)

        Args:
            color (str): the color of the player for which we want to create the boards

        Returns:
            tuple: a list of tuples containing the new boards and the piece-move tuple that led to them
        """
        
        different_boards_after_moves =  []
        #We iterate through the pieces of the same color
        for p in self.pieces:
            if p.get_color() == color:
                #We iterate through the legal moves of the piece
                for move in self.legal_moves(p):
                    #We create a new board for each move
                    new_board = self.copy()
                    new_p = new_board.pieces[self.pieces.index(p)]
                    new_board.move_piece(new_p.player, new_p.id, move)
                    different_boards_after_moves.append((new_board, (new_p, move)))

        return different_boards_after_moves
    

    def move_piece(self, player_id, piece_id, dest):
        """
        Function that moves a piece to a new position

        Args:
            piece (Piece): the piece to move
            move (tuple of ints): the new position of the piece in coords
        """
        piece = [p for p in self.pieces if p.id == piece_id and p.player == player_id].pop()
        piece.set_coords(dest)
        return 

    def add_piece(self, player_nr, coords):
        """
        Function that adds a piece to the board. Automatically assigns an id to the piece, based on the number of pieces of the same color

        Args:
            player_nr (int): the player
            coords (tuple of ints): the coordinates of the piece
        """
        id = len([p for p in self.pieces if p.color == self.list_players[player_nr].color])

        self.pieces.append(Piece(self.list_players[player_nr].id,self.list_players[player_nr].color,coords, id))

    def copy(self):
        """
        Function that returns a copy of the board
        """
        new_board = Board(self.list_players, copy=True, zones=self.zones, coordinates=self.coordinates, start_zones=self.start_zones, end_zones=self.end_zones)
        new_board.pieces = [p.copy() for p in self.pieces]

        return new_board
    
    def print_board(self):
        """
        Function that prints the board
        """

        side_size = 8
        pieces_coordinates =  [piece.coords for piece in self.pieces]

        print()

        for y in range(2*side_size+1):
            for x in range(3*side_size+1):
                if x%2 == y%2:
                    q = int((x+y-20)/2) #x =2*q+r+12
                    r = 8-y 
                    coords = (q,r,-q-r)
                    if not self.coords_in_boards(coords):
                        print(" ",end="")
                    elif not coords in pieces_coordinates: 
                        if coords == (0,0,0):
                            print(f"⬡",end="")
                        else:
                            print("⬢",end="")
                    else:
                        p = self.pieces[pieces_coordinates.index(coords)]
                        print(p,end="")
                else: print(" ", end="")
            print()

        print()
