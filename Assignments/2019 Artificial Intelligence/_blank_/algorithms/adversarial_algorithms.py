"""
:filename: adversarial_algorithms.py
:summary: Defines all adversarial search algorithms
:authors: Akira Wang (913391), Callum Holmes (899251)

ADVERSARIAL SEARCH ALGORITHMS:
1. Negamax - for 2 player states
2. Paranoid - for 3 player states
3. Directed Offensive - for 3 player states
4. Max^n - the most useless algorithm ever
"""

########################### IMPORTS ##########################

# Standard modules
from math import inf

# User-defined functions
from _blank_.state import State
from _blank_.algorithms.heuristics import desperation
from _blank_.algorithms.PARTA.IDA_star import original_search

# Global Imports
from _blank_.state import PLAYER_HASH, N_PLAYERS

MAX_DEPTH = 3

########################## FUNCTIONS #########################

def alpha_beta(state, counts, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH):
    """
    :summary: Simple yet effective implementation of minimax with alpha-beta pruning.
    :returns: vector of (evaluation, action_if_any)
    """
    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    best_action, best_new_action = None, None
    player = state.turn
    index = PLAYER_HASH[player]

    generated_actions = state.possible_actions(player)
    for action in generated_actions:
        new_state = State.apply_action(state, action, ignore_dead=True)

        # Only want vector of evaluations
        player_eval = alpha_beta(new_state, counts, heuristic, max_player, alpha, beta, depth_left-1)[0]

        if (player == max_player):
            # MaximisingPlayer wants to maximise alpha
            if player_eval[index] > alpha:
                alpha, best_action = player_eval[index], action
                if new_state.hash not in counts:
                    best_new_action = best_action
        else:
            # MinimisingPlayer wants to worsen beta
            if player_eval[index] < beta:
                beta, best_action = player_eval[index], action
                if new_state.hash not in counts:
                    best_new_action = best_action

        if alpha >= beta:
            return (player_eval, best_new_action) if best_new_action is not None else (player_eval, best_action)
    return (player_eval, best_new_action) if best_new_action is not None else (player_eval, best_action)

def paranoid(state, counts, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH, loser=False):
    """
    :summary: Paranoid assuming a 1 vs rest scenario.
    Used when winning / losing given a certain threshold.
    The implementation also uses alpha-beta pruning, with the assumption of good ordering.
    :returns: tuple of (evaluation, action_if_any)
    """

    if not depth_left:
        evals = heuristic(state)
        if loser:
            evals[PLAYER_HASH[max_player]] += desperation(state)[PLAYER_HASH[max_player]]
        return (evals, None)

    best_action, best_new_action = None, None
    player = state.turn
    index = PLAYER_HASH[player]

    generated_actions = state.possible_actions(player)
    for action in generated_actions:
        new_state = State.apply_action(state, action)

        # Only want vector of evaluations
        player_eval = paranoid(new_state, counts, heuristic, max_player, alpha, beta, depth_left-1)[0]

        if (player == max_player):
            # MaximisingPlayer wants to maximise alpha
            if player_eval[index] > alpha:
                alpha, best_action = player_eval[index], action
                if new_state.hash not in counts:
                    best_new_action = best_action
        else:
            # MinimisingPlayer wants to worsen beta
            if player_eval[index] < beta:
                beta, best_action = player_eval[index], action
                if new_state.hash not in counts:
                    best_new_action = best_action

        if alpha >= beta:
            return (player_eval, best_new_action) if best_new_action is not None else (player_eval, best_action)
    return (player_eval, best_new_action) if best_new_action is not None else (player_eval, best_action)

def directed_offensive(state, counts, heuristic, max_player, target, min_eval=inf, depth_left=MAX_DEPTH):
    """
    :summary: An algorithm aimed to MINIMISE a target player used in a 3 player
    scenario with no good pruning techniques possible.
    :assumption: all players will wish to maximise themselves (like a typical Max^n algorithm)
    :strategy: If we find an evaluation minimising a target's evaluation,
    and it is beneficial to us, that becomes our "best action".
    :returns: tuple of (evaluation, action_if_any)
    """

    if not depth_left:
        evals = heuristic(state)
        # Value should be offset by the situation the target is in
        evals[PLAYER_HASH[max_player]] -= desperation(state)[PLAYER_HASH[target]]

        return (evals, None)

    max_player_evals = [-inf]*N_PLAYERS
    best_action, best_new_action = None, None
    player = state.turn
    index = PLAYER_HASH[player]
    target_index = PLAYER_HASH[target]

    generated_actions = state.possible_actions(player, sort=(player==max_player))
    for action in generated_actions:
        new_state = State.apply_action(state, action)

        # Get vector of evaluations
        player_eval = directed_offensive(new_state, counts, heuristic, max_player, target, min_eval, depth_left-1)[0]

        if player != max_player:
            # NOT the max_player - we assume they will want to just maximise themselves
            if player_eval[index] > max_player_evals[index]:
                max_player_evals, best_action = player_eval, action
                if new_state.hash not in counts:
                    best_new_action = best_action
        else:
            # If this new eval LOWERS our target eval and our eval is NOT WORSE, then update our path with this action
            if player_eval[target_index] < min_eval and player_eval[index] >= max_player_evals[index]:
                max_player_evals, best_action, min_eval = player_eval, action, player_eval[target_index]
                if new_state.hash not in counts:
                    best_new_action = best_action

    return (player_eval, best_new_action) if best_new_action is not None else (player_eval, best_action)

def max_n(state, counts, heuristic, max_player_evals=[-inf]*N_PLAYERS, depth_left=MAX_DEPTH):
    """
    :summary: Max^N. A 3 player variant of minimax with no good pruning techniques available.
    Pretty useless (due to limited pruning) and is used little in game.
    :returns: tuple of (evaluation, action_if_any)
    """

    if not depth_left:
        evals = heuristic(state)
        return (evals, None)

    best_action, best_new_action = None, None
    player = state.turn
    index = PLAYER_HASH[player]

    generated_actions = state.possible_actions(player)

    for action in generated_actions:
        new_state = State.apply_action(state, action)

        # Get vector of evaluations
        player_eval = max_n(new_state, counts, heuristic, max_player_evals, depth_left-1)[0]

        if player_eval[index] > max_player_evals[index]:
            max_player_evals, best_action = player_eval, action
            if new_state.hash not in counts:
                best_new_action = best_action

    return (player_eval, best_new_action) if best_new_action is not None else (player_eval, best_action)

def part_A_search(data):
    """
    Performs the search algorithm used in Part A
    """
    optimal_solution = original_search(data)

    if (optimal_solution is not None):
        path = list()
        node_temp = optimal_solution

        # Re-assemble path taken
        while (node_temp is not None):
            path.append(node_temp)
            node_temp = node_temp.parent

        return path[::-1]

########################### DEPRECIATED ALGORITHMS ##########################

def negamax(state, counts, heuristic, max_player, alpha=-inf, beta=inf, depth_left=MAX_DEPTH):
    """
    :summary: Simple yet effective implementation of Negamax with alpha-beta pruning.
    The possible moves functions will always return good ordering for optimal pruning.
    :assumption: one player is dead - hence the game is merely 2-player.
    :returns: tuple of (evaluation, action_if_any)
    """

    if not depth_left:
        evals = runner(state)[PLAYER_HASH[max_player]]
        return (-evals, None)

    best_action, best_new_action = None, None
    player = state["turn"]

    for action in possible_actions(state, player):
        new_state = apply_action(state, action, ignore_dead=True)

        new_eval = -negamax(new_state, counts,heuristic, max_player, -beta, -alpha, depth_left - 1)[0]

        if new_eval >= beta:
            return (beta, best_new_action) if best_new_action is not None else (beta, best_action)

        if new_eval > alpha:
            alpha, best_action = new_eval, action
            if Z_hash(new_state) not in counts:
                best_new_action = best_action

    return (alpha, best_new_action) if best_new_action is not None else (alpha, best_action)
