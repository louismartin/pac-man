from time import sleep

from tools import timeit

from agents import Ghost, PacMan
from board import Board
from game import Game


if __name__ == '__main__':
    new_board = Board('simple_board.txt')
    game_speed = 0
    new_game = Game(new_board, game_speed)
    # Create agents
    pac_man_init_node = new_board.board_nodes[(5, 5)]
    pac_man = PacMan(pac_man_init_node)

    ghost1_init_node = new_board.board_nodes[(0, 0)]
    ghost1 = Ghost(ghost1_init_node)
    ghost2_init_node = new_board.board_nodes[(0, 5)]
    ghost2 = Ghost(ghost2_init_node)

    # Add agents to game
    new_game.add_pac_man(pac_man)
    new_game.add_ghost(ghost1)
    new_game.add_ghost(ghost2)

    nb_step = 100
    new_game.play_game(nb_step)
