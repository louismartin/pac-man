import time

import numpy as np


class TreeNode:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.n_visits = 1
        self.children = []

        self.score = 0

    def UCB_score(self, t):
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
        if state in self.nodes:
            self.nodes[state].n_visits += 1
        else:
            self.nodes[state] = TreeNode()

    def is_visited(self, state):
        visited = state in self.nodes
        return visited

    def get_node(self, state):
        return self.nodes[state]

    def update(self, state, win):
        if win:
            self.nodes[state].wins += 1
        else:
            self.nodes[state].losses += 1


class MCTS:
    def __init__(self, game):
        self.game = game
        self.tree = Tree()

    def choose_next_node(self, next_nodes, t):
        scores = [node.UCB_score(t) for node in next_nodes]
        indices = np.argwhere(scores == np.max(scores)).flatten()
        # choose one of the argmax at random
        return np.random.choice(indices)

    def backpropagate(self, path, win):
        for state in path:
            self.tree.update(state, win)

    def run_simulation(self, max_plays=10, display=False):
        self.game.reset()
        cum_reward = 0

        # Start from root
        state = self.game.get_state()
        path = [state]
        self.tree.visit(state)
        n_plays = 0
        if display:
            board_title = 'reward : {}'.format(cum_reward)
            self.game.draw_state(board_title)
        while not (self.game.game_finished):
            legal_moves = self.game.legal_moves()
            # States are keys to next nodes
            next_states = [self.game.next_state(move) for move in legal_moves]
            visited = [self.tree.is_visited(state) for state in next_states]
            if all(visited):
                next_nodes = [self.tree.get_node(state) for state
                              in next_states]

                # Choose a move based on the node it will lead to
                t = self.tree.get_node(state).n_visits
                i = self.choose_next_node(next_nodes, t)
                next_state = next_states[i]
                move = legal_moves[i]
                # print("Next states: {} - t={}".format(
                #     [self.tree.get_node(state) for state in next_states], t))
                # print("Chosen: {}".format(self.tree.get_node(next_state)))
            else:
                # At least one state has not been explored, choose the first
                for i, state in enumerate(next_states):
                    if not self.tree.is_visited(state):
                        next_state = state
                        move = legal_moves[i]
                        break

            # Append the state before the ghosts move
            self.tree.visit(next_state)
            path.append(next_state)

            reward = self.game.play(move)
            cum_reward += reward
            n_plays += 1

            # Append the state after the ghosts move
            # state = self.game.get_state()
            # self.tree.visit(next_state)
            # path.append(state)

            if display:
                board_title = 'reward : {}'.format(cum_reward)
                self.game.draw_state(board_title)

            if n_plays >= max_plays:
                self.game.game_over = True
        win = self.game.game_won
        self.backpropagate(path, win)

    def train(self, train_time):
        """Trains the algorithms for train_time seconds"""
        start_time = time.time()
        n_simulations = 0
        while (time.time() - start_time) < train_time:
            if n_simulations % 100 == 0:
                display = True
                print("Simulations: {} - Time: {}s".format(
                      n_simulations, int(time.time() - start_time)))
            else:
                display = False

            # Run one simulation
            self.run_simulation(display=display)
            n_simulations += 1
        print("Simulations: {} - Time: {}s".format(
              n_simulations, int(time.time() - start_time)))
