# Part A - report.pdf

## Authors: Callum Holmes (899251), Akira Wang (913391)
## Team: _blank_

MUST BE 1-2 pages STRICTLY

### FOCUS QUESTIONS ARE ITALICISED

#### *How have you formulated the game as a search problem?
(You could discuss how you view the problem in terms of states, actions, goal tests, and path costs, for example.)*

## Problem Formulation (answers Q1)

The problem of navigating pieces across a Chexers board to successful exit is:
1. Fully Observable (all exits are known, and all piece and board numbers and locations measurable)
2. Deterministic (There is no probability in the problem; outcomes of actions are certain)
3. Sequential (The benefit of a given move )
4. Static (There is no time factor in the actual problem; the game state/environment remains equal whilst actions are being decided)
5. Discrete (Finite number of outcomes, either all pieces are exited or not)

The problem was interpreted as a search problem on a directed graph of possible game states, reachable by playing different actions.
- States: the exact number and positions of each player piece and block.
- Actions: Move, Jump, and Exit (a move is assumedly always possible as per project specifications). All actions are of equal cost.
- Goal tests: Goal state achieved if no player pieces remaining on board, and has not been achieved otherwise.
- Path costs: Calculated as total no. of actions made (as all actions costed uniformly). An optimal path is one that reaches the goal with least possible cost from an origin state.

#### *What search algorithm does your program use to solve this problem, and why did you choose this algorithm?
(You could comment on the algorithm’s efficiency, completeness, and optimality. You could explain any
heuristics you may have developed to inform your search, including commenting on their admissibility.)*

## Algorithmic Approach (Answers Q2)

### Heuristic
Our heuristic was derived from a relaxed version of the search problem, which allows piece(s) to jump freely, even if there is no block/piece to jump over (an empty space to land still had to be available). In this version, pieces would not need to converge in attempt to jump over each other and reduce path costs, as pieces can reach the goal independently, at maximal speed, at their own independent minimal cost.

`Dijkstra_heuristic` evaluates the total minimal cost to exit all pieces if they move independently under these relaxed conditions. The board with the blocks (but not pieces) is preprocessed using an adapted Dijkstra graph search algorithm with a priority queue to map the minimum cost of exiting for a piece at any location. To evaluate a state, the cost associated with each piece position is aggregated.

#### Benefits
- **Admissibility**: The heuristic is admissible. The only difference between the relaxed and actual version of the problem is that 'relaxed pieces' can jump more often - meaning that they will never reach the goal slower than pieces in the actual problem.
- **Semi-memoizable**: The heuristic is computed by adding the cost of each piece's location for any child state. However only the blocks and goal positions determine the cost evaluation for each hex. As these are static for all possible states descending from the initial board state, the board costs only need computing once; then the heuristic can be evaluated in constant O(m) time/space computation, m being the number of player pieces. Given m is small, it is effectively O(1) time/space complexity to evaluate any node.

#### Limitations
For dense boards this heuristic can find optimal jumping paths and weight them as the best action to take - looking at **Figure 1 (image of test_file3_evaluation)**, pieces on this board would have ample jumping opportunities even if isolated - hence almost all positions have a clearly optimal neighbour.

However, for sparse graphs with few blocks, the heuristic evaluates the board in a 'flat' fashion, which can degenerate evaluations to uniform-cost search. **Figure 2 (image of 1BLOCK_evaluation)**, pieces on the bottom-left fringe would be indifferent to moving sideways or forwards, and no path is obviously optimal.

In other words, where there is great uncertainty (branching factor), the heuristic is weak. In cases with low branching factor (high certainty), evaluations are stronger.

Furthermore, as jumping is always possible in the relaxed version, the relaxed problem does not care if pieces try to jump over each other. This carries over to the heuristic - it fails to value movement that allows 'leapfrogging' piece movements (where a pair of pieces jump over each other repeatedly), which requires pieces make moves that converge towards other pieces' in addition to exits.

As leapfrogging is a stronger option on sparse boards, overall the heuristic significantly underestimates true solution cost in sparse graphs due to its simplifying assumptions.

### Search algorithm: IDA*
Iterative Deepening A* (IDA*) was used to search the game tree. IDA* combines the best-first search aspect of A*, evaluating states as f(n) = g(n) + h(n), where g(n) is the path cost to reach the state from the initial state, and h(n) a heuristic estimate of the cost to reach the goal from the state. Both algorithms are *optimal* given an admisible heuristic is used and are *complete* if solution states exist (which is assumed for this problem). [1]

We found in experimentation that IDA* had stronger performance on average compared to A* even with optimisations, and so was our algorithm of choice.s

As the entire solution path must be stored for this problem, all 'parent' states must be referenced. We used a tree structure, where child nodes are game states descending from a parent game state. This however meant O(b^m) space-complexity (b being branching factor, m the length of optimal path).

#### *What features of the problem and your program’s input impact your program’s time and space requirements?
(You might discuss the branching factor and depth of your search tree, and explain any other features of the
input which affect the time and space complexity of your algorithm.)*

## Problem and Input Complexity & Optimisations (Answers Q3)

### Program Input Considerations
The input is initially stored in a json file as a dictionary, containing a string representation for the player and two lists for the pieces and blocks, representing coordinates as lists of length 2. This is inefficient: coordinates of blocks/pieces are never altered, and the primary use of a state is to evaluate membership of other locations (to derive potential moves/jumps and exit opportunities). Furthermore, the data supplied is incomplete - information such as where pieces can exit from, and valid coordinates for movement, are not passed.

To deal with this: while the string representation for colour was retained, all coordinates were casted into tuples, which was found to reduce time-complexity. Furthermore, possible exit locations (for each colour) and valid board coordinates were pre-defined in global dictionaries/lists to avoid recalculations.

### Problem Considerations

Regarding depth: The path cost to achieve a goal state can vary from 1 to over 30 steps in some initial states, particularly where more pieces are used, the result being that the game tree has high average depth. Furthermore, a state can be entered repeatedly by 'backtracking', only adding to the depth and diluting the tree with repetition.

Regarding branching: In the worst case, when a state has a few, sparsely spread blocks, a game state can have up to 24 possible actions - movement in 6 directions for 4 pieces. Due to this, the problem tree has potental to be highly dense, which encroaches on time and space complexity.

Optimisations to counter depth and branching included:

1. The algorithm was coded to always exit pieces if exit actions were possible at any stage, reducing branching in the endgame to some extent.

2. A Transposition Table was used to memoize the unique states (and state evaluations) encountered during a search, using a collision-free hash function to index states efficiently. Newly expanded nodes were trimmed if they were of equal or worse total cost than a previous encounter of the same state - preventing re-searching of identical subtrees and ensuring that stored states were the most optimally reached so far

### Asymptotic Time-Space Complexity Analysis?
- **Use valgrind for space, it's better than getsizeof macro 4sure, infer a good O() and compare to theoretical estimates**
- **Maybe graph # generated vs bash time for test files, infer a good O() cost and compare to theoretical estimates**

Ultimately, runtime data indicates an average branching factor of about 8.5-9.5 generated children per parent. **MAY NEED FURTHER EVIDENCE TO CONCLUDE THAT THIS IS AN IMPROVEMENT FROM THE STATUS QUO**
The data suggests that our trimming optimisations only marginally decrease the branching factor. This is expected; our algorithms evaluates children post-creation.
- **Measure branching factor with a tree sweep post-generation TICK - average b is about 9-10 (10 for harder problems), average depth varies b/t 3 for easy, and 7-8 for difficult. Given difficult problems actually have depth 20-30, this is a a strong reduction in net generation - reduced from O(b^{d_optimal}) to O(b^{d_optimal/3})**

# Bibliography
StackExchange (n.d.) [Internet]. Available from: https://ai.stackexchange.com/questions/8821/how-is-iterative-deepening-a-better-than-a?fbclid=IwAR1j3LSIj9_p13C7Kr8bJuWgWi2dWvVanSKRWS5zebufixNq3ZPntyknNPU (Accessed 08/04/2019).
