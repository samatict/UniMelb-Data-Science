"""
:filename: gamenode.py
:summary: Implements GameNode class for use in graph/tree search algorithms.
:authors: Akira Wang (913391), Callum Holmes (899251)

Properties of GAMENODE (NOT INHERITED):
- node.counts[node.hash] --> # visits in the game
- node.hash --> node.hash
- node.update_root(action, kill) --> reassigns root, trims tree if kill
- node.get_node(statehash)

INHERITED:
- node.children
    --> gets children
    --> side effect auto-labels deads if they are in TT
    --> RETURNS [] IF DEAD
- node.parent
- node.depth
- node.action
- node.is_expanded
- node.is_bad
"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from collections import defaultdict
from structures.node import Node
from state import *
import numpy as np

class GameNode(Node):
    """
    :summary: Extends functionality of a base node to work with players
    Allows tracking of repeated states during a game as well as
    Efficient storage of all generated nodes
    Must be accessed by heuristics/etc. to be most effective.
    """

    def __init__(self, state=None):
        super().__init__(state)
        self.child_evaluations = dict()
        if self.parent:
            self.counts = self.parent.counts  # Tracks actual game
            self.TT = self.parent.TT  # Inherit memory if parent exists
        else:
            self.counts = defaultdict(int)
            self.TT = defaultdict()

        # Add to storage
        self.TT[self.hash] = self

    def increment(self, node):
        """
        Increase number of visits to a node
        """
        self.counts[node.hash] += 1

    def update_root(self, action, kill=False):
        """
        Called when an actual game move has been decided, updates tree
        :returns: new root for player to use
        """
        try:
            # print(f"\n{self.hash()}\n")

            root = [x for x in self.children if x.action == action].pop(0)
            if kill:
                self.overthrow()  # Delete all irrelevant siblings to free memory
                self.clean_tree()

            # Add to storage
            self.TT[root.hash] = root
            root.increment(root)
            return root
        except:
            self.debugger(self)

    def get_node(self, state_hash, draws):
        """
        Can jump to any (explored) state given the state
        """
        if draws:
            return self.counts[state_hash]
        else:
            return self.TT[state_hash]

    # Overriden behaviour
    def expand(self):
        assert(not self.is_expanded)
        if self.is_bad: return
        for action in self.possible_actions(self.turn):
            new_child = self.new_child(State.apply_action(self, action))
            self._children.append(new_child)

            # Use TT to verify it should be considered
            node_hash = new_child.hash
            if node_hash in self.TT:
                current = self.TT[node_hash]
                if (new_child.depth >= current.depth) and new_child != current:
                    # This is a duplicate
                    new_child.is_bad = True
                else:
                    # This is better, so flag the older one dead
                    current.is_bad = True

            self.TT[node_hash] = new_child

        self.is_expanded = True
        #### TODO: Decide ordering here

    @staticmethod
    def debugger(current):
        """Modified referee calls this, allows for navigation of search tree
        Can call anywhere in execution"""
        while(1):
            chosen = input(">> Change wt hash (c) goto parent (p) exec (e) state_info (s) heuristics (h) quit (q) >> ")
            if chosen not in "cpeqhs":
                print(">> Invalid, try again.")
            elif chosen == "c":
                try:
                    nodehash = int(input("Specify FULL hash for state >> ").strip())
                    current = current.get_node(nodehash, False)
                except:
                    print(">> invalid, try again.")
            elif chosen == "p":
                current = current.parent
                print(">> Navigated to parent.")
            elif chosen == "e":
                print(">> Executable activated. NOTE: current = GameNode.\n>> To release loop, trigger a NameError (type nonsense).")
                while(1):
                    try:
                        exec(input("\n!(exec) >> "))
                    except NameError:
                        break
                    except:
                        print(">> invalid, try again.")
            elif chosen == "h":
                from algorithms.heuristics import displacement, desperation, speed_demon, favourable_hexes, exits, achilles_real, end_game_heuristic, two_player_heuristics
                print("\n".join([f"{f.__name__} : {f(current)}" for f in [displacement, desperation, speed_demon, favourable_hexes, exits, achilles_real, end_game_heuristic, two_player_heuristics]]))
            elif chosen == "s":
                current.format()
            else:
                break

    def format(self):
        """
        Defines how to display a state in debugging.
        """
        self.printer(self)
        print(f"Depth {self.depth}, colour {self.turn} dead {self.is_bad} expanded {self.is_expanded}\nChildren: ")
        for child in self.children:
            print(f"FULL HASH {child.hash} - {child.action}",end="")
            if child.action in self.child_evaluations.keys():
                print(f" - {self.child_evaluations[child.action]}")
            else:
                print("")

    @staticmethod
    def printer(state):
        from algorithms.PARTA.formatting import print_board
        board_dict = {}
        for player in PLAYER_NAMES:
            for i in state.pieces(player):
                board_dict[i] = f"{player}"
        print_board(board_dict, False)
