from game_manager import GameManager
from board import Board
import server

if __name__ == "__main__":
    help(server)
    tictactoe_game = GameManager()
    tictactoe_game.play_game()
