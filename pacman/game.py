from time import sleep

from matplotlib import pyplot as plt

from pacman.tools import timeit


class Game:
    def __init__(self, board, speed, pacman_agent=None, ghost_agents=None):
        self.board = board
        self.pacman = pacman_agent
        self.speed = speed
        if (not ghost_agents):
            self.ghosts = []
        else:
            self.ghosts = ghost_agents

    def add_pacman(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.board_nodes):
            target_node = self.board.board_nodes[agent.current_node.position]
            self.pacman = agent
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

    def check_rules(self, pacman_old_node, pacman_new_node,
                    ghost_old_node, ghost_new_node):
        collision = False
        if (pacman_new_node.position == ghost_new_node.position):
            collision = True
        if ((pacman_new_node.position == ghost_old_node.position) and (
                pacman_old_node.position == ghost_new_node.position)):
            collision = True
        return collision

    def play_game(self):
        game_reward = 0
        game_finished = False
        while (not game_finished):
            # Compute next moves
            next_pacman_node = self.pacman.get_move()
            next_ghost_nodes = [ghost.get_move() for ghost in self.ghosts]
            current_ghost_nodes = [ghost.current_node for ghost in self.ghosts]

            # Check if game finished
            for current_ghost_node, next_ghost_node in zip(
                        current_ghost_nodes, next_ghost_nodes):
                collision = self.check_rules(self.pacman.current_node,
                                             next_pacman_node,
                                             current_ghost_node,
                                             next_ghost_node)
                if(collision):
                    game_finished = True
                    return game_reward

            # Move agents
            self.pacman.move(next_pacman_node)
            for idx, ghost in enumerate(self.ghosts):
                    ghost.move(next_ghost_nodes[idx])

            # Update rewards
            game_reward += self.pacman.current_node.reward
            self.pacman.current_node.reward = 0
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
        pacman_row, pacman_col = self.pacman.get_position()
        current_board[pacman_row, pacman_col] = 2
        return current_board

    @timeit
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
