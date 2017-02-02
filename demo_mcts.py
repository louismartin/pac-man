from pacman.agents import Ghost, PacMan
from pacman.algorithms import MCTS
from pacman.board import Board
from pacman.game import Game

board = Board('boards/3x3_board.txt')
game_speed = 0.1
game = Game(board, game_speed)

# Create agents and add them to game
pacman_init_node = board.nodes[(0, 0)]
pacman = PacMan(pacman_init_node)
game.add_pacman(pacman)

mcts = MCTS(game)
mcts.train(train_time=10)
