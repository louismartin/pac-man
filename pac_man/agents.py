from random import randint


class Agent:
    def __init__(self, current_node=None):
        self.current_node = current_node

    def move(self):
        children_nodes = self.current_node.children_nodes
        self.current_node = children_nodes[randint(0, len(children_nodes) - 1)]


class Ghost(Agent):
    def __init__(self, current_node, killable=False):
        super().__init__(current_node)
        self.killable = killable


class PacMan(Agent):
    def __init_(self, current_node):
        super().__init__(heigt)
