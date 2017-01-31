from random import randint
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from pacman.agents import Ghost, PacMan
from pacman.board import Board
from pacman.game import Game


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


def choose_next_node(next_nodes, t):
    scores = [node.UCB_score(t) for node in next_nodes]
    indices = np.argwhere(scores == np.max(scores)).flatten()
    # choose one of the argmax at random
    return np.random.choice(indices)


def backpropagate(tree_states, path, win):
    for state in path:
        tree.update(state, win)
    return tree


tree = Tree()

for i in tqdm(range(10000)):
    # Play one game
    board = Board('boards/3x3_board.txt')
    game_speed = 0.1
    game = Game(board, game_speed)

    # Create agents and add them to game
    pacman_init_node = board.nodes[(0, 0)]
    pacman = PacMan(pacman_init_node)
    game.add_pacman(pacman)

    game.reset()  # TODO
    cum_reward = 0
    state = game.get_state()
    path = [state]
    tree.visit(state)
    count = 0
    if i % 10 == 0:
        draw = True
    else:
        draw = False
    while not (game.game_finished):
        legal_moves = game.legal_moves()
        # States are keys to next nodes
        next_states = [game.next_state(move) for move in legal_moves]
        visited = [tree.is_visited(state) for state in next_states]
        if all(visited):
            next_nodes = [tree.get_node(state) for state in next_states]

            # Choose a move based on the node it will lead to
            t = tree.get_node(state).n_visits
            i = choose_next_node(next_nodes, t)
            next_state = next_states[i]
            move = legal_moves[i]
            print("Next states: {} - t={}".format(
                [tree.get_node(state) for state in next_states], t
            ))
            print("Chosen: {}".format(tree.get_node(next_state)))
        else:
            print("Exploring")
            # At least one state has not been explored, choose the first
            for i, state in enumerate(next_states):
                if not tree.is_visited(state):
                    next_state = state
                    move = legal_moves[i]
                    break

        if draw:
            board_title = 'reward : {}'.format(cum_reward)
            game.draw_state(board_title)

        # Append the state before the ghosts move
        tree.visit(next_state)
        path.append(next_state)

        reward = game.play(move)
        cum_reward += reward

        # Append the state after the ghosts move
        # state = game.get_state()
        # tree.visit(next_state)
        # path.append(state)

        count += 1
        if count >= 10:
            game.game_over = True
    if draw:
        board_title = 'reward : {}'.format(cum_reward)
        game.draw_state(board_title)
    # Backpropagate
    win = game.game_won
    tree = backpropagate(tree, path, win)
