import copy

from matplotlib import pyplot as plt
import numpy as np

from pacman.agents import PacMan, Ghost
from pacman.board import Candy, Node, InvalidPosition


class Game:
    def __init__(self, board, speed=0.0001, max_plays=np.inf,
                 pacman_agent=None, ghost_agents=[], candies=[]):
        self.board = board
        self.speed = speed
        self.max_plays = max_plays
        # Agents
        self.initial_pacman = pacman_agent
        self.initial_ghosts = []
        for ghost in ghost_agents:
            self.initial_ghosts.append(ghost)
        # Candies and pac-dots
        self.initial_candies = {}
        for candy in candies:
            self.initial_candies[candy.position] = candy
        self.pac_dot_reward = 1
        # Other game parameters
        self.plot = None
        # Initialize the game
        self.reset()

    def reset(self):
        self.n_plays = 0
        self.lost = False
        self.won = False
        self.pacman = copy.deepcopy(self.initial_pacman)
        self.ghosts = copy.deepcopy(self.initial_ghosts)
        self.candies = copy.deepcopy(self.initial_candies)
        self.initialize_pac_dots()
        if self.pacman:
            del self.pac_dots[self.pacman.position]

    @property
    def finished(self):
        return self.lost or self.won

    def initialize_pac_dots(self):
        """
        Pac-dots are stored in a dictionary where the keys are their position
        and the value their reward.
        """
        self.pac_dots = {}
        for node_pos in self.board.nodes:
            self.pac_dots[node_pos] = self.pac_dot_reward

    def add(self, name, position):
        name = name.lower()
        if position not in self.board.nodes:
            raise InvalidPosition("Invalid board position {}".format(position))
        init_node = self.board.nodes[position]
        if name == "pacman":
            self.add_pacman(PacMan(init_node))
        elif name == "ghost":
            self.add_ghost(Ghost(init_node))
        elif name == "candy":
            self.add_candy(Candy(init_node))
        else:
            raise KeyError("Invalid element: {}".format(name))

    def add_pacman(self, agent):
        target_position = agent.position
        if (target_position in self.board.nodes):
            self.initial_pacman = agent
            self.pacman = copy.deepcopy(agent)
            # Remove the pac-dot where pacman is initialized
            del self.pac_dots[self.pacman.position]
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_ghost(self, agent):
        target_position = agent.position
        if (target_position in self.board.nodes):
            self.initial_ghosts.append(agent)
            self.ghosts.append(copy.deepcopy(agent))
        else:
            raise InvalidPosition("Cannot add agent\
                to invalid board position")

    def add_candy(self, candy):
        position = candy.position
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
            if pacman.position == ghost.position:
                # Check if ghost eats the pacman or the contrary
                reward = self.resolve_collision(ghost, pacman)
                break
        return reward

    def resolve_collision(self, ghost, pacman):
        """Check if ghost eats the pacman or the contrary"""
        reward = 0
        if (not ghost.blue):
            self.lost = True
        elif(ghost.blue and not ghost.eaten):
            reward += pacman.eat_ghost(ghost)
        return reward

    def play(self, action):
        """
        Play one move
        Args:
            - move (Node): next node
        Returns:
            - reward (int)
        """
        reward = 0
        # Move the pacman
        self.pacman.move(action)

        # Check for collision before moving the ghosts
        reward += self.check_collision(self.pacman, self.ghosts)
        # Move the ghosts
        for ghost in self.ghosts:
            action = ghost.get_action()
            ghost.move(action)
        # Check for collision after moving the ghosts
        reward += self.check_collision(self.pacman, self.ghosts)

        # Check if the pacman is still alive to go forth with the events
        if not self.lost:
            # Check if candy is eaten
            if self.pacman.position in self.candies:
                del self.candies[self.pacman.position]
                for ghost in self.ghosts:
                    ghost.start_blue()

            # Update rewards
            pos = self.pacman.position
            if pos in self.pac_dots:
                reward += self.pac_dots[pos]
                del self.pac_dots[pos]
                if (len(self.pac_dots) + len(self.candies)) == 0:
                    self.won = True

        # Check if we did not reach the maximum number of plays
        self.n_plays += 1
        if self.n_plays > self.max_plays:
            self.lost = True

        return reward

    def play_game(self):
        cum_reward = 0
        board_title = 'reward : {}'.format(cum_reward)
        self.draw_state(board_title)
        while (not self.finished):
            # Compute next moves
            action = self.pacman.get_action()
            reward = self.play(action)
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
            pos = ghost.position
            if ghost.blue:
                if ghost.eaten:
                    current_board[pos] = ghost_eaten_value
                else:
                    current_board[pos] = ghost_blue_value
            else:
                current_board[pos] = ghost_value
        current_board[self.pacman.position] = pacman_value

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

    def legal_actions(self):
        current_node = self.pacman.current_node
        legal_actions = []
        for child_node in current_node.children_nodes:
            action = Node.nodes_to_action(current_node, child_node)
            legal_actions.append(action)
        return legal_actions

    def next_state(self, action):
        """Get next hashable state for the considered action"""
        # Save variables for reverting
        initial_node = self.pacman.current_node

        # Move TODO: take into account candy eating, ghost eating ?
        self.pacman.move(action)
        pos = self.pacman.position
        revert = False
        if pos in self.pac_dots:
            reward = self.pac_dots[pos]
            del self.pac_dots[pos]
            revert = True
        state = self.get_state()

        # Revert
        if revert:
            self.pac_dots[pos] = reward
        self.pacman.current_node = initial_node

        return state

    def __str__(self):
        return str(self.compute_grid())
