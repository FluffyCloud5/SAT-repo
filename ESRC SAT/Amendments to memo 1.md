
Assumptions: 
- Added an assumption that the inter-wing corridors are of length 4 in physical space (to match the representation provided).

Problem Outline: Changed to match new problem scope of memo A1.

Definitions: Changed the definition of a corridor.

A1:
- Inputs:
    - Added location property to VP giving a tuple as a location
    - Added wing property to VP
    - Removed cardinal angle from EP
- Outputs:
    - change move(a: angle, l: length) functions to move(x: East, y: North)
    - change output to have location of vertices not vertex names as the location of vertices. 

A2 - Salient Features:
- Changed Location and direction in the salient features as they are stored differently and abstracted differently than in memo 1.

A3:
 - Added tuple ADT.
- Updated the ADTs used in the algorithm
- Cannot mutate arrays, so ADT was updated for arrays.

B - Algorithmic Design:
- Removed the DFS option as it is quite bad for this problem.
- Added a Divide and Conquer solution
- Changed the discussion around the new algorithm

C - Code:
- To BFS code and pseudocode: 
	- change move and exit calls
- Accommodates for all options, including at least python code for all of the different algorithms.
- Change the representation to accommodate for new facility
- Change the output to only give raw output
- Added a comparison section to compare algorithms.
- Changes to pseudocode conventions including removing all END... statements.


D - Justification: 
- Modified the justification to accommodate for the new chosen algorithm (Brute Force).


---------------------------------

Read Memo A1 to make sure all requirements have been met