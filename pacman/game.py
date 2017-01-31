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
        self.game_over = False

    def reset(self):
        # TODO: there might be other stuff to reset
        self.game_over = False

    def add_pacman(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.nodes):
            self.pacman = agent
            self.pacman.current_node.reward = 0
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_ghost(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.nodes):
            self.ghosts.append(agent)
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_candy(self, candy):
        position = candy.node.position
        if (position in self.board.nodes):
            self.candies[position] = candy
        else:
            raise InvalidPosition("Cannot add candy\
                to invalid board position")

    def check_collision(self, pacman, ghosts):
        collision = False
        reward = 0
        for ghost in ghosts:
            # Check if pacman meets a ghost
            if pacman.current_node.position == ghost.current_node.position:
                # Check if ghost eats the pacman or the contrary
                reward = self.resolve_collision(ghost, pacman)
                break
        return reward

    def resolve_collision(self, ghost, pacman):
        """Check if ghost eats the pacman or the contrary"""
        reward = 0
        if (not ghost.blue):
            self.game_over = True
        elif(ghost.blue and not ghost.eaten):
            reward += pacman.eat_ghost(ghost)
        return reward

    def play(self, move):
        """
        Play one move
        Args:
            - move (Node): next node
        Returns:
            - reward (int)
        """
        reward = 0
        # Move the pacman
        self.pacman.move(move)

        # Check for collision before moving the ghosts
        reward += self.check_collision(self.pacman, self.ghosts)
        # Move the ghosts
        for ghost in self.ghosts:
            move = ghost.get_move()
            ghost.move(move)
        # Check for collision after moving the ghosts
        reward += self.check_collision(self.pacman, self.ghosts)

        # Check if the pacman is still alive to go forth with the events
        if not self.game_over:
            # Check if candy is eaten
            if self.pacman.current_node.position in self.candies:
                del self.candies[self.pacman.current_node.position]
                for ghost in self.ghosts:
                    ghost.start_blue()

            # Update rewards
            reward += self.pacman.current_node.reward
            self.pacman.current_node.reward = 0
        return reward

    def play_game(self):
        cum_reward = 0
        while (not self.game_over):
            # Compute next moves
            move = self.pacman.get_move()
            reward = self.play(move)
            cum_reward += reward

            board_title = 'reward : {}'.format(cum_reward)
            self.draw_state(board_title)

    def compute_grid(self):
        # TODO: Store it and only update what changed at the next move
        current_board = self.board.outline.copy()
        for position, node in self.board.nodes.items():
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
        current_board = self.compute_grid()
        if self.plot:
            plt.title(title)
            self.plot.set_data(current_board)
        else:
            plt.ion()
            plt.title(title)
            self.plot = plt.matshow(current_board, fignum=0)
        plt.pause(self.speed)

    def __str__(self):
        return str(self.compute_grid())
