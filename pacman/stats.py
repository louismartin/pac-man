import numpy as np


def running_mean(series, run_length):
    cumsum = np.cumsum(np.insert(series, 0, 0))
    return (cumsum[run_length:] - cumsum[:-run_length]) / run_length
