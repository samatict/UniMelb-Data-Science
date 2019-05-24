""" player.py

Base class for a Greedy Player.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
from math import inf

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
        self.depth = 0
        self.state = create_initial_state()

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action.
        """
        self.state = apply_action(self.state, action)

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        self.depth += 1
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program. Made it so greedy will always prefer exit moves
        """
        if len(self.state[self.colour]) == 0:
            return ("PASS",None)

        if self.depth%18 == 0:
            return choice(possible_actions(self.state, self.colour))

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
