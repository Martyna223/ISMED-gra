import requests
import json

"""
    Imports
    -------
    requests
    json

"""


def post_data(d):
    """ sends data to the server

    :param d: data to be transmitted
    :return: response received from server
    """

    d = json.dumps(d)
    response = requests.post("http://127.0.0.1:5000/api/setdata", data=d,
                             headers={'content-type': 'application/json'})

    return response.json()


def post_connect(id):
    """ sends request to server that contains id

    :param id: client id number
    :return: response received from server
    """

    data = {
        'i_am_here': True,
        'id': id,
    }
    return post_data(data)


def post_board(id, board):
    """ sends player board to the server

    :param id: id number of the client sending the information to the server
    :param board: current game board
    :return: response received from server
    """

    data = {
        'current_board': board,
        'id': id,
    }
    return post_data(data)


def post_marker(marker, id):
    """ sends information about player marker to the server

    :param marker: player marker 'x' or 'o'
    :param id: id number of the client sending the information to the server
    :return: response received from server
    """

    data = {
        'marker': marker,
        'id': id,
    }
    return post_data(data)


def post_tile(tile_id, id):
    """Sends to the server the number of the field occupied by the client on the board

    :param tile_id: field number on the board
    :param id: id number of the client sending the information to the server
    :return: response received from server
    """

    data = {
        'tile_id': tile_id,
        'id': id,
    }
    return post_data(data)


def get_board():
    """ gets the current board from the server

    :return: board with the current state of the game
    """

    response = requests.get("http://127.0.0.1:5000/api/getdata/board")
    return response.json()


def get_second_player_marker():
    """gets the second player marker based on the first player's selection from the server

    :return: second player marker 'x' or 'o'
    """

    response = requests.get("http://127.0.0.1:5000/api/getdata/ndplayer_mark")
    return response.json()


def get_first_player_marker():
    """gets the first player marker from the server

    :return: first player marker 'x' or 'o'
    """

    response = requests.get("http://127.0.0.1:5000/api/getdata/stplayer_mark")
    return response.json()


def get_current_player():
    """ gets information about which player has the turn from the server

    :return: player who has a turn
    """

    response = requests.get("http://127.0.0.1:5000/api/getdata/current_player")
    return response.json()
