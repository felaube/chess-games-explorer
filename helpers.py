import requests
import re


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

    while True:
        current_dict = parse_move(current_dict, pgn, current_move, white_move)

        if current_dict is not None:
            if not white_move:
                current_move += 1

            white_move = not white_move

        else:
            break


def parse_move(moves_dict, pgn, current_move, white_move):

    if white_move:
        # Find current move by white
        m = re.search(str(current_move)+r"\. [a-z, A-Z, 1-9, +, #, =, -]+ {", pgn)
    else:
        # Find current move by black
        m = re.search(str(current_move)+r"\.\.\. [a-z, A-Z, 1-9, +, #, =, -]+ {", pgn)

    # Check if a move was played in this position
    if m is not None:
        if white_move:
            move = m.group(0)[len(str(current_move)) + 2:-2]
        else:
            move = m.group(0)[len(str(current_move)) + 4:-2]

        if move in moves_dict:
            moves_dict[move]["count"] += 1
        else:
            moves_dict[move] = {"count": 1}

        return moves_dict[move]

    else:
        return None
