from src.Board import Board
from src.Piece import Piece

MAX_DISTANCE = 100

def eval(move, player):
    """ Return the evaluation of a board
    Args:
        move ((Board, (Piece, newCoords))): The board to evaluate
    """
    board = move[0]
    player_pieces = [piece for piece in board.pieces if piece.player == player]

    goal = average_coordinates(board.end_zones[player])

    return MAX_DISTANCE - sum_distance_to_goal(player_pieces, goal)

def sum_distance_to_goal(pieces, goal):
    """ Return the sum of the distance to the goal
    Args:
        pieces (list): The pieces to move
        goal (tuple): The goal position
    """
    return sum([distance_to_goal(piece, goal) for piece in pieces])

def distance_to_goal(piece, goal_pos):
    """ Return the distance to the goal
    Args:
        piece (Piece): The piece to move
        goal_pos (tuple): The goal position
    """
    return abs(piece.get_coords()[0] - goal_pos[0]) + abs(piece.get_coords()[1] - goal_pos[1]) + abs(piece.get_coords()[2] - goal_pos[2])

def average_coordinates(coords):
    """ Return the average coordinates
    Args:
        coords (list): The coordinates
    """
    c1 = sum([coord[0] for coord in coords]) // len(coords)
    c2 = sum([coord[1] for coord in coords]) // len(coords)
    c3 = sum([coord[2] for coord in coords]) // len(coords)

    return (c1, c2, c3)