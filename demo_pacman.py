from pacman.board import Board, Candy
from pacman.game import Game
from pacman.tools import timeit


board = Board('boards/simple_board.txt')
game_speed = 0.00001
game = Game(board, game_speed)

# Add agents and candies to the game
game.add("PacMan", position=(5, 5))
game.add("Ghost", position=(0, 0))
game.add("Ghost", position=(0, 5))
game.add("Candy", position=(5, 3))

total_reward = game.play_game()
print('Game finished !\nTotal_reward : {reward}'.format(reward=total_reward))
