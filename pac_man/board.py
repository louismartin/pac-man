from agents import Ghost, PacMan
from matplotlib import pyplot as plt
import numpy as np
from tools import timeit


class OutsideOfLegalPath(Exception):
    pass


class Node:
    def __init__(self, position, children_nodes=None, reward=1):
        self.position = position
        self.reward = reward
        if (children_nodes is None):
            self.children_nodes = []
        else:
            self.children_nodes = children_nodes

    def __str__(self):
        return ' position : {pos} \n children nb : {nb_children} \n'.format(
            nb_children=len(self.children_nodes), pos=self.position)


class Board:
    def __init__(self, board_path):
        self.agents = []
        board_nodes, board_outline = self.build_board(board_path)
        self.board_nodes = board_nodes
        self.board_outline = board_outline

    def build_board(self, board_path):
        board_outline = []
        with open(board_path) as f:
            for line in f:
                board_outline.append([int(char) for char in line.strip()])
        board_outline = np.array(board_outline)
        nb_board_row, nb_board_column = board_outline.shape

        board_nodes = {}
        # Create nodes
        for row in range(nb_board_row):
            for col in range(nb_board_column):
                if(board_outline[row, col] == 1):
                    new_position = (row, col)
                    new_node = Node(new_position)
                    board_nodes[new_position] = new_node
        # Link nodes to children
        for position, current_node in board_nodes.items():
            children = []
            row = position[0]
            col = position[1]
            if (row > 0 and (row - 1, col) in board_nodes.keys()):
                children.append(board_nodes[(row - 1, col)])
            if (row < nb_board_row and (row + 1, col) in board_nodes.keys()):
                children.append(board_nodes[(row + 1, col)])
            if (col > 0 and (row, col - 1) in board_nodes.keys()):
                children.append(board_nodes[(row, col - 1)])
            if (col < nb_board_column and
                    (row, col + 1) in board_nodes.keys()):
                children.append(board_nodes[(row, col + 1)])
            current_node.children_nodes = children
        return board_nodes, board_outline

    def add_agent(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board_nodes):
            target_node = self.board_nodes[agent.current_node.position]
            self.agents.append(agent)
        else:
            raise OutsideOfLegalPath("Cannot add agent\
                to invalid board position")

    def compute_board(self):
        current_board = self.board_outline.copy()
        for position, node in self.board_nodes.items():
            if (node.reward > 0):
                current_board[node.position[0], node.position[1]] = 4
        for agent in self.agents:
            agent_row = agent.current_node.position[0]
            agent_col = agent.current_node.position[1]
            if (isinstance(agent, PacMan)):
                current_board[agent_row, agent_col] = 2
            if (isinstance(agent, Ghost)):
                current_board[agent_row, agent_col] = 3
        return current_board

    @timeit
    def draw_board(self, title):
        current_board = self.compute_board()
        # plt.figure(1)
        plt.matshow(current_board, fignum=0)
        plt.title(title)
        plt.draw()
        plt.show(block=False)
        plt.clf()

    def __str__(self):
        return str(self.compute_board())
