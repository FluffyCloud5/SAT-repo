import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)

with app.setup(hide_code=True):
    #import functions
    import marimo as mo
    import random
    import networkx as nx
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
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


    #Some constants
    COLS, ROWS =12,12
    WING_COLS, WING_ROWS = 10, 10
    GAP = 3  # grid-unit gap between wings in the visualisation


    # colors: 
    COL_BG       = '#F5F7FA'
    COL_GRID     = '#C8D0DC'
    COL_WALL     = '#44546A'
    COL_ENTRY    = '#0B6E6B'
    COL_EXIT     = '#7A1E2C'
    COL_SUPPLY   = '#4AA8A0'
    COL_PATH     = '#0B6E6B'
    COL_VISITED  = '#B8D8D7'
    COL_FRONTIER = '#F4C97A'
    COL_CURRENT  = '#E8603C'
    COL_JUNCTION = '#7A1E2C'


@app.cell
def comments():
    #--------------------------------------------------------------
    #---------------------------OVERVIEW---------------------------
    #--------------------------------------------------------------


    #This marimo notebook is Kieran's response to the SAT notebooks


    #Some coding name conventions:
        #This notebook is a large project so there will likely be some unconventional or badly named objects.

        #v1 - memo 1
        #v2 - memo A1
        #v3 - memo A2
        #fac - facility
        #facility A - representation of the facility in Kodie Nielsen's way
        #facility B - representation of the facility in Kieran's defined in part A1 - Algorithmic problem statement
        #'m_' before something - to make that something
        #'c_' before something - to convert into that something


    #functions are defined inside one another for the reusability feature and being able to print them easily with inspect.getsource()
    return


@app.cell(hide_code=True)
def style():
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


@app.function(hide_code=True)
#Define make the A1 facility (m_fac_Av2)
def m_fac_Av2(seed): #make facility version 2

    def _neighbours(cols, rows, c, r):
        for dc, dr in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nc, nr = c + dc, r + dr
            if 0 <= nc < cols and 0 <= nr < rows:
                yield nc, nr

    def _build_wing(cols, rows, rng):
        """Build a single-wing maze as a spanning tree of the grid."""
        visited = [[False] * rows for _ in range(cols)]
        g = nx.Graph()
        for c in range(cols):
            for r in range(rows):
                g.add_node((c, r))

        def carve(c, r):
            visited[c][r] = True
            dirs = list(_neighbours(cols, rows, c, r))
            rng.shuffle(dirs)
            for nc, nr in dirs:
                if not visited[nc][nr]:
                    g.add_edge((c, r), (nc, nr), weight=1)
                    carve(nc, nr)

        carve(0, 0)
        return g

    int_seed = int(seed)
    n_wings   = 2 + (int_seed % 3)          # 2, 3, or 4 wings from seed
    wing_names = ['Alpha', 'Beta', 'Gamma', 'Delta'][:n_wings]

    # Build each wing from a deterministic derived seed
    wings = []
    for w in range(n_wings):
        wrng = random.Random(int_seed * 31 + w * 7919)
        wings.append(_build_wing(WING_COLS, WING_ROWS, wrng))

    # Inter-wing junctions: 2 corridors per adjacent wing pair
    # Each junction connects (w, WING_COLS-1, r) to (w+1, 0, r)
    junctions = []
    for w in range(n_wings - 1):
        jrng = random.Random(int_seed * 17 + w * 5003)
        rows_avail = list(range(2, WING_ROWS - 2))
        jrng.shuffle(rows_avail)
        r1, r2 = sorted(rows_avail[:2])
        junctions.append(((w, WING_COLS - 1, r1), (w + 1, 0, r1)))
        junctions.append(((w, WING_COLS - 1, r2), (w + 1, 0, r2)))

    # Fixed entry and exits
    entry  = (0, 0, 0)
    exit_a = (n_wings - 1, WING_COLS - 1, WING_ROWS - 1)
    exit_b = (n_wings - 1, WING_COLS - 1, 0)

    # Supply placement: spread across wings, prefer dead-end nodes
    srng = random.Random(int_seed * 13 + 42)
    reserved = {entry, exit_a, exit_b}
    for n1, n2 in junctions:
        reserved.add(n1)
        reserved.add(n2)

    # Collect dead-end candidates per wing
    per_wing_cands = []
    for w, wg in enumerate(wings):
        de = [
            (w, c, r) for (c, r) in wg.nodes()
            if wg.degree((c, r)) == 1 and (w, c, r) not in reserved
        ]
        srng.shuffle(de)
        per_wing_cands.append(de)

    # Round-robin: up to 2 supplies per wing, 5 total
    supplies = []
    for _ in range(2):
        for wl in per_wing_cands:
            if len(supplies) >= 5:
                break
            for n in wl:
                if n not in supplies:
                    supplies.append(n)
                    break
        if len(supplies) >= 5:
            break

    return {
        'n_wings':    n_wings,
        'wing_names': wing_names,
        'wings':      wings,
        'wing_cols':  WING_COLS,
        'wing_rows':  WING_ROWS,
        'entry':      entry,
        'exit_a':     exit_a,
        'exit_b':     exit_b,
        'supplies':   supplies[:5],
        'junctions':  junctions,
        'gap': GAP
    }


@app.function(hide_code=True)
#Define draw the facility for memo A1 (draw_fac_v2)
def draw_fac_v2(fac_Av2, highlight_path=None, node_colors=None,
                    supply_collected=None, title="Multi-Wing Facility", legend = True, grid = True):

    wc = fac_Av2['wing_cols']
    wr = fac_Av2['wing_rows']
    nw = fac_Av2['n_wings']
    total_w = nw * wc + (nw - 1) * GAP

    fig_w = max(10, total_w * 0.58)
    fig_h = max(5, wr * 0.58 + 1.2)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_facecolor(COL_BG)
    fig.patch.set_facecolor(COL_BG)

    def xoff(w):
        return w * (wc + GAP)

    # Draw each wing
    for w, wing in enumerate(fac_Av2['wings']):
        ox = xoff(w)

        # Grid lines
        if grid:
            for c in range(wc + 1):
                ax.plot([ox + c, ox + c], [0, wr],
                        color=COL_GRID, lw=0.4, zorder=1)
            for r in range(wr + 1):
                ax.plot([ox, ox + wc], [r, r],
                        color=COL_GRID, lw=0.4, zorder=1)


        # Wing border
        ax.add_patch(plt.Rectangle(
            (ox, 0), wc, wr,
            fill=False, edgecolor=COL_WALL, lw=2.2, zorder=3))

        # Wing label
        ax.text(ox + wc / 2, wr + 0.38,
                f"Wing {fac_Av2['wing_names'][w]}",
                ha='center', va='bottom', fontsize=9,
                fontweight='bold', color='#0B1F3B', zorder=8)

        # Internal walls (draw where no edge exists)
        for c in range(wc):
            for r in range(wr):
                if c + 1 < wc and not wing.has_edge((c, r), (c + 1, r)):
                    ax.plot([ox + c + 1, ox + c + 1], [r, r + 1],
                            color=COL_WALL, lw=1.4, zorder=3)
                if r + 1 < wr and not wing.has_edge((c, r), (c, r + 1)):
                    ax.plot([ox + c, ox + c + 1], [r + 1, r + 1],
                            color=COL_WALL, lw=1.4, zorder=3)

        # Node highlights
        if node_colors:
            for (ww, c, r), color in node_colors.items():
                if ww == w:
                    ax.add_patch(plt.Rectangle(
                        (ox + c, r), 1, 1,
                        color=color, alpha=0.5, zorder=2))

    # Inter-wing corridors and junction nodes
    for (w1, c1, r1), (w2, c2, r2) in fac_Av2['junctions']:
        x1, y1 = xoff(w1) + c1 + 0.5, r1 + 0.5
        x2, y2 = xoff(w2) + c2 + 0.5, r2 + 0.5
        ax.plot([x1, x2], [y1, y2],
                color=COL_JUNCTION, lw=1.8,
                linestyle='--', alpha=0.7, zorder=4)
        ax.plot(x1, y1, 'o', ms=8, color=COL_JUNCTION, zorder=5)
        ax.plot(x2, y2, 'o', ms=8, color=COL_JUNCTION, zorder=5)

    # Supply markers
    for i, (ws, cs, rs) in enumerate(fac_Av2['supplies']):
        ox = xoff(ws)
        already = supply_collected and (ws, cs, rs) in supply_collected
        col = '#AAAAAA' if already else COL_SUPPLY
        mkr = 'x' if already else '*'
        ax.plot(ox + cs + 0.5, rs + 0.5,
                marker=mkr, markersize=14, color=col,
                markeredgecolor=COL_ENTRY if not already else '#999',
                markeredgewidth=0.8, zorder=5)
        ax.text(ox + cs + 0.62, rs + 0.58, f'S{i + 1}',
                fontsize=6, color=COL_WALL, zorder=6)

    # Entry marker
    we, ce, re = fac_Av2['entry']
    ox = xoff(we)
    ax.add_patch(plt.Circle(
        (ox + ce + 0.5, re + 0.5), 0.28,
        color=COL_ENTRY, zorder=6))
    ax.text(ox + ce + 0.5, re + 0.5, 'E',
            ha='center', va='center',
            fontsize=6, color='white', fontweight='bold', zorder=7)

    # Exit markers
    for lbl, (wx, cx, rx) in [('A', fac_Av2['exit_a']), ('B', fac_Av2['exit_b'])]:
        ox = xoff(wx)
        ax.add_patch(plt.Circle(
            (ox + cx + 0.5, rx + 0.5), 0.28,
            color=COL_EXIT, zorder=6))
        ax.text(ox + cx + 0.5, rx + 0.5, lbl,
                ha='center', va='center',
                fontsize=6, color='white', fontweight='bold', zorder=7)

    # Highlight path
    if highlight_path and len(highlight_path) > 1:
        for i in range(len(highlight_path) - 1):
            w1, c1, r1 = highlight_path[i]
            w2, c2, r2 = highlight_path[i + 1]
            ax.plot(
                [xoff(w1) + c1 + 0.5, xoff(w2) + c2 + 0.5],
                [r1 + 0.5, r2 + 0.5],
                color=COL_PATH, lw=1.8, linestyle='--',
                alpha=0.75, zorder=4)

    # Legend
    if(legend):
        legend_items = [
            mpatches.Patch(color=COL_ENTRY,    label='Entry'),
            mpatches.Patch(color=COL_EXIT,     label='Exit A / B'),
            mpatches.Patch(color=COL_SUPPLY,   label='Supply unit'),
            mpatches.Patch(color=COL_JUNCTION, label='Inter-wing junction'),
        ]
        if node_colors:
            legend_items += [
                mpatches.Patch(color=COL_VISITED,  alpha=0.5, label='Visited'),
                mpatches.Patch(color=COL_FRONTIER, alpha=0.5, label='Frontier'),
                mpatches.Patch(color=COL_CURRENT,  alpha=0.7, label='Current'),
            ]
        ax.legend(handles=legend_items, loc='upper left',
                  fontsize=7, framealpha=0.9)

    ax.set_xlim(-0.5, total_w + 0.5)
    ax.set_ylim(-0.9, wr + 1.1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=11, fontweight='bold',
                 color='#0B1F3B', pad=10)
    plt.tight_layout()
    return fig, ax


@app.function(hide_code=True)
#Define c_Av2
def c_Av2(node, fac_Av2 = {"wing_cols":WING_COLS, "gap": GAP}):
    #maps node from facility B to facility A
    return (int((node[0]-(node[0]%(fac_Av2["wing_cols"] + fac_Av2["gap"])))/(fac_Av2["wing_cols"] + fac_Av2["gap"])),node[0]%(fac_Av2["wing_cols"] + fac_Av2["gap"]),node[1])


@app.function(hide_code=True)
#Define c_Bv2
def c_Bv2(node, fac_Av2 = {"wing_cols":WING_COLS, "gap": GAP}):
    #maps node from facility B to facility A
    return (node[1] + (fac_Av2["wing_cols"]+fac_Av2["gap"])*node[0], node[2])


@app.function(hide_code=True)
#Define convert facility A to facility B memo A1 (c_fac_Bv2)
def c_fac_Bv2(fac_Av2):
    # turn Mr Nielsen's implementation (A) into the implementation specified in part A1 (B)


    vertices = []
    G = nx.DiGraph()

    n_nodes = fac_Av2["n_wings"]*fac_Av2["wing_cols"]*fac_Av2["wing_rows"] #number of nodes

    #adds all sectors of fac_Av2 to G
    #Nodes are of the form (c,r)
    graph = [c_Bv2((i,c,r),fac_Av2) for c in range(fac_Av2["wing_cols"]) for r in range(fac_Av2["wing_rows"]) for i in range(fac_Av2["n_wings"])]
    G.add_nodes_from(graph)



    #Edges are of the form ((c1,r1),(c2,r2))
    for i in range(fac_Av2["n_wings"]):
        for edge in fac_Av2["wings"][i].edges(): #for each edge of the ith wing, edge a tuple of two nodes.
            G.add_edge(c_Bv2((i,edge[0][0],edge[0][1]),fac_Av2), c_Bv2((i,edge[1][0],edge[1][1]),fac_Av2))
            G.add_edge(c_Bv2((i,edge[1][0],edge[1][1]),fac_Av2), c_Bv2((i,edge[0][0],edge[0][1]),fac_Av2))

    for junc in fac_Av2["junctions"]:
        G.add_edge(c_Bv2(junc[0],fac_Av2),c_Bv2(junc[1],fac_Av2))
        G.add_edge(c_Bv2(junc[1],fac_Av2),c_Bv2(junc[0],fac_Av2))

    SU = {i for i in range(len(fac_Av2["supplies"]))}

    AS = {0}


    VP = {i:{"is_entry":False, "is_exit": False, "supply_unit": None, "wing": fac_Av2["wing_names"][c_Av2(i)[0]],"location": i} for i in G.nodes()}
    VP[c_Bv2(fac_Av2["entry"],fac_Av2)]["is_entry"] = True
    VP[c_Bv2(fac_Av2["exit_a"],fac_Av2)]["is_exit"] = True
    VP[c_Bv2(fac_Av2["exit_b"],fac_Av2)]["is_exit"] = True
    for i in range(len(fac_Av2["supplies"])):
        VP[c_Bv2(fac_Av2["supplies"][i],fac_Av2)]["supply_unit"] = i



    EP = {edge: {}  for edge in G.edges}


    SUP = {i:{"location": c_Bv2(fac_Av2["supplies"][i],fac_Av2)} for i in range(len(fac_Av2["supplies"]))}

    ASP = {0:{"location":  c_Bv2(fac_Av2["entry"],fac_Av2)}}

    GP = {}
    return G, AS, SU, VP, EP, SUP, ASP, GP


@app.function(hide_code=True)
#Define convert output B to a walk in A.
def c_out_Av2(out_Bv2): 
    #converts output from any of the algorithms to a walk in B
    return [c_Av2(v) for v in out_Bv2["walk"]]


@app.function(hide_code=True)
#Define BFS+DFS

def BFS_DFS(G, AS, SU, VP, EP, SUP, ASP, GP):

    #--------------------------------------------------
    #---------------------Imports----------------------
    #--------------------------------------------------

    import networkx as nx
    from collections import deque

    #--------------------------------------------------
    #------------Initialise Helper Functions-----------
    #--------------------------------------------------

    def _move(x,y):
        #move at x distance in x direction and y distance in y direction.
        return

    def _exit():
        #exit
        return

    def _BFS(G, s):
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

    def _make_sub_exits(G, VP):
        V = G.nodes()
        exit_map: dict[set] = {v: set() for v in V} #Map of empty sets
        exit_count = 0
        for v in V:
            if VP[v]["is_exit"]:
                exit_map[v].add(exit_count)
                exit_count = exit_count + 1
        return exit_count, exit_map

    def _backtrace_tree(parent, child_count, leaf_nodes, sub_exit, sub_SU):
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

    def _DFS(G, VP, s, parent, sub_exit, sub_SU, i):
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
                #CHANGED THIS by adding parent[v] == u to ensure that it stays on the tree found by BFS.
                if (not visited[v]) and (i in sub_exit[v]) and parent[v] == u: 
                    visited[v] = True
                    DFS_Stack.append(v)
                elif (not visited[v]) and sub_SU[v] and parent[v] == u:
                    Q.append(v) # ignores all vertices not in sub_exit or sub_SU

            #the nodes with just supply units below them are then appended on top.
            while Q: 
                v = Q.popleft()
                visited[v] = True
                DFS_Stack.append(v)


            previous_u = u

        while not VP[walk[-1]]["is_exit"]:
            walk.append(parent[walk[-1]])
            if (walk[-1] == None):
                raise Exception(f"Something went wrong, walk: {walk}, VP: {VP}, parent: {parent}")


        return walk

    def _shortest_walk(walks):
        min_index = 0
        min = len(walks[0])
        for i in range(len(walks)):
            if len(walks[i]) < min:
                min = len(walks[i])
                min_index = i

        return walks[min_index]

    #--------------------------------------------------
    #------------Initialise data structures------------
    #--------------------------------------------------

    CRUDY_1 = list(AS)[0]
    entry = ASP[CRUDY_1]["location"]
    V = G.nodes()

    #--------------------------------------------------
    # ------------------Main loop----------------------
    #--------------------------------------------------

    #1. BFS

    parent, child_count, leaf_nodes = _BFS(G, entry)

    #2. Backtrace Tree 

    exit_count, sub_exit = _make_sub_exits(G, VP)
    sub_SU = {v: not (VP[v]["supply_unit"] == None) for v in V}
    sub_exit, sub_SU = _backtrace_tree(parent, child_count, leaf_nodes, sub_exit, sub_SU)

    #3. DFS for all exits

    walks = []
    for i in range(exit_count):
        walks.append(_DFS(G, VP, entry, parent, sub_exit, sub_SU, i))

    #4. Calculating traversal_cost

    walk = _shortest_walk(walks)
    length = len(walk) - 1

    #--------------------------------------------------
    #-----------------return the output----------------
    #--------------------------------------------------

    #Outputing to the physical environment the instructions for the AS

    for i in range(length):
        dif_vec = (walk[i+1][0]-walk[i][0],walk[i+1][1]-walk[i][1])
        _move(dif_vec[0], dif_vec[1])
    _exit()

    return {"walk": walk, "traversal_cost": length, "supply_units_recovered": SU}


@app.function(hide_code=True)
#Define Brute Force
def Brute_Force(G, AS, SU, VP, EP, SUP, ASP, GP):

    #--------------------------------------------------
    #---------------------Imports----------------------
    #--------------------------------------------------

    import networkx as nx
    from collections import deque

    #--------------------------------------------------
    #------------Initialise Helper Functions-----------
    #--------------------------------------------------
    def _move(x,y):
        #move
        return

    def _exit():
        #exit
        return

    def _next_perm(perm):
        layer = -1
        max_index = -1

        #Finds the layer and max_index
        for i in range(len(perm)-1):
            if perm[i] < perm[i+1]:
                layer = i+1
                for j in range(i+1):
                    if perm[j] < perm[i+1]:
                        if max_index == -1:
                            max_index = j
                break

        #swaps layer and max_index
        if(layer != -1):  
            z = perm[layer]
            perm[layer] = perm[max_index]
            perm[max_index] = z
        else:
            layer = len(perm)

        #swaps the subpermuation up to layer around
        for i in range((layer+(layer%2))//2):
            z = perm[i]
            perm[i] = perm[layer-i-1]
            perm[layer-i-1] = z

        return perm


    def _BFS(G, s):
        #s is first vertex
        V = G.nodes()
        BFS_Queue = deque()
        BFS_Queue.append(s)
        visited = {v: False for v in V} #map
        visited[s] = True

        parent = {v: None for v in V} #map

        while BFS_Queue:
            u = BFS_Queue.popleft()
            for v in G[u]:
                if not visited[v]:

                    visited[v] = True
                    BFS_Queue.append(v)
                    parent[v] = u

        return parent

    #--------------------------------------------------
    #-----------------------Main-----------------------
    #--------------------------------------------------

    CRUDY_1 = list(AS)[0]
    entry = ASP[CRUDY_1]["location"]
    V = G.nodes()

    exits: set = set()
    for v in V:
        if VP[v]["is_exit"] == True: 
            exits.add(v)

    SU_locations = {SUP[su]["location"] for su in SU} # a set of SU locations

    POI = exits.copy()
    POI = POI.union(SU_locations)
    POI.add(entry)

    dm = {v:{u:None for u in POI} for v in POI} # Distance Matrix
    pm = {v:{u:None for u in POI} for v in POI} #Path Matrix



    #Getting distance and path between exits, the entry and SUs.
    for v in POI:
        parent = _BFS(G,v)
        for u in POI:
            w = u
            path = []
            while parent[w] != None:
                path.insert(0, w) #leaves out the first node
                w = parent[w]
            pm[v][u] = path
            dm[v][u] = len(path)


    #Finding shortest walk.

    min_perm = []
    min_dist = None

    su_perm = [i for i in range(len(SU_locations))]
    original_perm = su_perm.copy()
    su_loc = [v for v in SU_locations]
    while True: 
        for exit in exits: # su_perm is a list.
            dist = 0
            perm = [entry]
            for i in range(len(su_perm)):
                perm.append(su_loc[su_perm[i]])
            perm.append(exit)
            for i in range(len(perm)-1):
                dist = dist + dm[perm[i]][perm[i+1]]
            if min_dist == None:
                min_perm = perm
                min_dist = dist
            elif dist < min_dist:
                min_perm = perm
                min_dist = dist
        su_perm = _next_perm(su_perm)
        back_to_original = True
        for i in range(len(su_perm)):
            if su_perm[i] != original_perm[i]:
                back_to_original = False
                break
        if back_to_original:
            break

    walk = [entry]
    for i in range(len(min_perm)-1):
        walk += pm[min_perm[i]][min_perm[i+1]]

    for i in range(len(walk)-1):
        dif_vec = (VP[walk[i+1]]["location"][0]-VP[walk[i]]["location"][0],VP[walk[i+1]]["location"][1]-VP[walk[i]]["location"][1]) 
        # a tuple
        _move(dif_vec[0], dif_vec[1])
    _exit()

    return {"walk": walk, "traversal_cost": len(walk)-1, "supply_units_recovered": SU}


@app.function(hide_code=True)
#Define Greedy
def Greedy(G, AS, SU, VP, EP, SUP, ASP, GP):

    #--------------------------------------------------
    #---------------------Imports----------------------
    #--------------------------------------------------

    import networkx as nx
    from collections import deque

    #--------------------------------------------------
    #------------Initialise Helper Functions-----------
    #--------------------------------------------------

    def _move(x,y):
        #move
        return

    def _exit():
        #exit
        return

    def _BFS(G, s):
        #s is first vertex
        V = G.nodes()
        BFS_Queue = deque()
        BFS_Queue.append(s)
        visited = {v: False for v in V} #map
        visited[s] = True

        parent = {v: None for v in V} #map

        while BFS_Queue:
            u = BFS_Queue.popleft()
            for v in G[u]:
                if not visited[v]:

                    visited[v] = True
                    BFS_Queue.append(v)
                    parent[v] = u

        return parent

    #--------------------------------------------------
    #-----------------------Main-----------------------
    #--------------------------------------------------

    CRUDY_1 = list(AS)[0]
    entry = ASP[CRUDY_1]["location"]
    V = G.nodes()

    exits: set = set()
    for v in V:
        if VP[v]["is_exit"] == True: 
            exits.add(v)

    SU_locations = {SUP[su]["location"] for su in SU} # a set of SU locations

    POI = exits.copy()
    POI = POI.union(SU_locations)
    POI.add(entry)

    dm = {v:{u:None for u in POI} for v in POI} # Distance Matrix
    pm = {v:{u:None for u in POI} for v in POI} #Path Matrix



    #Getting distance and path between exits, the entry and SUs.
    for v in POI:
        parent = _BFS(G,v)
        for u in POI:
            w = u
            path = []
            while parent[w] != None:
                path.insert(0, w) #leaves out the first node
                w = parent[w]
            pm[v][u] = path
            dm[v][u] = len(path)



    got_su = {v:False for v in SU_locations}
    perm = [entry]

    #Go to closest SU
    for i in range(len(SU_locations)):
        closest_su = None
        u = perm[len(perm)-1]
        for v in POI:
            if v in SU_locations:
                if not got_su[v] and closest_su == None:
                    closest_su = v
                elif not got_su[v] and dm[u][v] < dm[u][closest_su]:
                    closest_su = v
        if closest_su == None:
            break
        perm.append(closest_su)
        got_su[closest_su] = True


    #Go to closest exit
    closest_exit = None
    u = perm[len(perm)-1]
    for v in POI:
        if v in exits:
            if  closest_exit == None:
                closest_exit = v
            elif dm[u][v] < dm[u][closest_exit]:
                closest_exit = v
    perm.append(closest_exit)  

    walk = [entry]
    for i in range(len(perm)-1):
        walk += pm[perm[i]][perm[i+1]]

    for i in range(len(walk)-1):
        dif_vec = (VP[walk[i+1]]["location"][0]-VP[walk[i]]["location"][0],VP[walk[i+1]]["location"][1]-VP[walk[i]]["location"][1]) 
        # a tuple
        _move(dif_vec[0], dif_vec[1])
    _exit()

    return {"walk": walk, "traversal_cost": len(walk)-1, "supply_units_recovered": SU}


@app.function(hide_code=True)
#Define Divide and Conquer
def Divide_and_Conquer(G, AS, SU, VP, EP, SUP, ASP, GP):

    #--------------------------------------------------
    #---------------------Imports----------------------
    #--------------------------------------------------

    import networkx as nx
    from collections import deque

    #--------------------------------------------------
    #------------Initialise Helper Functions-----------
    #--------------------------------------------------

    def _move(x,y):
        #move
        return

    def _exit():
        #exit
        return



    # 1. Break up graph into sub graphs by articulation points 
    def _BFS(G, exit, entry): #to find path, any will do.
        #s is first vertex
        V = G.nodes()
        BFS_Queue = deque()
        BFS_Queue.append(entry)
        visited = {v: False for v in V} #map
        visited[entry] = True

        parent = {v: None for v in V} #map

        while BFS_Queue:
            u = BFS_Queue.popleft()
            for v in G[u]:
                if not visited[v]:

                    visited[v] = True
                    BFS_Queue.append(v)

                    parent[v] = u

        path = [exit]
        while path[-1] != entry:
            path.append(parent[path[-1]])
        path.reverse()

        return path

    def _find_local_group(G, entry, pivots):
        if entry in pivots:
            raise Exception()

        V = G.nodes()
        BFS_Queue = deque()
        BFS_Queue.append(entry)
        visited = {v: False for v in V} #map
        visited[entry] = True
        local_group = {entry}

        while BFS_Queue:
            u = BFS_Queue.popleft()
            for v in G[u]:
                if not visited[v] and not v in pivots:
                    local_group.add(v)
                    visited[v] = True
                    BFS_Queue.append(v)
                elif v in pivots:
                    local_group.add(v)

        return local_group

    def _break_graph(G, ap, exit, entry):

        path = _BFS(G, exit, entry)


        pivots = []
        in_sub_graphs = []


        for i in range(1,len(path)-1):
            if path[i] in ap and G.degree(path[i]) == 4: #there are more spaces to split the graph, but its a bit complicated so I'm not gonna go there. (i.e. when the other degrees of the path are trees.)
                pivots.append(path[i])
                in_sub_graphs.append(path[i+1])

        sub_graphs = []
        sub_graphs.append(_find_local_group(G, entry, pivots))

        for u in in_sub_graphs:
            if u in pivots:
                sub_graphs.append({u,pivots[pivots.index(u)-1]})
            else:
                sub_graphs.append(_find_local_group(G, u, pivots))

        missed_nodes = set(G.nodes())
        for sub_graph in sub_graphs:
            missed_nodes -= sub_graph

        while missed_nodes:
            u = missed_nodes.pop()
            local_group = _find_local_group(G, u, pivots)
            for sub_graph in sub_graphs:
                if local_group&sub_graph:
                    sub_graph |= local_group
                    break
            missed_nodes -= local_group


        return sub_graphs, pivots


    #--------------------------------------------------
    #-----------------------Main-----------------------
    #--------------------------------------------------

    CRUDY_1 = list(AS)[0]
    V = G.nodes()

    exits = set()
    for v in V:
        if VP[v]["is_exit"] == True:
            exits.add(v)

    SU_locations = {SUP[su]["location"] for su in SU}
    entry = ASP[CRUDY_1]["location"]
    POI = exits.copy()

    walks = []

    VPbrute = {v: VP[v].copy() for v in G.nodes()}
    VPbrute[entry]["is_entry"] = False
    for exit in exits:
        VPbrute[exit]["is_exit"] = False

    SUPbrute = {su:{"location":su} for su in SU_locations}

    ap = set(nx.articulation_points(G.to_undirected(as_view = True)))

    for exit in exits:

        sub_graphs, pivots = _break_graph(G, ap, exit, entry)

        pivots.insert(0,entry)
        pivots.append(exit)

        walk = [entry]
        for i in range(len(sub_graphs)):
            sub_graph = G.subgraph(sub_graphs[i])

            SU_sub_graph = sub_graphs[i]&SU_locations

            VPbrute[pivots[i]]["is_entry"] = True
            VPbrute[pivots[i+1]]["is_exit"] = True

            #Refer to the Brute Force algorithm option to see what goes on here.
            walk += Brute_Force(sub_graph, {0}, SU_sub_graph, VPbrute, {}, SUPbrute, {0:{"location":pivots[i]}}, {})["walk"][1:]

            VPbrute[pivots[i]]["is_entry"] = False
            VPbrute[pivots[i+1]]["is_exit"] = False

        walks.append(walk)



    best_walk = None
    for check_walk in walks:
        if best_walk == None:
            best_walk = check_walk
        elif len(check_walk) < len(best_walk):
            best_walk = check_walk

    for i in range(len(best_walk)-1):
        dif_vec = (VP[best_walk[i+1]]["location"][0]-VP[best_walk[i]]["location"][0],VP[best_walk[i+1]]["location"][1]-VP[best_walk[i]]["location"][1]) # a tuple
        _move(dif_vec[0], dif_vec[1])
    _exit()


    return {"walk": best_walk, "traversal_cost": len(best_walk)-1, "supply_units_recovered": SU}


@app.function(hide_code=True)
#Define validate output

def validate_output(_out, G, AS, SU, VP, EP, SUP, ASP, GP):
    _walk = _out["walk"]
    _SU = _out["supply_units_recovered"]


     #----------------verifying walk------------------
    for i in range(len(_walk)-1):
        #constraint 3
        if not _walk[i] in G.nodes():
            return "Walk contains a false node"
        #constraint 4
        if not (_walk[i],_walk[i+1]) in G.edges():
            return "Walk contains a false edge"
    #constraint 3
    if not _walk[-1] in G.nodes():
        return "Walk contains a false node"


    #constraint 1
    if not VP[_walk[0]]["is_entry"]:
        return "Walk doesn't start at the entry"
    #constraint 2
    if not VP[_walk[-1]]["is_exit"]:
        return "Walk doesn't end at an exit"


    #-------verifying supply units collected--------- 
    walk_set = set(_walk)

    #constraint 5
    if _SU - set(SUP.keys()):
        return "A supply unit recovered doesn't exist"
    if ({SUP[s]["location"] for s in _SU} - walk_set):
        return "A supply unit recovered was not recovered by the walk"
    elif ({SUP[s]["location"] for s in SU} - {SUP[s]["location"] for s in _SU})&walk_set:
        return "Not all supply units recovered by walk were stated"


    #-----------verifying traversal cost-------------

    #constraint 6
    if (len(_walk)-1 != _out["traversal_cost"]):
        return "Traversal cost is not accurate."

    return "valid"


@app.function(hide_code=True)
#Define algorithms map
def m_algorithms():
    algorithms = {}
    algorithms["BFS+DFS"] = BFS_DFS
    algorithms["Brute Force"] = Brute_Force
    algorithms["Greedy"] = Greedy
    algorithms["Divide and Conquer"] = Divide_and_Conquer
    return algorithms


@app.cell(hide_code=True)
def _(algorithms, seed_input):
    #define m_gif_v2
    def front_focus_v2(_walk):
        leading = "#FF0000"
        base_col = '#58D4D3' 

        _col_dict = {c_Av2(v):base_col for v in _walk}

        _col_dict[c_Av2(_walk[len(_walk)-1])] = leading

        return _col_dict

    def default_title(mini = "Multi-Wing Facility",seed = None, has_walk = False, walk_length = -1, algorithm = None, memo = None,n_wing = -1,animated = False):
        if seed == None:
            seed = seed_input.value

        title = ""
        if mini != "" and mini != None:
            title += mini


        if seed != None:
            if title != "": title += " -- "
            title += "Seed " + str(seed)

        if memo != None:
            if title != "": title += " · "
            title += "memo "+ memo

        if n_wing >= 0: 
            if title != "": title += " · "
            title += f"{n_wing} Wings"


        if has_walk and algorithm != None:
            if title != "": title += " · "
            if animated:
                title += "Animation of "
            title += f"{algorithm}'s "
            if walk_length >= 0:
                title += f"{walk_length} Long "
            title += "Walk"

        return title


    def m_gif_v2(custom_seed = None, algorithm = "BFS+DFS", title = None):
        seed = seed_input.value

        if(custom_seed != None):
            seed = custom_seed

        if not os.path.exists("figs/"):
           os.mkdir("figs/")

        if (os.path.exists("figs/"+ str(seed)+ f"_{algorithm}_v2" + ".gif")):
            return "exists already"


        _fac = m_fac_Av2(seed)
        _G, _AS, _SU, _VP, _EP, _SUP, _ASP, _GP = c_fac_Bv2(_fac)
        _walk = algorithms[algorithm](_G, _AS, _SU, _VP, _EP, _SUP, _ASP, _GP)["walk"]


        if(title == None):
            title = default_title(mini = "", seed = seed, has_walk = True, algorithm = algorithm,animated = True)

        _fig, _ax= draw_fac_v2(_fac, legend = False, title = title)

        for _i in range(len(_walk)): 
            _highlight_path = [c_Av2(v) for v in _walk[0:_i+1]]
            _node_colors = front_focus_v2(_walk[0:_i+1])


            if _highlight_path and len(_highlight_path) > 1:
                px = [0.5 + c_Bv2((w,c,r))[0] for w,c,r in _highlight_path] 
                py = [0.5 + r for w,c,r in _highlight_path] 
                path_plot, = _ax.plot(px, py, color=COL_PATH, lw=1.8, linestyle='--', alpha=0.75, zorder=4)

            if _node_colors:
                rectangles = []
                for node, color in _node_colors.items():
                    c, r = c_Bv2(node)
                    rect = plt.Rectangle((c, r), 1, 1, color=color, alpha=0.50, zorder=2)
                    rectangles.append(rect)
                    _ax.add_patch(rect)


            name = "figs/"
            name += str(seed) + "_"
            name += f"{algorithm}_"
            name += "v2_"
            name += str(_i)
            name += ".png"

            plt.savefig(name)
            if _highlight_path and len(_highlight_path) > 1:
                path_plot.remove()

            if _node_colors:
                for rect in rectangles:
                    rect.remove()
        plt.close()

        list_of_im_paths = []
        for _i in range(len(_walk)): 
            _name = "figs/"
            _name += str(seed) + "_"
            _name += f"{algorithm}_"
            _name += "v2_"
            _name += str(_i)
            _name += ".png"
            list_of_im_paths.append(_name)

        path_to_save_gif = "figs/"+ str(seed)+ f"_{algorithm}_v2" + ".gif" 
        ims = [imageio.v2.imread(f) for f in list_of_im_paths]
        dur = [0.05 for f in list_of_im_paths]
        dur[len(dur)-1] = 2
        imageio.v2.mimsave(path_to_save_gif, ims, duration = dur, loop = 10000)

        for _i in range(len(list_of_im_paths)):
            if os.path.exists(list_of_im_paths[_i]):
                os.remove(list_of_im_paths[_i])

        return "ran successfully"


    return default_title, front_focus_v2, m_gif_v2


@app.cell(hide_code=True)
def _():
    #Seed Input
    seed_input = mo.ui.number(
        value=30012009,
        start=0,
        stop=99999999,
        step=1,
        label="Seed "

    )
    mo.callout(mo.vstack([
        mo.md("### Enter the seed, then press Enter to rebuild the facility."),
        seed_input
    ]),kind = "success")
    return (seed_input,)


@app.cell
def _():
    algorithms = m_algorithms()
    return (algorithms,)


@app.cell(hide_code=True)
def _(algorithms, seed_input):
    # RUN algorithms

    def benchmark_algorithm(algorithm, seed = None):
        if seed == None:
            seed = seed_input.value

        G, AS, SU, VP, EP, SUP, ASP, GP = c_fac_Bv2(m_fac_Av2(seed))

        tracemalloc.start()
        tracemalloc.reset_peak()
        _size1, _peak1 = tracemalloc.get_traced_memory()

        _start_time = time.perf_counter()
        out = algorithms[algorithm](G, AS, SU, VP, EP, SUP, ASP, GP)
        time_taken = time.perf_counter() - _start_time
        _size2, _peak2 = tracemalloc.get_traced_memory()

        #print("size: "+str(_size2)+", peak:" + str(_peak2))
        #print("size: "+str(_size2-_size1)+", peak:" + str(_peak2-_peak1))
        tracemalloc.stop()
        is_valid = validate_output(out, G, AS, SU, VP, EP, SUP, ASP, GP)
        return out, _peak2 - _size1, time_taken, {"G": G, "AS": AS, "SU": SU, "VP":VP,"EP": EP,"SUP": SUP,"ASP": ASP,"GP": GP}, is_valid

    return (benchmark_algorithm,)


@app.cell(hide_code=True)
def _(algorithms, benchmark_algorithm):
    out_v2, memory_v2, speed_v2, walk_v2, valid_v2 = {},{},{},{},{}
    for _algorithm in algorithms.keys():
        out_v2[_algorithm], memory_v2[_algorithm],speed_v2[_algorithm], _, valid_v2[_algorithm] = benchmark_algorithm(_algorithm) 
        walk_v2[_algorithm] = out_v2[_algorithm]["walk"]
    return memory_v2, out_v2, speed_v2, valid_v2, walk_v2


@app.cell
def _(seed_input):
    fac_Av2 = m_fac_Av2(seed_input.value)
    return (fac_Av2,)


@app.cell
def _(seed_input):
    G, AS, SU, VP, EP, SUP, ASP, GP = c_fac_Bv2(m_fac_Av2(seed_input.value))
    return AS, ASP, EP, G, GP, SU, SUP, VP


@app.cell(hide_code=True)
def _():
    mo.callout(mo.accordion({"<p style = 'font-size: 25px'>Code to test algorithms</p>":rf"""

    Below is the copy-paste code to quickly test the algorithms.

    Use main1 to test algorithms based off the facility seeds, and main2 to do it based of the the facilities themselves. Choose which algorithm to test via the key 'algorithm', however note that 'Brute Force' is the algorithm selected in part D.

    An example of how to use the main1 function:
    ```python
    #Example of how to use main1
    #main1([1,2,3,4,5,6,7,8], algorithm = "BFS+DFS") 
    #main1([1,2,3,4,5,6,7,8], algorithm = "Divide and Conquer") 
    main1([1,2,3,4,5,6,7,8], algorithm = "Brute Force") 
    #main1([1,2,3,4,5,6,7,8], algorithm = "Greedy") 
    ```

    Code:
    ```python
    import networkx as nx
    import random
    from collections import deque

    WING_COLS = 10
    WING_ROWS = 10
    GAP = 3



    def main1(seeds, algorithm = "Brute Force"): #tests based off seeds
        algorithms = m_algorithms()
        outputs = []
        for seed in seeds:
            G, AS, SU, VP, EP, SUP, ASP, GP = c_fac_Bv2(m_fac_Av2(seed))
            out_Bv2 = algorithms[algorithm](G, AS, SU, VP, EP, SUP, ASP, GP)
            outputs.append(c_out_Av2(out_Bv2))
        return outputs

    def main2(facilities, algorithm = "Brute Force"): #same as main1, except tests bases off facilities
        algorithms = m_algorithms()
        outputs = []
        for fac in facilities:
            G, AS, SU, VP, EP, SUP, ASP, GP = c_fac_Bv2(fac)
            out_Bv2 = algorithms[algorithm](G, AS, SU, VP, EP, SUP, ASP, GP)
            outputs.append(c_out_Av2(out_Bv2))
        return outputs




    {inspect.getsource(m_algorithms)}

    {inspect.getsource(m_fac_Av2)}

    {inspect.getsource(c_Av2)}

    {inspect.getsource(c_Bv2)}

    {inspect.getsource(c_fac_Bv2)}

    {inspect.getsource(c_out_Av2)}

    {inspect.getsource(BFS_DFS)}

    {inspect.getsource(Brute_Force)}

    {inspect.getsource(Greedy)}

    {inspect.getsource(Divide_and_Conquer)}

    ```

    """}))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Amendments to memo 1

    Assumptions:
    - Added an assumption that the inter-wing corridors are of length 4 in physical space (to match the representation provided).

    Problem Outline:
    - Changed to match new problem scope of memo A1.

    Definitions:
    - Changed the definition of a corridor.

    A:
    - A1:
        - Inputs:
            - Added location property to VP giving a tuple as a location
            - Added wing property to VP
            - Removed cardinal angle from EP
        - Outputs:
            - Changed move(a: angle, l: length) functions to move(x: East, y: North)
            - Changed v in V from G = (V,E) to be named by coordinate location.

    - A2 - Salient Features:
        - Changed Location and direction in the salient features as they are stored differently and abstracted differently than in memo 1.

    - A3:
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
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Action 1 Revision -- Data Model Redesign

    #### Part 1 -- Identify limitations of the Memo 1 model
    The inputs and outputs described in memo 1 part A1 are sufficient to accommodate for the memo A1 problem. However they were a bit clunky and some unrelated changes were made, including:

    - Inputs:
        - Added location property to VP giving a tuple as a location
        - Added wing property to VP
        - Removed cardinal angle from EP
    - Outputs:
        - Changed move(a: angle, l: length) functions to move(x: East, y: North)
        - Changed output to have location of vertices not vertex names as the location of vertices.

    #### Part 2 -- Evaluate two design approaches
    - Flat Graph:
        - The current algorithmic problem statement handles this perfectly.
        - Pro: It allows for easy traversal between the wings as they are abstracted away.
        - Con: Might be worse for a heuristic algorithm approach, as traversing through each wing sequentially is an efficient solution.
    - Hierarchical Graph:
        - This would involve changing the algorithmic problem statement by adding another overarching graph.
        - Pro: It would allow for clear segmentation between the wings.
        - Con: It causes the input to become incredibly complicated and makes algorithms to find optimal solutions harder to implement.
    #### Part 3 -- Select, specify, and justify
    - The tuple ADT was added to allow for coordinate positions to be represented in the graph. A tuple was selected as it is an immutable data type, allowing for constants to be easily conveyed.


    ### Action 2 Revision -- Algorithm Redesign

    #### Part 1 -- Identify the new sub-problems
    Some new challenges brought by the addition of additional wing(s) are:
    - Introduces cycles into the graph, meaning it is no longer a tree.
    - Introduces additional nodes into the graph, and different types of edges.

    These were addressed by:
    - Flattening the graph to abstract the wings away.
    - The multiple inter-wing corridors (cycles) were addressed by each algorithm differently:
        - BFS+DFS: This creates a minimum spanning tree of the graph, so it always ignores the cycle.
        - Greedy: Doesn't care about cycles so it treats it as a normal edge.
        - Brute Force: Tries each potential route to find the best one.
        - Divide and Conquer: Tries each potential route (in a more efficient way) to find the best one.

    #### Part 2 -- Evaluate two wing-traversal strategies
    Exhaustive (moves through the wings one by one):
    - Although seems like a smart way to minimise backtracking, there are sometimes more optimal routes that involve looping around through the inter-wing corridors.

    Interleaved (treating the wings together as one big graph):
    - This was the approach my algorithms took, where they took the whole graph in together, not just parts of it. Although more computationally expensive, it allows for a more thorough solution. And when the speeds are in the milliseconds, there is no need to worry about speed.

    #### Part 3 -- Describe your revised algorithm in full
    As has been stated before, the facility is treated as one big connected graph, not multiple different graphs. Therefore all my algorithms function fundamentally the same as before, although 'Brute Force' was chosen in part D over 'BFS+DFS' (the previous algorithm) as justified by the introduction of cycles.

    A description of the implementation 'Brute Force' can be found in part B.

    ### Action 3 Revision -- Pseudocode Update
    As all the wings are flattened onto the graph G, there is no special 'intra-wing traversal logic' separate from 'inter-wing traversal logic'. This allows for a streamlined and more straightforward solution. Therefore, no special wings affect the solution (like wings without supply units) as the algorithms simply traverse straight through them.

    To see the updated pseudocode, refer to part C1. 'Brute Force' is the one utilised for reasons specified in part D.


    ### Action 3b Revision -- Revised Algorithm Implementation -- Multi-wing.

    All revised algorithms can be seen in part C2. Use part C3 and C4 to run, test and compare the algorithms. 'Brute Force' is the one utilised for reasons specified in part D.

    ### Action 4 Revision -- Justification Update.

    Please refer to part D to see the updated justification.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Memo 1 to Memo A1 Changes

    This colour coding system conveys how changes were made to the rest of the document.
    - <span class = "y">Yellow text describes changes made.</span>
    - <span class = "g">Green text is newly added content.</span>
    - <span class = "r">Red text is removed content.</span>

    Although an effort was made to highlight all changes, some changes involved complex structures that can't be highlighted and others were too small to mention (like spelling). In the case of a complex structure being added, deleted or changed, yellow text should be present to describe the changes made.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Problem Outline (memo  <span class = "r">1</span> <span class = "g">A1</span> ):

    Seismic activity has destabilised the Emberlight Subterranean Research Complex (ESRC). Five critical supply units — designated S1 through S5 — remain scattered throughout the structure and are to be recovered.

    <div class = "r">
    <p>The ESRC is organised as a sector grid. Each sector is a discrete navigable unit. Sectors are connected by reinforced corridors. The sector grid can be seen below.</p>

    <p>The objective is to command CRUDY-1 (Corridor Reconnaissance and Utility Drone — Year 1)--an Autonomous System (AS)--to navigate the facility’s corridor network and transport recovered supply units to an extraction point while maximising recovered supply units and ensuring a safe extraction.</p>
    </div><br>

    <div class = "g">
    <p>The ESRC is organised as multiple sector grids. Each sector grid is a rectangle containing 10 by 10 sectors. Each sector is a discrete navigable unit. Sectors are connected by reinforced intra-wing corridors, and sector grids are connected by inter-wing corridors. The sector grid can be seen below.</p>

    <p>The objective is to command CRUDY-1 (Corridor Reconnaissance and Utility Drone — Year 1)--an Autonomous System (AS)--to navigate the facility’s corridor network and transport recovered supply units to an extraction point while ensuring a safe extraction. Ideally, the route taken by the AS minimises traversal cost and maximises the number of supply units recovered.</p></div>




    (Nielsen, 2026)
    """)
    return


@app.cell
def _(default_title, fac_Av2):
    #draw_facility
    draw_fac_v2(fac_Av2, title = default_title(n_wing=2))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <mark>Facility Changed.</mark>
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    This notebook explores the development of a design strategy to complete this task, including
    1. deciding how the facility and mission should be represented computationally;
    2. identifying the constraints governing the AS's operation;
    3. designing an initial strategy and communicating it clearly;
    4. analysing efficiency and feasibility;
    5. refining and improving the design as new constraints emerge;
    6. justifying decisions and comparing alternatives with depth.

    (Nielsen, 2026)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Definitions:
    Spaces:
    - ESRC: The Emberlight Subterranean Research Complex, the scope of this problem.
    - Sector: A single unit of space, which can be occupied by an autonomous system (AS).
    - Sector Grid: A grid of sectors, joined by corridors and contained within the ESRC.


    Movement Options:
    - <span class = "r">Corridor: Connects two adjacent sectors in the same sector grid that do not have a wall in-between them. Can be bidirectional or one-way.</span>
    - <span class = "g">Inter-wing Corridor: This is shown as the red dotted line connecting two sectors from two different sector grids, which allows for direct movement between those two sectors.</span>
    - <span class = "g">Intra-wing Corridor: an intra-wing corridor is the absence of a wall between two adjacent sectors in the same sector grid</span>
    - <span class = "g">Corridor: A corridor is an intra-wing corridor or an inter-wing corridor.</span>

    Types of Sectors:
    - Exit: (or Extraction Point), this is where an AS can end its journey.
    - Entry: (or starting sector), this is where an AS begins its journey.
    - Supply Unit: the sector contains a supply unit
    - Point of Interest (POI): an exit, an entry or a supply unit sector.

    Acronyms:
    - G: (Graph of a Sector Grid) = (V,E)
    - V: (Vertices or Nodes of G)
    - E: (Edges, corridors in this case of G)
    - SU: (Supply Unit)
    - AS: (Autonomous System)
    - EP: (Edge Properties)
    - VP: (Vertex Properties)
    - SUP: (Supply Unit Properties)
    - ASP: (Autonomous Systems Properties)
    - GP: (Graph Properties)

    <div class = "g">
    Other:<br>
    &#x2022; Facility: Another word for the ESRC, the environment containing all the sector grids.<br>
    &#x2022; Facility A: The representation of the facility defined by Kodie Nielsen.<br>
    &#x2022; Facility B: The representation of the facility defined by Kieran in part A1 - Algorithmic Problem Statement.
    </div>

    ## Assumptions:
    1.  An Autonomous System (AS) knows the layout of the ESRC sector grid before it navigates it (e.g. it has the blueprints).
    2.  ASs can navigate in all directions without turning, and ASs know their original orientation.
    3.  <span class = "g">inter-wing corridors have a length of 4 and intra-wing corridors have a length of 1, to match the facility representation. this is not correlated to traversal cost.</span>
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part A - Problem Specification:
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A1 - Algorithmic problem statement:
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Inputs:

    The input is a <b><u>directed</u></b> unweighted graph, two sets and five maps. <br>
    **Note**: the five maps are just providing properties for the elements of the four sets (as a graph is just two sets) and properties of the whole environment.

    Graph: <br>
    G: (Graph of a Sector Grid) = (V,E)<br>

    Sets: <br>
    SU: (Supply Units)<br>
    AS: (Autonomous Systems)<br>

    Maps: <br>
    EP: (Edge Properties)<br>
    VP: (Vertex Properties)<br>
    SUP: (Supply Unit Properties)<br>
    ASP: (Autonomous Systems Properties)<br>
    GP: (Graph Properties)

    #### Graph - Sector Grid, G=(V,E):

    Graph, G = (V,E) where V = set of all vertices in G and E = set of all edges in G. Each vertex in V is a sector and each edge in E is a corridor between two sectors.

    This can be represented as:

    G = (V,E)

    V = {v | v is a sector in the Emberlight Subterranean Research Complex}

    E = {(u,v) | u,v∈V ∧ u is adjacent to v ∧ direct movement can be taken from u into v, without going through any other sectors}

    #### Sets

    The following two sets contain elements from the ESRC.

    ##### Set 1 - Supply Units (SU):

    This is a set containing all supply units in the Sector Grid.<br>
    SU = {x | x is a supply unit in the Sector Grid}.

    ##### Set 2 - Autonomous Systems (AS):

    This is a set containing all Autonomous Systems (AS) being deployed in the Sector Grid.<br>
    AS = {x | x is an Autonomous System being deployed in the Sector Grid}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md("""
    #### Maps

    The following four ADTs are maps of maps, where the keys map to a map of properties of that key. The properties might have keys with values, such as 'weight: 1'. The final map gives properties of the whole ESRC.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ##### Map 1 - Edge Properties (EP):

    The first map, EP (Edge Properties), takes the edges as keys and returns a map that contains:

    <span class = "r">- a real number indicating which direction this edge is pointing (cardinal angle). 0° faces north, 90° east, 180° south and 270° west.</span>

    <span class = "g">- nothing in memo A1 problem scope</span>

    Beyond the scope of memo  <span class = "r">1</span> <span class = "g">A1</span>:

    - a real number indicating the cost to traverse (as it is all the same)
    - a real number indicating the stability of the corridor.
    - a real number indicating the length of the corridor.

    In memo  <span class = "r">1</span> <span class = "g">A1</span>, a possible implementation of this is:

    <span class = "r">EP = {(u,v):{ "cardinal_angle": real number (cardinal angle from u to v)}
    	| u,v ∈ V ∧ (u,v) ∈ E}</span>

    <span class = "g">EP = {(u,v):{}}</span>

    ##### Map 2 - Vertex Properties (VP):

    This map, VP (Vertex Properties), takes vertices (or sectors) as keys and returns a map that contains:

    - a string indicating what supply unit lies within the sector, or null if no supply unit is contained.
    - a Boolean value indicating whether it is an entry.
    - a Boolean value indicating whether it is an exit.

    - <span class = "g">a tuple of real valued numbers indicating position, where 1 unit length is equal to 1 intra-wing corridor's length.</span>
    - <span class = "g">a string indicating which wing the vertex is located in.</span>

    Beyond the scope of memo  <span class = "r">1</span> <span class = "g">A1</span>:

    - a value indicating the stability of the sector.
    - size
    - shape

    In memo  <span class = "r">1</span> <span class = "g">A1</span>, a possible implementation of this is:

    VP = {v : {
        "supply_unit": nullable string (name of supply unit within the sector, null if it does not contain a supply unit),<br>
        "is_entry": Boolean (true if the sector is an entry, false otherwise), <br>
        "is_exit": Boolean (true if the sector is an extraction point, false otherwise),<br>
        <span class = "g">"wing": String (name of the wing v is in), </span><br>
        <span class = "g">"location": (Integer, Integer)} </span><br>
        | v ∈ V}

    ##### Map 3 - Supply Unit Properties (SUP):

    This map, SUP (Supply Unit Properties), takes a supply unit as a key and returns a map that contains:

    - a sector (a vertex of graph G) indicating location (the sector on which the supply unit lies)

    Beyond the scope of memo  <span class = "r">1</span> <span class = "g">A1</span>:<br>
    In the memo  <span class = "r">1</span> <span class = "g">A1</span> problem scope, these properties of the supply units are irrelevant, so they won't be included in the map returned for each supply unit:
    - a real number indicating the weight of the supply unit (as in the memo  <span class = "r">1</span> <span class = "g">A1</span> problem, all supply unit weights are the same)
    - fragility
    - importance
    - size
    - lifespan

    In memo  <span class = "r">1</span> <span class = "g">A1</span>, a possible implementation of this is:

    SUP = {s:{"location": v (the sector of the SU)} | v∈V∧s∈SU}

    ##### Map 4 - Autonomous System Properties (ASP):

    This map, ASP (Autonomous System Properties), takes Autonomous Systems (ASs) as keys and returns a map that contains:

    - a vertex which is the starting location (or entry) of the AS.

    Beyond the scope of memo  <span class = "r">1</span> <span class = "g">A1</span>:

    - a string indicating type (e.g. CRUDY-1) (as in memo  <span class = "r">1</span> <span class = "g">A1</span> there is only one type)
    - a real number indicating the total weight the AS can carry. (as in memo  <span class = "r">1</span> <span class = "g">A1</span> this equals the total supply units on the map)
    - a real number indicating how many supply units AS can carry at once. (that is different from the weight, right now they are the same so this is not necessary)
    - a real number indicating total energy of the AS.
    - a real number indicating how much energy a corridor takes.
    - a list of SUs that the AS has been assigned to extract.
    - a vertex indicating assigned extraction point for the AS.
    - a real number indicating speed of the AS.

    In memo  <span class = "r">1</span> <span class = "g">A1</span>, a possible implementation of this is:

    ASP (Autonomous System Properties) = {x:{"entry": v (indicates entry for AS)}| x ∈ AS ∧ v ∈ V}

    ##### Map 5 - Graph Properties (GP):

    This map provides properties of the whole environment, such as:

    - a Boolean value indicating whether emergency lighting is operational
    - a time limit

    These are all beyond the memo  <span class = "r">1</span> <span class = "g">A1</span> problem scope, so:

    GP = {}

    ### Outputs

    #### Computational Outputs

    The output of the algorithm that the AS is running is a map containing:
    - A walk taken by the AS that maximises the number of supply units extracted. It starts at an entry and ends at an exit. (as a list). <span class = "g">The list for the walk is the sequence of locations of the vertices visited</span>
    - Total energy expended (as a real number)
    - Supply Units recovered (as these are collected instantaneously) (as a set)

    It doesn't have to be a perfect solution, but it should aim to be an efficient one.

    so the output might look like:

    <div class = "r">output = {"walk":  [$v_1$,$v_2$,$v_3$,...,$v_n$],<br>
    "traversal_cost": real number,<br>
    "supply_units_recovered": {$s_1$,$s_2$,$s_3$,...$s_m$}}</div>

    <span class = "g">output = {"walk":</span><br>
    <span class = "g">[ $(x_1,y_1)$ , $(x_2,y_2)$ , $(x_3,y_3)$ ,..., $(x_n,y_n)$ ],</span><br>
    <span class = "g">"traversal_cost": real number,</span><br>
    <span class = "g">"supply_units_recovered": {$s_1$,$s_2$,$s_3$,...$s_m$}}</span>



    #### Environmental Outputs

    It also has a continuous set of environmental outputs (controlling its actions) in the form of commands including:
    <div class = "r">1. move(a: angle, d: distance) → None         # allows the AS to move 'd' distance at 'a' cardinal angle.</div>
    <div class = "g">1. move(x: distance in x direction, y: distance in y direction) → None         # allows the AS to move 'x' distance in the x direction and 'y' distance in the y direction.</div>
    <div>2. exit() → None         # if at an exit (extraction point), it allows the AS to exit the sector grid</div>

    Note: There is no command that specifically orders to pickup a supply unit as that is automatically done when occupying the same sector as the supply unit.<br>
    Note: There is no command to scan the environment as it is assumed that the AS already knows the layout of the ESRC.


    ### Constraints

    1. The first vertex of the walk AS makes must be an entry.
    2. The last vertex of the walk AS makes must be an exit.
    3. $\forall i [i \in \mathbb{N} \land i \in [1,n] \implies v_i \in V]$
    - meaning all vertices in the walk must be vertices of graph G.
    4. $\forall i [i \in \mathbb{N} \land i \in [1,n-1] \implies (v_i,v_{i+1}) \in E]$
    - meaning all edges in the walk must be edges of graph G.

    <div class = "g">
    5. Supply units collected must match the sectors with supply units traversed by the walk<br>
    6. Traversal cost must match the traversal cost of the walk.
    </div>

    *3 and 4 are simply ensuring the walk is indeed a walk on graph G.

    ### Objectives

    1. Maximise supply unit recovery.
    2. Minimise energy cost. In memo  <span class = "r">1</span> <span class = "g">A1</span><!--TODO in memo A2, change this as not proportional to no edges traversed in the walk-->, this is proportional to the number of edges traversed in the walk, so ||walk|| should be minimised. This is a lower priority compared to the first objective.
    3. Minimise computational time of the algorithm

    These three objectives mean that in the memo  <span class = "r">1</span> <span class = "g">A1</span> problem, the objective is to compute the shortest walk collecting all supply units and making it to the exit with a minimal computational time. This is as the memo  <span class = "r">1</span> <span class = "g">A1</span> problem is quite small and therefore even a brute force approach is relatively fast.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A2 - Salient Features:
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Position
    <div class = "r">1. The position of an object is defined as a vertex of the graph G, with edges describing its position relative to other vertices.</div>
    <div class = "g">1. The position of on object is defined as a tuple (x,y) indicating coordinate location where 1 unit distance is equal to the length of 1 intra-wing corridor.</div>
    2. The direct position (for example as GPS coordinates) is abstracted away and only shown in reference to that of the starting vertex (the entry), as the AS only needs to know where it is in the sector grid relative to other vertices.

    Direction
    <div class = "r">1. This is modelled as a cardinal angle assigned to each edge of the graph G and the direction that the AS is facing. 0º doesn't have to be north, it only has to be consistent.</div>
    <span class = "g">1. The direction can be calculated from the vector going from one vertex to another
        $,\vec{v} = (\Delta x, \Delta y)$ and
        $\theta = tan(\Delta y/ \Delta x)$</span><br>
    2. The physical layout of the sector grid is abstracted away into this grid, as it only matters how to get from one sector to another sector to be able to traverse the whole grid. This can be calculated using the cardinal direction. (i.e. only relative space matters, not absolute.)

    Length
    <div class = "r">1. The length of an edge (i.e. a corridor) can be abstracted away as in memo 1, all corridors have the same length, meaning the AS only has to move in multiples of one edge length of the graph.</div>
    <div class = "g">
    1. Length in physical space in Memo A1 is modelled through magnitude of the displacement vector from one location tuple to another, this however is not to be confused with traversal cost.<br>
    2. Therefore, the length of an edge is the magnitude of the displacement vector from the location of the initial node to its destination. <br>
    3. The length of a walk is the sum of the lengths of the edges in the walk.</div>


    Time
    1. Time is not modelled in the abstraction of memo  <span class = "r">1</span> <span class = "g">A1</span>.
    2. This is a safe abstraction as conditions are stable.

    Mass
    1. Mass is modelled in units. The weight of supply units are all identical (weight = 1) so they can be abstracted away.
    2. As the AS can carry up to 5 units of weight, this is identical to saying the AS can carry up to 5 supply units.
    3. The unit is some weight, which is irrelevant, it only matters relative to other masses.

    Corridors
    1. These are modelled as two edges between the sectors it is between, representing the two ways that one can pass through a corridor. The direction of the corridor is modelled as an cardinal angle.
    2. The shape of the corridor and the roughness of it is abstracted away as it is assumed that all corridors are traversable by the AS. This may or may not be a safe abstraction.<span class = "r"> The length of these corridors are abstracted away as they have the same length and the stability is abstracted away as it is assumed that conditions are stable in memo 1.</span>

    Sectors
    1. These are modelled as vertices on the graph G.
    2. The size and shape of the sectors are abstracted away as they are all assumed to be the same and traversable by the AS. Also the stability isn't modelled as it is assumed to be stable.

    Walls
    1. These are modelled by the lack of an edge connecting the vertices representing the sectors either side of it, marking it as untraversable.
    2. Its existence is somewhat abstracted away and only marked with a 'this is not a route' label, which is fine since the AS can then choose simply never to try going through the wall.

    Supply Units
    1.  These are modelled with a location (being the vertex of G on which they sit).
    2. The supply units are assumed to all be strong enough to handle the AS's handling of them, have an arbitrarily long lifespan, be a size that the AS can handle and all be equally important. These are assumed as there has been no indication otherwise.

    Autonomous Systems (AS)
    1. These are modelled (in the environment) with a location (being a vertex on the graph) and a maximum load capacity.
        - a real number indicating how many supply units AS can carry at once. (that is different from the weight, right now they are the same so this is not necessary)
        - total energy of the AS. (currently irrelevant in the memo  <span class = "r">1</span> <span class = "g">A1</span> problem scope, the AS has more than enough energy)
        - SUs that the AS has been assigned to extract. (all of them so doesn't need to be explicitly mentioned to the AS)
        - assigned extraction point for the AS. (doesn't matter as AS can exit at any extraction point)
        - speed of the AS. (doesn't matter as time is irrelevant in the memo  <span class = "r">1</span> <span class = "g">A1</span> problem scope)
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## A3 - ADTs for Modelling
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ADTs
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
    <span class = "y">To avoid ambiguity, names have been changed:</span><br>
    insert_at(l: list, i: Index, e: Element) → list<br>
    <span class = "r">insert_at</span> <span class = "g">concatenate_at</span>(l1: list, i: Index, l2: list) → list<br>
    append(l: list, e: Element) → list<br>
    <span class = "r">append</span> <span class = "g">concatenate</span>(l1: list, l2: List) → list<br>
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
    <span class = "r">remove_at(a: Array, i: Index) → Array</span><br>
    lookup(a: Array, i: Index) → Element<br>
    length(a: Array) → Integer

    Note:
    - array_name[i] ⇔ array_name.lookup(i) (when getting the value at i)
    - array_name[i] ← e ⇔ array_name.set(i,e) (when setting the value at i to e)

    <div class = "g">
    9. Tuple<br>
    lookup(t: Tuple, i: Index) → Element<br>
    length(t: Tuple) → Integer<br>

    Note:<br>
    &#x2022; tuple_name[i] ⇔ tuple_name.lookup(i) (when getting the value at i)
    </div>

    ### ADTs used <!--potential improvements to be made-->

    #### Inputs:

    - A Graph of the Sector Grid,
    - Maps of properties of the graph, vertices, edges, autonomous systems ASs and supply units SUs.
    - Sets of ASs and SUs.

    The graph is ideal to model a 2d space with discrete points where one can be, as graphs are well suited to finding paths and walks in space.<br>
    The sets are ideal to convey what is in the environment as order doesn't matter and it can store many items effectively.
    The maps are ideal to convey information about elements in the environment as they take an element and return a value (which can be made of multiple values) giving key information about said element.

    #### Outputs:

    map containing the whole output, including a:
    - List (of vertices <span class = "r">and edges</span> traversed in walk).
    - set (of supply units recovered)
    - Integer (cost of the walk)

    having these outputs all in a map allows for ease of use as they are packaged together.

    #### Within the Algorithm

    Some key ADTs used by the 'Brute Force' algorithm are:
    - A map of maps for an traversal cost matrix.
    - A list of the walk and of the permutation.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part B - Algorithm Design:
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Problem properties
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    Known properties of the memo  <span class = "r">1</span> <span class = "g">A1</span> problem:

    - All edges have the same weight, so it can be treated as an unweighted graph <!--TODO change in memo A2-->
    - <span class = "r">the graph is a tree</span>
    - The maximum degree of any vertex is 4 as it is in a grid, meaning it is a 'sparse' graph for the sake of computation
    - There are <span class = "g">4-</span>5 supply units
    - There are 2 exits
    - <span class = "g">There are relatively few cycles</span>
    - <span class = "r">There are ||V|| = 144 sectors</span>

    <div class = "r">
    BFS is the best way to find the shortest path from a node to all nodes O(V+E) for an unweighted graph.<br>

    Note: if edge traversal cost starts to differ (but stays positive) use Dijkstra's instead of BFS, O(log(V)(V+E)).<br>

    Note: if there are negative edges (but not negative cycles), use Bellman Ford instead of BFS, O(VE).
    </div>
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Options
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <div class = "r">

    <h3>Option 0: DFS</h3>

    <h4>Pros and Cons:</h4>

    Pros:<br>

    - Time complexity is O(V+E)<br>
    - Simple to understand<br>
    - Works in about any situation<br>

    Cons:<br>

    - Walk is often suboptimal<br>

    <h4>Algorithm:</h4>

    Do a DFS until all the supply units have been collected and then do another DFS until an exit has been reached.<br>

    </div>



    ### Option 1: Greedy (with BFS)

    #### Pros and Cons:

    Pros:

    - Good time complexity of O((V+E)(S)) where S is supply units.
    - Works if the edge traversal cost is different between edges
    - Works on any graph as long as there are no negative cycles, for all edges. (doesn't have to be a tree)
    - A version works if there the AS doesn't have enough energy to extract all supply units.

    Cons:

    - Walk is not always optimal.

    #### Algorithm:

    <div class = "r">Use BFS (single source all shortest paths) to find the path to the closest supply unit. Repeat from that node to the next closest unvisited supply unit and so on until there are no more supply units. Then use BFS to find the nearest exit and navigate there for extraction.</div>

    <div class = "g">
    Uses BFS to compute the distance and path between all POI (the exit, entry and supply units). Then starting from the entry, always going to the closest unvisited supply unit, traverse all supply units. Then it traverses to the nearest exit.
    </div>

    ### Option 2: Brute Force (with BFS)

    #### Pros and Cons

    Pros:

    - Simple to understand
    - always returns optimal solution
    - <span class = "g">efficient for facilities with few supply units, which is the case in memo A1 where there are 4 to 5 supply units.</span>

    Cons:

    - Very inefficient with time complexity of O((V+E)(S) + S!) = O(S!) (if S >> (V+E))

    #### Algorithm:

    Firstly it finds all the shortest paths between the supply units, the entry and the exits and puts these into a path and distance matrix.

    Secondly use said matrix to find the length of the walk Entry, ..., $s_1$, ..., $s_2$, ..., $s_n$, ..., Exit,
    where each permutation of $s_1$ to $s_n$ is tried along with different exit options.

    ### Option 3: BFS + DFS

    #### Pros and Cons:

    Pros:

    <span class = "r">- Returns the optimal walk.</span>
    - Works well for graphs with few cycles.
    - Good time complexity with O(#Exits(V+E)).

    Cons:

    - only works <span class = "g">optimally</span> if:
    	- the graph is a tree.
    	- the AS has to collect all supply units.
    - Complicated, and prone to human error

    #### Algorithm:

    Overview:

    1. Run BFS, retaining parent vertices, number of children vertices and a set of leaf nodes.
    2. Backwards trace the graph from the leaf nodes giving a property to each node whether it has a supply unit (SU) beneath it, and whether it has an exit beneath it.
    3. For each exit:
    	1. Run DFS on the graph retaining the walk taken, where branches with SUs without exits are explored first. (ignore all branches without a SU or an exit)
    4. Find which of the walks is shortest and return that.
    """)
    return


@app.cell(hide_code=True)
def _():
    #DFS returns best walk for a tree proof
    mo.callout(mo.accordion({"**BFS+DFS returns best walk for a tree proof**": """
    Scope: undirected trees. (can be weighted)

    POI = Points of Interest, here meaning entries, exits and supply units.

    Conjecture: A shortest walk containing all POI (points of interest) ending at a specific node can be found utilising a modified DFS on a subtree with only POI as leaf nodes.

    Lemma 1: to visit all nodes and return to the source, DFS provides a shortest walk.
    1. Since to get to a node from another node there is only one path as G is a tree.
    2. To get to a single node and back to the source, all edges in that path have to be traversed at least twice as there is only one path to go there and back.
    3. Each edge in the graph has to connect at least one node to the tree connected to the source meaning that all edges have to be traversed at least twice to visit all nodes and return to the source.
    4. Therefore the walk has to have length at <u>**least**</u> 2sum(E) (where sum(E) is the sum of all edge weights) as each edge is traversed twice.
    5. But DFS produces a walk of length 2sum(E) as it has to traverse all edges (in a tree) and then back again.
    6. This means DFS produces an optimal walk for its length is the shortest it could be.

    Lemma 2: DFS can produce a walk with length 2sum(E) - dist(source,v), if it has to visit all nodes from a source and end at v.
    1. Consider if DFS stacks the node with v as a descendant or v itself first at each iteration. Then DFS will explore all other branches before it pops v, and at that point it will explore the desendants of v. once it has explored all nodes, DFS will start returning to the source, and v has to be on that route as it (or a desendant of v) was explored last.
    2. Therefore as it will end at v having explored all nodes and on a direct path to the source with distance dist(source,v) and we know that a full DFS takes 2sum(E), the length of this walk must be 2sum(E) - dist(source,v).

    Lemma 3 There is no walk shorter than 2sum(E) - dist(source,v), if it has to visit all nodes from a source and end at v.
    1. Assume the opposite, there is a walk with length l < 2sum(E) - dist(source,v) that visits all nodes starting at the source and ending at v.
    2. Then l + dist(source,v) equals the return trip length of a walk visiting all nodes starting and ending at the source, as one just has to go from v to source and dist(source,v) = dist(v, source), which must be at least 2sum(E) from lemma 1.
    3. but l + dist(source,v) < 2sum(E) - dist(source,v) + dist(source,v) = 2sum(E).
    4. 2sum(E) $\leq$ l + dist(source,v) < 2sum(E) $\implies$ 2sum(E) < 2sum(E)
    5. Therefore by contradiction Lemma 3 is true.

    Lemma 4: DFS provides a shortest walk to traverse all nodes from an arbitrary node to an arbitrary node.
    1. By lemma 2 and lemma 3 DFS must produce the shortest walk possible from an arbitrary node to an arbitrary node traversing all nodes as its length is equal to the lower bound.

    Lemma 5: DFS provides a shortest walk containing all leaf nodes and ending at an arbitrary node.
    - As the graph is a tree, there is only one path between any two nodes, meaning to get to a leaf node from the source, all parents of the leaf node must be traversed.
    - As every node in a graph is either a parent of a leaf node or a leaf node, all nodes must be traversed if all leaf nodes are to be traversed.
    - As all nodes must be traversed, this problem falls under lemma 4, showing lemma 5 to be true.

    Applying to a specific POI:
    - consider a minimal subtree of the tree that is big enough to contain all the POI
    - This means that all leaf nodes will be POI as otherwise they could be trimmed.
    - Lemma 5 applies here meaning that the shortest walk to contain the POI is 2sum(E) - dist(source,exit) but sum(E) is of edges in the the subgraph.
    - Q.E.D.

    #### Proof Summary

    As the BFS+DFS algorithm utilises DFS in the manner discussed in the proof, BFS+DFS returns the shortest walk for memo 1, but not necessarily memo A1."""}))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <div class = "g">

    <h3>Option 4: Divide and Conquer</h3>

    <h4>Pros and Cons</h4>

    Pros:<br>
    - Returns optimal walk<br>
    - Simplifies the problem significantly to a much smaller graph.<br>
    - divides the simplified graph into smaller sub problems.<br>
    Cons: <br>
    - Difficult to program - prone to human error.<br>

    <h4>Algorithm</h4>

    Divide and Conquer is broken up into 3 main steps.<br>


    1. Break up graph into sub graphs by articulation points - nodes where, if removed cause the graph to be broken in two.<br>
    2. Utilise Brute force on sub graphs to find optimal walk (refer to brute force, option 2.)<br>
    3. Stitch the whole walk back together

    </div>
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Discussion
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <span class = "g">The discussion for part B will take place after part C once we are able to directly compare the algorithms.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <div class = "r">
    Every option above has its merits and its drawbacks, but option 3 seems to be the most optimal for the memo 1 problem as it balances speed with finding the optimal solution. Its time complexity is O(#Exits(V+E)), which is only always beaten by the DFS algorithm in terms of speed.<br>

    Compared to the Brute force option, with time complexity O((V+E)S+S!) where S is #of supply units, the BFS + DFS solution is significantly faster for large values of S.<br>

    A significant drawback of the BFS + DFS algorithm is that it relies on the graph being a tree which might not be the case in memos beyond memo 1, leading to a potentially suboptimal solution for graphs with cycles.</div>
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part C - Pseudocode
    """)
    return


@app.cell(hide_code=True)
def _(algorithms):
    #Choose Algorithm
    algorithm_input = mo.ui.tabs({_algo:"" for _algo in algorithms.keys()}, value = "Divide and Conquer")

    mo.callout(mo.vstack([ algorithm_input],align = "center"),kind = "success")
    return (algorithm_input,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <span class = "y">The dropdown to select different algorithms is new. All algorithm implementations are new, except for BFS+DFS.</span>
    """)
    return


@app.cell(hide_code=True)
def _(algorithm_input):
    mo.md(rf"""
    ## C1 - Algorithm in pseudocode - {algorithm_input.value}
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.callout(mo.accordion({"Pseudocode Conventions Used":"""
    1. Start a 'function', 'for loop', 'while', 'if', 'else if' and 'else' with FUNCTION, FOR...DO, WHILE, IF...THEN, ELSE IF...THEN, ELSE 
    2. Do not end a flow control parameter with END ... (e.g. END FUNCTION), simply use indentation to convey the end of the flow control.
    3. Use '//' for comments
    4. Use '←' for assignment
    5. Use object.ADT_signature_name() for to utilise an ADT's signature.
    6. {} mean dictionaries or sets.
    7. [] mean lists, or accessing indexes.
    """}))
    return


@app.cell(hide_code=True)
def _(algorithm_input):
    #Pseudocode
    BFS_DFS_pseudocode = r"""
    <div class = "y">
    <h4>Changes to BFS+DFS pseudocode:</h4>
    &#x2022; Name changed from ember_rescue to BFS_DFS<br>
    &#x2022; move() function have been changed to take x,y as the vector v in the direction it needs to go.<br>
    &#x2022; END FUNCTION WHILE FOR IF etc have been removed for simplified pseudocode.
    &#x2022; added logic to DFS to ensure that the walk taken traverses the spanning tree only.
    </div>

    ```

    //1 indexed
    FUNCTION BFS_DFS(G: Directed Unweighted Graph, SU: Set, AS: Set, VP: Map, EP: Map, SUP: Map, ASP: Map, GP: Map) -> Map
        // G = (V,E)


        //--------------------------------------------------
        // -----------Initialise data structures------------
        //--------------------------------------------------

        CRUDY_1 ← AS.get_random()
        entry ← ASP[CRUDY_1]["location"]
        V ← G.Vertices()

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
            walks.append(DFS(G, VP, entry, parent, sub_exit, sub_SU, i))

        //4. Calculating traversal_cost

        walk ← shortest_walk(walks)
        length ← walk.length() - 1

        //--------------------------------------------------
        // ----------------RETURN the output----------------
        //--------------------------------------------------

        //Outputing to the physical environment the instructions for the AS

        FOR i ← 1 to length DO
            dif_vec = walk[i+1]-walk[i] // a tuple
            move(dif_vec[1], dif_vec[2])
        exit()

        RETURN {"walk": walk, "traversal_cost": length, "supply_units_recovered": SU}

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

    	RETURN parent, child_count, leaf_nodes

    FUNCTION make_sub_exits(G: Graph, VP: Map) -> Integer, Map
    	exit_map ← {v: {} | v ∈ V} //Map of empty sets
    	V ← G.vertices()
    	exit_count ← 0
    	FOR v ∈ V DO
    		IF VP[v]["is_exit"] THEN
    			exit_count ← exit_count + 1
    			exit_map[v].add(exit_count)

    	RETURN exit_count, exit_map

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

    	RETURN sub_exit, sub_SU

    FUNCTION DFS(G: Graph, VP: Map, s: Vertex, parent: Map, sub_exit: Map, sub_SU: Map, i: Integer) -> list
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
    		walk.append(u)

    		//makes sure that vertices with exits below them are pushed first.
    		FOR v ∈ G.Neighbours(u) DO
                //Changed this to ensure that v is a child of u.
    			IF (not visited[v]) and sub_exit[v].contains(i) and parent[v] = u THEN
    				visited[v] ← true
    				DFS_Stack.push(v)
    			ELSE IF not visited[v] and sub_SU[v] and parent[v] = u THEN
    				Q.push(v)
                // ignores all vertices not in sub_exit or sub_SU

    		//the nodes with just supply units below them are then pushed on top.
    		WHILE not Q.is_empty() DO
    			v ← Q.pop()
    			visited[v] ← true
    			DFS_Stack.push(v)

    		previous_u ← u

    	WHILE not VP[walk[walk.length()]]["is_exit"] DO
    		walk.append(parent[walk[walk.length()]])

    	RETURN walk

    FUNCTION shortest_walk(walks: List) -> List
    	min_index ← -1
    	min ← positive infinity
    	FOR i ← 1 to walks.length() DO
    		IF walks[i].length() < min THEN
    			min ← walks[i].length()
    			min_index ← i

    	RETURN walks[min_index]
    ```
    """

    Greedy_pseudocode = r"""
    <span class = "y">This is a newly implemented algorithm</span>

    ```
    FUNCTION Greedy(G: Directed Unweighted Graph, SU: Set, AS: Set, VP: Map, EP: Map, SUP: Map, ASP: Map, GP: Map) -> Map

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
                parent ← BFS(G,v)
                FOREACH u ∈ POI DO
                    w ← u
                    path ←[]
                    WHILE parent[w] != null DO
                        path.insert_at(0, w) 
                        w ← parent[w]
                    pm[v][u] ← path //without first node
                    dm[v][u] ← path.length()


            //Finding shortest walk.
            got_su ← {v:False | v ∈ SU_locations}
            perm ← [entry]

            //Go to closest SU
            FOR i from 1(inclusive) to SU_locations.length() (inclusive) DO
                closest_su ← None
                u ← perm[perm.length()]
                FOR v ∈ POI DO
                    IF v ∈ SU_locations THEN
                        IF not got_su[v] and closest_su = None THEN
                            closest_su ← v
                        ELSE IF not got_su[v] and dm[u][v] < dm[u][closest_su] THEN
                            closest_su ← v
                IF closest_su = None THEN
                    break
                perm.append(closest_su)
                got_su[closest_su] ← True


            //Go to closest exit
            closest_exit ← None
            u ← perm[perm.length()]
            FOR v ∈ POI DO
                IF v ∈ exits THEN
                    IF  closest_exit = None THEN
                        closest_exit ← v
                    ELSE IF dm[u][v] < dm[u][closest_exit] THEN
                        closest_exit ← v
            perm.append(closest_exit)  


            walk ← [entry]
            FOR i from 1 (inclusive) to perm.length() (exclusive) DO
                walk.concatenate(pm[perm[i]][perm[i+1]])

            FOR i ← 1 (inclusive) to walk.length() (exclusive) DO
                dif_vec ← VP[walk[i+1]]["location"]-VP[walk[i]]["location"] // a tuple
                move(dif_vec[1], dif_vec[2])
            exit()

            RETURN {"walk": walk, "traversal_cost": walk.length()-1, "supply_units_recovered": SU}


    FUNCTION BFS(G: Graph, s: Vertex) -> Map
    	//s is first vertex
    	V ← G.vertices()
    	BFS_Queue ← queue
    	BFS_Queue.push(s)
    	visited ← {v: false | v ∈ V} //map
    	visited[s] ← true

    	parent ← {v: null | v ∈ V} //map

    	WHILE not BFS_Queue.is_empty() DO
    		u ← BFS_Queue.pop()
    		FOR v ∈ G.Neighbours(u) DO
    			IF not visited[v] THEN
    				visited[v] ← true
    				BFS_Queue.push(v)
    				parent[v] ← u
    	RETURN parent
    ```
    """

    Brute_Force_pseudocode = r"""
    <span class = "y">This is a newly implemented algorithm</span>

    ```
    FUNCTION Brute_Force(G: Directed Unweighted Graph, SU: Set, AS: Set, VP: Map, EP: Map, SUP: Map, ASP: Map, GP: Map) -> Map

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
                parent ← BFS(G,v)
                FOREACH u ∈ POI DO
                    w ← u
                    path ←[]
                    WHILE parent[w] != null DO
                        path.insert_at(0, w) 
                        w ← parent[w]
                    pm[v][u] ← path //without first node
                    dm[v][u] ← path.length()


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

            RETURN {"walk": walk, "traversal_cost": walk.length()-1, "supply_units_recovered": SU}


    FUNCTION BFS(G: Graph, s: Vertex) -> Map
    	//s is first vertex
    	V ← G.vertices()
    	BFS_Queue ← queue
    	BFS_Queue.push(s)
    	visited ← {v: false | v ∈ V} //map
    	visited[s] ← true

    	parent ← {v: null | v ∈ V} //map

    	WHILE not BFS_Queue.is_empty() DO
    		u ← BFS_Queue.pop()
    		FOR v ∈ G.Neighbours(u) DO
    			IF not visited[v] THEN
    				visited[v] ← true
    				BFS_Queue.push(v)
    				parent[v] ← u
    	RETURN parent
    ```
    """

    Divide_and_Conquer_pseudocode = rf"""

    <span style = "font-size: 100px">🚧🔨</span><br>
     **No pseudocode is available for {algorithm_input.value}** <!--TODO add pseudocode for Divide and Conquer-->

    """

    _out = """"""
    if(algorithm_input.value == "BFS+DFS"):
        _out = BFS_DFS_pseudocode
    elif(algorithm_input.value == "Greedy"):
        _out = Greedy_pseudocode
    elif(algorithm_input.value == "Brute Force"):
        _out = Brute_Force_pseudocode
    elif(algorithm_input.value == "Divide and Conquer"):
        _out = Divide_and_Conquer_pseudocode

    mo.stop(_out == "")
    mo.md(_out)
    return


@app.cell(hide_code=True)
def _(algorithm_input):
    mo.md(rf"""
    ## C2 - Algorithm in python - {algorithm_input.value}
    """)
    return


@app.cell(hide_code=True)
def _(algorithm_input, algorithms):
    #Python Code
    BFS_DFS_python = rf"""
    <div class = "y">
    <h4>Changes to python code:</h4>
    &#x2022; move() function have been changed to take x,y as the vector v in the direction it needs to go.
    &#x2022; added logic to DFS to ensure that the walk taken traverses the spanning tree only.
    </div>

    ```python
    import networkx as nx
    from collections import deque

    {inspect.getsource(BFS_DFS)}
    ```
    """


    Generic_new_python = rf"""
    <span class = "y">'{algorithm_input.value}' is a newly implemented algorithm</span>

    ```python
    {inspect.getsource(algorithms[algorithm_input.value])}
    ```
    """

    _out = """"""

    if(algorithm_input.value == "BFS+DFS"):
        _out = BFS_DFS_python
    else:
        _out = Generic_new_python


    mo.stop(_out == "")
    mo.md(_out)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## C3 - Displaying the Process
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Inputs
    """)
    return


@app.cell(hide_code=True)
def _():
    #What are the inputs again?
    _info1 = mo.accordion({"What are the inputs again?":mo.md("""
    The inputs are: G, AS, SU, VP, EP, SUP, ASP and GP.
    - G: (Graph of a Sector Grid) = (V,E)
    - AS: (Autonomous System)
    - SU: (Supply Unit)
    - EP: (Edge Properties)
    - VP: (Vertex Properties)
    - SUP: (Supply Unit Properties)
    - ASP: (Autonomous Systems Properties)
    - GP: (Graph Properties)""")})

    _info2 = mo.accordion({"How is the generated facility converted into G, AS, SU, VP, EP, SUP, ASP and GP?":rf"""
    The following function c_fac_Bv2 is used to convert the generated facility (fac_Av2) into the representation discussed in part A1 - Algorithmic Problem Statement.<br>
    It has two helper functions, c_Av2 and c_Bv2 to help convert singular nodes.

    ```python
    import networkx as nx

    WING_COLS = {WING_COLS}
    GAP = {GAP}

    {inspect.getsource(c_Av2)}

    {inspect.getsource(c_Bv2)}

    {inspect.getsource(c_fac_Bv2)}
    ```
    """})

    mo.callout(mo.vstack([_info1, _info2]))
    return


@app.cell(hide_code=True)
def _(AS, ASP, EP, G, GP, SU, SUP, VP):
    #Display Inputs
    _G = f"""
    ```python
    G = {G} = (in adjacency-list form) { {v:list(dict(G[v]).keys()) for v in G.nodes()} }
    ```
    """
    _SU = f"""
    ```python
    SU = {SU}
    ```
    """
    _AS = f"""
    ```python
    AS = {AS}
    ```
    """
    _EP = f"""
    ```python
    EP = {EP}
    ```
    """
    _VP = f"""
    ```python
    VP = {VP}
    ```
    """
    _SUP = f"""
    ```python
    SUP = {SUP}
    ```
    """
    _ASP = f"""
    ```python
    ASP = {ASP}
    ```
    """
    _GP = f"""
    ```python
    GP = {GP}
    ```
    """


    mo.callout(mo.vstack([
            mo.md(_G),
        mo.md(_SU),
        mo.md(_AS),
        mo.md(_EP),
        mo.md(_VP),
        mo.md(_SUP),
        mo.md(_ASP),
        mo.md(_GP),     
        ], gap=0),kind = "info")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### Outputs
    """)
    return


@app.cell(hide_code=True)
def _(algorithm_input, seed_input):
    # Choose Algorithm and Seed 
    mo.callout(mo.hstack([algorithm_input, seed_input],align = "center"),kind = "success")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ####<span class = "g">Environmental Outputs:</span><br>

    <!-- TODO add a legend to the animations/gif-->
    """)
    return


@app.cell(hide_code=True)
def _():
    #Choose between Image and Animation displays
    im_gif = mo.ui.tabs({"Image":"","Animation":""}, value = "Animation")
    im_gif
    return (im_gif,)


@app.cell(hide_code=True)
def _(algorithm_input, im_gif, m_gif_v2, seed_input):
    #Display Gif
    mo.stop(im_gif.value != "Animation")
    _out = m_gif_v2(algorithm = algorithm_input.value)
    if(_out == "ran successfully"):
        time.sleep(10)
    mo.stop(_out == "error")
    mo.image("figs/"+ str(seed_input.value) +f"_{algorithm_input.value}_v2"+ ".gif")
    return


@app.cell(hide_code=True)
def _(
    algorithm_input,
    default_title,
    fac_Av2,
    front_focus_v2,
    im_gif,
    walk_v2,
):
    #Display Image
    mo.stop(im_gif.value != "Image")
    draw_fac_v2(fac_Av2, node_colors = front_focus_v2(walk_v2[algorithm_input.value]), highlight_path = [c_Av2(v) for v in walk_v2[algorithm_input.value]], legend = False, title = default_title(has_walk = True, algorithm=algorithm_input.value))
    return


@app.cell(hide_code=True)
def _(
    AS,
    ASP,
    EP,
    G,
    GP,
    SU,
    SUP,
    VP,
    algorithm_input,
    memory_v2,
    out_v2,
    speed_v2,
):
    mo.callout(mo.hstack([
            mo.stat(label=f"Traversal Cost (minimum is {out_v2['Brute Force']['traversal_cost']})",    value=str(out_v2[algorithm_input.value]["traversal_cost"])),
            mo.stat(label="Time to Compute",    value=str((int)(speed_v2[algorithm_input.value]*1000))+" ms"),
            mo.stat(label="Memory to Compute",    value=str(round(memory_v2[algorithm_input.value]/1000))+" KB"),
            mo.stat(label="Supply Units Recovered",  value=str(len(out_v2[algorithm_input.value]["supply_units_recovered"]))+"/" + str(len(SU))),
            mo.stat(label="Output is Valid",  value=str(validate_output(out_v2[algorithm_input.value],G, AS, SU, VP, EP, SUP, ASP, GP)) ),
        ], gap=0, wrap=True),kind = "info")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <div class = "g">
    <h4>Computational Outputs:</h4>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(algorithm_input, out_v2):
    mo.callout(mo.md(rf"""
    **raw output:**
    ```python
    {out_v2[algorithm_input.value]}
    ```

    **Facility A walk:**
    ```python
    {c_out_Av2(out_v2[algorithm_input.value])}
    ```
    """), kind = "info")
    return


@app.cell(hide_code=True)
def _():
    mo.callout(mo.accordion({"How can this output be converted to a walk traversing generated facility (facility A)?":rf"""
    Please use the c_out_Av2 function to convert from facility B's output (out_Bv2) to a walk in facility A.

    ```python
    WING_COLS = {WING_COLS}
    GAP = {GAP}

    {inspect.getsource(c_out_Av2)}

    {inspect.getsource(c_Av2)}
    ```


    """}))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## <span class = "g">C4 - Comparisons</span>
    """)
    return


@app.cell(hide_code=True)
def _():
    sample_set_size = mo.ui.slider(start = 5, stop = 500, step = 5, value = 100, full_width= True, label = "Sample Set Size Slider")
    table_options = mo.ui.tabs({"Current Seed": "", "Sample Set":sample_set_size})
    return sample_set_size, table_options


@app.cell(hide_code=True)
def _(
    SU,
    algorithms,
    benchmark_algorithm,
    memory_v2,
    out_v2,
    sample_set_size,
    seed_input,
    speed_v2,
    table_options,
    valid_v2,
):
    # make table
    def m_comparison_table():
        _tc = {alg:0 for alg in algorithms.keys()}
        _s = {alg:0 for alg in algorithms.keys()}
        _m = {alg:0 for alg in algorithms.keys()}
        _su = {alg:0 for alg in algorithms.keys()}
        _valid = {alg:"valid" for alg in algorithms.keys()}

        _SU = 0
        if table_options.value == "Sample Set":
            for i in range(sample_set_size.value):
                _seed = random.randint(0,99999999)

                for alg in algorithms.keys():
                    _out_v2, _memory_v2, _speed_v2, _input, _is_valid = benchmark_algorithm(alg, seed = _seed)
                    _tc[alg] += _out_v2["traversal_cost"]
                    _s[alg] += _speed_v2
                    _m[alg] += _memory_v2
                    _su[alg] += 100*len((_out_v2["supply_units_recovered"]))/len(_input["SU"])
                    if _valid[alg] == "valid":
                        _valid[alg] = _is_valid

            for alg in algorithms.keys():
                _tc[alg] /= sample_set_size.value
                _s[alg] /= sample_set_size.value
                _m[alg] /= sample_set_size.value
                _su[alg] /= sample_set_size.value
            _SU /= sample_set_size.value

        else:
            for alg in algorithms.keys():
                _tc[alg] = out_v2[alg]["traversal_cost"]
                _s[alg] = speed_v2[alg]
                _m[alg] = memory_v2[alg]
                _su[alg] = 100*len((out_v2[alg]["supply_units_recovered"]))/len(SU)
                if _valid[alg] == "valid":
                    _valid[alg] = valid_v2[alg]




        corner = seed_input.value
        if table_options.value == "Sample Set":
            corner = f"{sample_set_size.value} seeds"

        d1 = {corner:"Traversal Cost"} | {algorithm:round(_tc[algorithm]) for algorithm in algorithms} 
        d2 = {corner:"Speed (ms)"} | {algorithm:(int)(round(_s[algorithm]*1000)) for algorithm in algorithms}
        d3 = {corner:"RAM Used (KB)"} | {algorithm:round(_m[algorithm]/1000) for algorithm in algorithms}
        d4 = {corner:f"SUs recovered (%)"} | {algorithm:round(_su[algorithm]) for algorithm in algorithms}
        d5 = {corner:"Valid Output"} | {algorithm:_valid[algorithm] for algorithm in algorithms}

        best1 = [list(algorithms.keys())[0]]
        best2 = best1.copy()
        best3 = best1.copy()
        best4 = best1.copy()

        for alg in list(algorithms.keys())[1:]:
            v1 = _tc[alg]
            v2 = _tc[best1[0]]
            if v1 < v2:
                best1 = [alg]
            elif v1 == v2:
                best1.append(alg)

            v1 = _s[alg]
            v2 = _s[best2[0]]
            if v1 < v2:
                best2 = [alg]
            elif v1 == v2:
                best2.append(alg)

            v1 = _m[alg]
            v2 = _m[best3[0]]
            if v1 < v2:
                best3 = [alg]
            elif v1 == v2:
                best3.append(alg)

            v1 = _su[alg]
            v2 = _su[best4[0]]
            if v1 > v2:
                best4 = [alg]
            elif v1 == v2:
                best4.append(alg)

        def _to_str(a):
            b = str(a[0])
            for i in range(1,len(a)):
                b += ", "+ a[i]
            return b

        d1 |= {"Best": _to_str(best1)}
        d2 |= {"Best": _to_str(best2)}
        d3 |= {"Best": _to_str(best3)}
        d4 |= {"Best": _to_str(best4)}





        return mo.ui.table(
            data=[d4,d1,d2,d3, d5],
            selection = None
        )
    table = m_comparison_table()
    return (table,)


@app.cell
def _(table, table_options):
    mo.callout(mo.vstack([table_options,table]), kind = "success")
    return


@app.cell(hide_code=True)
def _():
    mo.callout(mo.accordion({"How is the validity of an algorithm's output checked?": rf"""
    The output is run through the "validate_ouput" automated checker to make sure the walk matches the constraints specified in part A1.
    ```python
    {inspect.getsource(validate_output)}
    ```
    """}))
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <div class = "g">
    <h1>Part B2 - Discussion</h1>

    <p>Please refer to the table in part C4, which was used to decide on an algorithm.</p>

    Every option above has its merits and its drawbacks, with simpler algorithms, perfect solutions or efficient computations. The four options are considered:<br>

    1. Brute Force: Brute forcing this problem is straightforward and efficient as there are only 4-5 supply units (which the time complexity depends on). Brute force is therefore a simple, optimal and efficient solution.<br>

    2. BFS+DFS: BFS+DFS has unmatched computational speed and relatively good traversal cost here, being a good heuristic for this problem.<br>

    3. Divide and Conquer: Divide and Conquer should be a more efficient version of Brute Force by breaking the problem into smaller parts, but likely due to overhead is outperformed by Brute Force in all benchmarks, making it obsolete. <br>


    4. Greedy: Unfortunately this doesn't perform well in this environment, returning a significantly more expensive walk.<br>


    <p>
    As minimising traversal cost is rather important, and the difference in speed and memory use between the algorithms is negligible, Brute Force is the best algorithm for the job for its speed, simplicity and optimality.
    </p>

    </div>
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part D - Justification
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <div class = "g">
    <h3>Suitability:</h3>
    <p>The facility is a fully connected undirected unweighted graph with cycles. The current 'Brute Force' implementation can handle undirected and fully connected graphs. Therefore the facility fits into the scope of what the 'Brute Force' is designed to solve, showing the suitability of Brute force for this problem.</p>


    <p>
    For a sample set of a reasonable size (100 or more seeds, refer to table and slider) it can be seen that 'Brute Force' performs optimally (compared to the other algorithms) for 3 of the 4 benchmarks, only beaten in speed by several milliseconds. Despite not being specifically designed for this problem to account for the few cycles, like 'Divide and Conquer', it has almost no overhead allowing it to run lightning fast.
    </p>


    <h3>Coherence:</h3>
    <p>The 'Brute Force' implementation natively utilises the inputs specified in part A1, taking G, AS, SU, VP, EP, SUP, ASP and GP as inputs. It then returns the output map specified in part A1, meaning it is well integrated and coherent with the problem specification in part A.</p>

    <p>However, a problem with the implementation is that it is a bit clunky with many parts that aren't in use or rather redundant, namely SU, AS, SUP, ASP and GP</p>

    <p>Perhaps an improvement would be to wrap the inputs into a map to help hide the clunk and make the pseudocode and python code cleaner. This might look like:</p>

    ```python
    fac_B = {"G":G, "AS":AS, "SU":SU, "VP":VP, "EP":EP, "SUP":SUP, "ASP":ASP, "GP": GP}
    ```

    <h3>Fitness for purpose -- stress test:</h3>
    If one inter-wing corridor was blocked, Brute Force would handle the situation effectively as it utilises BFS to find paths, which ensures that it will always find a walk if one exists.<br>

    The blockage of one inter-wing corridor means that at least one cycle of the graph would be removed.
    Unlike Divide and Conquer however, 'Brute Force' will not utilse the removal of a cycle to optimise its speed.
    </div>
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Previous Justifications
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.callout(mo.accordion({"### Fitness for Purpose -- Does 'Brute Force' meet all constraints?":"""
    1. Does Brute Force's walk start at an entry? 
    When Brute Force constructs the walk, it defines it as  'walk = [entry]', and only appends to the list, meaning that the walk does start at an entry.
    2. Is the last vertex of the walk an exit?
    In the Brute Force code, an exit is always appended to the end of the walk permutation as in 'perm.append(exit)', meaning the last node visited will always be an exit.
    3. Are all nodes in the walk nodes in G?
    The only nodes added to the walk list are the entry and nodes from the pm. As these are all nodes of G, all nodes of the walk must be in G.
    4. Are all edges of the walk edges of G?
    Each edge of the walk is found in the pm by BFS. As BFS only traverses between nodes by edges of the graph G, all edges of the walk must be in G.
    5. Is the "supply_units_recovered" set consistent with the supply units traversed by the walk?
    As the 'Brute Force' algorithm visits all supply units, and it returns that it recovered all supply units, the "supply_units_recovered" output is consistent with reality.
    6. Does 'traversal_cost' match the traversal cost of the walk?
    Since the 'traversal_cost' returned is the number of nodes (repetitions counted) in the walk minus 1, this is consistent with the traversal cost of the walk, as an unweighted length of a walk is just the number of edges in the walk, = |V| - 1

    Therefore all constraints are met. This can be verified for a sample set of seeds automatically by utilising the table in part C4.""", "What are the constraints again?":mo.md(r"""
    ### Constraints as defined in part A1 - Algorithmic Problem Statement

    1. The first vertex of the walk AS makes must be an entry.
    2. The last vertex of the walk AS makes must be an exit.
    3. $\forall i [i \in \mathbb{N} \land i \in [1,n] \implies v_i \in V]$
    - meaning all vertices in the walk must be vertices of graph G.
    4. $\forall i [i \in \mathbb{N} \land i \in [1,n-1] \implies (v_i,v_{i+1}) \in E]$
    - meaning all edges in the walk must be edges of graph G.
    5. Supply units collected must match the sectors with supply units traversed by the walk<br>
    6. Traversal cost must match the traversal cost of the walk.

    *3 and 4 are simply ensuring the walk is indeed a walk on graph G.

    """)}),kind = "success")
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    <div class = "r">
    ### Suitability:

    The ESRC is a **undirected, unweighted tree** meaning that my BFS+DFS algorithm--which requires an unweighted and undirected graph and returns an optimal solution for a tree--is a perfect match. It is also rather efficient (O((V+E)#Exits)), so for this particular problem (as #exits = 2 and it is sparse with ||E|| =143), it outperforms more general solutions, such as brute force and greedy.

    ### Coherence:

    ADTs Used:
    - the map VP--for vertex properties--is called with VP[v]["supply_unit"] to check if a sector has a supply unit, in order to help build a subtree of G.
    - The graph G is used in BFS to find the neighbours of a vertex v, with G.vertices().
    Mismatch Problems between BFS+DFS algorithm and part A's ADTs.

    My ADT design is a bit over the top including lots of details in multiple places as well as some parts that aren't relevant to the memo 1 problem, such as ASP, AS, SUP and GP as they are static, which my algorithm ignores.<br>
    In part A, I call the graph the combination of two sets--V and E--but then I call it its own ADT which I use in the pseudocode and python.

    ### Constraints:

    1. The first vertex of the walk AS makes must be an entry.
        - The source node is the first node in the walk from DFS.
    2. The last vertex of the walk AS makes must be an exit.
        - Refer to proof, as DFS traverses all nodes and can choose any node to be on the return path.
    3. Aim to maximise supply unit recovery while ensuring making it to an extraction point is possible.
        - Refer to proof, all supply units are recovered and the last node is an exit.
    4. Aim to minimise energy/traversal cost.
        - Refer to proof, the shortest walk is returned.
    6. Crudy can carry at most 5 supply units.
       - As there are only 5 supply units, this isn't an issue.

    Therefore, all constraints are met!</div>
    """)
    return


if __name__ == "__main__":
    app.run()
