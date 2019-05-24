""" player.py

Base class for any RunnerPlayer.
Plays a paranoid implementation and attempts to get to the goal fastest.
Uses number_of_pieces_lost = 0 and retrograde_dijkstra as heuristic

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
from collections import defaultdict
# User-defined functions
from mechanics import *
from moves import exit_action
from algorithms.adversarial_algorithms import paranoid, alpha_beta
from algorithms.heuristics import runner

PATH = list()

class RunnerPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.state = create_initial_state()
        self.colour = colour
        self.counts = defaultdict(int)

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = apply_action(self.state, action)
        self.counts[Z_hash(self.state)] += 1

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        if self.state['depth'] % 18 == 0:
            return choice(possible_actions(self.state, self.colour))

        if is_dead(self.state, self.colour):
            return ("PASS", None)
        else:
            possible_exits = exit_action(self.state, self.colour)
            if self.state['exits'][self.colour] == 3 and len(possible_exits) > 0:
                return possible_exits[0]
            return paranoid(self.state, self.counts, runner, self.colour)[1]
