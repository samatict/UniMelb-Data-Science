"""
:filename: player.py
:summary: Base class for any MPMixPlayer (Chexers)
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################

# Standard modules
from math import inf
from time import process_time
from collections import defaultdict

# User-defined files
from mechanics import (
    create_initial_state, num_opponents_dead, apply_action, possible_actions,
    get_remaining_opponent, Z_hash
)
from moves import get_axial_ordered, get_cubic_ordered
from book import opening_moves

from algorithms.logic import mp_mix
from algorithms.adversarial_algorithms import paranoid, part_A_search
from algorithms.heuristics import  two_player_heuristics, end_game_heuristic, runner

# Global imports
from mechanics import PLAYER_HASH, MAX_EXITS

PATH = list()

######################## MP-Mix Player #######################
class MPMixPlayer:
    MID_GAME_THRESHOLD = 0 # The first two moves for each player (four possible good moves)
    END_GAME_THRESHOLD = 99

    def __init__(self, colour):
        """
        Initialises an MPMixPlayer agent.
        """
        self.colour = colour
        self.state = create_initial_state()
        self.clock = 0
        self.counts = defaultdict(int)

    def update(self, colour, action):
        """
        Updates a players action and adds a turn count.
        """
        self.state = apply_action(self.state, action)
        self.counts[Z_hash(self.state)] += 1

    def action(self):
        """
        Returns an action given time constraints (55 seconds CPU)
        """
        if not self.state[self.colour]:
            return ("PASS", None)

        if self.clock <= 50:
            start = process_time()

            if num_opponents_dead(self.state) == 1:
                action = self.run_2_player()
            elif num_opponents_dead(self.state) == 2:
                action = self.djikstra()
            elif self.start_mid_game():
                action = self.mid_game()
            else:
                action = self.early_game()
            self.clock += process_time() - start
            print(self.clock)
        else:
            action = self.greedy_action()

        return action

    def early_game(self):
        """
        :strategy: Uses the best opening moves found by the Monte Carlo method. (Booking)
        If opening move not available, run paranoid and make sure that we maintain good piece structure
        """
        return opening_moves(self.state, self.colour) if not False else paranoid(self.state, self.counts, end_game_heuristic, self.colour)[1]

    def mid_game(self):
        """
        :strategy: Runs the MP-Mix Algorithm.
        :returns: The best evaluated function. If True is returned, we are at a good level to attempt a greedy approach.
        """
        action = mp_mix(self.state, self.counts, end_game_heuristic, defence_threshold=0, offence_threshold=0)

        if action == True: # if True then run Greedy
            return self.end_game()
        return action

    def run_2_player(self):
        """
        :strategy: Run the paranoid algorithm with a higher depth.
                   This works because paranoid defaults to alpha-beta by ignoring
                   dead players.
        """
        action = mp_mix(self.state, self.counts, two_player_heuristics, defence_threshold=0, offence_threshold=0, two_player=True)
        if action is False: # If False just use Dijkstra (we are sufficiently ahead)
            action =  self.djikstra(single_player=False)
        elif action is True: # if True then run Greedy
            return self.end_game()
        return action

    def end_game(self):
        """
        :strategy: Use booking or a stronger quiesence search
        """
        return self.greedy_action()

    def djikstra(self, single_player=True):
        """
        :strategy: If everyone is dead, it becomes Part A. Literally Part A code...
        """
        global PATH
        FLAGS = ["MOVE", "JUMP", "EXIT"]

        # AKIRA - RETURN DIJKSTRA'S GIVEN A PLAYER IS STILL ALIVE
        if not single_player:
            state = dict()
            state['colour'] = self.colour

            # TODO: Calculate jump distance for each piece and then return closest pieces for exit
            n_exited = self.state["exits"][self.colour]
            n = MAX_EXITS - n_exited

            alive_opponent = get_remaining_opponent(self.state)

            temp = sorted(
                [get_cubic_ordered(tup) for tup in self.state[self.colour]],
                key=lambda x: x[PLAYER_HASH[self.colour]],
                reverse=True
            )
            state['pieces'] = [get_axial_ordered(tup) for tup in temp[:n]]
            state['blocks'] = [get_axial_ordered(tup) for tup in temp[n:]] + self.state[alive_opponent]
            action = list(map(lambda x: x.action_made, part_A_search(state)))[1] # attempting the runner so take first move
            # (pos, flag, new_pos=None)

            return (FLAGS[action[1]], action[0]) if FLAGS[action[1]] == "EXIT" else (FLAGS[action[1]], (action[0], action[2]))

        if not bool(PATH):
            # Create part_A appropriate data
            state = dict()
            state['colour'] = self.colour

            # TODO: Calculate jump distance for each piece and then return closest pieces for exit
            n_exited = self.state["exits"][self.colour]
            n = MAX_EXITS - n_exited

            temp = sorted(
                [get_cubic_ordered(tup) for tup in self.state[self.colour]],
                key=lambda x: x[PLAYER_HASH[self.colour]],
                reverse=True
            )
            state['pieces'] = [get_axial_ordered(tup) for tup in temp[:n]]
            state['blocks'] = [get_axial_ordered(tup) for tup in temp[n:]]

            PATH = list(map(lambda x: x.action_made, part_A_search(state)))[1:]
            print(PATH)

            # (pos, flag, new_pos=None)
            PATH = [(FLAGS[x[1]], x[0]) if FLAGS[x[1]] == "EXIT" else (FLAGS[x[1]], (x[0], x[2])) for x in PATH]

            # (FLAG_str: (pos1, pos2=None))
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| GG! 1 PLAYER GAME DIJKSTRA")
        return PATH.pop(0)

    def start_mid_game(self):
        """
        Starts mid game after 3 moves per player.
        """
        if self.state["depth"] == self.MID_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to midgame")
        return (self.state["depth"] >= self.MID_GAME_THRESHOLD)

    def start_end_game(self):
        """
        Determines when to shift strategy to the end game given deciding factors.
        TODO: Add a flag once a player has been eliminated
        """
        if self.state["depth"] == self.END_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to endgame")
        return (self.state["depth"] >= self.END_GAME_THRESHOLD)

    def greedy_action(self):
        """
        :strategy: Choose the best action without considering opponent moves.
        """
        best_eval, best_action, best_new_action = -inf, None, None

        for action in possible_actions(self.state, self.colour):
            new_state = apply_action(self.state, action)
            new_eval = runner(new_state)[PLAYER_HASH[self.colour]]
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = action
                if Z_hash(new_state) not in self.counts:
                    best_new_action = action
        return best_new_action if not None else best_action
