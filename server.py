from flask import Flask, json, request

app = Flask(__name__)

"""
    Imports
    ----------
    Flask, json, request
    
    Data
    ----------
    players: dict
        a dictionary that stores id players
    markers: dict
        a dictionary that stores players markers
    board: list
        a list that stores players' moves
    current_player: int
        stores the id of the player who currently has a turn
    current_tile: int
        stores the id of the tile that was last selected by the player
"""

players = {"player1": None, "player2": None}
markers = {}
board = []
current_player = None
current_tile = 0

@app.route("/")
def homepage():
    """ displays "Tic-tac-toe" on the server

    :return:
    """

    return "<html><body>Tic-tac-toe</body></html>"  # tu jest to co sie wyswietla dla uzytkownika


@app.route("/api/getdata/tile_id", methods=['GET'])
def get_tiles():
    """ gets the id of the tile selected by the client

    :return: id of the tile that was last selected by the player, number that indicates the request has succeeded
    """

    return current_tile, 200

@app.route("/api/getdata/board", methods=['GET'])
def get_board():
    """ sends the board to the client

    :return: board, number that indicates the request has succeeded
    """

    return json.dumps(board), 200

@app.route("/api/getdata/ndplayer_mark", methods=['GET'])
def get_second_player_marker():
    """ sends the second player marker to the client

    :return: marker of second player 'x' or 'o',  number that indicates the request has succeeded
    """

    if players['player1'] not in markers:
        return {}, 200
    markers[players['player2']] = 'o' if markers[players['player1']] == 'x' else 'x'
    return json.dumps(markers[players['player2']]), 200


@app.route("/api/getdata/stplayer_mark", methods=['GET'])
def get_first_player_marker():
    """ sends the first player marker to the client

    :return: marker of first player 'x' or 'o', number that indicates the request has succeeded
    """

    markers[players['player1']] = 'o' if markers[players['player2']] == 'x' else 'x'
    return json.dumps(markers[players['player1']]), 200

@app.route("/api/getdata/current_player", methods=['GET'])
def get_current_player():
    """ sends information about the id of the player who has a turn

    :return: current player id, number that indicates the request has succeeded
    """

    global current_player
    return str(current_player), 200


@app.route("/api/setdata", methods=['POST'])
def setdata():
    """ receives data from the customer
        recognizes and sets data according to the key

    :return: response, number that indicates that request has succeeded and a new resource has been created as a result
    """

    data = request.get_json()
    response = None
    status = 201
    if data is not None:
        if 'i_am_here' in data:
            response = set_connect(data)

        elif 'marker' in data:
            response = set_marker(data)

        elif 'current_board' in data:
            response = set_board(data)

        elif 'tile_id' in data:
            response = set_tile(data)

    return response, status


def set_connect(data):
    """ connects the client to the server by id number

    :param data: client id
    :return: dictionary with communicate to client and number describing order in which player joined the server
    """

    global current_player
    if players['player1'] is None:
        players['player1'] = data['id']
        current_player = players['player1']
        return {"prompt": "You're player 1!", "number": 1}
    elif players['player2'] is None:
        players['player2'] = data['id']
        return {"prompt": "You're player 2!", "number": 2}
    elif players['player1'] == data['id']:
        return {"prompt": "Player 1, welcome back!", "number": 3}
    elif players['player2'] == data['id']:
        return {"prompt": "Player 2, welcome back!", "number": 4}
    else:
        return {"prompt": "There already is a maximum number of players.", "number": -1}


def set_marker(data):
    """ gets information from the client which marker the first player chose
        sets chosen marker

    :param data: player marker 'x' or 'o'
    :return: empty dict
    """

    if players['player1'] == data['id']:
        markers[players['player1']] = data['marker']
        return {}


def set_tile(data):
    """ gets information from the client about chosen tile
        sets current tile id

    :param data: chosen tile id
    :return: empty dict
    """

    global current_tile
    current_tile = data['tile_id']
    switch_player()
    return {}


def set_board(data):
    """ gets boards from the client
        set current board

    :param data: the board to be set
    :return: empty dict
    """

    global board
    board = data['current_board']
    return {}


def switch_player():
    """ changes the player who has a turn
    """

    global current_player
    current_player = players['player2'] if current_player == players['player1'] else players['player1']

@app.route("/api/clear", methods=['POST'])
def reset_server():
    """ resets server to default values

    :return: empty dict, number that indicates that request has succeeded and a new resource has been created as a result
    """
    global players, markers, board, current_player, current_tile
    request.get_json()
    players = {"player1": None, "player2": None}
    markers = {}
    board = []
    current_player = None
    current_tile = 0

    return {}, 201



if __name__ == "__main__":
    app.run()

