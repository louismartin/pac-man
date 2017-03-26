from matplotlib import pyplot as plt
import numpy as np

from pacman.agents import Ghost, PacMan
from pacman.algorithms import MCTS
from pacman.board import Board
from pacman.game import Game

board = Board('boards/3x3_board.txt')
game_speed = 0.01
game = Game(board, game_speed, max_plays=100,
            final_reward=0, state_type="board")

# Create agents and add them to game
game.add("PacMan", position=(0, 0))

mcts = MCTS(game, verbose=False)
mcts.train(train_time=10, display_interval=100,
           discount_factor=0.8)
