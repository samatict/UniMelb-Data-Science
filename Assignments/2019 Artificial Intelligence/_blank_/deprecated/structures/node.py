"""
:filename: node.py
:summary: Implements Node class for use in graph/tree search algorithms.
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################
# Standard modules
# User-defined files
from mechanics import possible_actions, apply_action, player

class Node:
    """
    Node superclass with core (initialized) attributes and methods
    Subclasses e.g. IDANode(Node) define and add extra functionality
    """
    trim_total = 0
    count_total = 0

    def __init__(self, state, parent=None):
        """
        Creates new node
        """
        self.parent = parent  # Points to parent node
        self.is_expanded = False  # Flags the fact that children have been generated
        self.action = None  # Action that parent made to get here
        self.state = state  # Stores data. Must have been a deepcopy
        self._is_dead = False  # DO NOT continue to explore
        self._children = list()  # list of children
        Node.count_total += 1

    @property
    def children(self):
        """Generate children if not done so already, and return them"""
        if not self.is_expanded:
            self.expand()
        return self._children

    @property
    def is_dead(self):
        return self._is_dead

    @is_dead.setter
    def is_dead(self, value):
        self._is_dead = value

    def expand(self):
        """Generate children"""
        for action in possible_actions(self.state, player(self.state)):
            new_child = self.new_child(apply_action(self.state, action), self)
            new_child.action = action
            self._children.append(new_child)
        self.is_expanded = True
        #### TODO: Decide ordering here

    @classmethod
    def new_child(cls, state, parent):
        """Creates new, empty instance"""
        return cls(state, parent)

    @classmethod
    def create_root(cls, initial_state):
        """Creates first instance"""
        return cls.new_child(state=initial_state, parent=None)

    def clean_tree(self):
        """Kill trees below any dead nodes"""
        for child in self._children:
            if child.is_dead:
                child.kill_tree()
            else:
                child.clean_tree()

    def kill_tree(self):
        """Recursively kills down subtree, however will not kill ignores
        Inferred that references to ignore nodes are retained externally"""
        # Kill each subtree
        for child in self._children:
            child.kill_tree()
        Node.trim_total += 1
        del(self)

    def overthrow(self):
        """Recursively kill down each subtree"""
        # Parent makes itself the king first if not already
        if self.parent:
            if self.parent.parent:
                self.parent.overthrow()
            # Now that parent is king, usurp it
            for sibling in self.parent._children:
                if sibling != self:
                    sibling.kill_tree()
            Node.trim_total += 1
            del(self.parent)
            self.parent = None

    def recursive_print(self):
        """Prints tree structure"""
        print(self)
        if self.is_expanded:
            for child in self.children:
                child.recursive_print()
