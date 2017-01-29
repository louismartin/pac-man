from agents import Ghost, PacMan
from board import Board
from time import sleep
from tools import timeit


def play_games(board, game_steps, speed):
    game_reward = 0
    for step in range(game_steps):
        for agent in board.agents:
            agent.move()
            if (isinstance(agent, PacMan)):
                game_reward += agent.current_node.reward
                agent.current_node.reward = 0
        board_title = 'reward : ' + str(game_reward)
        board.draw_board(board_title)
        sleep(speed)

if __name__ == '__main__':
    new_board = Board('simple_board.txt')
    # Add pacman
    pac_man_init_node = new_board.board_nodes[(5, 5)]
    pac_man = PacMan(pac_man_init_node)

    # Add ghosts
    ghost1_init_node = new_board.board_nodes[(0, 0)]
    ghost1 = Ghost(ghost1_init_node)
    ghost2_init_node = new_board.board_nodes[(0, 5)]
    ghost2 = Ghost(ghost2_init_node)

    new_board.add_agent(pac_man)
    new_board.add_agent(ghost1)
    new_board.add_agent(ghost2)

    game_speed = 0
    nb_step = 100
    play_games(new_board, nb_step, game_speed)
