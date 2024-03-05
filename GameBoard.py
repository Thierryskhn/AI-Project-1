import math 

class Board: 
    zones = dict
    def __init__(self,side_size,num_players, list_players, list_pieces):
       if num_players in (2,3,4,6) : self.num_players = num_players 
       else: self.num_players = 2 #number of players by default
       self.side_size = side_size #change the size of the board because why not?
       self.zones = self.create_zones(self.num_players,self.side_size)

        #TODO: arranger comment bien copier cette liste
       self.list_players = list_players #copy it better because it does not work this way
       self.list_pieces = list_pieces #copy it better because it does not work this way


    #create each zones with the correct cooridnates
    def create_zones(self,num_players,side_size):
        zones = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

        #start and end zones player 1
        for x in range(-side_size, 0):
            for y in range(side_size+1, side_size -x + 1):
                    zones[0].append((x,y))
                    zones[4].append((-x,-y))

        # start and end zone player 2
        for x in range(0, side_size + 1):
            for y in range(side_size - x + 1, side_size + 1):
                zones[2].append((x,y))
                zones[5].append((-x,-y))
                

        # start and end zone player 3
        for x in range(side_size+1, 2*side_size+1):
            for y in range(-side_size, side_size -x + 1):
                zones[3].append((x,y))
                zones[6].append((-x,y))

        #neutral zone ie zone 0
        for x in range(-side_size, side_size + 1):
            y1 = max(-side_size, -x - side_size)
            y2 = min(side_size, -x + side_size)
            for y in range(y1, y2 + 1):
                zones[0].append((x,y))

    def coords_in_boards(self,coords):
        #TODO : Check if it works well
        x,y = coords
        return -self.side_size <= x <= self.side_size and -self.side_size <= y <= self.side_size and abs(x+y) <= self.side_size


    def is_adjacent_piece(self, piece_coords, coords_to_check):
        return (piece_coords._1 - coords_to_check._1) **2 +(piece_coords._2 - coords_to_check._2) == 2

    def legal_moves(self, piece):
        #TODO : add the z dimension if done

        #This part of the function takes care of computing the legal moves for a piece

        #list containing the legal moves for a specific piece
        legal_moves = []
        #First get the piece's coordinates
        piece_x, piece_y = piece.get_coords()
        legal_moves_length = 0

        #Then we have to search if there is any adjacent piece blocking the current piece
        neighbor_pieces = []
        for p in self.list_pieces:
            p_coords = p.get_coords()
            #compute the euclidean distance of the piece to the current piece 
            if self.is_adjacent_piece((piece_x, piece_y), p_coords):
                neighbor_pieces.append(p)
        
        #Adding the neighboring spaces that are not filed up by the adjacent pieces
        for i in range(-1, 1):
            for j in range(-1, 1):
                if self.coords_in_boards((piece_x + i, piece_y + j)) and (piece_x + i, piece_y + j) not in [(p.get_coords()) for p in neighbor_pieces]:
                    legal_moves.append((piece_x + i, piece_y + j))

        #Now we have to append the spaces that can be added with jumps   

        #we will potentially put this in another private function 
        for p in neighbor_pieces:
            p_coords = p.get_coords()
            #if the space after the piece is empty, then we can jump over it
            #substract to get the perfect aligned space 
            #TODO : add z dimension if done
            x = p_coords._1 - piece_x
            y = p_coords._2 - piece_y 

            piece_coords_to_check = (p.coords_1 + x, p.coords_2 + y)
            if self.coords_in_boards(piece_coords_to_check) and piece_coords_to_check not in [(pc.get_coords()) for pc in self.list_pieces]:
                legal_moves.append(piece_coords_to_check)


        while len(legal_moves) != legal_moves_length:
            legal_moves_length = len(legal_moves)
            for p in neighbor_pieces:
                #Now we want to check the possible spaces where we can go after jumping over a piece
                if not(self.is_adjacent_piece((piece_x, piece_y), p.get_coords())):
                    for k in self.list_pieces:
                        if(self.is_adjacent_piece(p.get_coords(), k.get_coords())):
                            #TODO add z dimension if done
                            x = k.get_coords()._1 - p.get_coords()._1
                            y = k.get_coords()._2 - p.get_coords()._2
                            piece_coords_to_check = (k.get_coords()._1 + x, k.get_coords()._2 + y)
                            if self.coords_in_boards(piece_coords_to_check) and piece_coords_to_check not in [(pc.get_coords()) for pc in self.list_pieces]:
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
                if piece.coords not in player.goal_states:
                    break
                #Otherwise one player satisified the goal states ! 
                else:
                    return (True, player)
                

    def create_all_moves_boards(self, color):
        #This part of the class takes care of creating all the possible moves for each piece 
        different_boards_after_moves =  []
        #We iterate through the pieces of the same color
        for p in self.list_pieces:
            if p.color == color:
                #We iterate through the legal moves of the piece
                for move in p.legal_moves:
                    #We create a new board for each move
                    new_board = self
                    new_board.move_piece(p, move)
                    different_boards_after_moves.append(new_board)

        return different_boards_after_moves
    

    def move_piece(self, piece, move):
        #This part of the class takes care of moving a piece to a new position
        piece.set_coords(move)
        return 