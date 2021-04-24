"""
Implement the functions used when the user
chooses either platform (Chess.com or Lichess)
"""
from collections import OrderedDict


def calculate_percentages(moves_dict):
    """
    Calculate the winning, losing and drawing percentages
    of each position in moves_dict
    """

    for move in moves_dict["next_moves"]:

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
    """
    Order the moves dictionary by the number of times
    the position was reached.
    E.g. the position 1.e4 was reached in 500 games, and
    the position 1.d4 was reached in 200 games, so, the first position
    in moves_dict will be 1.e4 and the second will be 1.d4
    """

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


def increment_move_in_moves_dict(moves_dict, move, result):
    """
    Add the information to the moves dictonary that the 'move'",
    found previously in some game, was reached again in another game.
    """
    moves_dict["next_moves"][move]["count"] += 1

    if result == 1:
        moves_dict["next_moves"][move]["white_wins"] += 1
    elif result == 0:
        moves_dict["next_moves"][move]["black_wins"] += 1


def create_move_in_moves_dict(moves_dict, move, result):
    """
    Add the information to the moves dictonary that a new 'move',
    never found previously in a game, was reached in the current analyzed game.
    """
    if result == 1:
        move_info = {"count": 1, "white_wins": 1, "black_wins": 0, "next_moves": {}}
    elif result == 0:
        move_info = {"count": 1, "white_wins": 0, "black_wins": 1, "next_moves": {}}
    else:
        move_info = {"count": 1, "white_wins": 0, "black_wins": 0, "next_moves": {}}

    moves_dict["next_moves"][move] = move_info
