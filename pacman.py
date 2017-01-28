import numpy as np


class Agent:
    def __init__(self, current_node=None):
        self.current_node = current_node


class Ghost(Agent):
    def __init__(self, current_node, killable=False):
        super().__init__(current_node)
        self.killable = killable

    def move():
        pass


class PacMan(Agent):
    def __init_(self, current_node):
        super().__init__(heigt)


class Node:
    def __init__(self, position, children_nodes=None, reward=1):
        self.position = position
        self.reward = reward
        if (children_nodes is None):
            self.children_nodes = []
        else:
            self.children_nodes = children_nodes

    def __str__(self):
        return ' position : {pos} \n children nb : {children_nb} \n'.\
            format(children_nb=str(len(self.children_nodes)),
                   pos=self.position)


class Board:
    def __init__(self, board_file_name):
        self.agents = []
        board_nodes, board_outline = Board.construct_board(board_file_name)
        self.board_nodes = board_nodes
        self.board_outline = board_outline

    @staticmethod
    def construct_board(board_file_name):
        board_outline = []
        with open(board_file_name) as f:
            for line in f:
                board_outline.append(list(line.strip()))
        board_outline = np.array(board_outline)
        board_row_nb, board_column_nb = board_outline.shape

        board_nodes = {}
        # Create nodes
        for board_row_idx in range(board_row_nb):
            for board_column_idx in range(board_column_nb):
                if(board_outline[board_row_idx, board_column_idx] == '+'):
                    new_position = (board_row_idx, board_column_idx)
                    new_node = Node(new_position)
                    board_nodes[new_position] = new_node
        # Associate nodes to children
        for position, current_node in board_nodes.items():
            children = []
            row = position[0]
            col = position[1]
            if (row > 0 and (row - 1, col) in board_nodes.keys()):
                children.append(board_nodes[(row - 1, col)])
            if (row < board_row_nb and (row + 1, col) in board_nodes.keys()):
                children.append(board_nodes[(row + 1, col)])
            if (col > 0 and (row, col - 1) in board_nodes.keys()):
                children.append(board_nodes[(row, col - 1)])
            if (col < board_column_nb and
                    (row, col + 1) in board_nodes.keys()):
                children.append(board_nodes[(row, col + 1)])
            current_node.children_nodes = children
            print(current_node)
        return board_nodes, board_outline

    def add_agent(self, agent):
        target_node = self.board_nodes[agent.current_node.position]
        self.agents.append(agent)

    def __str__(self):
        current_board = self.board_outline.copy()
        for agent in self.agents:
            agent_row = agent.current_node.position[0]
            agent_col = agent.current_node.position[1]
            if (isinstance(agent, PacMan)):
                current_board[agent_row, agent_col] = 'p'
            if (isinstance(agent, Ghost)):
                current_board[agent_row, agent_col] = 'u'
        return current_board.__str__()

if __name__ == '__main__':
    new_board = Board('simple-path.txt')
    print(new_board.board_nodes[(0, 0)])
    # Add pacman
    pac_man_init_node = new_board.board_nodes[(0, 0)]
    pac_man = PacMan(pac_man_init_node)

    # Add ghosts
    ghost1_init_node = new_board.board_nodes[(5, 5)]
    ghost1 = Ghost(ghost1_init_node)
    ghost2_init_node = new_board.board_nodes[(0, 5)]
    ghost2 = Ghost(ghost2_init_node)

    new_board.add_agent(pac_man)
    new_board.add_agent(ghost1)
    new_board.add_agent(ghost2)

    print(new_board)