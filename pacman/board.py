import numpy as np

from pacman.agents import Ghost, PacMan


class Candy:
    def __init__(self, node, effect='blue'):
        self.node = node
        self.effect = effect


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
