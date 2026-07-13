import marimo

__generated_with = "0.23.9"
app = marimo.App(auto_download=["html"])


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import random
    import networkx as nx
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.colors as mcolors
    from collections import deque
    import json
    import os
    import datetime
    import textwrap
    import matplotlib
    import imageio
    import time
    import tracemalloc
    import math
    import inspect
    import copy
    import heapq

    return (mo,)


@app.cell(hide_code=True)
def style(mo):
    mo.md(r"""
    <style>
        h1 {
          font-size: 50px;
          color: darkblue;
        }
        h2 {
          font-size: 38px;
          color: darkblue;
        }
        h3 {
          font-size: 28px;
          color: darkblue;
        }
        h4 {
          font-size: 20px;
          color: darkblue;
        }
        h5 {
          font-size: 18px;
          color: darkblue;
        }
        h6 {
          font-size: 14px;
          color: darkblue;
        }
        .r {
        background-color: #FF6666;
        text-decoration: line-through;
        }
        .g {
         background-color: limegreen;
        }
        .y {
            background-color: yellow;
        }
    </style>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Side Memo S1-A -- ADT Design Under Pressure
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"### ADTs From Memo A2":"""      
    **1. Graph (Nielsen, 2026)**<br>
    add_vertex(g: Graph, v: Vertex) → Graph<br>
    add_edge(g: Graph, u: Vertex, v: Vertex) → Graph<br>
    neighbours(g: Graph, v: Vertex) → Set[Vertex]<br>
    has_edge(g: Graph, u: Vertex, v: Vertex) → Boolean<br>
    has_vertex(g: Graph, u: Vertex) → Boolean<br>
    vertices(g: Graph) → Set[Vertex]<br>
    edges() → Set[Edges]

    **2. Maps:**<br>
    add(m: Map, k: Key, e: Element) → Map<br>
    set(m: Map, k: Key, e: Element) → Map<br>
    remove(m: Map, k: Key) → Map<br>
    lookup(m: Map, k: Key) → Element<br>
    contains(m: Map, k: Key) → Boolean<br>
    keys(m: Map) → Set[Keys]

    Note:<br>
    - map_name[k] ⇔ map_name.lookup(k) (when getting the value with key k)
    - map_name[k] ← e ⇔ map_name.set(k,e) (when setting the value at key k to e)

    **3. Sets:**<br>
    add(s: Set, e: Element) → Set<br>
    remove(s: Set, e: Element) → Set<br>
    contains(s: Set, e: Element) → Boolean<br>
    intersection(s1: Set, s2: Set) → Set<br>
    Union(s1: Set, s2: Set) → Set<br>
    difference(s1: Set, s2: Set) → Set<br>
    is_empty(s: Set) → Boolean<br>
    size(s: Set) → Integer<br>
    get_random(s: Set) → Element

    Note:
    - u ∈ V ⇔ V.contains(u) or means forall u where V.contains(u)
    - U ⊆ V ⇔ V.is_subset(U)

    **4. Lists**<br>
    insert_at(l: list, i: Index, e: Element) → list<br>
    concatenate_at(l1: list, i: Index, l2: list) → list<br>
    append(l: list, e: Element) → list<br>
    concatenate(l1: list, l2: List) → list<br>
    set(l: list, i: Index, e: Element) → list<br>
    remove_at(l: list, i: Index) → list<br>
    lookup(l: list, i: Index) → Element<br>
    length(l: list) → Integer

    Note:
    - list_name[i] ⇔ list_name.lookup(i) (when getting the value at i)
    - list_name[i] ← e ⇔ list_name.set(i,e) (when setting the value at i to e)


    **5. Stack**<br>
    push(s: Stack, e: Element) → Stack<br>
    pop(s: Stack) → Stack X Element<br>
    peek(s: Stack) → Element<br>
    size(s: Stack) → Integer<br>
    is_empty(s: Stack) → Boolean

    **6. Queue**<br>
    push(q: Queue, e: Element) → Queue<br>
    pop(q: Queue) → Queue X Element<br>
    peek(q: Queue) → Element<br>
    size(q: Queue) → Integer<br>
    is_empty(q: Queue) → Boolean


    **7. Priority Queue**<br>
    push(pq: Priority Queue, e: Element, i: Importance) → Priority Queue<br>
    pop_highest(pq: Priority Queue) → Priority Queue X Element<br>
    peek_highest(pq: Priority Queue) → Element<br>
    pop_lowest(pq: Priority Queue) → Priority Queue X Element<br>
    peek_lowest(pq: Priority Queue) → Element<br>
    size(pq: Priority Queue) → Integer<br>
    is_empty(pq: Priority Queue) → Boolean

    **8. Array**<br>
    set(a: Array, i: Index, e: Element) → Array<br>
    remove_at(a: Array, i: Index) → Array<br>
    lookup(a: Array, i: Index) → Element<br>
    length(a: Array) → Integer

    Note:
    - array_name[i] ⇔ array_name.lookup(i) (when getting the value at i)
    - array_name[i] ← e ⇔ array_name.set(i,e) (when setting the value at i to e)

    9. Tuple<br>
    lookup(t: Tuple, i: Index) → Element<br>
    length(t: Tuple) → Integer<br>

    Note:<br>
    - tuple_name[i] ⇔ tuple_name.lookup(i) (when getting the value at i)
    """})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Revised Graph ADT**:

    **Search-Graph**<br>

    Prexisting Operations:<br>
    add_vertex(g: Graph, v: Vertex) → Search-Graph<br>
    add_edge(g: Search-Graph, u: Vertex, v: Vertex) → Search-Graph<br>
    neighbours(g: Search-Graph, v: Vertex) → Set[Vertex]<br>
    has_edge(g: Search-Graph, u: Vertex, v: Vertex) → Boolean<br>
    has_vertex(g: Search-Graph, u: Vertex) → Boolean<br>
    vertices(g: Search-Graph) → Set[Vertex]<br>
    edges() → Set[Edges]

    New Operations:<br>
    unvisited_neighbours(g: Search-Graph, v: Vertex) → Search-Graph X Set[Vertex]

    **Behaviour**:<br>
    The new unvisited_neighbours ADT takes a search-graph g, and one of its vertices v as inputs and then returns a set containing all neigbours of v that are marked as *unvisited*, as well as a new search-graph where v is marked as *visited*. At the initialisation of the search-graph, all nodes are marked as unvisited, but each time the unvisited_neighbours is called, the vertex v in question is marked as visited.

    **Justification**:
    The Search-Graph could be composed of a seperated graph 'G' and a map 'visited', but to iterate through the unvisited_neighbours set, one has to:

    ```
    set visited[u] to True

    FOR v in G.neighbours(u) DO
        IF not visited[v] THEN
            #Do smth
    ```

    Or, one can do the oneline operation:

    ```

    FOR v in G.unvisited_neighbours(u) DO
        # Do smth
    ```

    As these operations are needed in BFS, DFS and Dijkstra's algorithm, this new operation would naturally make these algorithms more cohesive and understandable.

    **Note**: not containing a previously collected supply unit was ommited as each time a sector is traversed with a supply unit it is collected, so all supply units in unvisited areas are NOT previously collected.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Side Memo S1-B -- Contingency Planning
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Please refer to the memos, section B, to find the different algorithms explored.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Side Memo S1-C -- Abstraction Audit
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Brute Force Pseudocode":
    """
    ```
    FUNCTION Brute_Force(G: Directed Graph, SU: Set, AS: Set, VP: Map, EP: Map, SUP: Map, ASP: Map, GP: Map) -> Map

            CRUDY_1 ← AS.get_random()
            entry ← ASP[CRUDY_1]["location"]
            V ← G.vertices()

            exits ← {}
            FOREACH v ∈ V DO
                IF VP[v]["is_exit"] = true THEN
                    exits.add(v)

            SU_locations ← {SUP[su]["location"] | su ∈ SU} // a set of SU locations

            POI ← clone of exits
            POI ← POI.Union(SU_locations)
            POI.add(entry)

            dm ← {v:{u:∞ | u∈POI} | v∈POI} // Distance Matrix
            pm ← {v:{u:null | u∈POI} | v∈POI} //Path Matrix

            //Getting distance and path between exits, the entry and SUs.
            FOREACH v ∈ POI DO
                dist, parent ← Dijstras(G, EP, v)
                FOREACH u ∈ POI DO
                    w ← u
                    path ←[]
                    WHILE parent[w] != null DO
                        path.insert_at(0, w) 
                        w ← parent[w]
                    pm[v][u] ← path //without first node
                    dm[v][u] ← dist[u]


            //Finding shortest walk.

            min_perm ← []
            min_dist ← ∞
            FOREACH permutation of SU_locations: su_perm DO
                FOREACH exit in exits DO // su_perm is a list.
                dist ← 0
                perm ← [entry]
                perm ← perm.concatenate(su_perm)
                perm ← perm.append(exit)
                FOR i from 1 (inclusive) to perm.length() (exclusive) DO
                    dist ← dist + dm[perm[i]][perm[i+1]]
                IF dist < min_dist THEN
                    min_perm ← perm
                    min_dist ← dist

            walk ← [entry]
            FOR i from 1 (inclusive) to min_perm.length() (exclusive) DO
                walk.concatenate(pm[min_perm[i]][min_perm[i+1]])

            FOR i ← 1 (inclusive) to walk.length() (exclusive) DO
                dif_vec ← VP[walk[i+1]]["location"]-VP[walk[i]]["location"] // a tuple
                move(dif_vec[1], dif_vec[2])
            exit()

            RETURN {"walk": walk, "traversal_cost": min_dist, "supply_units_recovered": SU}


    FUNCTION Dijkstras(G, EP, s) -> map X map
            V ← G.vertices()
            visited ← {v: False | v ∈ V}
            dist ← {v: None | v ∈ V}
            parent ← {v: None | v ∈ V}
            dist[s] ← 0
            pq ← Priority Queue
            pq.push(s,0)
            WHILE not pq.is_empty() DO
                u ← pq.pop_lowest()
                IF visited[u] THEN:
                    skip to next iteration of WHILE
                visited[u] ← True
                FOR v ∈ G.neighbours(u) DO
                    w ← EP[(u,v)]['w']
                    IF visited[v] THEN
                        skip to next iteration of FOR
                    IF dist[v] = None or dist[v] > dist[u] + w THEN
                        parent[v] ← u
                        dist[v] ← dist[u] + w
                        pq.push(v, dist[v])
            return dist, parent
    ```
    """, "Dijkstra's Algorithm":
    """
    ```
    FUNCTION Dijkstras(G, EP, s) -> map X map
            V ← G.vertices()
            visited ← {v: False | v ∈ V}
            dist ← {v: None | v ∈ V}
            parent ← {v: None | v ∈ V}
            dist[s] ← 0
            pq ← Priority Queue
            pq.push(s,0)
            WHILE not pq.is_empty() DO
                u ← pq.pop_lowest()
                IF visited[u] THEN:
                    skip to next iteration of WHILE
                visited[u] ← True
                FOR v ∈ G.neighbours(u) DO
                    w ← EP[(u,v)]['w']
                    IF visited[v] THEN
                        skip to next iteration of FOR
                    IF dist[v] = None or dist[v] > dist[u] + w THEN
                        parent[v] ← u
                        dist[v] ← dist[u] + w
                        pq.push(v, dist[v])
            return dist, parent
    ```
    """, "Inline Code": """
    ```
            //Finding shortest walk.
            min_perm ← []
            min_dist ← ∞
            FOREACH permutation of SU_locations: su_perm DO
                FOREACH exit in exits DO // su_perm is a list.
                dist ← 0
                perm ← [entry]
                perm ← perm.concatenate(su_perm)
                perm ← perm.append(exit)
                FOR i from 1 (inclusive) to perm.length() (exclusive) DO
                    dist ← dist + dm[perm[i]][perm[i+1]]
                IF dist < min_dist THEN
                    min_perm ← perm
                    min_dist ← dist

    ```
    """
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Justification of Functional Abstraction:

    **Functional Abstraction Chosen:**<br>
    Dijkstra's algorithm.

    **What responsibility does this abstraction encapsulate?**<br>
    Dijkstra's algorithm is responsible for using a graph, a tuple (the source), and a map containing the edge weights to return the distance between all nodes and the source as well as the 'parent' map. The parent map can be then used to reconstruct the path between the source and all nodes.

    **Why is that responsiblility distinct enough to warrant seperation from the main algorithm?**<br>

    The main concept of 'Brute Force' is to try all different combinations or permutations to find the 'optimal' one. However, Dijkstra's algorithm isn't intergral to the concept of Brute Force, and would just make the reasonablility of the algorithm more complicated and convoluted.

    **What would be lost -- in terms of clarity, correctness, or reusability -- if it were inlined?**<br>

    If Dijkstra's algorithm were to be inlined, nothing would break, however the coherence of the algorithm would suffer. Seperating it out allows for the clear distinction between the two well defined concepts of 'Brute Force' and Dijkstra's algorithm to be made.

    ### Inline Code:

    The inline code (shown above) to try all permutations of the supply units with different exits is left directly within the 'Brute Force' algorithm. This is as trying all permutations of something is an intergral part of 'Brute Force' algorithm, helping solidify the concept, thus increasing coherence of the algorithm.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Side Memo S1-D -- Devil's Advocate
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Strongest Objection to the Brute Force algorithm

    The Engineering Division review panel has found Kieran Meinshausen's 'Brute Force' algorithm to be too dependent on there being few supply units present. While the initial review of the situation included only 5 supply units, there is potential for there to be more supply units in a larger section of the Emberlight Subterranean Research Complex (ESRC), enough to make computing the optimal path take longer than  the heat death of the universe.

    ### Rebutal and Concession

    It is conceeded that given enough supply units, Brute Force would no longer function due extreme computational time. In this situation, 'Brute Force' would unfortunately not remain the most appropriate solution to the problem of collecting all supply units.

    However, for this reason some other algorithms were considered as well, including 'Divide and Conquer' which would perform well if all the supply units were spread out across multiple wings, or the heuristic 'BFS+DFS', which despite not being made for graphs with cycles remains close to optimal with almost zero computational time (averaging 2ms).

    ### Reflection

    This objection has helped to identify potential *future* problems with the 'Brute Force' algorithm and has highlighted the potential for an undetectable error if 'Brute Force' is feed a facility with too many supply units. Potentially a better solution would involve an algorithm to first determine which of the four algorithms considered (Brute Force, Divide and Conquer, BFS+DFS and Greedy) would likely be best for the problem, and pass the problem to that algorithm.
    """)
    return


if __name__ == "__main__":
    app.run()
