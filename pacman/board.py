import numpy as np


class Candy:
    def __init__(self, node, effect='blue'):
        self.node = node
        self.effect = effect


class Node:
    def __init__(self, position, children_nodes=None):
        self.position = position
        if (children_nodes is None):
            self.children_nodes = []
        else:
            self.children_nodes = children_nodes

    @staticmethod
    def relative_position(node_1, node_2):
        """
        Example: node_1.position = (4, 3), node_1.position = (5, 3)
        relative_position = (1, 0)
        """
        relative_position = (
            node_2.position[0] - node_1.position[0],
            node_2.position[1] - node_1.position[1]
        )
        return relative_position

    def __str__(self):
        string = 'Position: {pos} - Children: {children}'.format(
            pos=self.position,
            children=[child.position for child in self.children_nodes]
        )
        return string

    def __repr__(self):
        return self.__str__()


class Board:
    def __init__(self, board_path):
        nodes, outline = self.build_board(board_path)
        self.nodes = nodes
        self.outline = outline

    def build_board(self, board_path):
        outline = []
        with open(board_path) as f:
            for line in f:
                outline.append([int(char) for char in line.strip()])
        outline = np.array(outline)
        nb_row, nb_column = outline.shape

        nodes = {}
        # Create nodes
        for row in range(nb_row):
            for col in range(nb_column):
                if(outline[row, col] == 1):
                    new_position = (row, col)
                    new_node = Node(new_position)
                    nodes[new_position] = new_node
        # Link nodes to children
        for position, current_node in nodes.items():
            children = []
            row = position[0]
            col = position[1]
            if (row > 0 and (row - 1, col) in nodes.keys()):
                children.append(nodes[(row - 1, col)])
            if (row < nb_row and (row + 1, col) in nodes.keys()):
                children.append(nodes[(row + 1, col)])
            if (col > 0 and (row, col - 1) in nodes.keys()):
                children.append(nodes[(row, col - 1)])
            if (col < nb_column and
                    (row, col + 1) in nodes.keys()):
                children.append(nodes[(row, col + 1)])
            current_node.children_nodes = children
        return nodes, outline
