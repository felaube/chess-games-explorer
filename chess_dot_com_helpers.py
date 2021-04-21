import requests
import re
import time
import aiohttp
import asyncio


def get_chess_dot_com_moves_history(username, color, rating,
                                    time_class, time_control):
    """
    Construct the moves history from chess.com archives
    """

    archives_list = get_monthly_archives(username)

    if archives_list is not None:
        moves_history = {"next_moves": {}}

        start = time.time()
        games = asyncio.run(get_games_data(archives_list))
        end = time.time()
        print(f"Time elapsed to make all the"
              f" requests in archives_list: {end - start}")

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

        return moves_history

    else:
        return None


def get_monthly_archives(username):
    """
    Make a request to chess.com API to obtain a list
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
    m = re.search(r"\[Result \"(?P<result>[1, /, 2, 0]+-[1, /, 2, 0]+)\"]",
                  pgn)
    result = m.group("result")

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

    if white_to_move:
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


async def get_games_data(archives_list):

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(run_api_request(session, url))
                 for url in archives_list]

        games_per_archive = await asyncio.gather(*tasks)

    games = [game for games_list in games_per_archive for game in games_list]

    return games


async def run_api_request(session, url):

    async with session.get(url) as response:
        json_response = await response.json()
        games = json_response["games"]

        # Sleep to avoid 429 error (too many requests)
        await asyncio.sleep(4)

        return games
