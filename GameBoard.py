import math 
from src.Piece import Piece 
from src.Player import Player

class Board:

    def __init__(self, num_players, list_players):
        self.num_players = num_players
        self.zones = self.create_zones(self.num_players)
        self.pieces = []
        self.list_players = list_players.copy()
        self.coordinates = [self.zones[0],self.zones[1],self.zones[2],self.zones[3],self.zones[4],self.zones[5],self.zones[6]]
        self.start_zones = {list_players[0]:self.zones[1],list_players[1]:self.zones[4]} if num_players==2 else {list_players[0]:self.zones[1],list_players[1]:self.zones[3],list_players[2]:self.zones[5]} #remplacer les nombres par les players?
        self.end_zones = {list_players[0]:self.zones[4], list_players[1]:self.zones[1]} if num_players == 2 else {list_players[0]:self.zones[4], list_players[1]:self.zones[6],list_players[2]:self.zones[2]}

    #create each zones with the correct coordinates
    def create_zones(self,num_players):
        side_size = 4
        zones = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

        #start and end zones player 1
        for q in range(-side_size, 0):
            for r in range(side_size+1, side_size -q + 1):
                    zones[0].append((q,r,-q-r))
                    self.pieces.append(Piece(self.list_players[0].id,self.list_players[0].color,(q,r,-q-r)) )
                    zones[4].append((-q,-r,q+r))
                    if num_players == 2 : self.pieces.append(Piece(self.list_players[1].id,self.list_players[1].color,(-q,-r,q+r)) )
        
        for q in range(0, side_size + 1):
            for r in range(side_size - q+ 1, side_size + 1):
                zones[2].append((q,r,-q-r))
                zones[5].append((-q,-r,q+r))
                if num_players == 3 : self.pieces.append(Piece(self.list_players[2].id,self.list_players[2].color,(-q,-r,q+r)) )
                

        # start and end zone player 3
        for q in range(side_size+1, 2*side_size+1):
            for r in range(-side_size, side_size -q + 1):
                zones[3].append((q,r,-q-r))
                if num_players == 3 : self.pieces.append(Piece(self.list_players[1].id,self.list_players[1].color,(q,r,-q-r)) )
                zones[6].append((-q,-r,q+r))

        #neutral zone ie zone 0
        for q in range(-side_size, side_size + 1):
            r1 = max(-side_size, -q - side_size)
            r2 = min(side_size, -q + side_size)
            for r in range(r1, r2 + 1):
                zones[0].append((q,r,-q-r))

        return zones

    def coords_in_boards(self,coords):
        return coords in self.coordinates


    def is_adjacent_piece(self, piece_coords, coords_to_check):
        return (piece_coords._1 - coords_to_check._1) **2 +(piece_coords._2 - coords_to_check._2)**2 + (piece_coords._3 - coords_to_check._3)**2 == 2

    def legal_moves(self, piece):
        #list containing the legal moves for a specific piece
        legal_moves = []
        #First get the piece's coordinates
        piece_x, piece_y, piece_z = piece.get_coords()
        legal_moves_length = 0

        #Then we have to search if there is any adjacent piece blocking the current piece
        neighbor_pieces = []
        for p in self.pieces:
            p_coords = p.get_coords()
            #compute the euclidean distance of the piece to the current piece 
            if self.is_adjacent_piece((piece_x, piece_y, piece_z), p_coords):
                neighbor_pieces.append(p)
        
        #TODO : add the z dimension if done
        #Adding the neighboring spaces that are not filled up by the adjacent pieces
        coords_to_check = [(piece_x+1, piece_y-1, piece_z), (piece_x+1, piece_y, piece_z-1), (piece_x, piece_y+1, piece_z-1),
                        (piece_x-1, piece_y+1, piece_z), (piece_x-1, piece_y, piece_z+1), (piece_x, piece_y-1, piece_z+1)]
        for coords in coords_to_check:
            if self.coords_in_boards(coords) and coords not in [(p.get_coords()) for p in neighbor_pieces]:
                legal_moves.append(coords)
        #Now we have to append the spaces that can be added with jumps   

        #we will potentially put this in another private function 
        for p in neighbor_pieces:
            p_coords = p.get_coords()
            #if the space after the piece is empty, then we can jump over it
            #substract to get the perfect aligned space 
            x = p_coords[0] - piece_x
            y = p_coords[1] - piece_y 
            z = p_coords[2] - piece_z

            piece_coords_to_check = (p_coords[0] + x, p_coords[1] + y, p_coords[2] + z)
            if self.coords_in_boards(piece_coords_to_check) and piece_coords_to_check not in [(pc.get_coords()) for pc in self.pieces]:
                legal_moves.append(piece_coords_to_check)

        #TODO maybe this loop won't work / have a problem
        while len(legal_moves) != legal_moves_length:
            legal_moves_length = len(legal_moves)
            for p in neighbor_pieces:
                #Now we want to check the possible spaces where we can go after jumping over a piece
                if not(self.is_adjacent_piece((piece_x, piece_y), p.get_coords())):
                    for k in self.pieces:
                        if(self.is_adjacent_piece(p.get_coords(), k.get_coords())):
                            #TODO add z dimension if done
                            x = k.get_coords()[0] - p.get_coords()[0]
                            y = k.get_coords()[1] - p.get_coords()[1]
                            z = k.get_coords()[2] - p.get_coords()[2]
                            piece_coords_to_check = (k.get_coords()[0] + x, k.get_coords()[1] + y , k.get_coords()[2] + z)
                            if self.coords_in_boards(piece_coords_to_check) and piece_coords_to_check not in [(pc.get_coords()) for pc in self.pieces]:
                                legal_moves.append(piece_coords_to_check)
        return legal_moves

    def game_finished(self, list_players):
        #This part of the class takes care of checking 
        #if one of players satisfied all the goal states and hence won the game
        #iterating through the players list
        for player in list_players:
            #iterating through the pieces of each player
            for piece in player.pieces_array:
                #if the piece does not satisfy the goal state, just break
                if piece.get_coords() not in player.goal_states:
                    return False
                #Otherwise one player satisified the goal states ! 
                else:
                    print("The winner is: player" + player.get_id())
                    return True
                

    def create_all_moves_boards(self, color):
        #This part of the class takes care of creating all the possible moves for each piece 
        different_boards_after_moves =  []
        #We iterate through the pieces of the same color
        for p in self.pieces:
            if p.color == color:
                #We iterate through the legal moves of the piece
                for move in self.legal_moves(p):
                    #We create a new board for each move
                    new_board = self
                    new_board.move_piece(p, move)
                    different_boards_after_moves.append((new_board, (p, move)))

        return different_boards_after_moves
    

    def move_piece(self, piece, move):
        #This part of the class takes care of moving a piece to a new position
        piece.set_coords(move)
        return 

    
    def get_all_pieces_color(self, player):

        color_player = player.get_color()
        pieces_color = []
        for piece in self.pieces:
            if piece.color == color_player:
                pieces_color.append((piece, piece.get_coords()))

        return pieces_color
    