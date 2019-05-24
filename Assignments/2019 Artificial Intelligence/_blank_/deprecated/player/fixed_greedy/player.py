""" player.py

Base class for a Greedy Player.

"""

########################### IMPORTS ##########################
# Standard modules
from math import inf
from collections import defaultdict

# User-defined files
from mechanics import *
from algorithms.heuristics import greedy

class GreedyPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.

        "I am speed" - Lightning McQueen

        """
        self.colour = colour
        self.state = create_initial_state()
        self.counts = defaultdict(int)

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action.
        """
        self.state = apply_action(self.state, action)
        self.counts[Z_hash(self.state)] += 1

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program. Made it so greedy will always prefer exit moves
        """
        if len(self.state[self.colour]) == 0:
            return ("PASS",None)
        best_eval, best_action = -inf, None
        for action in possible_actions(self.state, self.colour):
            if action[0] == "EXIT":
                return action
            new_state = apply_action(self.state, action)
            new_eval = greedy(new_state)[PLAYER_HASH[self.colour]]
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = action

        return best_action
