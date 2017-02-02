import time

import numpy as np


class TreeNode:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.n_visits = 0
        self.children = []

        self.score = 0

    def UCB_score(self, t):
        if self.n_visits == 0:
            # If the node was never visited, we need to visit it
            score = np.inf
        else:
            mean = self.wins/self.n_visits
            score = mean + np.sqrt(np.log(t)/(2*self.n_visits))
        self.score = score
        return score

    @property
    def is_leaf(self):
        is_leaf = (len(self.children) == 0)
        return is_leaf

    def __str__(self):
        string = "{wins}/{losses} - {score:.2f}".format(
            wins=self.wins, losses=self.losses, score=self.score
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
        self.nodes[state].n_visits += 1

    def is_visited(self, state):
        visited = state in self.nodes
        return visited

    def get_node(self, state):
        if state in self.nodes:
            node = self.nodes[state]
        else:
            node = TreeNode()
        return node

    def update(self, state, win):
        if win:
            self.nodes[state].wins += 1
        else:
            self.nodes[state].losses += 1


class MCTS:
    def __init__(self, game):
        self.game = game
        self.tree = Tree()

    def select(self):
        """Select a child node from the current node using UCB"""
        # TODO: if state is already visited, legal_moves are known and are
        # the children of the current node (need to link nodes in tree)
        legal_moves = self.game.legal_moves()
        # States are keys to next nodes
        next_states = [self.game.next_state(move) for move in legal_moves]
        next_nodes = [self.tree.get_node(state) for state in next_states]

        # Choose a move based on the node it will lead to
        t = self.tree.get_node(self.current_state).n_visits
        scores = [node.UCB_score(t) for node in next_nodes]
        indexes = np.argwhere(scores == np.max(scores)).flatten()
        # choose one of the argmax at random
        index = np.random.choice(indexes)
        next_state = next_states[index]
        move = legal_moves[index]
        return move, next_state

    def self_select(self):
        """Play a move in self-play mode (nodes were never visited)"""
        legal_moves = self.game.legal_moves()
        # Choose next move at random
        # TODO: Use a simple heuristic
        index = randint(0, len(legal_moves)-1)
        move = legal_moves[index]
        return move

    def backpropagate(self, path, win):
        for state in path:
            self.tree.update(state, win)

    def run_simulation(self, max_plays=10, display=False):
        self.game.reset()
        cum_reward = 0

        # Start from root
        self.current_state = self.game.get_state()
        path = [self.current_state]
        self.tree.visit(self.current_state)

        n_plays = 0
        self.display(cum_reward, display)

        # (1) Selection step: Traverse until we select a child not in the tree
        move, next_state = self.select()
        while self.tree.is_visited(next_state) and not self.game.finished:
            # Visit the state before the ghosts move
            self.tree.visit(next_state)
            path.append(next_state)

            reward = self.game.play(move)
            self.current_state = next_state
            cum_reward += reward
            n_plays += 1
            self.display(cum_reward, display)
            # Append the state after the ghosts move
            # state = self.game.get_state()
            # self.tree.visit(next_state)
            # path.append(state)

            move, next_state = self.select()
            if n_plays >= max_plays:
                # TODO: n_plays and max_plays handled inside game
                self.game.lost = True

        # (2) Expansion step: Add this child to the tree
        self.tree.visit(next_state)
        path.append(next_state)

        # (3) Simulation step: Self-play until the end of the game
        while not self.game.finished:
            reward = self.game.play(move)
            cum_reward += reward
            n_plays += 1
            self.display(cum_reward, display)
            if n_plays >= max_plays:
                # TODO: n_plays and max_plays handled inside game
                self.game.lost = True

        # (4) Backpropagation step: Backpropagate to the traversed nodes
        # TODO: Backpropagate the reward instead of win/loss
        win = self.game.won
        self.backpropagate(path, win)

    def train(self, train_time):
        """Trains the algorithms for train_time seconds"""
        start_time = time.time()
        simu_count = 0
        while (time.time() - start_time) < train_time:
            if simu_count % 100 == 0:
                display = True
                print("Simulations: {} - Time: {}s".format(
                      simu_count, int(time.time() - start_time)))
            else:
                display = False

            # Run one simulation
            self.run_simulation(display=display)
            simu_count += 1
        print("Simulations: {} - Time: {}s".format(
              simu_count, int(time.time() - start_time)))

    def display(self, cum_reward, display):
        if display:
            board_title = 'reward : {}'.format(cum_reward)
            self.game.draw_state(board_title)
