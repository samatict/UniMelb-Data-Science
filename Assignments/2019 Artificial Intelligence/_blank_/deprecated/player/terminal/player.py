""" player.py

Base class for any TerminalPlayer.
Asks for inputs directly from command line.

"""

########################### IMPORTS ##########################
# Standard modules
import re
from ast import literal_eval
# User-defined files
from mechanics import create_initial_state, apply_action

class TerminalPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player.
        """
        self.colour = colour
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
        while(True):
            raw_action = input("Enter next action >>> ").strip()
            try:
                flag = raw_action[:4]
                raw_pieces = list(map(lambda x: literal_eval(f"{x}"), re.findall(r"-?\d\D*-?\d", raw_action[4:])))
                if flag == "PASS":
                    return (flag, None)
                elif flag == "EXIT":
                    return (flag, raw_pieces.pop())
                elif flag in ("MOVE", "JUMP"):
                    return (flag, tuple(raw_pieces))
                else:
                    print("ERROR: Missing flag")
            except:
                print("ERROR: Invalid input")
