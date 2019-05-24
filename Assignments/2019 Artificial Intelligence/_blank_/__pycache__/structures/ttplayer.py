""" player.py

Base class for a Greedy Player.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice
from math import inf

# User-defined files
from state import State
from structures.gamenode import GameNode
from collections import defaultdict

class TTPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.root = GameNode()
        self.kill = True

    @property
    def colour(self):
        return self.root.turn

    def debug(self):
        GameNode.debugger(self.root)

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action.
        """
        # Steal root child with this state and overthrow
        self.root = self.root.update_root(action, kill=self.kill)
