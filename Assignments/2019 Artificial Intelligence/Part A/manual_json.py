""" json_board.py

Easy creation of new state by command line entry.
Always appends to tests

"""

from formatting import *
from moves import *

def program_board():
    """Creates a board given cmd line specification"""
    state = {"colour": None, "pieces": list(), "blocks": list()}
    print_board(None, number_hexes=True)
    while(True):
        state['colour'] = input("Enter colour {red, blue, green} >> ")
        if state['colour'] not in {'red', 'blue', 'green'}:
            print ("Invalid colour")
        else:
            break

    while(True):
        pieces = input("Enter pieces separated by commas >> ").strip().replace(" ", "").split(",")
        # Checks that a) all unique and b) all valid
        print(len(set(pieces)), len(pieces), sum([int(i) in range(1,38) for i in pieces]))
        if not (len(set(pieces)) == len(pieces) == sum([int(i) in range(1,38) for i in pieces])):
            print("Invalid piece(s)")
        else:
            state['pieces']  = [list(VALID_COORDINATES[int(i)-1]) for i in pieces]
            state['pieces'].sort()
            break
    while(True):
        blocks = input(f"Enter blocks separated by commas >> ").strip().replace(" ", "").split(",")
        # Checks that a) all unique and b) all valid
        if not (len(set(blocks)) == len(blocks) == sum([int(i) in range(1,38) for i in blocks])):
            print("Invalid block(s)")
        elif len(set(blocks).intersection(set(pieces))):
            print("Piece/block overlap")
        else:
            state['blocks']  = [list(VALID_COORDINATES[int(i)-1]) for i in blocks]
            state['blocks'].sort()
            break

    output = str(state).replace(")","]").replace("(","[").replace("'", '"')
    print(output)
    import os
    os.chdir('tests')
    name = input("Enter name (without .json) for file >> ")
    new_file = open(name + ".json" , "w")
    new_file.write(output)
    new_file.close()

if __name__ == "__main__":
    program_board()
