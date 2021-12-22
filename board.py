class Board:
    """
    A class used to represent a Tic-tac-toe board

    Attributes
    ----------
    state: list[str]
        stores the status of all fields in the array
    drawn_board: str
        stores the current appearance of the board

    Methods:
    ----------
    _init_state()
        sets the default state value
    _init_drawn_board()
        sets the default drawn_board value
    reset()
        sets the state and drawn_board to the default value
    draw()
        displays board
    place(marker, tile_id)
        places a marker on the field selected by the user
    check_can_place(tile_id)
        checks if the selected field is allowed
    check_full()
        checks if there are still allowed fields in the board
     check_win()
        checks if there is a winning configuration on the board
    get_state()
        returns the state of the board
    set_state(state)
        sets the state of the board according to the given parameter
    draw_from_state()
        displays current board
    """

    def __init__(self):
        """ sets the default state and drawn_board values by calling _init_state and _init_drawn_board
        """

        self._state = self._init_state()
        self._drawn_board = self._init_drawn_board()

    def _init_state(self):
        """ initializes the 9-item list filled with '#'

        :return:
            a list of strings representing the markers on board
        """

        return ['#'] * 9

    def _init_drawn_board(self):
        """ initializes the default appearance of the board

        :return: the appearance of the board
        """

        return """
    ___________________
    |     |     |     |
    |  1  |  2  |  3  |
    |     |     |     |
    |-----------------|
    |     |     |     |
    |  4  |  5  |  6  |
    |     |     |     |
    |-----------------|
    |     |     |     |
    |  7  |  8  |  9  |
    |     |     |     |
    |-----------------|
    """

    def reset(self):
        """ resets state and board values by calling _init_state() and _init_drawn_board()
        """

        self._state = self._init_state()
        self._drawn_board = self._init_drawn_board()

    def draw(self):
        """ prints what the board looks like
        """

        print(self._drawn_board)

    def place(self, marker, tile_id):
        """ sets the state of the field according to the user's choice

        :param marker: 'x' or 'o'
        :param tile_id: field number selected by the user
        :return: True if the marker has been correctly placed or False if not
        """

        if self.check_can_place(tile_id):
            self._state[tile_id] = marker
            self._drawn_board = self._drawn_board.replace(str(tile_id+1), marker)
            return True, "Marker is placed."
        else:
            return False, "Cannot place marker."

    def check_can_place(self, tile_id):
        """ checks if the selected field is allowed

        :param tile_id: the number of the field to be checked
        :return: True if in selected field was '#'
        """
        return self._state[tile_id] == '#'

    def check_full(self):
        """ checks if all fields on the board are occupied

        :return: False if in state is min. 1 field filled '#'
        """

        return not any([tile == '#' for tile in self._state])

    def check_win(self):
        """ Checks all lines on the board for a winning configuration

        :return: True if the fields in the line are filled with the same marker or False if not
        """

        # horizontal check
        for i in range(0, 7, 3):
            if self._state[i] == self._state[i+1] == self._state[i+2] and self._state[i] != '#':
                return True
        # vertical check
        for i in range(0, 3, 1):
            if self._state[i] == self._state[i+3] == self._state[i+6] and self._state[i] != '#':
                return True
        # diagonal check
        if self._state[0] == self._state[4] == self._state[8] and self._state[0] != '#':
            return True
        if self._state[2] == self._state[4] == self._state[6] and self._state[2] != '#':
            return True
        return False

    def get_state(self):
        """ gets the state

        :return: a list of strings representing the markers on board
        """

        return self._state

    def set_state(self, state):
        """ sets the state of the board according to the given parameter

        :param state: list of values of board's tiles
        """

        self._state = state

    def draw_from_state(self):
        """ changes the player's selected fields from # to marker and displays board
        """
        for index, val in enumerate(self._state):
            if val != '#':
                self._drawn_board = self._drawn_board.replace(str(index + 1), val)
        self.draw()
