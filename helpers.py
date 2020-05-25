import requests
import re
from collections import OrderedDict


def get_archives_list(username):
    """
    Get a list of all monthly archives available for the player
    """

    # Get array of monthly archives available for this player
    try:
        response = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives")
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        archives = response.json()
        return archives["archives"]
    except (KeyError, TypeError, ValueError):
        return None


def parse_pgn(moves_dict, pgn, current_move=1):
    """
    Parse PGN file saving the moves in the moves dictionary
    """

    current_dict = moves_dict
    white_move = True

    # Get result of the game to calculate the winning percentage later
    m = re.search(r"\[Result \"(?P<result>[1, /, 2, 0]+-[1, /, 2, 0]+)\"]", pgn)
    result = m.group("result")

    if result == "1-0":
        result = 1
    elif result == "0-1":
        result = 0
    else:
        # It was a draw
        result = 0.5

    # Parse one move at a time iteratively
    while True:
        current_dict = parse_move(current_dict, pgn, current_move, white_move, result)

        if current_dict is not None:
            # Update current move and white/black move variable
            if not white_move:
                current_move += 1

            white_move = not white_move

        else:
            break


def parse_move(moves_dict, pgn, current_move, white_move, result):

    if white_move:
        # Find current move by white
        m = re.search(str(current_move)+r"\. (?P<move>[a-z, A-Z, 1-9, +, #, =, -]+) {", pgn)
    else:
        # Find current move by black
        m = re.search(str(current_move)+r"\.\.\. (?P<move>[a-z, A-Z, 1-9, +, #, =, -]+) {", pgn)

    # Check if a move was played in this position
    if m is not None:
        move = m.group("move")

        if move in moves_dict["next_moves"]:
            moves_dict["next_moves"][move]["count"] += 1
            if result == 1:
                moves_dict["next_moves"][move]["white_wins"] += 1
            elif result == 0:
                moves_dict["next_moves"][move]["black_wins"] += 1
        else:
            if result == 1:
                moves_dict["next_moves"][move] = {"count": 1, "white_wins": 1, "black_wins": 0, "next_moves": {}}
            elif result == 0:
                moves_dict["next_moves"][move] = {"count": 1, "white_wins": 0, "black_wins": 1, "next_moves": {}}
            else:
                moves_dict["next_moves"][move] = {"count": 1, "white_wins": 0, "black_wins": 0, "next_moves": {}}

        return moves_dict["next_moves"][move]

    else:
        # No move was played in this position - the game ended here
        return None


def calculate_percentages(moves_dict):
    for move in moves_dict["next_moves"]:
        # Declare aux_dict only to shorten lines
        aux_dict = moves_dict["next_moves"][move]

        aux_dict["white_percentage"] = round(aux_dict["white_wins"] /
                                             aux_dict["count"]*100)

        aux_dict["black_percentage"] = round(aux_dict["black_wins"] /
                                             aux_dict["count"]*100)

        aux_dict["draw_percentage"] = 100 - (aux_dict["white_percentage"] +
                                             aux_dict["black_percentage"])

        # Iterate recursively through all positions
        calculate_percentages(aux_dict)


def order_dict(moves_dict):
    # Initialize ordered dictionary
    new_dict = OrderedDict()

    # Check if this is the first lement of the dictionary,
    # which has only the "next_moves" key
    if len(moves_dict) != 1:
        # Copy all information into the new dictionary
        new_dict["count"] = moves_dict["count"]
        new_dict["white_wins"] = moves_dict["white_wins"]
        new_dict["black_wins"] = moves_dict["black_wins"]
        new_dict["white_percentage"] = moves_dict["white_percentage"]
        new_dict["black_percentage"] = moves_dict["black_percentage"]
        new_dict["draw_percentage"] = moves_dict["draw_percentage"]

    new_dict["next_moves"] = OrderedDict()

    # Iterate through all moves to order everything
    for move in moves_dict["next_moves"]:
        moves_dict["next_moves"][move] = order_dict(moves_dict["next_moves"][move])

    # Initialize the variable which holds the move
    # with the largest count
    aux_move = {"move": "", "count": 0}
    for _ in range(len(moves_dict["next_moves"])):
        for move in moves_dict["next_moves"]:
            # Check if the count of the current move is larger than
            # the count of the aux variable
            if moves_dict["next_moves"][move]["count"] > aux_move["count"]:
                aux_move["move"] = move
                aux_move["count"] = moves_dict["next_moves"][move]["count"]

        # Copy the "move" dictionary into the "next_moves" key of the new dictionary
        new_dict["next_moves"][aux_move["move"]] = moves_dict["next_moves"][aux_move["move"]].copy()
        # Set the "count" of this move to 0, to get the next largest count value
        moves_dict["next_moves"][aux_move["move"]]["count"] = 0
        # Reset aux_move
        aux_move = {"move": "", "count": 0}

    # Return the ordered dictionary
    return new_dict
