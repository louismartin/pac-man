from random import randint


class Agent:
    def __init__(self, current_node=None):
        self.current_node = current_node

    def get_move(self):
        children_nodes = self.current_node.children_nodes
        next_node = children_nodes[randint(0, len(children_nodes) - 1)]
        return next_node

    def move(self, node):
        self.current_node = node

    def get_position(self):
        return self.current_node.position


class Ghost(Agent):
    def __init__(self, current_node, blue=False):
        super().__init__(current_node)
        self.blue = blue
        self.eaten = False
        self.blue_time_left = 0

    def start_blue(self, blue_time_left=20):
        self.blue = True
        self.eaten = False
        self.blue_time_left = blue_time_left

    def stop_blue(self):
        self.blue = False
        self.eaten = False
        self.blue_time_left = 0


class PacMan(Agent):
    def __init__(self, current_node):
        super().__init__(current_node)
        self.reward = 0

    def eat_ghost(self, ghost, reward=10):
        ghost.eaten = True
        self.reward += reward