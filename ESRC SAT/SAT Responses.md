Math Symbols: ∀∃∈∉≈ ⊆⊂⊈⊄∧∨⇒⇔¬←

# Problem Specification:

The problem is contained within the Emberlight Subterranean Research Complex (ESRC). Inside the ESRC there might multiple Sector Grids, and inside each sector grids there exist sectors (currently 144 sectors per sector grid 12x12). Due to unique circumstances, a CRUDY-1 (Corridor Reconnaissance and Utility Drone Year 1) needs to be employed to traverse a sector grid to collect critical supply units and bring them to an extraction point.

## Definitions:
Spaces:
- ESRC: Emberlight Subterranean Research Complex, the scope of this problem (currently)
- Sector Grid: A grid of sectors, contained within the ESRC.
- Sector: A single unit of space, which can be occupied by an AS can be connected to other sectors via corridors. 
Movement Options
- Corridor: Connects two adjacent sectors in the same sector grid that don't have a wall in-between them. Can be bidirectional or one-way.
Types of Sectors: 
- Exit: (or Extraction Point), this is where an AS can end its journey. 
- Entry: (or starting sector), this is where an AS begins its journey.
- Supply Unit: the sector contains a supply unit\
- Vertex of interest: an exit, an entry or a supply unit sector.
Abbreviations: 
- G: (Graph of a Sector Grid) = (V,E)
- SU: (Supply Unit)
- AS: (Autonomous System) 
- EP: (Edge Properties)
- VP: (Vertex Properties)
- SUP: (Supply Unit Properties)
- ASP: (Autonomous Systems Properties)



## Assumptions: 
1.  An Autonomous System (AS) knows the layout of the ESRC sector grid before it navigates it. (e.g. it has the blueprints)
2. The algorithm A1 is asking about is the algorithm that the AS is running. 
3. The AS can turn on the spot. 
4. The ASs can navigate in all directions without turning, and the AS starts oriented in the cardinal direction corresponding to 0°\*.
	- \*The cardinal angle of 0° doesn't have to be pointing north, it just has to be consistent. Also that the AS is facing 0° at the entry just ensures it knows which way to go based of the graph. 

# Part A - Problem Specification:

## A1 - Algorithmic problem statement:

### Inputs:

The input is a <b><u>directed</u></b> unweighted graph paired with one map, four other nested maps and two more sets.
Note, the five maps are just providing properties for the four sets (as a graph is just two sets) and properties of the whole environment.

G: (Graph of a Sector Grid) = (V,E)
SU: (Supply Unit)
AS: (Autonomous Systems) 
EP: (Edge Properties)
VP: (Vertex Properties)
SUP: (Supply Unit Properties)
ASP: (Autonomous Systems Properties)

#### Graph (Sector Grid, G=(V,E)):
Graph, G = (V,E) where V = set of all vertices in G and E = set of all edges in G. Each Vertex in V is a sector and each edge in E is a corridor between two sectors.

This can be represented as:

G = (V,E)

V = {v | v is a sector in the Emberlight Subterranean Research Complex}

E = {(u,v) | u,v∈V ∧ u is adjacent to v ∧ direct movement can be taken from u into v, without going through any other sectors}

#### Set 1 (Supply Units (SU):
This is a set containing all supply units in the Sector Grid. 
SU = {x | x is a supply unit in the Sector Grid}.

#### Set 2 (Autonomous Systems (AS)):
This is a set containing all Autonomous Systems (AS) being deployed in the Sector Grid.
AS = {x | x is an Autonomous System being deployed in the Sector Grid}

#### **NOTE on Maps:** 
The following four ADTs are maps of maps, where the key gives you a map of properties of that object. The properties might have keys with values, such as 'weight: 1', but not all objects of the same type will have maps of properties containing the same key values, as they may be not applicable to one object but not the other. An example: 
VP\[v\] = {"supply_unit": "s1", is_exit: True}
whereas: 
VP\[u\] = {"is_entry": True}.

#### Map 1 (Corridor Properties (EP):

The first map, EP (Edge Properties) takes the edges as keys and returns a map potentially detailing:
- a real number indicating which direction this edge is pointing (cardinal angle).
Beyond current scope:
- a real number indicating the cost to traverse (as it is all the same)
- a real number indicating the stability of the corridor.
- a real number indication the length of the corridor.
The map associated with one edge may not include all the keys listed above, if a certain property of the edge is not applicable. For example if the edge has no cost of traversal, it will not include a key associated with it. 

In the current problem scope, a possible implementation of this is: 
EP = {(u,v):{ "cardinal_angle": real number (cardinal angle from u to v)}
	| u,v ∈ V ∧ (u,v) ∈ E}

#### Map 2 (Sector Properties (VP)):

This map, VP (Vertex Properties) takes vertices (or sectors) as keys and returns a map potentially containing the properties:
- a string indicating what supply unit lies within the sector, or null if no supply unit is contained, (if not specified it can be assumed no supply unit is in the sector).
- a Boolean value indicating whether it is an entry (assume False if not specified),
- a Boolean value indicating whether it is an exit (assume False if not specified).
Beyond current scope:
- a value indicating the stability of the sector.
- size
- shape

In the current problem scope, a possible implementation of this is: 
VP = {v : \{ 
	"supply_unit": nullable string (name of supply unit within the sector, null if it doesn't contain a supply unit),
	"is_entry": Boolean (true if the sector is an entry, false otherwise) ,
	"is_exit": Boolean (true if the sector is an extraction point, false otherwise )}
	| v ∈ V}

#### Map 3 (Supply Unit Properties (SUP)):

This map, SUP (Supply Unit Properties), takes a supply unit as a key, and returns a map of the properties of the supply unit. These properties may include
- a sector (of vertex of graph G) location (the sector on which the supply unit lies)
Beyond current scope:
 - a real number indicating the weight of the supply unit (as currently all the same and thus not needed)
- fragility 
- importance
- size
- lifespan
In the current problem scope, most of these properties of the supply units are currently irrelevant, so they won't be included in the map returned for each supply unit. Currently, only location will be considered. 
- A vertex, v, on which s, the supply unit lies
In the current problem scope, a possible implementation of this is: 
SUP = {s:{"location": v (the sector of the SU)} | v∈V∧s∈SU}

#### Map 4 (Autonomous System Properties (ASP)):
This map, ASP (Autonomous System Properties) takes Autonomous Systems (ASs) as keys and returns a map of properties of the AS, potentially including: 
- a vertex which is the starting location (or entry) of the AS.
~~- a real number indicating the cardinal direction AS begins facing.~~
**Beyond current scope:**
- a string indicating type (e.g. CRUDY-1) (as currently there is only one type)
- a real number indicating the total weight the AS can carry. (as currently this equals the total supply units on the map)
- a real number indicating how many supply units AS can carry at once. (that is different from the weight, right now they are the same so this is not necessary)
- a real number indicating total energy of the AS.
- a real number indicating how much energy a corridor takes. 
- a list of SUs that the AS has been assigned to extract. 
- a vertex indicating assigned extraction point for the AS.
- a real number indicating speed of the AS.

In the current problem scope, a possible implementation of this is: 
ASP (Autonomous System Properties) = {x:{"entry": v (indicates entry for AS)}| x ∈ AS ∧ v ∈ V}

#### Map 5 (Graph Properties (GP)): 
This map provides properties of the whole environment, such as 
- a Boolean value indicating whether emergency lighting is operational
- a time limit
These are currently all beyond the current scope of the problem so:
GP = {}
### Outputs

#### Computational Outputs
The outputs of the algorithm that the AS is running are: 
a map containing: 
- A walk of where the AS goes that minimizes total energy used and maximises the number of supply units extracted. It starts at an entry and ends at an exit. (as a list)
- Total energy expended (as a real number)
- Supply Units recovered (as these are collected instantaneously) (as a set)
It doesn't have to be a perfect solution, but it should aim to be an efficient one. 

so the output might look like: 
output = {"walk":  \[$v_1$,,$v_2$,,$v_3$,...,,$v_n$\],
	"energy_expended": real number,
	"supply_units_recovered": {$s_1$,$s_2$,$s_3$,...$s_m$}}

#### Environmental Outputs
It also has a continuous set of environmental outputs (controlling its actions) in the form of commands including: 
	1. move(a: angle, d: distance) → None         \# allows the AS to move 'd' distance at 'a' cardinal angle.
	2. exit() → None         \# if at an exit (extraction point), it allows the AS to exit the sector grid.
Note: no command is for picking up a supply unit as that is automatically done. 
Note: no command is for reading environment as it is currently assumed that the AS gets that as an input before the whole thing. 


### Constraints

1. The first vertex of the walk AS makes must be an entry.
2. The last vertex of the walk AS makes must be an exit.
3. $\forall i [i \in \mathbb{N} \land i \in [1,n] \implies v_i \in V]$ 
	- meaning all vertices in the walk must be vertices of graph G.
4. $\forall i [i \in \mathbb{N} \land i \in [1,n-1] \implies e_i \in E \land e_i = (v_i,v_{i+1})]$ 
	- meaning all edges in the walk must be edges of graph G and that the edge $e_i$ must be from $v_i$ to $v_{i+1}$.
5. Aim to maximise supply unit recovery while ensuring making it to an extraction point is possible. This means the walk traverses through as many sectors with supply units in them as possible. 
6. 5. Aim to minimise energy cost, which at this stage is proportional to the number of edges traversed in the walk, so ||walk|| should be minimised. At this stage, this is lowest priority compared to other constraints.

\*3 and 4 are simply ensuring the walk is indeed a walk on graph G.

## A2 - Salient Features: 

For each salient feature, state 
(a) what it is, 
(1) how it is modelled, 
(2) what is deliberately abstracted away and why.
1. Position 
	1. It is modelled as a vertex on a graph of the Sector Grid, in relation to other vertices on G. 
	2. The direct position (for example as GPS coordinates) is abstracted away and only shown in reference to that of the starting vertex (the entry), as the AS only needs to know where in the sector grid it is, not the whole world
2. Direction 
	1. This is modelled as a cardinal angle assigned to each edge of the graph G and the direction that the AS is facing. 0º doesn't have to be north, it only has to be consistent. 
	2. The physically layout of the sector grid is abstracted away into this grid, as it only matters how to get from one sector to another sector to be able to traverse the whole grid. This can be calculated using the direction. (i.e. only relative space matters, not absolute.)
3. Length 
	1. One unit of length is modelled using a real-valued number in the properties of the edges of the graph (in EP). (Currently) This is set to 1 for all edges.  
	2. The length of an edge (i.e. a corridor) can be abstracted away as (currently) all corridors have the same length, meaning the AS only has to move in multiples of the length of one of the edges of the graph.
4. Time
	1. Time is currently not modelled in the abstraction. 
	2. This is (currently) a safe abstraction as conditions are stable. 
5. Mass
	1. Mass is currently modelled as a unitless value uniform between the supply units, and another maximum load value for the AS.
	2. The unit is abstracted away as the relative mass is all that matters. Individual mass of the supply units however, isn't abstracted away.
6. Corridors
	1. These are modelled as two edges between the sectors it is between, representing the two ways that one can pass through a corridor. The direction of the corridor is modelled as an cardinal angle. 
	2. The shape of the corridor and the roughness of it is abstracted away as it is assumed that currently all corridors are traversable by the AS. This may or may not be a safe abstraction. The length of these corridors are abstracted away as they have the same length and the stability is abstracted away as it is assumed that currently conditions are stable.
7. Sectors
	1. These are modelled as Vertices on the graph G.
	2. The size and shape of the sectors are abstracted away as they are all assumed to be the same and traversable by the AS. Also the stability isn't modelled as it is assumed to be stable.
8. Walls
	1. These are modelled by the lack of an edge connecting the Vertices representing the sectors either side of it, marking it as untraversable. 
	2. Its existence is somewhat abstracted away and only marked with a 'this is not a route' label, which is fine since the AS can then choose simply never to try going through the wall. 
9. Supply Units
	1.  These are modelled with a location (being the vertex of G on which they sit) and their weight. 
	2. The supply units are assumed to all be strong enough to handle the AS's handling of them and have an arbitrarily long lifespan. They are also assumed to be of a size that the AS can handle and all be equally important. These are assumed as there has been no indication otherwise while also not impacting the AS's task.
10. Autonomous Systems (AS)
	1. These are modelled (in the environment) with a location (being a vertex on the graph), a cardinal direction and a maximum load capacity. 
	2.  
		- a real number indicating how many supply units AS can carry at once. (that is different from the weight, right now they are the same so this is not necessary)
		- total energy of the AS. (currently irrelevant, the AS has more than enough energy)
		- SUs that the AS has been assigned to extract. (all of them so doesn't need to be explicitly mentioned to the AS)
		- assigned extraction point for the AS. (doesn't matter as AS can exit at any extraction point currently)
		- speed of the AS. (doesn't matter as time is currently irrelevant)

## A3 - ADTs for Modelling 

### ADTs  

#### 1. Graph (Nielson, 2026)
add_vertex(v: Vertex) → None
add_edge(u: Vertex, v: Vertex) → None
neighbours(v: Vertex) → Set\[Vertex\]
has_edge(u: Vertex, v: Vertex) → Boolean
has_vertex(u: Vertex) → Boolean
vertices() → Set\[Vertex\]

#### 2. Maps: 
add(k: Key, e: Element) → None
set(k: Key, e: Element) → None
remove(k: Key) → None
lookup(k: Key) → Element
contains(k: Key) → Boolean
keys() → Set\[Keys\]

Note:
- map_name\[k\] ⇔ list_name.lookup(k) (when getting the value with key k)
- map_name\[k\] ← e ⇔ list_name.set(k,e) (when setting the value at key k to e)

#### 3. Sets: 
add(e: Element) → None
remove(e: Element) → None
contains: (e: Element) → Boolean


#### 4. Lists
insert_at(i: Index, e: Element) → None
insert_at(i: Index, l: list) → None
append(e: Element) → None
append(l: List) → None
set(i: Index, e: Element) → None
remove_at(i: Index) → None
lookup(i: Index) → Element
length() → Integer

Note:
- list_name\[i\] ⇔ list_name.lookup(i) (when getting the value at i)
- list_name\[i\] ← e ⇔ list_name.set(i,e) (when setting the value at i to e)

#### 5. Stack
push(e: Element) → None
pop() → Element
peak() → Element
is_empty() → Boolean

#### 6. Queue 
push(e: Element) → None
pop() → Element
peak() → Element
is_empty() → Boolean

#### 7. Priority Queue
push(e: Element, i: Importance) → None
pop_highest() → Element
peak_highest() → Element
pop_lowest() → Element
peak_lowest() → Element
is_empty() → Boolean

#### 8. Array
set(i: Index, e: Element) → None
remove_at(i: Index) → None
lookup(i: Index) → Element
length() → Integer

Note:
- array_name\[i\] ⇔ array_name.lookup(i) (when getting the value at i)
- array_name\[i\] ← e ⇔ array_name.set(i,e) (when setting the value at i to e)

### ADTs used #TODO show reason why selected adt is best

#### Inputs: 
Graph (of the Sector Grid), 
maps (of properties of the graph, vertices, edges, autonomous systems ASs, supply units SUs), 
sets (of the ASs and the SUs.)

In future, other ADTs may be nested in the maps. 
#### Outputs: 
map containing the whole output
List (of vertices and edges traversed in walk).


#### Within the Algorithm #TODO
It will use at minimum all the input ADTs as well as all the output ADTs.


# Part B - Algorithm Design:

## Problem properties
Known properties of the problem: 
- (currently) all edges have the same weight, so it can be treated as an unweighted graph. 
- (currently) the graph is a tree
- (currently) the maximum degree of any vertex is 4 as it is in a grid, meaning it is a 'sparse' graph for the sake of computation. (so an adjacency list is the way to go here).
- There are 5 supply units 
- There are 2 exits.
- There are ||V|| = 144 sectors. 

BFS is currently the best way to find the shortest path from a node to all nodes.

Note: if edge traversal cost starts to differ (but stays positive) use Dijkstra's instead of BFS.
- O(log(V)(V+E))
Note: if there are negative edges (but not negative cycles), use Bellman Ford instead of BFS.
- O(VE)

## Options
### Option 0: DFS
#### Pros and Cons:
Pros:
- Time complexity is O(V+E)
- Simple to understand
- Works in about any situation
Cons: 
- Walk is often suboptimal 

#### Algorithm: 
Do a DFS until all the supply units have been collected and then do another DFS until an exit has been reached. 


### Option 1: Greedy (BFS)

#### Pros and Cons:
Pros: 
- Good time complexity of O((V+E)(S)) where S is supply units. 
- Works if the edge traversal cost is different between edges
- Works on any graph as long as there are no negative cycles, for all edges. (doesn't have to be a tree)
- A version works if there the AS doesn't have enough energy to extract all supply units. 
Cons: 
- Walk is not always optimal.

#### Algorithm: 
Use BFS (single source all shortest paths) to find the path to the closest supply unit. Repeat from that node to the next closest unvisited supply unit and so on until there are no more supply units. Then use BFS to find the nearest exit and navigate their for extraction. 


### Option 2: Brute Force (BFS)

#### Pros and Cons
 Pros: 
- Simple to understand
- always returns optimal solution
 Cons: 
- Very inefficient with time complexity of O((V+E)(S) + S!) = O(S!) (if S >> (V+E))

#### Algorithm: 
First: Finds all shortest paths between the supply units, the entry and the exits, put these into a (S+\#entries + \#exits) squared matrix.
Secondly use said matrix to find the length of the walk Entry, ..., $s_1$, ..., $s_2$, ..., $s_n$, ..., Exit, 
where each permutation of $s_1$ to $s_n$ is tried along with different exit options. 
### Option 3: BFS + DFS

#### Pros and Cons:
Pros: 
- Returns the optimal route
- Not bad time efficiency  O(#Exits(V+E)) 
Cons:
- only works if:
	- the graph is a tree.
	- the AS has to collect all supply units.
- Complicated, and prone to human error

#### Algorithm

Overview: 
1. Do BFS retaining paths, number of children and leaf nodes O(V+E)
2. Backwards trace the graph from the leaf nodes giving a property to each node whether it has a supply unit (SU) beneath it, and whether it has an exit beneath it. O(V)
3. For each exit: O(\#Exits(V+E))
	1. Do DFS on the graph (retaining walk), where branches with SUs without exits are explored first. (ignore all branches without a SU or an exit)
4. Find which of the walks is shortest and return that. O(\#Exits V)

Total time complexity O(V+E) + O(V) + O(\#Exits(V+E)) + O(\#Exits V) = O(\#Exits(V+E))




## Discussion
Every option above has its merits and its drawbacks, but option 3 seems to be the most optimal for the current situation as it balances speed with finding the optimal solution. Its time complexity is O(#Exits(V+E)) (though it should be noted that for small V or E other solutions are likely faster), which is only always beaten by the DFS algorithm. 

Compared to the Brute force option, with time complexity O((V+E)S+S!) where S is \#of supply units, the BFS + DFS solution is significantly faster for large values of S. 

A significant drawback of the BFS + DFS algorithm is that it relies on the graph being a tree, which might be the case sometimes, leading to no solutions in that case. 



# Part C - Pseudocode 
## C1 - Algorithm in pseudocode (Nielson, 2026)


Pseudocode: 
```
//1 indexed. 
FUNCTION ember_rescue(G: Directed Unweighted Graph, SU: Set, AS: Set, VP: Map, EP: Map, SUP: Map, ASP: Map, GP: Map) -> Map
	// G = (V,E)
	
	
	//--------------------------------------------------
    // -----------Initialise data structures------------
    //--------------------------------------------------
    
    CRUDY_1 ← the element contained in the set AS
	entry ← ASP[CRUDY_1]["location"]
	V ← G.Vertices
	
	//--------------------------------------------------
    // ------------------Main loop----------------------
    //--------------------------------------------------
    
	//1. BFS
	
	parent, child_count, leaf_nodes ← BFS(G, entry)
	
	//2. Backtrace Tree 
	
	exit_count, sub_exit ← make_sub_exits(G, VP)
	sub_SU ← {v: not (VP[v]["supply_unit"] = null) | v ∈ V}
	sub_exit, sub_SU ← backtrace_tree(parent, child_count, leaf_nodes, sub_exit, sub_SU)
	
	//3. DFS for all exits
	
	walks ← empty list
	FOR i ← 1 to exit_count DO
		walks.append(DFS(G, entry, parent, sub_exit, sub_SU, i))
	END FOR
	
	//4. Calculating traversal_cost
	
	walk ← shortest_walk(walks)
	length ← walk.length() - 1
	
	//--------------------------------------------------
    // ----------------Return the output----------------
    //--------------------------------------------------
    
    //Outputing to the physical environment the instructions for the AS
    
    FOR i ← 1 to length DO
	    move(EP[(walk[i], walk[i+1])]["cardinal_angle"],1)
	END FOR
	exit()
    
    RETURN {"walk": walk, "energy_expended": length, "supply_units_recovered": SU}  
END FUNCTION

FUNCTION BFS(G: Graph, s: Vertex) -> Map, Map, Set 
	//s is first vertex
	V ← G.vertices()
	BFS_Queue ← queue
	BFS_Queue.push(s)
	visited ← {v: false | v ∈ V} //map
	visited[s] ← true
	
	parent ← {v: null | v ∈ V} //map
	child_count ← {v: 0 | v ∈ V} //map
	leaf_nodes ← clone of V
	
	WHILE not BFS_Queue.is_empty() DO
		u ← BFS_Queue.pop()
		FOR v ∈ G.Neighbours(u) DO 
			IF not visited[v] THEN
			
				visited[v] ← true
				BFS_Queue.push(v)
				
				parent[v] ← u
				child_count[u] ← child_count[u] + 1
				leaf_nodes.remove(u)
				
			END IF
		END FOR
	END WHILE
	
	return parent, child_count, leaf_nodes
END FUNCTION

FUNCTION make_sub_exits(G: Graph, VP: Map) -> Integer, Map
	exit_map ← {v: {} | v ∈ V} //Map of empty sets
	V ← G.vertices()
	exit_count ← 0
	FOR v ∈ V DO
		IF VP[v]["is_exit"] THEN
			exit_count ← exit_count + 1
			exit_map[v].add(exit_count)
		END IF
	END FOR
	
	RETURN exit_count, exit_map
END FUNCTION

FUNCTION backtrace_tree(parent: Map, child_count: Map, leaf_nodes: Set, sub_exit: Map, sub_SU: Map) -> Map, Map
	
	WHILE leaf_nodes is not empty DO 
		u ← an element from leaf_nodes
		leaf_nodes.remove(u)
		IF not parent[u] = null THEN
			sub_exit[parent[u]] ← sub_exit[parent[u]] ∪ sub_exit[u] //Union
			sub_SU[parent[u]] ← sub_SU[parent[u]] or sub_SU[u]
			child_count[parent[u]] ← child_count[parent[u]] - 1
			IF child_count[parent[u]] = 0 THEN 
				leaf_nodes.add(parent[u])
			END IF
		END IF
	END WHILE
	
	RETURN sub_exit, sub_SU
END FUNCTION

FUNCTION DFS(G: Graph, s: Vertex, parent: Map, sub_exit: Map, sub_SU: Map, i: Integer) -> list
	//initialisation
	DFS_Stack ← stack
	DFS_Stack.push(s)
	V ← G.vertices()
	visited ← {v: false | v ∈ V}
	visited[s] ← true
	
	walk ← []
	previous_u ← null
	
	//DFS
	WHILE not DFS_Stack.is_empty() DO
		
		u ← DFS_Stack.pop()
		Q ← empty queue
		
		//Building the walk
		IF not (previous_u = parent[u]) THEN
			WHILE not parent[u] = walk[walk.length()]
				walk.append(parent[walk[walk.length()]])
			END WHILE
		END IF
		walk.append(u)
		
		//makes sure that vertices with exits below them are pushed first.
		FOR v ∈ G.Neighbours(u) DO
			IF not visited[v] and sub_exit[v].contains[i] THEN 
				visited[v] ← true
				DFS_Stack.push(v)
			ELSE IF not visited[v] and sub_SU[v] THEN
				Q.push(v)
			END IF // ignores all vertices not in sub_exit or sub_SU
		END FOR
		
		//the nodes with just supply units below them are then pushed ontop.
		WHILE not Q.is_empty() DO 
			v ← Q.pop()
			visited[v] ← true
			DFS_Stack.push(v)
		END WHILE
		
		previous_u ← u
		
		
	END WHILE
	
	WHILE not VP[walk[walk.length()]]["is_exit"] DO
		walk.append(parent[walk[walk.length()]])
	END WHILE
	
	RETURN walk
END FUNCTION

FUNCTION shortest_walk(walks: List) -> List
	min_index ← -1
	min ← positive infinity
	FOR i ← 1 to walks.length() DO
		IF walks[i].length() < min THEN
			min ← walks[i].length()
			min_index ← i
		END IF
	END FOR
	
	RETURN walks[min_index]
END FUNCTION
```

## C2 - Algorithm in python

```
# G = (V,E)
import networkx as nx

def BFS_DFS(G, AS, SU, VP, EP, SUP, ASP, GP):
    #--------------------------------------------------
    #------------Initialise data structures------------
    #--------------------------------------------------

    CRUDY_1 = 0
    entry = ASP[CRUDY_1]["location"]
    V = G.nodes()

    #--------------------------------------------------
    # ------------------Main loop----------------------
    #--------------------------------------------------

    #1. BFS

    parent, child_count, leaf_nodes = BFS(G, entry)

    #2. Backtrace Tree 

    exit_count, sub_exit = make_sub_exits(G, VP)
    sub_SU = {v: not (VP[v]["supply_unit"] == None) for v in V}
    sub_exit, sub_SU = backtrace_tree(parent, child_count, leaf_nodes, sub_exit, sub_SU)

    #3. DFS for all exits

    walks = []
    for i in range(exit_count):
        walks.append(DFS(G, entry, parent, sub_exit, sub_SU, i))

    #4. Calculating traversal_cost

    walk = shortest_walk(walks)
    length = len(walk) - 1

    #--------------------------------------------------
    #-----------------Return the output----------------
    #--------------------------------------------------

    #Outputing to the physical environment the instructions for the AS

    for i in range(length):
        move(EP[(walk[i], walk[i+1])]["cardinal_angle"],1)
    exit()

    return {"walk": walk, "energy_expended": length, "supply_units_recovered": SU}  

def move(a,b):
    #move at a angle b distance
    return
def exit():
    #exit
    return

def BFS(G, s):
    #s is first vertex
    V = G.nodes()
    BFS_Queue = deque()
    BFS_Queue.append(s)
    visited = {v: False for v in V} #map
    visited[s] = True

    parent = {v: None for v in V} #map
    child_count = {v: 0 for v in V} #map
    leaf_nodes = set(V).copy()

    while BFS_Queue:
        u = BFS_Queue.popleft()
        for v in G[u]:
            if not visited[v]:

                visited[v] = True
                BFS_Queue.append(v)

                parent[v] = u
                child_count[u] = child_count[u] + 1
                leaf_nodes.discard(u)

    return parent, child_count, leaf_nodes


def make_sub_exits(G, VP):
    V = G.nodes()
    exit_map: dict[set] = {v: set() for v in V} #Map of empty sets
    exit_count = 0
    for v in V:
        if VP[v]["is_exit"]:
            exit_map[v].add(exit_count)
            exit_count = exit_count + 1
    return exit_count, exit_map


def backtrace_tree(parent, child_count, leaf_nodes, sub_exit, sub_SU):
    while leaf_nodes: 
        u = leaf_nodes.pop()
        if parent[u] == None:
            continue

        sub_exit[parent[u]] = sub_exit[parent[u]] | sub_exit[u] #Union
        sub_SU[parent[u]] = sub_SU[parent[u]] or sub_SU[u]
        child_count[parent[u]] = child_count[parent[u]] - 1
        if child_count[parent[u]] == 0:
            leaf_nodes.add(parent[u])

    return sub_exit, sub_SU

def DFS(G, s, parent, sub_exit, sub_SU, i):
    V = G.nodes()
    DFS_Stack = []
    DFS_Stack.append(s)

    visited = {v: False for v in V}
    visited[s] = True

    walk = []
    previous_u = None

    #DFS
    while DFS_Stack:

        u = DFS_Stack.pop()
        Q = deque()

        #Building the walk
        if not (previous_u == parent[u]):
            while not parent[u] == walk[len(walk)-1]:
                walk.append(parent[walk[len(walk)-1]])
        walk.append(u)

        #makes sure that vertices with exits below them are appended first.
        for v in G[u]:
            if (not visited[v]) and (i in sub_exit[v]): 
                visited[v] = True
                DFS_Stack.append(v)
            elif (not visited[v]) and sub_SU[v]:
                Q.append(v) # ignores all vertices not in sub_exit or sub_SU

        #the nodes with just supply units below them are then appended ontop.
        while Q: 
            v = Q.popleft()
            visited[v] = True
            DFS_Stack.append(v)


        previous_u = u

    while not VP[walk[len(walk)-1]]["is_exit"]:
        walk.append(parent[walk[len(walk)-1]])
	
    
    return walk

def shortest_walk(walks):
    min_index = -1
    min = 14400000
    for i in range(len(walks)):
        if len(walks[i]) < min:
            min = len(walks[i])
            min_index = i

    return walks[min_index]


```

# Part D - Justification

## DFS returns best path proof.
Scope: undirected trees.

Conjecture: A shortest walk containing all P.O.I. (points of interest) ending at a specific node can be found utilising a modified DFS on a subtree with only P.O.I. as leaf nodes. 

Lemma 1: to visit all nodes and return to the source, DFS provides a shortest walk.
- Since to get to a node there is only one path, all of those edges have to be traversed at least twice, and each edge in the graph has to connect at least one node to the tree connected to the source, meaning that every edge has to be traversed at least twice, meaning the walk has to have length at least 2sum(E).
- But DFS produces a walk of length 2sum(E) as it has to traverse all edges (in a tree) and then back again. This means DFS produces an optimal walk for its length is the shortest it could be.

Lemma 2: DFS provides a shortest walk to traverse all nodes and end at an arbitrary node.
- A DFS route with the exit on the return trip exists as it doesn't matter which branch is pushed to the stack first meaning if branches containing the exit are always pushed first, the last leaf node visited will be the exit itself, or a child of the exit.
- So this provides a walk with length 2sum(E) - dist(source,exit). There can be no walk shorter than this (adhering to constraints)  as a walk shorter would mean that w + dist(source,exit) < 2sum(E) - dist(source,exit) + dist(source,exit) = 2sum(E), meaning that it defies lemma 1 so by contradiction lemma 2 holds. 

Lemma 3: DFS provides a shortest walk containing all leaf nodes and ending at an arbitrary node.
- As the graph is a tree, there is only one path between any two nodes, meaning to get to a leaf node from the source, all parents of the leaf node must be traversed. 
- As every node in a graph is either a parent of a leaf node or a leaf node, all nodes must be traversed if all leaf nodes are to be traversed.
- As all nodes must be traversed, this problem falls under lemma 2, meaning, showing that lemma 3 is true. 

Applying to a specific P.O.I:
- consider a minimal subtree of the tree that is big enough to contain all the P.O.I.
- Lemma 3 applies here meaning that the shortest walk to contain the P.O.I is 2sum(E) - dist(source,exit) but sum(E) is of edges in the the subgraph.

my algorithm (DFS) is the best Q.E.D.
(returns the optimal walk)

## THE REST :( #TODO

**1. Suitability** Why is this algorithm appropriate for _this_ problem?

- What properties of the Emberlight facility make your algorithm a natural fit?
- Consider: does the facility structure (tree, grid, dead-end placements) favour your approach? Use evidence from the Graph Explorer.
- Are there properties of the problem that your algorithm handles _better_ than the alternatives you considered in B1?

**2. Coherence** How does your algorithm integrate with your data model?

- Name two ADT operations from Part A and explain exactly how they are used in your algorithm (not just "I use a graph" — be specific about which operation, when it is called, and what it returns).
- Are there any tensions between your ADT design and your algorithm? For example, does your algorithm require an operation that isn't in your ADT signature?

**3. Fitness for purpose** Does your solution meet the mission directive?

- Go through each operational constraint from Memo 01 and state explicitly whether your solution satisfies it, and how.
- Are there any constraints your solution _fails_ to satisfy? If so, acknowledge this honestly and explain whether it is an acceptable trade-off.

