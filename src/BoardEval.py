import math

MAX_TOTAL_DISTANCE = 140 # These values were found by testing all positions
MIN_TOTAL_DISTANCE = 20
MAX_EVAL = MAX_TOTAL_DISTANCE - MIN_TOTAL_DISTANCE

def goal_distance_eval(player, state):
    """ Evalution function based on the distance to the goal
    Args:
        state (Board): The state to evaluate
    """
    player_pieces = [piece for piece in state.pieces if piece.color == player.color]
    
    goal = max_coordinates(state.end_zones[player])

    score = MAX_EVAL - (sum_distance_to_goal(player_pieces, goal) -  MIN_TOTAL_DISTANCE)

    if (score < 0):
        raise ValueError(f"Score is negative: {score}")

    return score

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
    piece_coords = piece.coords

    # The division by 2 is to get the distance in hex coordinates
    return (abs(piece_coords[0] - goal_pos[0]) + abs(piece_coords[1] - goal_pos[1]) + abs(piece_coords[2] - goal_pos[2]))/ 2

def max_coordinates(coords):
    """ Return the max absolute coordinates
    Args:
        coords (list): The coordinates
    """
    max_coord = (0, 0, 0)
    for coord in coords:
        if abs(coord[0]) + abs(coord[1]) + abs(coord[2 ]) >= abs(max_coord[0]) + abs(max_coord[1]) + abs(max_coord[2]):
            max_coord = coord
    return max_coord