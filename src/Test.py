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
    list_players = []
    list_players.append(AIPlayer(1, colors[0]))
    list_players.append(AIPlayer(2, colors[1]))
    board = Board(num_players, list_players) 

    board.move_piece(1, 0, (-1, 4, -3))
    board.move_piece(1, 1, (-1, 2, -1))
    board.move_piece(1, 2, (0, 0, -0))

    board.print_board()

    print("Possible moves for piece 9 (player 1)")
    for m in board.create_all_moves_boards(list_players[0].color):
        if m[1][0].id == 9 and m[1][0].player == 1:
            m[0].print_board()

main()
