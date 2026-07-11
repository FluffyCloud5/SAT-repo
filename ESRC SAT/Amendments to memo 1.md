
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
    - Changed move(a: angle, l: length) functions to move(x: East, y: North)
    - Changed v in V from G = (V,E) to be named by coordinate location.

A2 - Salient Features:
- Changed Location and direction in the salient features as they are stored differently and abstracted differently than in memo 1.

A3:
 - Added tuple ADT.
- Updated the ADTs used in the algorithm
- The ADT was updated for arrays as they are immutable in length.

B - Algorithmic Design:
- Removed the DFS option as it is suboptimal
- Added a Divide and Conquer algorithm
- Changed the discussion around the new algorithm, and moved it to after the C section.

C - Code:
- To BFS code and pseudocode: 
	- change move and exit calls
- Accommodated for all algorithms, including at least python code for all of the different algorithms.
- Changed the representation of the facility to accommodate for multi-wings.
- Changed the output section to only give the raw output.
- Added a comparison section to compare algorithms.
- Changes to pseudocode conventions including removing all END... statements.


D - Justification: 
- Modified the justification to accommodate for the new chosen algorithm (Brute Force).
