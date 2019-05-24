""" moves.py

Defines core game structure, globals, and actions

"""

########################## IMPORTS ###########################
# Standard modules
from collections import defaultdict
from queue import PriorityQueue as PQ
from copy import deepcopy

# User-defined files
from classes import *

########################## GLOBALS ###########################
INF = float('inf')

# Goals for each player
GOAL = {
    "red": ((3, -3), (3, -2), (3, -1), (3, 0)),
    "blue": ((-3,0),(-2,-1),(-1,-2),(0,-3)),
    "green": ((-3, 3), (-2, 3), (-1, 3), (0, 3))
}

POSSIBLE_DIRECTIONS = [(0,1),(1,0),(1,-1),(0,-1),(-1,0),(-1,1)]

# As point indices range from -3 to 3
MAX_COORDINATE_VAL = 3

# action_flags for use in action tuples
MOVE, JUMP, EXIT = 0, 1, 2

#################### CLASSES & FUNCTIONS #####################

def possible_actions(state, debug_flag = False):
    """Possible actions from current location"""
    result = list()

    # if a piece can exit, great! Do that immediately for Part A
    possible_exit = [i for i in state["pieces"] if i in GOAL[state["colour"]]]
    if possible_exit:
        return [(possible_exit[0], EXIT, None)]

    for piece in state["pieces"]:
        result.extend([(piece, MOVE, dest) for dest in move(piece, state)])
        result.extend([(piece, JUMP, dest) for dest in jump(piece, state)])

    return result

def move(coordinate, state, relaxed=False):
    """Finds possible move actions given a coordinate"""
    # Non-movable pieces on board
    if relaxed:
        occupied = state["blocks"]
    else:
        occupied = state["blocks"] + state["pieces"]

    possible_moves = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = add(coordinate, direction)

        if adjacent_hex in VALID_COORDINATES: # Then it's not off-board
            if adjacent_hex not in occupied: # Then it's free for the taking
                possible_moves.append(adjacent_hex)

    return sorted(possible_moves)

def jump(coordinate, state, relaxed=False):
    """Finds possible jump actions given a coordinate"""
    if relaxed:
        occupied = state["blocks"]
    else:
        occupied = state["blocks"] + state["pieces"]

    possible_jumps = list()

    for direction in POSSIBLE_DIRECTIONS:
        adjacent_hex = add(coordinate, direction)
        target_hex = add(adjacent_hex, direction)

        if relaxed or adjacent_hex in occupied: # Then you can jump over it
            if target_hex in VALID_COORDINATES: # Then not off-board
                if target_hex not in occupied: # Then actual place to land
                    possible_jumps.append(target_hex)

    return sorted(possible_jumps)

# Determines if exit action possible
def exit_action(coordinate, state):
    return coordinate in GOAL[state["colour"]]

@memoize
def dijkstra_board(state):
    """Evaluates minimum cost to exit for each non-block position"""
    valid_goals = set(GOAL[state['colour']]).difference(set(state['blocks']))

    visited = set() # Flags if visited or not
    cost = {x:INF for x in VALID_COORDINATES} # Stores costs
    cost.update({x:1 for x in valid_goals}) # Sets goals cost
    queue = PQ()

    # Add exits to queue to get it started
    for goal in valid_goals:
        queue.put((cost[goal], goal))

    # Loop over queue (dijsktra)
    while not queue.empty():
        curr_cost, curr = queue.get()
        if curr not in visited:
            visited.add(curr)
            poss_neighbours = set(move(curr, state, True)).union(set(jump(curr, state, True)))
            for new in poss_neighbours:
                est_cost = curr_cost + 1
                if est_cost < cost[new]: # Better path than previous
                    cost[new] = est_cost
                queue.put((cost[new], new))
    return cost
