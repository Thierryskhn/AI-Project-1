from Player import Player, Board

import numpy as np


class AIPlayer(Player):

    def __init__(self, color, name, pieces_array, goal_states):
        self.name  = name
        self.color = color
        #Adding this array to just handle the pieces on te baord 

        #Il faudra arranger comment on assigne a la liste 
        self.pieces_array = pieces_array
        self.goal_states = goal_states


        
    def __str__(self):
        return self.name

    def get_move(self, board: Board):

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