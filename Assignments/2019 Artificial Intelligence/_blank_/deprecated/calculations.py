"""
:filename: calculations.py
:summary: Used to calculate estimated nodes generated at certain depths.
Used to approximate suitable depth values for lookahead in AI that would
maximise exploration without exceeding resource budget.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################

# Standard modules
import numpy as np
from math import inf

########################## FUNCTIONS #########################

def player_max_actions(n):
    """
    :summary: Worst case maximum actions with n pieces = 6 * pieces
    :returns: int
    """
    return 6*n

def b_factor(n_matrix, k=1):
    """
    :summary: computes branching factor over 3k turns (k cycles)
    :returns: int, approximation
    """
    result = 1
    for n in n_matrix:
        result *= player_max_actions(n) if (n > 0) else 1
    return result**k

def d_factor(n_matrix, th=15000):
    """
    :summary: Gets depth allowed that reaches threshold
    :returns: decimal approximation
    """
    return 3*math.log(th) / math.log(b_factor(n_matrix))

N = np.array([12,11,10,9,8,7,6,5,4])
# Worst case for N pieces in 3 player game
worst_case = lambda N: np.array([N / 3.0]*3)
worst = [worst_case(n) for n in N]
# Worst case for N pieces in 2 player game
two_player_worst_case = np.vectorize(lambda N: np.array([N / 2.0]*2 + [0]))
two_worst = [two_player_worst_case(n) for n in N]

# Estimated maximal threshold for # nodes
depth_t = 1500000

for n in N:
    print(f"{n} - 3P {b_factor(worst_case(n))} --> depth {d_factor(worst_case(n), depth_t):.3f}", end='')
    print(f" 2P {b_factor(two_player_worst_case(n))} --> depth {d_factor(two_player_worst_case(n), depth_t):.3f}")
