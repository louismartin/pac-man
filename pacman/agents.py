from random import randint

from pacman.board import Node, Action, InvalidPosition


class Agent:
    def __init__(self, node):
        self.current_node = node

    # TODO: Replace all current_node.position with position
    @property
    def position(self):
        return self.current_node.position

    def get_action(self):
        children_nodes = self.current_node.children_nodes
        next_node = children_nodes[randint(0, len(children_nodes) - 1)]
        action_value = Node.relative_position(self.current_node, next_node)
        return Action(action_value)

    def move(self, action):
        next_position = (self.position[0] + action.value[0],
                         self.position[1] + action.value[1])

        # Find the node corresponding to next_position
        next_node = None
        for child_node in self.current_node.children_nodes:
            if child_node.position == next_position:
                next_node = child_node
                break

        # Check if we found the next node
        if next_node:
            self.current_node = next_node
        else:
            error_msg = "Cannot take action {} to go from position {} \
                to position {}".format(action, self.position, next_position)
            raise InvalidPosition(error_msg)

    def get_position(self):
        return self.current_node.position


class Ghost(Agent):
    def __init__(self, node, blue=False):
        super().__init__(node)
        self.blue = blue
        self.eaten = False
        self.blue_time_left = 0

    def move(self, action):
        super(Ghost, self).move(action)
        if (self.blue_time_left):
            self.blue_time_left -= 1
        if (not self.blue_time_left):
            self.blue = False
            self.eaten = False

    def start_blue(self, blue_time_left=10):
        self.blue = True
        self.eaten = False
        self.blue_time_left = blue_time_left

    def stop_blue(self):
        self.blue = False
        self.eaten = False
        self.blue_time_left = 0


class PacMan(Agent):
    def eat_ghost(self, ghost, reward=10):
        ghost.eaten = True
        return reward
