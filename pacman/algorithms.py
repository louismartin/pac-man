import time
from random import randint

import numpy as np


class TreeNode:

    def __init__(self):
        self.empirical_mean = 0
        self.n_visits = 0
        self.score = 0

    def visit(self):
        self.n_visits += 1

    def update(self, cum_reward):
        n = self.n_visits
        self.empirical_mean = self.empirical_mean * \
            (n - 1) / n + cum_reward / n

    def UCB_score(self, t):
        if self.n_visits == 0:
            # If the node was never visited, we need to visit it
            score = np.inf
        else:
            score = self.empirical_mean + \
                np.sqrt(np.log(t) / (2 * self.n_visits))
        self.score = score
        return score

    def __str__(self):
        string = "{mean:.1f}/{visits} {score:.2f}".format(
            mean=self.empirical_mean, visits=self.n_visits, score=self.score
        )
        return string

    def __repr__(self):
        return self.__str__()


class Tree:

    def __init__(self):
        # self.nodes is a dictionary with the keys being the states
        # and the values being TreeNode objects
        self.nodes = {}

    def visit(self, state):
        if state not in self.nodes:
            self.nodes[state] = TreeNode()
        self.nodes[state].visit()

    def is_visited(self, state):
        visited = (state in self.nodes) and (self.nodes[state].n_visits > 0)
        return visited

    def get_node(self, state):
        if state in self.nodes:
            node = self.nodes[state]
        else:
            node = TreeNode()
        return node

    def update(self, state, cum_reward):
        self.nodes[state].update(cum_reward)


class MCTS:

    def __init__(self, game, verbose=False):
        self.game = game
        self.verbose = verbose
        self.tree = Tree()

    def select(self):
        """Select a child node from the current node using UCB"""
        # TODO: if state is already visited, legal_actions are known and are
        # the children of the current node (need to link nodes in tree)
        legal_actions = self.game.legal_actions()
        # States are keys to next nodes
        next_states = [self.game.next_state(a) for a in legal_actions]
        next_nodes = [self.tree.get_node(state) for state in next_states]

        # Choose an action based on the node it will lead to
        t = self.tree.get_node(self.current_state).n_visits
        scores = [node.UCB_score(t) for node in next_nodes]
        indexes = np.argwhere(scores == np.max(scores)).flatten()
        # choose one of the argmax at random
        index = np.random.choice(indexes)
        next_state = next_states[index]
        action = legal_actions[index]
        if self.verbose:
            print("Node: {} - Next nodes: {} - Chosen: {}".format(
                self.tree.get_node(self.current_state),
                next_nodes,
                index
            ))

        return action, next_state

    def self_select(self):
        """Play an action in self-play mode (nodes were never visited)"""
        legal_actions = self.game.legal_actions()
        # Choose next action at random
        # TODO: Use a simple heuristic
        index = randint(0, len(legal_actions) - 1)
        action = legal_actions[index]
        return action

    def backpropagate(self, path, cum_reward):
        for state in set(path):
            if self.verbose:
                print("Updating state {}".format(state))
            self.tree.update(state, cum_reward)

    def run_simulation(self, display=False, discount_factor=0.95):
        """
        :param discount_factor: discount factor for the reward
        """
        self.game.reset()
        cum_reward = 0

        # Start from root
        self.current_state = self.game.get_state()
        self.tree.visit(self.current_state)
        path = [self.current_state]
        self.display(cum_reward, display)

        # (1) Selection step: Traverse until we select a child not in the tree
        action, next_state = self.select()

        game_step = 0
        while self.tree.is_visited(next_state) and not self.game.finished:
            # State before the ghosts move
            path.append(next_state)

            reward = self.game.play(action)
            self.tree.visit(next_state)
            self.current_state = next_state
            game_step += 1
            cum_reward += discount_factor**game_step * reward
            self.display(cum_reward, display)
            # Append the state after the ghosts move
            # state = self.game.get_state()
            # self.tree.visit(next_state)
            # path.append(state)

            action, next_state = self.select()

        # (2) Expansion step: Add this child to the tree
        self.tree.visit(next_state)
        path.append(next_state)

        # (3) Simulation step: Self-play until the end of the game
        while not self.game.finished:
            game_step += 1
            reward = self.game.play(action)
            cum_reward += discount_factor**game_step * reward
            self.display(cum_reward, display)
            action = self.self_select()

        # (4) Backpropagation step: Backpropagate to the traversed nodes
        self.backpropagate(path, cum_reward)
        return cum_reward, self.game.won

    def train(self, train_time, display_interval=100, discount_factor=0.95):
        """Trains the algorithms for train_time seconds"""
        start_time = time.time()
        simu_count = 1
        running_time = int(time.time() - start_time)
        final_rewards = []
        wins = []
        while running_time < train_time:
            if simu_count % display_interval == 0:
                display = True
                print("Simulations: {} - Time: {}s".format(
                      simu_count, running_time))
            else:
                display = False
            # Run one simulation
            final_reward, game_won = self.run_simulation(
                display=display, discount_factor=discount_factor)
            final_rewards.append(final_reward)
            wins.append(game_won)
            simu_count += 1
            running_time = int(time.time() - start_time)
        print("Simulations: {} - Time: {}s".format(simu_count, running_time))
        return final_rewards, wins

    def display(self, cum_reward, display):
        if display:
            board_title = 'reward : {rew:.2f}'.format(rew=cum_reward)
            self.game.draw_state(board_title)
