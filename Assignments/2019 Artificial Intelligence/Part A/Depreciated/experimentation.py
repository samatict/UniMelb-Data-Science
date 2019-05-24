""" Experimentation.py

"""

from sys import argv
import json
from moves import *
from classes import *
from queue import Queue

def optimal_relaxed_paths(state, cost):
    """Given relaxed costs, infers all optimal paths from pieces to exit"""
    optimal_neighbours = defaultdict(set)
    queue = Queue()
    for piece in state['pieces']:
        queue.put(piece)
    while not queue.empty():
        new = queue.get()
        for neighbour in set(move(new, state, True)).union(set(jump(new, state, True))):
            if cost[neighbour] < cost[new]:
                optimal_neighbours[new].add(neighbour)
                queue.put(neighbour)
        # All optimal neighbours computed
    return optimal_neighbours

# Annoying: it is possible that JP paths are used on paths that are NOT optimal for relaxed solution
# HOWEVER it seems that despite this, only JP's on relaxed paths occur - that is, they are predictable
# SOLN: You need relaxed path hierachies for ALL positions

# Intuition: relaxed_paths is a bare minimum cost (the best you could do)
# So aspire to have actual path lie on a relaxed path as much as possible
# More coverage (without expense of cost) = lower cost
# BIG Q: Can you benefit from moving to sub-optimal positions?
     # IDEA: ... no. Going to suboptimal = same or higher evaluation + 1 wasted.
     # So in BEST CASE, you get optimal + 1 > optimal.
     # ACTUAL: 'suboptimal' with respect to relaxed is POSSIBLE (see 30MOVE - it does JP's that don't lie on any relaxed path from piece origins)

def straight_paths(cost, rpaths):
    """Given relaxed paths, costs and state, finds all JP-possible RELAXED paths"""
    """CONDITION: a point a in the direction b is jump-worthy if:
    0. a is not inf (please)
    1. a+b is not inf (room for another piece to be jumped over)
    2. a+2b is not inf (room for landing)
    The JP-value of a path from a in b = JP(a,b) = a + (n-2)*b, n being # consecutive non-infs (incl. a) in direction b
    VALUES:
    - -3 ==> Not valid
    - -2 ==> I'm inf
    - -1 ==> I'm notinf, next one is
    - 0 ==> I'm notinf, nor is next, but one after that is
    - 1+ ==> We can jump n times consecutively
    Key logic:
    - JP(a,b) = k, k >-2 ==> JP(a+b,b) = max(-2, k-1)
    - JP(a,b) = k, a-b non-inf ==> JP(a-b,b) = k+1
    - a is inf ==> ALL move/jump neighbours are JP-0 in direction of a"""

    """Output structure: dictionary of locn:dirxn:JP(locn, dirxn)"""

    # logic
    JP = defaultdict(lambda: defaultdict(int))
    for location in rpaths:
        for dirxn in POSSIBLE_DIRECTIONS:
            current = location
            m_adjacent = Vector.add(location, dirxn)
            j_adjacent = Vector.add(m_adjacent, dirxn)
            if m_adjacent in rpaths and j_adjacent in rpaths[current]:
                JP[location][dirxn] += 1
                current = m_adjacent
                m_adjacent = j_adjacent
                j_adjacent = Vector.add(m_adjacent, dirxn)
                while m_adjacent in rpaths and j_adjacent in rpaths[current]:
                    JP[location][dirxn] += 1
                    current = m_adjacent
                    m_adjacent = j_adjacent
                    j_adjacent = Vector.add(m_adjacent, dirxn)




            '''if dirxn not in JP[location]: # Not already visited before
                # Check next one exists
                new = Vector.add(location, dirxn)
                if new not in rpaths:
                    # Then you can't even consider this as a JP
                    continue
                # Ok you might be able to continue to next place.
                current_path = [location]
                current = new
                while (current in rpaths and cost[current] != INF):
                    # print(f"{current} in dirxn {dirxn} => ", end="")
                    current_path.append(current)
                    current = Vector.add(current, dirxn)
                else:
                    # Go through path from recent to first, updating VALUES
                    for point in current_path[::-1]:
                        JP[point][dirxn] = max(current_path.index(point) - 2, 0)'''

    return JP

direction_template = """
#      ,-' `-._,-' `-.
#     | {04:} | {03:} |
#     |  0,-1 |  1,-1 |
#  ,-' `-._,-' `-._,-' `-.
# | {05:} |       | {02:} |
# | -1, 0 |{00:}|  1, 0 |
#  `-._,-' `-._,-' `-._,-'
#     | {06:} | {01:} |
#     | -1, 1 |  0, 1 |
#      `-._,-' `-._,-'           """

if __name__ == "__main__":
    with open(argv[1]) as file:
        data = json.load(file)

    data = convert_to_tuples(data)
    cost = dijkstra_board(data)
    print_board(debug(data), debug=False)
    print_board(cost)
    rpaths = optimal_relaxed_paths(data, cost)
    JP = straight_paths(cost, rpaths)
    print("\n".join(f"{locn}: {rpaths[locn]}" for locn in rpaths))
    for locn in JP:
        print(direction_template.format(f"{locn}".center(7), *[f"{JP[locn][i]}".center(5) for i in POSSIBLE_DIRECTIONS]))
