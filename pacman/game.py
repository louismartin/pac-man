from matplotlib import pyplot as plt

from pacman.tools import timeit


class InvalidPosition(Exception):
    pass


class Game:
    def __init__(self, board, speed, pacman_agent=None, ghost_agents=None):
        self.board = board
        self.pacman = pacman_agent
        self.speed = speed
        self.candies = {}

        if (not ghost_agents):
            self.ghosts = []
        else:
            self.ghosts = ghost_agents
        self.plot = None

    def add_pacman(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.board_nodes):
            self.pacman = agent
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_ghost(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.board_nodes):
            self.ghosts.append(agent)
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_candy(self, candy):
        position = candy.node.position
        if (position in self.board.board_nodes):
            self.candies[position] = candy
        else:
            raise InvalidPosition("Cannot add candy\
                to invalid board position")

    def check_collision(self, pacman, pacman_new_node,
                        ghost, ghost_new_node):
        collision = False
        if (pacman_new_node.position == ghost_new_node.position):
            collision = True
        if ((pacman_new_node.position == ghost.current_node.position) and (
                pacman.current_node.position == ghost_new_node.position)):
            collision = True
        return collision

    def resolve_collision(self, ghost, pacman):
        game_finished = False
        if (not ghost.blue):
            game_finished = True
        elif(ghost.blue and not ghost.eaten):
            pacman.eat_ghost(ghost)
        return game_finished

    def play_game(self):
        game_finished = False
        while (not game_finished):
            # Compute next moves
            next_pacman_node = self.pacman.get_move()
            next_ghost_nodes = [ghost.get_move() for ghost in self.ghosts]
            current_ghost_nodes = [ghost.current_node for ghost in self.ghosts]

            # Check if game finished
            for ghost, next_ghost_node in zip(
                        self.ghosts, next_ghost_nodes):
                collision = self.check_collision(self.pacman,
                                                 next_pacman_node,
                                                 ghost,
                                                 next_ghost_node)
                if(collision):
                    game_finished = self.resolve_collision(ghost, self.pacman)
                    if game_finished:
                        return self.pacman.reward

            if (next_pacman_node.position in self.candies):
                del self.candies[next_pacman_node.position]
                for ghost in self.ghosts:
                    ghost.start_blue()

            # Move agents
            self.pacman.move(next_pacman_node)
            for idx, ghost in enumerate(self.ghosts):
                    ghost.move(next_ghost_nodes[idx])

            # Update rewards
            self.pacman.reward += self.pacman.current_node.reward
            self.pacman.current_node.reward = 0
            board_title = 'reward : ' + str(self.pacman.reward)
            self.draw_state(board_title)

    def compute_state(self):
        current_board = self.board.board_outline.copy()
        for position, node in self.board.board_nodes.items():
            if (node.reward > 0):
                current_board[node.position[0], node.position[1]] = 4
        for row, col in self.candies:
            current_board[row, col] = 6
        for ghost in self.ghosts:
            row, col = ghost.get_position()
            if ghost.blue:
                if ghost.eaten:
                    current_board[row, col] = 3
                else:
                    current_board[row, col] = 7
            else:
                current_board[row, col] = 5
        pacman_row, pacman_col = self.pacman.get_position()
        current_board[pacman_row, pacman_col] = 2
        return current_board

    def draw_state(self, title):
        current_board = self.compute_state()
        if self.plot:
            plt.title(title)
            self.plot.set_data(current_board)
        else:
            plt.ion()
            plt.title(title)
            self.plot = plt.matshow(current_board, fignum=0)
        plt.pause(self.speed)

    def __str__(self):
        return str(self.compute_state())
