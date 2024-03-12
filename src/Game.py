import random  
from Board import Board
from AIPlayer import AIPlayer
from RealPlayer import RealPlayer
from enum import Enum
from time import sleep

SLEEP_TIME = 1.5

class Color(Enum):
    RED = '\33[91m'
    GREEN = '\33[92m'
    YELLOW = '\33[93m'
    BLUE = '\33[94m'
    PURPLE ='\33[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def main():
    colors = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE, Color.PURPLE]
    random.shuffle(colors)
    num_players = 0
    
    #We ask the number of players and check if it is valid
    print()
    while num_players not in (2,3):
        num_players = input("Enter the number of players (2 or 3): ").strip()
        if not (num_players.isnumeric() and int(num_players) in (2,3)):
            print("The number of players is not valid")
            continue
        num_players = int(num_players)
    print()

    list_players = []
    #We ask the type of player for each player and instanciate the correct class
    for i in range(num_players):
        type = ""
        while(type.lower() not in ("human", "ai")):
            type = input("Enter the type of player " + str(i+1) + " (AI or Human): ")

            if(type.lower() not in ("human", "ai")):
                print("The type of player is not valid")
                
        if type.lower() == "ai":
            list_players.append(AIPlayer(i+1, colors[i]))
        else:
            list_players.append(RealPlayer(i+1, colors[i]))

    #Instanciate the board with the correct parameters
    board = Board(num_players, list_players) 

    #While the game is not finished, we loop through the players and ask them to play
    while board.game_finished(list_players) == False:
        for player in list_players:

            print(f"\n{Color.BOLD.value}Current board")
            board.print_board()
            print(f"\n{player.color.value}{Color.BOLD.value}Player {player.id}{Color.END.value}{Color.BOLD.value}'s turn {Color.END.value}")

            move = player.get_move(board)
            board.move_piece(move[0], move[1])

            sleep(SLEEP_TIME)

    #Once the game is finished we can print the winner 
    if board.game_finished(list_players) == True:
        print("The winner is: " + board.game_finished(list_players)[1])

main()
