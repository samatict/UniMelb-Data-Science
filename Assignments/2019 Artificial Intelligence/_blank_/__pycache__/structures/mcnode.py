""" MC.py

Core functionality for Monte-Carlo tree searches and variants.
A more succinct implementation, which our code was inspired by:
https://github.com/brilee/python_uct/blob/master/numpy_impl.py

Process:
- 1. Select an unexpanded node by choosing highest scored branch iteratively, scoring with wins/visits via UCB1
- 2. Expand this node and randomly choose a child.
- 3. Simulate a game by randomly choosing actions, until depth_limit is reached or game finishes.
        - Return either the outcome [1 0 0] for win, or who had the max (exits + desperation)
- 4. Backpropagate outcome to re-evaluate wins and visits for parent nodes

In addition to GameNode functionality:
STATICMETHOD - MCNode.evaluate(state)
- self.visits                   Total no. visits (currently total child wins)
- self.score                    UCB1 score
- self.select_simulation()      (1, 2)
- self.simulate()               (3)
- self.backpropagate(result)    (4)
- self.search()                 (main function)

Ideas:
- Consider NOT cutting the simulation off - run it to completion. Heuristics will 'bias' the data somewhat.
"""

########################### IMPORTS ##########################
# Standard modules
import numpy as np
import math
from random import choice
from copy import deepcopy
# User-defined files
from state import *
from structures.gamenode import GameNode
from algorithms.heuristics import *

class MCNode(GameNode):
    """
    Main node structure for monte carlo search.
    """

    total_visits = 0   # Tracks total UCT visits
    scale = math.sqrt(2)    # Sets scaling for exploration in UCB1 equations

    # Number of times MC will select and simulate a node
    # This is 'sample size' - larger sample size will give better estimates
    iterations = 10

    # Number of moves made before cutting off a simulation with heuristic evaluation
    depth_limit = 3

    def __init__(self, state=None):
        super().__init__(state)
        self.wins = np.zeros(N_PLAYERS)  # Total wins/player
        self.visits = 0

    @property
    def score(self):
        """
        Computes UCB1 score, i.e. exploitation + exploration
        """
        return self.Q() + self.U()

    def Q(self):
        """
        Fetches exploitation factor, i.e. measures whether this path wins
        """
        return self.wins[PLAYER_HASH[self.turn]] / (self.visits + 1)

    def U(self):
        """
        Fetches exploration factor, i.e. measures extent of unexploration
        """
        try:
            return MCNode.scale * np.sqrt(math.log(MCNode.total_visits) / (self.visits + 1))
        except ValueError:
            print(MCNode.scale, MCNode.total_visits, self.visits + 1)
            MCNode.debugger(self)

    def select_simulation(self):
        """
        Step 1 & 2 - recurse down to the best, unexpanded child.
        Then expand it and pick a child to simulate
        :returns: chosen state to simulate
        """
        current = self
        while current.is_expanded:
            try:
                scores = np.array([child.score if not child.is_bad else -math.inf for child in current.children])
                current = current.children[np.argmax(scores)] # CHECK THIS
            except IndexError:
                print(f"INDEXERROR - {MCNode.total_visits}")
                MCNode.debugger(self)
                print([child.score for child in current.children])
                print(scores)
                print(np.argmax(scores))
                print(len(current.children))
                raise IndexError

        # Expand child and choose (randomly) a child of this to simulate
        return choice(current.children)

    def evaluate(self, heuristic=end_game_heuristic):
        """
        Evaluate a terminal simulation state with heuristics, otherwise
        return a vector of winner (1 0 0) or tie (1/3 1/3 1/3)
        """
        if self.game_won():
            result = (exits(self) == MAX_EXITS).astype(float)
        elif self.game_drawn(self.counts):
            result = np.ones(N_PLAYERS)
        else:
            total = np.array(heuristic(self))
            result = (total == total.max()).astype(float)
        return result / np.sum(result)

    def simulate(self):
        """Run a simulation of this (unexpanded) node and return result"""
        # TODO - Maybe quiescence search result to depth_limit is better?
        # This would make MC more like A*
        current = self

        # IDEA: Push to depth_limit randomly and return heuristic evaluation
        for i in range(MCNode.depth_limit):
            if current.game_won():
                break
            else:
                current = choice(current.children)

            self.counts[current.draw_hash] += 1
        result = current.evaluate()

        while current != self and current != None:
            self.counts[current.draw_hash] -= 1
            current = current.parent
        return result

    def backpropagate(self, result):
        """Updates parents recursively (note that visits is implicit on wins)
        Assumes the simulated child has already updated"""
        current = self
        MCNode.total_visits += 1  # Result must total 1 due to evaluate function
        while isinstance(current, MCNode):
            current.wins = current.wins + result
            current = current.parent

    def search(self):
        """Performs the UCT search on a node for given iterations
        :returns: optimal action based on search"""
        for i in range(self.iterations):
            leaf = self.select_simulation()  # Steps 1 and 2
            result = leaf.simulate()  # Step 3
            leaf.backpropagate(result)   # Step 4

        # Return action of child that was most visited
        #### TODO: Some sources say focus on visits, others say wins,
        #### and one presumes others would say wins/visits. I don't know
        #### What's best.
        child_visits = np.array([child.visits for child in self.children])
        chosen_action = self.children[np.argmax(child_visits)].action
        return chosen_action
