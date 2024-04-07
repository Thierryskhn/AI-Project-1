from itertools import combinations

WINNING_PIECE_BONUS = 10 # The bonus for a piece in the end zone

CLOSE_PIECES_THRESHOLD = 4 # The maximum distance between two pieces to be considered close
CLOSE_PIECES_MAX_SCORE = 25 # The maximum score for the packed pieces score, knowing that there are 45 pairs per player

MAX_TOTAL_DISTANCE = 140 # These values were found by testing all positions
MIN_TOTAL_DISTANCE = 20
MAX_DISTANCE_SCORE = MAX_TOTAL_DISTANCE - MIN_TOTAL_DISTANCE

ALREADY_PLAYED_PENALTY = 0.2 # Penalty for playing a move that was already played recently

def eval(player, state, find_constant=False):
    """ Evalution function based on the distance to the goal
    Args:
        player (Player): The player to evaluate
        state (Board): The state to evaluate
        find_constant (bool): If True, find the constants and exit
    """
    if find_constant == True:
        find_constants(player, state)

    player_pieces = [piece for piece in state.pieces if piece.color == player.color]
    
    goal = max_coordinates(state.end_zones[player])

    distance_score = MAX_DISTANCE_SCORE - (sum_distance_to_goal(player_pieces, goal) -  MIN_TOTAL_DISTANCE)
    winning_piece_bonus = compute_winning_piece_bonus(player, state, player_pieces)
    packed_pieces_score = compute_packed_pieces_score(player_pieces)
    
    score = distance_score + winning_piece_bonus + packed_pieces_score
    
    if player.saves_moves and build_recently_played_elem(player, state) in player.recently_played:
        score *= (1 - ALREADY_PLAYED_PENALTY)

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
        if abs(coord[0]) + abs(coord[1]) + abs(coord[2]) >= abs(max_coord[0]) + abs(max_coord[1]) + abs(max_coord[2]):
            max_coord = coord
    return max_coord

def compute_winning_piece_bonus(player, state, player_pieces):
    """ Compute the winning piece bonus (if the piece is in the end zone)
    Args:
        player (Player): The player to evaluate
        state (Board): The board
        player_pieces (list): The pieces
    """
    winning_piece_bonus = 0
    for piece in player_pieces:
        if piece.coords in state.end_zones[player]:
            winning_piece_bonus += WINNING_PIECE_BONUS
    return winning_piece_bonus

def compute_packed_pieces_score(player_pieces):
    """ Compute the packed pieces score (if the pieces are close to each other)
    Args:
        player_pieces (list): The pieces
    """
    packed_pieces_score = 0

    pairs = set(combinations(player_pieces, 2))
    for comb in pairs:
        if distance_to_goal(comb[0], comb[1].coords) <= CLOSE_PIECES_THRESHOLD:
            packed_pieces_score += 1

    return packed_pieces_score / len(pairs) * CLOSE_PIECES_MAX_SCORE

def build_recently_played_elem(player, board):
    """ Build the set to add to the recently_played list 
        The set contains the coordinates of the player's pieces, not saving the opponent's pieces
        or what piece is in each position
    """
    return set(p.coords for p in board.pieces if p.color == player.color)

def find_constants(player, state):
    """ Find the constants for the evaluation function
    Args:
        player (Player): The player to evaluate
        state (Board): The state to evaluate
    """
    min_goal = max_coordinates(state.start_zones[player])
    max_goal = max_coordinates(state.end_zones[player])

    print()
    print("Constants found :")
    print("MAX_TOTAL_DISTANCE", find_max_total_distance(player, state, max_goal))
    print("MIN_TOTAL_DISTANCE", find_min_total_distance(player, state, min_goal))
    print()

    exit()

def find_max_total_distance(player, state, goal):
    """ Find the max total distance to the goal (used to get the correct values for the constants)
    Args:
        player (Player): The player to evaluate
        state (Board): The state to evaluate
        goal (tuple): The goal position
    """
    b = state.copy()

    dist = []
    piece = [p for p in b.pieces if p.color == player.color][0]
    coords = [p for zo in b.coordinates for p in zo if p != None]
    for pos in coords:
        piece.coords = pos
        if len(dist) < 10:
            dist.append(distance_to_goal(piece, goal))
        elif distance_to_goal(piece, goal) > min(dist):
            dist[dist.index(min(dist))] = distance_to_goal(piece, goal)
    return sum(dist)

def find_min_total_distance(player, state, goal):
    """ Find the min total distance to the goal (used to get the correct values for the constants)
    Args:
        player (Player): The player to evaluate
        state (Board): The state to evaluate
        goal (tuple): The goal position
    """
    b = state.copy()
    
    dist = []
    piece = [p for p in b.pieces if p.color == player.color][0]
    coords = [p for zo in b.coordinates for p in zo if p != None]
    for pos in coords:
        piece.coords = pos
        if len(dist) < 10:
            dist.append(distance_to_goal(piece, goal))
        elif distance_to_goal(piece, goal) < max(dist):
            dist[dist.index(max(dist))] = distance_to_goal(piece, goal)
    return sum(dist)
