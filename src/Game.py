import random  
from Board import Board
from AIPlayer import AIPlayer
from RealPlayer import RealPlayer
from Color import Color
from time import sleep

TURN_SLEEP_TIME = 0 # Time to wait between turns, in seconds (recommended: 1.5)

def main():
    colors = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE, Color.PURPLE]
    random.shuffle(colors)
    num_players = 2
    
    print()

    list_players = []
    #We ask the type of player for each player and instanciate the correct class
    for i in range(num_players):
        type = "invalid"
        while(type.lower() not in ("human", "ai", "")):
            type = input("Enter the type of player " + str(i+1) + " (AI [default] or Human): ")

            if(type.lower() not in ("human", "ai", "")):
                print("The type of player is not valid")
                
        if type.lower() == "ai" or type == "":
            list_players.append(AIPlayer(i+1, colors[i], ))
        else:
            list_players.append(RealPlayer(i+1, colors[i]))

    # As the players are created one after the other, we have to manually set the opponent for each player
    list_players[0].opponent = list_players[1]
    list_players[1].opponent = list_players[0]


    #Instanciate the board with the correct parameters
    board = Board(list_players) 

    #While the game is not finished, we loop through the players and ask them to play
    forfeit = None
    while board.game_finished(list_players) == False and forfeit == None:
        for player in list_players:

            print(f"\n{Color.BOLD.value}Current board{Color.END.value}")
            board.print_board()
            print(f"\n{player.color.value}{Color.BOLD.value}Player {player.id}{Color.END.value}{Color.BOLD.value}'s turn {Color.END.value}")

            move = player.get_move(board)

            if move == None:
                forfeit = player
                break

            piece, dest = move
            board.move_piece(piece.player, piece.id, dest)

            sleep(TURN_SLEEP_TIME)

    #Once the game is finished we can print the winner 
    if board.game_finished(list_players) == True:
        winner = board.get_winner(list_players)
        print(f"\n{winner.color.value}{Color.UNDERLINE.value}{Color.BOLD.value}Player {winner.id} has won the game!{Color.END.value}")
    else:
        print(f"{forfeit.color.value}Player {forfeit.id}{Color.END.value} has forfeited the game")

main()
