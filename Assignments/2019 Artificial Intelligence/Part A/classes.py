""" classes.py

All common, multi-purpose classes go here.

"""

########################## IMPORTS ###########################
# Standard modules
from collections import defaultdict

# User-defined modules

########################## GLOBALS ###########################
NUM_EXIT_STATES = 4
NUM_HEXES = 37
HASH_LEN = 82 # Bit length of any hash
CODE_LEN = 2 # Bit length of each flag. Can be 0,1,2,3
NUM_PLAYERS = 3

# Bidirectional lookup for player bit code
# Starts from 0 so that calculating heuristic values is a little smoother
PLAYER_CODE = {
    "red": 0b00,
    "green" : 0b01,
    "blue" : 0b10,
    "none" : 0b11
}
# For bidirectionality
PLAYER_CODE.update(dict(zip(PLAYER_CODE.values(), PLAYER_CODE.keys())))

# Exit code hashing scheme lookup
EXIT_CODE = list(range(3))

# Game valid coordinate positions (taken from the test generator script)
VALID_COORDINATES = [(-3, 0), (-3, 1), (-3, 2), (-3, 3),
                    (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3),
                    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
                    (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3),
                    (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
                    (2, -3), (2, -2), (2, -1), (2, 0), (2, 1),
                    (3, -3), (3, -2), (3, -1), (3, 0)]

######################### DECORATORS #########################

"""ADAPTED FROM https://www.python-course.eu/python3_memoization.php"""
def memoize(method):
    """Caches result of a function to prevent recalculation under same input"""
    memo = []
    def helper(*args, **kwargs):
        if not len(memo):
            memo.append(method(*args, *kwargs))
        return memo[0]
    return helper

########################## VECTORS ##########################

def add(tuple_1, tuple_2):
    """Allows for "vector_1 + vector_2"""
    return (tuple_1[0] + tuple_2[0], tuple_1[1] + tuple_2[1])

########################## HASHING ############################

"""
Implements a minimal collision hash for states

Each of the 37 hexes has a 2-bit flag:
 + one flag for turn player
 + 3 flags for exit_totals
 = an 82-bit long int

"""

def Z_hash(data):
    """Hash the board state"""
    hashed = 0

    """Hash of the form
        0b(turn)(red_exits)(green_exits)(blue_exits)(37 hex state flags....)
    Where
    - For turn player:
        - 00 for red
        - 01 for green
        - 10 for blue
    - For the 37 hexes:
        - 00 for empty
        - 01 for player
        - 10 for block # Could have been 11, just needed to not be 00 or 01"""

    # Append turn player
    hashed = hashed | PLAYER_CODE[data["colour"]]

    # just a fix to make room for num_exits for part B
    hashed = hashed << NUM_PLAYERS * CODE_LEN

    # Encode coordinates: First, make space
    hashed = hashed << NUM_HEXES * CODE_LEN

    # ith pair of 2-bits = ith location in VALID_COORDINATES
    for piece in data["blocks"]:
        hashed = hashed ^ (0b10 << CODE_LEN * VALID_COORDINATES.index(piece))
    for piece in data["pieces"]:
        hashed = hashed ^ (0b01 << CODE_LEN * VALID_COORDINATES.index(piece))
    return hashed

def Z_data(hashed):
    """Return data for board"""
    result = defaultdict(list)
    result["colour"] = PLAYER_CODE[hashed >> HASH_LEN - CODE_LEN] # First entry

    hex_codes = [(hashed >> CODE_LEN*i) & 0b11 for i in range(NUM_HEXES)]
    for i, coordinate in enumerate(VALID_COORDINATES):
        # ith coordinate = 2ith 2-bit combination in hash
        hex_code = (hashed >> CODE_LEN*i) & 0b11

        if hex_code == 0b01:
            result["pieces"].append(coordinate)
        elif hex_code == 0b10:
            result["blocks"].append(coordinate)

    return dict(result)
