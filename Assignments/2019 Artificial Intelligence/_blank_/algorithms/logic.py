"""
:filename: logic.py
:summary: Defines the core structure of an MP-MIX agent
:authors: Akira Wang (913391), Callum Holmes (899251)

Concept adapted from:
The MP-MIX algorithm: Dynamic Search Strategy Selection in Multi-Player Adversarial Search

Authors:
Inon Zuckerman, Ariel Felner

:thresholds: If defence_threshold or offence_threshold are 0, it will degenerate to:
             1. Paranoid when winning
             2. Offensive when losing
:strategy: Determine whether the agent should be paranoid (1 vs all), maxn (everyone will maximise themself), offence (minimise a target)
"""

# TODO NOTE: potential custom eval functions that are fixed given mp-mix logic (rather than passing a single heuristic)

########################### IMPORTS ##########################

# Standard modules
from math import inf
from pprint import pprint

# User-defined functions
from _blank_.algorithms.heuristics import *
from _blank_.algorithms.adversarial_algorithms import alpha_beta, paranoid, directed_offensive, max_n

# Global Imports
from _blank_.state import PLAYER_NAMES, PLAYER_HASH, N_PLAYERS

########################### GLOBALS ##########################

KILL_DEPTH = 3 # multiple of 3 to ensure achilles(last_move) reasonable (1 full turn look ahead)
PARANOID_MAX_DEPTH = 3 # multiple of 3 to ensure achilles(last_move) reasonable (1 full turn look ahead)
TWO_PLAYER_MAX_DEPTH = 4 # multiple of 2 to ensure achilles(last_move) reasonable (2 full turns look ahead)
DEFAULT_DEPTH = 3
MAX_UTIL_VAL = 5 # TODO: Calculate a max utility value! For now, this is the equivalent of a "free" exit (worth 10 points)

########################## FUNCTIONS #########################

def mp_mix(state, counts, heuristic, defence_threshold=0, offence_threshold=0, two_player=False):
    """
    Main function for MP-Mix.
    :strategy: Always returns exits if we are way ahead (force_exit)
                Otherwise pulls logic of 2/3 player game depending on state
    :returns: vector of valuations
    """

    # The max_player (us)
    max_player = state.turn

    leader, rival, loser, leader_edge, second_edge = score(state, heuristic)

    move, possible = winning_move(state, max_player, two_player)
    if possible:
        print("\t\t\t\t\t\t\t\t\t\t\t\t* ||| FREE WIN!")
        return move

    if two_player:
        return two_player_logic(state, counts, heuristic, max_player, leader_edge, depth=TWO_PLAYER_MAX_DEPTH, defence_threshold=MAX_UTIL_VAL)

    # If we are the leader, we use a running heuristics which avoids conflict to the goal
    if max_player == leader:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LEADER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, counts, heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    # If we are the rival and we have excess pieces, we will attack the leader
    if max_player == rival and desperation(state)[PLAYER_HASH[max_player]] > 0 and state.exits[leader] > 0:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| RIVAL - USING DIRECTED OFFENSIVE AGAINST LEADER  {leader} | DEPTH = {KILL_DEPTH}")
        return directed_offensive(state, counts, heuristic, max_player, leader, depth_left=KILL_DEPTH)[1]
    else: # leader doesnt have exits so whatever
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| RIVAL - USING PARANOID | DEPTH = {DEFAULT_DEPTH}")
        return paranoid(state, counts, heuristic, max_player, depth_left=PARANOID_MAX_DEPTH)[1]

    # If we are losing then we are desperate :^)
    if max_player == loser:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| LOSER - USING PARANOID | DEPTH = {PARANOID_MAX_DEPTH}")
        return paranoid(state, counts, heuristic, max_player, depth_left=PARANOID_MAX_DEPTH, loser=True)[1]

    # Otherwise, we will just use our default OP heuristic
    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| DEFAULTING TO MAX N (RIVAL) | DEPTH = {DEFAULT_DEPTH}")
    return max_n(state, counts, heuristic, depth_left=DEFAULT_DEPTH)[1]

def score(state, heuristic):
    """
    :summary: Function which ranks players by their initial heuristic evaluation
    :returns: best, mid and worst scores, as well as margins
    """
    evals = heuristic(state)
    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| Initial Evaluations {evals}")

    scores = {PLAYER_NAMES[i] : evals[i] for i in range(N_PLAYERS)}
    scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    leader, rival, loser = scores[0][0], scores[1][0], scores[2][0]
    high, medium, low = scores[0][1], scores[1][1], scores[2][1]

    leader_edge = high - medium
    second_edge = medium - low

    return leader, rival, loser, leader_edge, second_edge

def winning_move(state, max_player, two_player=False):
    """
    :summary: Forces our agent to make a winning move:
    1. Exit our 4th piece
    2. Capture the opponents last piece (given it is a two player scenario)
    :returns: tuple of (action, IS_WINNING_MOVE boolean)
    """
    possible_exits = state.exit_action(max_player)
    if state.exits[max_player] == 3 and len(possible_exits) > 0:
        return (possible_exits[0], True)

    if two_player:
        alive_opponent = state.get_remaining_opponent()
        occupied_hexes = state.get_occupied(PLAYER_NAMES)
        captures = state.capture_jumps( occupied_hexes, max_player)
        if len(state.pieces(alive_opponent)) == 1 and len(captures) > 0:
            return (captures[0], True)
    return (None, False)

def two_player_logic(state, counts, heuristic, max_player, leader_edge, depth, defence_threshold=0):
    """
    :summary: MP-Mix 2 player strategy (no need to be offensive).
    :default: alpha_beta which will have a higher depth if sparse
    :returns: action_if_any
    """
    alive_opponent = state.get_remaining_opponent()

    if desperation(state)[PLAYER_HASH[alive_opponent]] < 0 and leader_edge >= defence_threshold:
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| WE ARE SIGNIFICANTLY AHEAD - DOING A RUNNER AGAINST OPPONENT")
        return False

    if sum(no_pieces(state)) >= 6: # less than six pieces on board
        depth = 2

    if sum(no_pieces(state)) <= 4: # less than six pieces on board
        depth = 6

    print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| ALPHA-BETA AGAINST REMAINING PLAYER USING TWO_PLAYER_HEURISTICS | DEPTH = {depth}")
    # if distance is close to enemy goal, troll them. Else run to our own goal using different heuristic.
    return alpha_beta(state, counts, heuristic, max_player, depth_left=depth)[1]
