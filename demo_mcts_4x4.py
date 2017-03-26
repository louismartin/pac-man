from pacman.agents import Ghost, PacMan
from pacman.algorithms import MCTS
from pacman.board import Board
from pacman.game import Game

board = Board('boards/4x4_board.txt')
game_speed = 0.01
game = Game(board, game_speed, max_plays=100, state_type="features")

# Create agents and add them to game
game.add("PacMan", position=(0, 0))
game.add("Ghost", position=(3, 3))

mcts = MCTS(game, verbose=False)
mcts.train(train_time=60, display_interval=500)
