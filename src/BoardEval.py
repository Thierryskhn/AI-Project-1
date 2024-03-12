MAX_DISTANCE = 100 # TODO change this value
MIN_TOTAL_DISTANCE = 0 # TODO change this value

def eval(player, move):
    """ Return the score of a given move
    Args:
        move ((Board, (Piece, newCoords))): The board to evaluate
    """
    board = move[0]
    player_pieces = [piece for piece in board.pieces if piece.color == player.color]

    goal = average_coordinates(board.end_zones[player])

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

    c1 = abs(piece_coords[0] - goal_pos[0])
    c2 = abs(piece_coords[1] - goal_pos[1])
    c3 = abs(piece_coords[2] - goal_pos[2])

    return (c1 + c2 + c3) / 2 # The division by 2 is to get the distance in hex coordinates

def average_coordinates(coords):
    """ Return the average coordinates
    Args:
        coords (list): The coordinates
    """
    c1 = sum([coord[0] for coord in coords]) / len(coords)
    c2 = sum([coord[1] for coord in coords]) / len(coords)
    c3 = sum([coord[2] for coord in coords]) / len(coords)

    return (c1, c2, c3)