"""
Implement the functions responsible for handling the Chess.com API requests
and building the moves history obtained from those requests.
"""
import re
import requests
from helpers import increment_move_in_moves_dict, create_move_in_moves_dict


# Define regex pattern used multiple times
RESULT_REGEX_PATTERN = r"\[Result \"(?P<result>[1, /, 2, 0]+-[1, /, 2, 0]+)\"]"
WHITE_MOVE_REGEX_PATTERN = r"\. (?P<move>[a-z, A-Z, 1-9, +, #, =, -]+) {"
BLACK_MOVE_REGEX_PATTERN = r"\.\.\. (?P<move>[a-z, A-Z, 1-9, +, #, =, -]+) {"


def get_chess_dot_com_moves_history(username: str, color: str, rating: int,
                                    time_class: str, time_control: str):
    """
    Construct the moves history from chess.com archives
    """

    archives_list = get_monthly_archives(username)

    if archives_list is not None:
        moves_history = {"next_moves": {}}
        with requests.Session() as session:
            games = []
            for url in archives_list:
                response = session.get(url)
                response = response.json()

                # games = response["games"]
                games.extend(response["games"])

            filtered_games = (game for game in games
                                if is_filter_satisfied(game, username,
                                                       color, rating,
                                                       time_class, time_control))

            for game in filtered_games:
                # Parse each game from the archive
                try:
                    pgn = game["pgn"]

                    parse_pgn(moves_history, pgn)
                except KeyError:
                    pass
        return moves_history

    return None


def is_filter_satisfied(game, username, color, rating, time_class, time_control):
    """
    Returns True if all filtering conditions are satisfied,
    returns False otherwise
    """
    # Filter chess variations
    if game["rules"] == "chess":
        # Filter by color
        if game[color]["username"] == username:
            # Filter by rating
            if rating:
                if int(game[color]["rating"]) < rating:
                    return False

            # Filter by time class
            if time_class:
                if game["time_class"] != time_class:
                    return False

            # Filter by time control
            if time_control:
                if game["time_control"] != time_control:
                    return False

            return True

    return False


def get_monthly_archives(username):
    """
    Make a request to chess.com API to obtain a structure
    containing the list of monthly archives available for the player.

    The monthly archive is a url to which an API request must be made
    to get the games played in that month.
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
    white_to_move = True

    # Get result of the game to calculate the winning percentage later
    result_search = re.search(RESULT_REGEX_PATTERN, pgn)
    result = result_search.group("result")

    if result == "1-0":
        result = 1
    elif result == "0-1":
        result = 0
    else:
        # It was a draw
        result = 0.5

    # Parse one move at a time, iteratively
    while True:
        current_dict = parse_move(current_dict, pgn, current_move,
                                  white_to_move, result)

        if current_dict is not None:
            # Update current move and white/black move variable
            if not white_to_move:
                current_move += 1

            white_to_move = not white_to_move

        else:
            break


def parse_move(moves_dict, pgn, current_move, white_to_move, result):
    """
    Find the move given by current_move in the pgn,
    parse it and add it to the moves dictionary
    """

    if white_to_move:
        # Find current move by white
        move_search = re.search(str(current_move) + WHITE_MOVE_REGEX_PATTERN, pgn)
    else:
        # Find current move by black
        move_search = re.search(str(current_move) + BLACK_MOVE_REGEX_PATTERN, pgn)

    # Check if a move was played in this position
    if move_search is not None:
        move = move_search.group("move")

        if move in moves_dict["next_moves"]:
            increment_move_in_moves_dict(moves_dict, move, result)
        else:
            create_move_in_moves_dict(moves_dict, move, result)

        return moves_dict["next_moves"][move]

    # No move was played in this position - the game ended here
    return None
