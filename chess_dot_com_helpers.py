import requests
import re
import time


def get_chess_dot_com_moves_history(username, color, rating, time_class, time_control):
    """
    Construct the moves history from chess dot com archives
    """
    start = time.time()
    archives_list = get_archives(username)
    end = time.time()
    print(f"Time spent to get the archives_list: {end - start}")

    if archives_list is not None:
        acumulated_time = 0
        moves_history = {"next_moves": {}}
        for url in archives_list:
            start = time.time()
            response = requests.get(url)
            end = time.time()

            acumulated_time = acumulated_time + end - start

            response = response.json()

            games = response["games"]

            for game in games:

                # Don't consider chess variations
                # other than the classical one
                if game["rules"] == "chess":

                    # Apply filters
                    # Filter by color
                    if game[color]["username"] == username:

                        # Filter by rating
                        if rating:
                            if int(game[color]["rating"]) < int(rating):
                                continue

                        # Filter by time class
                        if time_class:
                            if game["time_class"] != time_class:
                                continue

                        # Filter by time control
                        if time_control:
                            if game["time_control"] != time_control:
                                continue

                        # Parse each game from the archive
                        try:
                            pgn = game["pgn"]

                            parse_pgn(moves_history, pgn)
                        except KeyError:
                            pass

        print(f"Time elapsed to make all the requests in archives_list: {acumulated_time}")
        
        return moves_history

    else:

        return None


def get_archives(username):
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
