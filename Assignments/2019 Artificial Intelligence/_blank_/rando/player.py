""" player.py

Base class for any RandomPlayer.
Asks for inputs directly from command line.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice

# User-defined functions
from _blank_.state import State

class RandomPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.state = State()

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = State.apply_action(self.state, action)

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        return choice(self.state.possible_actions(self.state.turn))
