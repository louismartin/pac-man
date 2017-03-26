import numpy as np
from matplotlib import pyplot as plt

from pacman.algorithms import MCTS


def running_mean(series, run_length):
    cumsum = np.cumsum(np.insert(series, 0, 0))
    return (cumsum[run_length:] - cumsum[:-run_length]) / run_length


def train_and_monitor_mcts(game, train_time=500, display_interval=10000,
                           discount_factors=[0.95]):
    """
    Trains several mcts for the various discount_factors
    :param discount_factors: list of various discount_factors to use
    :return discount_rewards: final rewards as list
    of rewards for the various discounts
    :return discount_wins: ordered list of booleans
    for win status of simulations
    """
    discount_rewards = []
    discount_wins = []
    for discount_factor in discount_factors:
        mcts = MCTS(game, verbose=False)
        rewards, wins = mcts.train(train_time=train_time,
                                   display_interval=display_interval,
                                   discount_factor=discount_factor)
        discount_rewards.append(rewards)
        discount_wins.append(wins)
    return discount_rewards, discount_wins


def plot_running(scores, params, param_name="discount factor",
                 score_name='rewards', mean_step=200):
    """
    Plots running mean of all performances lists on a unique figure
    :param params: list of varying params
    :param scores: list of performance lists
    """

    for i in range(len(params)):
        plt.plot(running_mean(scores[i], mean_step))
    lgd = plt.legend([str(param) for param in params], title=param_name)
    plt.ylabel('running mean of {0}'.format(score_name))
    plt.xlabel('simulation iteration')
    plt.show()
