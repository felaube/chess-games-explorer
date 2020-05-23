import requests


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
