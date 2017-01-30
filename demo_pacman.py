from pacman.agents import Ghost, PacMan
from pacman.board import Board, Candy
from pacman.game import Game
from pacman.tools import timeit


board = Board('boards/simple_board.txt')
game_speed = 0.00001
game = Game(board, game_speed)

# Create agents and add them to game
pacman_init_node = board.nodes[(5, 5)]
pacman = PacMan(pacman_init_node)
game.add_pacman(pacman)

ghost1_init_node = board.nodes[(0, 0)]
ghost1 = Ghost(ghost1_init_node)
game.add_ghost(ghost1)

ghost2_init_node = board.nodes[(0, 5)]
ghost2 = Ghost(ghost2_init_node)
game.add_ghost(ghost2)

candy1_node = board.nodes[(5, 3)]
candy1 = Candy(candy1_node)
game.add_candy(candy1)

total_reward = game.play_game()
print('Game finished !\nTotal_reward : {reward}'.format(reward=total_reward))
