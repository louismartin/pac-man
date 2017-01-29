from time import sleep

from matplotlib import pyplot as plt
from tqdm import tqdm

from pacman.tools import timeit


class Game:
    def __init__(self, board, speed, pac_man_agent=None, ghost_agents=None):
        self.board = board
        self.pac_man = pac_man_agent
        self.speed = speed
        if (not ghost_agents):
            self.ghosts = []
        else:
            self.ghosts = ghost_agents

    def add_pac_man(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.board_nodes):
            target_node = self.board.board_nodes[agent.current_node.position]
            self.pac_man = agent
        else:
            raise OutsideOfLegalPath("Cannot add agent\
                to invalid board position")

    def add_ghost(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.board_nodes):
            target_node = self.board.board_nodes[agent.current_node.position]
            self.ghosts.append(agent)
        else:
            raise OutsideOfLegalPath("Cannot add agent\
                to invalid board position")

    def play_game(self, game_steps):
        game_reward = 0
        for step in tqdm(range(game_steps)):
            self.pac_man.move()
            game_reward += self.pac_man.current_node.reward
            self.pac_man.current_node.reward = 0
            for ghost in self.ghosts:
                ghost.move()

            board_title = 'reward : ' + str(game_reward)
            self.draw_state(board_title)
            sleep(self.speed)

    def compute_state(self):
        current_board = self.board.board_outline.copy()
        for position, node in self.board.board_nodes.items():
            if (node.reward > 0):
                current_board[node.position[0], node.position[1]] = 4
        for ghost in self.ghosts:
            row, col = ghost.get_position()
            current_board[row, col] = 3
        pac_man_row, pac_man_col = self.pac_man.get_position()
        current_board[pac_man_row, pac_man_col] = 2
        return current_board

    def draw_state(self, title):
        current_board = self.compute_state()
        # plt.figure(1)
        plt.matshow(current_board, fignum=0)
        plt.title(title)
        plt.draw()
        plt.show(block=False)
        plt.clf()

    def __str__(self):
        return str(self.compute_state())
