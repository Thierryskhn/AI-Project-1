import GameBoard

import numpy as np


class AIPlayer:

    def __init__(self, color, name, pieces_array, goal_states):
        self.name  = name
        self.color = color
        #Adding this array to just handle the pieces on te baord 

        #Il faudra arranger comment on assigne a la liste 
        self.pieces_array = pieces_array
        self.goal_states = goal_states


        
    def __str__(self):
        return self.name

    def AI_move(self):

        #Creating the min-max implementation
        #The AI will be able to calculate the best move to make
        
        #Sort the array of piece according to the biggest coords (x, y)
        self.pieces_array.sort(key=lambda piece: piece.coords[1]**2 + piece.coords[0]**2, reverse=True)
        
        #a arranger
        for piece in self.pieces_array:
            
            #Check if the piece can move
                if piece.can_move():
                    #Move the piece
                    piece.move()
                    break
    

    def real_move(self): 
        #a arranger tres probablement

        #Choosing which piece to move
        piece_to_move = input("Which piece do you want to move ?")
        while piece_to_move not in self.pieces_array:
            piece_to_move = input("Which piece do you want to move ? (please enter a valid piece) : ")
        
        #Computing the legal moves for the piece
        moves = board.legal_moves(piece_to_move)

        
        move = input("Where do you want to move it ?")
        while move not in moves:
            move = input("Where do you want to move it ? (please enter a valid move  in the good format) : ")

        piece_to_move.set_coords(move)
    
