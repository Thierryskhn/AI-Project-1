import numpy as np
import random

from GameBoard import Board

def main():

    colors = random.shuffle(["FF0000", "00ff00", "0000FF", "FFFF00"])
    num_players = 0
    
    #We ask the number of players and check if it is valid
    while num_players not in (2,3):
        num_players = int(input("Enter the number of players (2 or 3): "))
        if(num_players not in (2,3)):
            print("The number of players is not valid")

    list_players = []
    #We ask the type of player for each player and instanciate the correct class
    for i in range(num_players):
        type = None
        while(type.lower not in ("human", "ai")):
            type = input("Enter the type of player" + str(i+1) + " (AI or Human): ")
            if(type.lower not in ("human", "ai")):
                print("The type of player is not valid")
        if type.lower == "ai":
            list_players.append(AIPlayer(i, colors[i]))
        else:
            list_players.append(RealPlayer(i, colors[i]))

    #Instanciate the board with the correct parameters
    board = Board(num_players, list_players, []) # le dernier élément du board est censé être une liste de pièces, mais on ne l'a pas encore implémenté/ discuté

    #While the game is not finished, we loop through the players and ask them to play
    while board.game_finsished(list_players) == False:
        for player in list_players:
            move = player.get_move(board)
            board.move_piece(move)
    #Once the game is finished we can print the winner 
    if board.game_finished(list_players)._1 == True:
        print("The winner is: " + board.game_finished(list_players)._2)



main()
