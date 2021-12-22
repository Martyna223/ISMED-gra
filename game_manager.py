import sys
import re
from board import Board
import client


class GameManager:
    """
    A class controlling the course of the game of tic-tac-toe

    Imports
    ----------
        sys
        re
        Board
        client

    Attributes
    ----------
    board: Board
        represents a board for a game tic-tac-toe
    current_player: int
        stores information about which player has a turn
    id: int
        stores the player's identification number
    player_number: int
        number describing order in which player joined the server
    my_marker: str
        player marker x or o

    Methods:
    ----------
    marker_choice()
        gives a choice of x or o
    replay_choice()
        asks for a replay of the game
    tile_choice()
        asks for the field in which the user wants to put a marker
    set_player()
        assigns a marker to the player
    place_marker()
        places the appropriate marker on the board
    has_ended()
        checks if the game has finished
    generate_id()
        sets the player id
    play_game()
        controls the game
    """

    def __init__(self):
        """ sets default values

            :param board
            :param current_player: default None
            :param id: default 0000
            :param player_number: default 0
            :param my_marker:
        """

        self._board = Board()
        self._current_player = None
        self._id = 0000
        self._player_number = 0
        self._my_marker = ' '

    def marker_choice(self):
        """ asks for selection and sets the player marker
            if the selected marker is inappropriate, repeats the question

        :return: selected marker 'x' or 'o' in str format
        """

        while True:
            marker = input("Please choose your marker (x or o): ")
            if str(marker).isalpha() and len(marker) == 1:
                if marker.lower() == 'x' or marker.lower() == 'o':
                    return marker.lower()
            print("It's not a valid symbol.")

    def replay_choice(self):
        """asks for a replay of the game
           if the selected answer is inappropriate, repeats the question


        :return: True if player want to play again or False if not
        """
        while True:
            answer_play = input("Do you want to play again? (y or n): ")
            if str(answer_play).isalpha() and len(answer_play) == 1:
                if answer_play.lower() == 'y':
                    return True
                elif answer_play.lower() == 'n':
                    return False
                else:
                    print("It's not a valid symbol.")

    def tile_choice(self):
        """ asks for the field in which the user wants to put a marker
            if the selected field is not available or elected answer is inappropriate, repeats the question

        :return: number of the selected field in string format
        """

        while True:
            print("Current player: " + str(self._my_marker))
            tile_id = input("Please choose an unoccupied tile - from 1 to 9. ")
            num_format = re.compile(r'^[1-9]$')
            if re.match(num_format, tile_id):
                tile_id = int(tile_id) - 1
                if self._board.check_can_place(tile_id):
                    return tile_id
                else:
                    print("This tile is occupied.")
            else:
                print("It's not a valid symbol.")

    def set_player(self):
        """ assigns the selected marker to the player
            sends this information to the server by calling post_marker(my_marker) from class client
        """

        self._my_marker = self.marker_choice()
        client.post_marker(self._my_marker, self._id)

    def place_marker(self):
        """ sets the user marker in the selected place
            sends this information to the server by calling post_tile(my_marker) from class client
        """

        tile_id = self.tile_choice()
        marker = self._my_marker
        self._board.place(marker, tile_id)
        client.post_tile(tile_id, self._id)

    def has_ended(self):
        """ checks if the game has finished
            informs the user about the result of the game: win, lose, draw

        :return: False if the game is not over
        """

        if self._board.check_win():
            if self._id != client.get_current_player():
                print("Congratulations! You won!")
            else:
                print("You lost!")
            sys.exit(0)
        elif self._board.check_full():
            print("It's a draw!")
            sys.exit(0)
        return False

    def generate_id(self):
        """ allows the user to set an id
        """

        print("Please enter your id (must be an integer): ")
        while True:
            try:
                id = int(input())
                self._id = id
                break
            except ValueError:
                print("Id must be an integer, please enter a correct number: ")

    def play_game(self):
        """controls the game by calling methods form class Board, file client.py and self methods
        """

        print("Welcome to Tick-Tack-Toe!")
        self.generate_id()
        connection_response = client.post_connect(self._id)
        print(connection_response['prompt'])
        if connection_response['number'] == -1:
            sys.exit(0)
        self._player_number = connection_response['number']
        while True:
            if self._player_number == 1:
                self.set_player()
                client.post_board(self._id, self._board._state)
            elif self._player_number == 2:
                self._current_player = 1
                while True:
                    marker = client.get_second_player_marker()
                    if marker == 'x' or marker == 'o':
                        self._my_marker = marker
                        break
            elif self._player_number == 3:
                self._my_marker = client.get_first_player_marker()
                self._board._state = client.get_board()
                self._current_player = client.get_current_player()
                self._player_number == 1
            elif self._player_number == 4:
                self._my_marker = client.get_second_player_marker()
                self._board._state = client.get_board()
                self._current_player = client.get_current_player()
                self._player_number == 2
            while not self.has_ended():
                self._current_player = int(client.get_current_player())
                while self._current_player != self._id:
                    self._current_player = int(client.get_current_player())
                self._board.set_state(client.get_board())
                self._board.draw_from_state()
                if self.has_ended():
                    break
                self.place_marker()
                self._board.draw_from_state()
                client.post_board(self._id, self._board._state)
