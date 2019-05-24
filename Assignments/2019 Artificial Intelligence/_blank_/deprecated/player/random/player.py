""" player.py

Base class for any RandomPlayer.
Asks for inputs directly from command line.

"""

########################### IMPORTS ##########################
# Standard modules
from random import choice

# User-defined functions
from mechanics import possible_actions, create_initial_state, apply_action

class RandomPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.state = create_initial_state()

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent, assumedly correct,
        action."""
        self.state = apply_action(self.state, action)

    ################# DEFINE EVERY IMPLEMENTATION ################

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        return choice(possible_actions(self.state, self.state['turn']))
