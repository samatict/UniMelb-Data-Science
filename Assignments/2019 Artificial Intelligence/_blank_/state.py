"""
:filename: state.py
:summary: Defines state object attributes and functionality.
:authors: Akira Wang (913391), Callum Holmes (899251
"""

########################### IMPORTS ##########################
# Standard modules
import numpy as np
from copy import copy, deepcopy
# User-defined functions and globals

POSSIBLE_DIRECTIONS = [(-1,+0),(+0,-1),(+1,-1),(+1,+0),(+0,+1),(-1,+1)]

VALID_COORDINATES = [
    (-3, 0), (-3, 1), (-3, 2), (-3, 3),
    (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3),
    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
    (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3),
    (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
    (2, -3), (2, -2), (2, -1), (2, 0), (2, 1),
    (3, -3), (3, -2), (3, -1), (3, 0),
]

VALID_SET = {
    (-3, 0), (-3, 1), (-3, 2), (-3, 3),
    (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-2, 3),
    (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
    (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3),
    (1, -3), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
    (2, -3), (2, -2), (2, -1), (2, 0), (2, 1),
    (3, -3), (3, -2), (3, -1), (3, 0)
}

CORNER_SET = {
    (-3, 0), (-3, 3), (0, 3), (3, 0), (3, -3), (0, -3)
}

OPPONENTS = {
    'red': ['green', 'blue'],
    'green': ['blue', 'red'],
    'blue': ['red', 'green']
}

GOALS = {
    'red': [(3,-3), (3,-2), (3,-1), (3,0)],
    'green': [(-3,3), (-2,3), (-1,3), (0,3)],
    'blue': [(-3,0), (-2,-1), (-1,-2), (0,-3)],
}

OPPONENT_GOALS = {
    'red': {
        (-3,3), (-2,3), (-1,3), (0,3),
        (-3,0), (-2,-1), (-1,-2), (0,-3)
    },
    'green': {
        (3,-3), (3,-2), (3,-1), (3,0),
        (-3,0), (-2,-1), (-1,-2), (0,-3)
    },
    'blue': {
        (3,-3), (3,-2), (3,-1), (3,0),
        (-3,3), (-2,3), (-1,3), (0,3)
    }
}

RED, GREEN, BLUE = 'red', 'green', 'blue'

N_PLAYERS = 3
INITIAL_EXITED_PIECES = 0
MAX_TURNS = 256 # PER PLAYER
MAX_EXITS = 4
MAX_COORDINATE_VAL = 3

# Startig hexes
STARTS = {
    'red': [(-3,3), (-3,2), (-3,1), (-3,0)],
    'green': [(0,-3), (1,-3), (2,-3), (3,-3)],
    'blue': [(3, 0), (2, 1), (1, 2), (0, 3)],
}

# A default list of all the player names
PLAYER_NAMES = ["red", "green", "blue"]

# For hashing
NUM_HEXES = 37
CODE_LEN = 2 # Bit length of each flag. Can be 0,1,2,3

# bidirectional lookup for player index/hash code
PLAYER_HASH = {
    "red": 0b00,
    "green" : 0b01,
    "blue" : 0b10,
    "none" : 0b11
}
PLAYER_HASH.update(dict(zip(PLAYER_HASH.values(), PLAYER_HASH.keys())))

###################### VECTOR FUNCTIONS ######################

def add(u, v):
    """
    :summary: adds two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (u[0] + v[0], u[1] + v[1])

def sub(u, v):
    """
    :summary: subtracts two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (u[0] - v[0], u[1] - v[1])

def get_cubic_ordered(v):
    """
    :summary: converts axial to cubic, but in order of (x, z, y) in order to allow for colour hashing.
    :returns: cubic coordinates in player ordering
    """
    return (v[0], v[1], -v[0]-v[1])

def get_axial_ordered(v):
    """
    :summary: converts player-ordered cubic coordinates to axial coordinates
    :returns: axial coordinates
    """
    return (v[0], v[1])

def midpoint(u, v):
    """
    :summary: finds midpoint of two vectors u, v (tuple representation)
    :returns: tuple vector
    """
    return (int((u[0] + v[0]) / 2), int((u[1] + v[1]) / 2))

######################## STATE CLASS #########################

class State:
    """
    :summary: Encapsulates all relevant information for a game state.
    Includes functionality for fetching possible actions, opponents and
    applying actions to states.
    """
    def __init__(self, state=None):
        # Base state is the starting state
        if state:
            # Make a copy of it
            for attr in [RED, GREEN, BLUE, 'turn', 'exits', 'depth', 'action', 'parent']:
                setattr(self, attr, deepcopy(getattr(state, attr)))
        else:
            self.initial_state()

    def pieces(self, player):
        try:
            return getattr(self, player)
        except AttributeError:
            print ("# ERROR: Invalid attribute for state")
            raise AttributeError

    def initial_state(self):
        """
        :summary: Defines initial state (start of game)
        :returns: None
        """
        self.red = STARTS[RED]
        self.green = STARTS[GREEN]
        self.blue = STARTS[BLUE]
        self.turn = RED
        self.exits = {name: INITIAL_EXITED_PIECES for name in PLAYER_NAMES}
        self.depth = 0
        self.action = None
        self.parent = None

    def next_player(self, ignore_dead=False):
        """
        :summary: determines next player.
        :ignore-dead TRUE: Fetches the non-dead opponent (2-player game).
        :returns: player string
        """
        if ignore_dead and len(self.players_left()) < N_PLAYERS:
            curr_player = self.turn
            alive_opponents = [i for i in self.get_opponents() if not self.is_dead(i) and i != curr_player]
            if not alive_opponents:
                return curr_player
            elif len(alive_opponents) == 1:
                return alive_opponents.pop(0)
            else:
                return self.next_player(False)
        else:
            # Normal functionality
            current_index = PLAYER_HASH[self.turn]
            return PLAYER_NAMES[(current_index + 1) % N_PLAYERS]

    def game_won(self):
        """
        :summary: Detects if someone has exited 4 pieces
        :returns: boolean
        """
        return (MAX_EXITS in self.exits.values())

    def game_drawn(self, counts):
        """
        :summary: Detects if game drawn
        :returns: boolean
        """
        return (counts[self.hash] >= MAX_EXITS or self.depth == MAX_TURNS*N_PLAYERS)

    def possible_actions(self, player, sort=False):
        """
        :summary: Returns list of possible actions for a given state
        :returns: list of properly formatted actions for Part B
        """
        actions = list()

        # All occupied hexes (doesn't account for who's who)
        occupied_hexes = self.get_occupied(PLAYER_NAMES)

        actions.extend(self.exit_action(player))
        if sort:
            actions.extend(self.jump_sort(self.jump_action(occupied_hexes, player), player))
        else:
            actions.extend(self.jump_action(occupied_hexes, player))
        actions.extend(self.move_action(occupied_hexes, player))

        if not actions:
            return [("PASS", None)]
        else:
            return actions

    @staticmethod
    def apply_action(state, action, ignore_dead=False):
        """
        :summary: applies an action to a State object
        :returns: new fully updated state
        """
        flag, pieces = action
        new_state = deepcopy(state)
        turn_player = new_state.turn
        new_state.action = action

        if new_state.is_dead(turn_player):
            # print(f"\n\t\t\t\t\t\t\t\tPlayer {turn_player} is dead and skipping state")
            new_state.turn = state.next_player(ignore_dead)
            return new_state

        player_pieces = new_state.pieces(turn_player)
        if flag in ("MOVE", "JUMP"):
            old, new = pieces
            player_pieces.remove(old)
            player_pieces.append(new)

            # Check for captures
            if flag == "JUMP":
                adjacent_hex = midpoint(old, new)
                if adjacent_hex not in player_pieces:
                    player_pieces.append(adjacent_hex)
                    # Identify opponent and remove it
                    for player in PLAYER_NAMES:
                        if player != turn_player and adjacent_hex in new_state.pieces(player):
                            new_state.pieces(player).remove(adjacent_hex)

        elif flag == "EXIT":
            player_pieces.remove(pieces)
            new_state.exits[turn_player] += 1

        elif flag == "PASS":
            pass

        # Update turn player
        new_state.turn = state.next_player(ignore_dead)
        new_state.depth += 1

        return new_state

    def is_capture(self, action, player):
        """
        :summary: Checks if an action to be applied to a state will capture colour
        :returns: boolean
        """
        flag, pieces = action
        if flag != "JUMP": return False
        old, new = pieces
        # Returns true if what it would jump over is not its own
        return (midpoint(old, new) not in self.pieces(player))

    def get_occupied(self, players):
        """
        Fetches set of all pieces for all colours
        :returns: {pieces_for_specified_colours}
        """
        occupied = set()
        for player in players:
            occupied.update(set(self.pieces(player)))
        return occupied

    def is_dead(self, player):
        """
        :summary: Returns whether a specified player (colour) has lost all player_pieces
        :returns: boolean
        """
        return not bool(self.pieces(player))

    def num_opponents_dead(self):
        """
        :summary: Find the number of dead players (player with no pieces left)
        """
        return sum([self.is_dead(player) for player in PLAYER_NAMES])

    def two_players_left(self):
        """
        :summary: Checks if one player has lost all pieces
        :returns: boolean
        """
        return len(self.players_left()) == 2

    def get_opponents(self):
        """
        :summary: Fetches a turn player's opponents
        :returns: list(
        opponent_names in order)
        """
        return [player for player in PLAYER_NAMES if player != self.turn]

    def get_remaining_opponent(self):
        """
        :summary: Fetches a turn player's only remaining (alive) opponent
        :assumption: only one opponent left (2 players)
        :returns: list(alive_opponent_names in order)
        """
        ### TODO NOTE: Seems redundant but I left it here until we discuss it
        return [opponent for opponent in self.get_opponents() if not self.is_dead(opponent)].pop(0)

    def players_left(self):
        """
        :summary: Fetches all players left
        :returns: list(all_alive_players in order)
        """

        return [player for player in PLAYER_NAMES if not self.is_dead(player)]

    @property
    def hash(self):
        """
        :summary: Implements a minimal collision NON-INVERTIBLE hash for states.
        Hash of form
            0b(turn)(37 hex state flags....)(exits)
        """
        hashed = 0

        # Append turn player
        hashed = hashed | PLAYER_HASH[self.turn]

        # Encode coordinates: First, make space
        hashed = hashed << NUM_HEXES * CODE_LEN

        # ith pair of 2-bits = ith location in VALID_COORDINATES
        for player in PLAYER_NAMES:
            for piece in self.pieces(player):
                hashed = hashed | (PLAYER_HASH[player] + 1 << CODE_LEN * VALID_COORDINATES.index(piece))

        # Encode exits
        hashed = hashed << CODE_LEN * N_PLAYERS
        for i, player in enumerate(PLAYER_NAMES):
                hashed = hashed | (self.exits[player] << i)

        return hashed

    @property
    def draw_hash(self):
        """
        Hashing scheme but without the exits - so that draws can be detected
        """
        return self.hash >> CODE_LEN * N_PLAYERS

    def exit_action(self, player):
        """
        :summary: Function to see if an exit is possible.
        :assumption: if a piece is at a goal hex, it is not blocked (since you are at a goal hex).
        :returns: Coordinates of pieces that can exit
        """
        return [("EXIT", piece) for piece in self.pieces(player) if piece in GOALS[player]]

    def move_action(self, occupied_hexes, player):
        """
        :summary: Function to see if a move action is possible.
        :returns: list of possible move directions.
        """
        possible_moves = list()

        for piece in self.pieces(player):
            for direction in POSSIBLE_DIRECTIONS:
                adjacent_hex = add(piece, direction)
                if adjacent_hex in VALID_COORDINATES and adjacent_hex not in occupied_hexes:
                    possible_moves.append(("MOVE", (piece, adjacent_hex)))

        return possible_moves

    def jump_action(self, occupied_hexes, player):
        """
        :summary: Function to see if a jump action is possible.
        :returns: list of possible jump directions.
        """
        possible_jumps = list()

        for piece in self.pieces(player):
            for direction in POSSIBLE_DIRECTIONS:
                adjacent_hex = add(piece, direction)
                target_hex = add(adjacent_hex, direction)
                if adjacent_hex in occupied_hexes:
                    if target_hex in VALID_COORDINATES and target_hex not in occupied_hexes:
                        possible_jumps.append(("JUMP", (piece, target_hex)))

        return possible_jumps

    ######################## MOVE ORDERING #######################

    def capture(self, old, new, player):
        """
        :summary: Checks if the jump is a capturing jump.
        :returns: boolean
        """
        return midpoint(old, new) not in self.pieces(player)

    def capture_jumps(self, occupied_hexes, player):
        """
        :summary: Fetches all jump actions that could capture pieces
        :returns: list of actions
        """
        captures = list()

        for piece in self.pieces(player):
            for direction in POSSIBLE_DIRECTIONS:
                adjacent_hex = add(piece, direction)
                target_hex = add(adjacent_hex, direction)
                if adjacent_hex in occupied_hexes:
                    if target_hex in VALID_COORDINATES and target_hex not in occupied_hexes and self.capture(piece, target_hex, player):
                        captures.append(("JUMP", (piece, target_hex)))

        return captures

    def jump_sort(self, possible_jumps, player):
        """
        :summary: Orders all possible jumps from capturing jumps to self jumps.
        Useful for alpha-beta pruning.
        :returns: list of jump actions
        """
        capture_jumps = list()
        self_jumps = list()

        for jump in possible_jumps:
            if self.capture(jump[1][0], jump[1][1], player):
                capture_jumps.append(jump)
            else:
                self_jumps.append(jump)

        return capture_jumps + self_jumps
