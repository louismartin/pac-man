from matplotlib import pyplot as plt
import copy

from pacman.tools import timeit


class InvalidPosition(Exception):
    pass


class Game:
    def __init__(self, board, speed,
                 pacman_agent=None, ghost_agents=[], candies=[]):
        self.board = board
        # Agents
        self.initial_pacman = pacman_agent
        self.initial_ghosts = []
        for ghost in ghost_agents:
            self.initial_ghosts.append(ghost)
        # Candies and pac-dots
        self.initial_candies = {}
        for candy in candies:
            self.initial_candies[candy.current_node.position] = candy
        self.pac_dot_reward = 1
        # Other game parameters
        self.plot = None
        self.speed = speed
        # Initialize the game
        self.reset()

    def reset(self):
        # TODO: rename game_* to *
        self.game_over = False
        self.game_won = False
        self.pacman = copy.deepcopy(self.initial_pacman)
        self.ghosts = copy.deepcopy(self.initial_ghosts)
        self.candies = copy.deepcopy(self.initial_candies)
        self.initialize_pac_dots()
        if self.pacman:
            del self.pac_dots[self.pacman.current_node.position]

    @property
    def game_finished(self):
        return self.game_over or self.game_won

    def initialize_pac_dots(self):
        """
        Pac-dots are stored in a dictionary where the keys are their position
        and the value their reward.
        """
        self.pac_dots = {}
        for node_pos in self.board.nodes:
            self.pac_dots[node_pos] = self.pac_dot_reward

    def add_pacman(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.nodes):
            self.initial_pacman = agent
            self.pacman = copy.deepcopy(agent)
            # Remove the pac-dot where pacman is initialized
            del self.pac_dots[self.pacman.current_node.position]
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_ghost(self, agent):
        target_position = agent.current_node.position
        if (target_position in self.board.nodes):
            self.initial_ghosts.append(agent)
            self.ghosts.append(copy.deepcopy(agent))
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_candy(self, candy):
        position = candy.node.position
        if (position in self.board.nodes):
            self.initial_candies[position] = candy
            self.candies[position] = copy.deepcopy(candy)
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
            pos = self.pacman.current_node.position
            if pos in self.pac_dots:
                reward += self.pac_dots[pos]
                del self.pac_dots[pos]
                if (len(self.pac_dots) + len(self.candies)) == 0:
                    self.game_won = True

        return reward

    def play_game(self):
        cum_reward = 0
        while (not self.game_finished):
            # Compute next moves
            move = self.pacman.get_move()
            reward = self.play(move)
            cum_reward += reward

            board_title = 'reward : {}'.format(cum_reward)
            self.draw_state(board_title)
        return cum_reward

    def compute_grid(self):
        # TODO: Store it and only update what changed at the next move
        pac_dot_value = 4
        candy_value = 6
        ghost_value = 5
        ghost_blue_value = 7
        ghost_eaten_value = 3
        pacman_value = 2

        current_board = self.board.outline.copy()
        # Fill the board with the elements
        for pac_dot_pos in self.pac_dots:
            current_board[pac_dot_pos] = pac_dot_value
        for candy_pos in self.candies:
            current_board[candy_pos] = candy_value
        for ghost in self.ghosts:
            pos = ghost.get_position()
            if ghost.blue:
                if ghost.eaten:
                    current_board[pos] = ghost_eaten_value
                else:
                    current_board[pos] = ghost_blue_value
            else:
                current_board[pos] = ghost_value
        current_board[self.pacman.get_position()] = pacman_value

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

    def get_state(self):
        """Returns a hashable representation of the current state"""
        # TODO: Ghosts hide candies in this state representation
        hashable_state = tuple(self.compute_grid().flatten())
        return hashable_state

    def legal_moves(self):
        return self.pacman.current_node.children_nodes

    def next_state(self, move):
        """Get next hashable state for move being the next pacman node"""
        # Save variables for reverting
        initial_node = self.pacman.current_node

        # Move TODO: take into account candy eating, ghost eating ?
        self.pacman.move(move)
        pos = self.pacman.current_node.position
        revert = False
        if pos in self.pac_dots:
            reward = self.pac_dots[pos]
            del self.pac_dots[pos]
            revert = True
        state = self.get_state()

        # Revert
        if revert:
            self.pac_dots[pos] = reward
        self.pacman.move(initial_node)

        return state

    def __str__(self):
        return str(self.compute_grid())
