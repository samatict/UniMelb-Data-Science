""" player.py

Base class for any MCPlayer.
Runs a MC search using a cached tree - see the file for further details.

"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from state import State
from structures.mcnode import MCNode
from structures.ttplayer import TTPlayer

class MCPlayer(TTPlayer):

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.root = MCNode(None)
        self.kill = False

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.
        """
        return self.root.search()
