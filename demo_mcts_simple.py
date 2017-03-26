from matplotlib import pyplot as plt
import numpy as np

from pacman.agents import Ghost, PacMan
from pacman.algorithms import MCTS
from pacman.board import Board
from pacman.game import Game

board = Board('boards/simple_board.txt')
game_speed = 0.01
game = Game(board, game_speed, max_plays=np.inf, final_reward=100)

# Create agents and add them to game
game.add("PacMan", position=(0, 0))
game.add("Ghost", position=(5, 10))

mcts = MCTS(game, verbose=False)
mcts.train(train_time=1000, display_interval=1000,
           discount_factor=0.98)
