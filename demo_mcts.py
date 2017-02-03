from pacman.agents import Ghost, PacMan
from pacman.algorithms import MCTS
from pacman.board import Board
from pacman.game import Game

board = Board('boards/3x3_board.txt')
game_speed = 0.01
game = Game(board, game_speed, max_plays=10)

# Create agents and add them to game
game.add("PacMan", position=(0, 0))

mcts = MCTS(game)
mcts.train(train_time=10)
