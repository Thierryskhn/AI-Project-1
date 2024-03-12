MAX_DISTANCE = 100 # TODO change this value
MIN_TOTAL_DISTANCE = 0 # TODO change this value

def eval(player, state):
    """ Return the score of a given move
    Args:
        state (Board): The state to evaluate
    """
    player_pieces = [piece for piece in state.pieces if piece.color == player.color]

    goal = average_coordinates(state.end_zones[player])

    return MAX_DISTANCE - (sum_distance_to_goal(player_pieces, goal) -  MIN_TOTAL_DISTANCE)

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
    piece_coords = piece.get_coords()

    # The division by 2 is to get the distance in hex coordinates
    return (abs(piece_coords[0] - goal_pos[0]) + abs(piece_coords[1] - goal_pos[1]) + abs(piece_coords[2] - goal_pos[2]))/ 2

def average_coordinates(coords):
    """ Return the average coordinates
    Args:
        coords (list): The coordinates
    """
    c1 = sum([coord[0] for coord in coords]) / len(coords)
    c2 = sum([coord[1] for coord in coords]) / len(coords)
    c3 = sum([coord[2] for coord in coords]) / len(coords)

    return (c1, c2, c3)