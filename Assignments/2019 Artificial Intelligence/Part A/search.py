"""
################################################################################
##########    COMP30024 Artificial Intelligence, Semester 1 2019    ############
##########          Solution to Project Part A: Searching           ############
##########       Akira Wang (913391), Callum Holmes (899251)        ############
##########                       Team: _blank_                      ############
################################################################################
"""

########################## IMPORTS ###########################
# Standard modules
from json import load
from sys import argv

# User-defined files
from formatting import convert_to_tuples, pikawin
from algorithms import *

######################### FUNCTIONS ##########################

def main():
    # Read argv input for initial state
    with open(argv[1]) as file:
        data = load(file)

    data = convert_to_tuples(data)

    print("# Prepare for amazingness")
    optimal_solution = IDA_control_loop(data, dijkstra_heuristic)

    if (optimal_solution is not None):
        print(f'# A solution was found! Cost: {optimal_solution.depth}\n# Sequence of moves:')
        path = list()
        node_temp = optimal_solution

        # Re-assemble path taken
        while (node_temp is not None):
            path.append(node_temp)
            node_temp = node_temp.parent

        for move in path[::-1]:
            if (move.action_made is not None):
                piece, action, dest = move.action_made
                if (action == MOVE):
                    print(f'MOVE from {piece} to {dest}.')
                elif (action == JUMP):
                    print(f'JUMP from {piece} to {dest}.')
                elif (action == EXIT):
                    print(f'EXIT from {piece}.')
        print(pikawin)
    else:
        print(f'# ERROR: No solution found at this depth')

# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
