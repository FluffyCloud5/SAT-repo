
Assumptions: 
- Add assumption that the interwing corridors are of length 4 in physical space (to match the representation provided).

Problem Outline: change to match new problem.


A1:
- Inputs:
    - add location property to VP giving a tuple as a location
    - add wing property to VP
    - remove cardinal angle from EP
- Outputs:
    - change move(a: angle, l: length) functions to move(x: East, y: North)

A2 - Salient Features:
- Location and direction are stored differently and abstracted differently.

A3:
- ADTs used in the algorithm

B - Algorithmic Design:
- Remove the DFS option as it is quite bad.
- Add a new **<u>brute force</u>** option that divides and conquers (ish).

C - Code:
- change based of algo, make it to accommodate for different algorithms.

D - Justification: 
- make the justification for the new algorithm.