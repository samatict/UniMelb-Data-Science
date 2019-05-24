"""
:filename: player.py
:summary: Base class for any MPMixPlayer (Chexers)
:authors: Akira Wang (913391), Callum Holmes (899251)
"""

########################### IMPORTS ##########################

# Standard modules
from math import inf
from time import process_time

# User-defined files
from mechanics import create_initial_state, num_opponents_dead, apply_action, possible_actions, get_remaining_opponent
from moves import get_axial_ordered, get_cubic_ordered
from book import opening_moves

from algorithms.logic import mp_mix
from algorithms.adversarial_algorithms import paranoid, part_A_search
from algorithms.heuristics import achilles_unreal, speed_demon, end_game_heuristic, two_player_heuristics

from structures.gamenode import GameNode
from structures.ttplayer import TTPlayer

# Global imports
from mechanics import PLAYER_HASH, MAX_EXITS

PATH = list()

######################## MP-Mix Player #######################
class MPMixPlayer(TTPlayer):
    MID_GAME_THRESHOLD = 0 # The first three moves for each player (four possible good moves)
    END_GAME_THRESHOLD = 99

    def __init__(self, colour):
        """
        Initialises an MPMixPlayer agent.
        """
        super().__init__(colour)
        self.clock = 0

    def action(self):
        """
        Returns an action given time constraints (55 seconds CPU)
        """
        if not self.root.state[self.colour]:
            print("Thought no actions were available as colour {self.colour}")
            return ("PASS", None)

        if self.clock <= 70:
            start = process_time()

            if num_opponents_dead(self.root.state) == 1:
                action = self.run_2_player()
                if (action == None): print("run2"); GameNode.debugger(self.root)
            elif num_opponents_dead(self.root.state) == 2:
                action = self.djikstra()
                if (action == None): print("dijk"); GameNode.debugger(self.root)
            elif self.start_mid_game():
                action = self.mid_game()
                if (action == None): print("mid"); GameNode.debugger(self.root)
            else:
                action = self.early_game()
                if (action == None): print("earl"); GameNode.debugger(self.root)

            self.clock += process_time() - start
            print(self.clock)
        else:
            action = self.greedy_action()
            if (action == None): print("greed"); GameNode.debugger(self.root)

        return action

    def action_logic(self):
        """
        Returns an action given conditions.
        """
        raise NotImplementedError

    def early_game(self):
        """
        :strategy: Uses the best opening moves found by the Monte Carlo method. (Booking)
        """
        return opening_moves(self.root.state, self.colour) if not False else paranoid(self.root.state, self.root.counts, achilles_unreal, self.colour)

    def mid_game(self):
        """
        :strategy: Runs the MP-Mix Algorithm.
        :returns: The best evaluated function. If True is returned, we are at a good level to attempt a greedy approach.
        """
        action = mp_mix(self.root.state, self.root.counts, end_game_heuristic, defence_threshold=0, offence_threshold=0)

        if action == True: # if True then run Greedy
            return self.end_game()
        return action

    def run_2_player(self):
        """
        :strategy: Run the paranoid algorithm with a higher depth.
                   This works because paranoid defaults to alpha-beta by ignoring
                   dead players.
        """
        action = mp_mix(self.root.state, self.root.counts, two_player_heuristics, defence_threshold=0, offence_threshold=0, two_player=True)
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
            n_exited = self.root.state["exits"][self.colour]
            n = MAX_EXITS - n_exited

            alive_opponent = get_remaining_opponent(self.root.state)

            temp = sorted(
                [get_cubic_ordered(tup) for tup in self.state[self.colour]],
                key=lambda x: x[PLAYER_HASH[self.colour]],
                reverse=True
            )
            state['pieces'] = [get_axial_ordered(tup) for tup in temp[:n]]
            state['blocks'] = [get_axial_ordered(tup) for tup in temp[n:]] + self.root.state[alive_opponent]

            action = list(map(lambda x: x.action_made, part_A_search(state)[0]))[1] # attempting the runner so take first move
            # (pos, flag, new_pos=None)

            return (FLAGS[action[1]], action[0]) if FLAGS[action[1]] == "EXIT" else (FLAGS[action[1]], (action[0], action[2]))

        if not bool(PATH):
            # Create part_A appropriate data
            state = dict()
            state['colour'] = self.colour

            # TODO: Calculate jump distance for each piece and then return closest pieces for exit
            n_exited = self.root.state["exits"][self.colour]
            n = MAX_EXITS - n_exited

            temp = sorted(
                [get_cubic_ordered(tup) for tup in self.state[self.colour]],
                key=lambda x: x[PLAYER_HASH[self.colour]],
                reverse=True
            )
            state['pieces'] = [get_axial_ordered(tup) for tup in temp[:n]]
            state['blocks'] = [get_axial_ordered(tup) for tup in temp[n:]]

            PATH = list(map(lambda x: x.action_made, part_A_search(state)[0]))[1:]

            # (pos, flag, new_pos=None)
            PATH = [(FLAGS[x[1]], x[0]) if FLAGS[x[1]] == "EXIT" else (FLAGS[x[1]], (x[0], x[2])) for x in PATH]

            # (FLAG_str: (pos1, pos2=None))
        print(f"\n\t\t\t\t\t\t\t\t\t\t\t\t* ||| GG! 1 PLAYER GAME DIJKSTRA")
        return PATH.pop(0)


    def start_mid_game(self):
        """
        Starts mid game after 3 moves per player.
        """
        if self.root.state["depth"] == self.MID_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to midgame")
        return (self.root.state["depth"] >= self.MID_GAME_THRESHOLD)

    def start_end_game(self):
        """
        Determines when to shift strategy to the end game given deciding factors.
        TODO: Add a flag once a player has been eliminated
        """
        if self.root.state["depth"] == self.END_GAME_THRESHOLD:
            print(f"* ({self.colour}) is switching to endgame")
        return (self.root.state["depth"] >= self.END_GAME_THRESHOLD)

    def greedy_action(self):
        """
        :strategy: Choose the best action without considering opponent moves.
        """
        if not self.root.state[self.colour]:
            return ("PASS", None)

        best_eval, best_action = -inf, None

        # TODO: Use TT to prevent recalculation

        for child in self.root.children:
            if child.action[0] == "EXIT":
                return child.action
            new_eval = speed_demon(child.state)[PLAYER_HASH[self.colour]]
            self.root.child_evaluations[child.action] = new_eval
            # ONLY select non-repetitive moves
            if new_eval > best_eval:
                best_eval = new_eval
                best_action = child.action
        self.root.fully_evaluated = True

        if best_action == None:
            print("The none error.")
            GameNode.debugger(self.root)
        return best_action
