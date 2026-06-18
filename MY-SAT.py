import marimo

__generated_with = "0.23.9"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell
def _():
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

    return deque, imageio, mo, mpatches, nx, os, plt, random, time, tracemalloc


@app.cell(hide_code=True)
def _(mo):
    #style
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
    </style>
    """)
    return


@app.cell
def _(mo):
    #VALUES
    COLS, ROWS =12,12
    seed_input = mo.ui.number(
        value=30012009,
        start=0,
        stop=99999999,
        step=1,
        label="Your facility seed (from your cover sheet)"
    )
    mo.vstack([
        mo.md("### Enter your seed, then press Tab to rebuild the facility."),
        seed_input
    ])
    return COLS, ROWS, seed_input


@app.cell
def _(seed_input):
    seed = seed_input.value
    return (seed,)


@app.cell(hide_code=True)
def _(COLS, ROWS, nx, random, seed):
    # make MR version
    def _neighbours(cols, rows, c, r):
        for dc, dr in [(1,0),(-1,0),(0,1),(0,-1)]:
            nc, nr = c+dc, r+dr
            if 0 <= nc < cols and 0 <= nr < rows:
                yield nc, nr

    def _build_graph(cols, rows, rng):
        visited = [[False] * rows for _ in range(cols)]
        graph = nx.Graph()
        for c in range(cols):
            for r in range(rows):
                graph.add_node((c, r), pos=(c + 0.5, r + 0.5))

        def carve(c, r):
            visited[c][r] = True
            dirs = list(_neighbours(cols, rows, c, r))
            rng.shuffle(dirs)
            for nc, nr in dirs:
                if not visited[nc][nr]:
                    graph.add_edge((c, r), (nc, nr), weight=1)
                    carve(nc, nr)

        carve(0, 0)
        for c in range(cols):
            for r in range(rows):
                if not visited[c][r]:
                    for nc, nr in _neighbours(cols, rows, c, r):
                        if visited[nc][nr]:
                            graph.add_edge((c, r), (nc, nr), weight=1)
                            carve(c, r)
                            break
        return graph

    def _place_supplies(graph, cols, rows, rng, reserved):
        dead_ends = [n for n in graph.nodes
                     if graph.degree(n) == 1 and n not in reserved]
        rng.shuffle(dead_ends)
        quadrants = [
            (0, cols//2, 0, rows//2),
            (cols//2, cols, 0, rows//2),
            (0, cols//2, rows//2, rows),
            (cols//2, cols, rows//2, rows),
        ]
        result, used = [], set(reserved)
        for qc1, qc2, qr1, qr2 in quadrants:
            if len(result) >= 5:
                break
            cands = [n for n in dead_ends
                     if qc1 <= n[0] < qc2 and qr1 <= n[1] < qr2
                     and n not in used]
            if cands:
                result.append(cands[0])
                used.add(cands[0])
        for n in dead_ends:
            if len(result) >= 5:
                break
            if n not in used:
                result.append(n)
                used.add(n)
        return result[:5]

    def get_facility(seed):
        rng = random.Random(int(seed))
        graph = _build_graph(COLS, ROWS, rng)
        entry  = (0, 0)
        exit_a = (COLS-1, ROWS-1)
        exit_b = (COLS-1, 0)
        reserved = {entry, exit_a, exit_b}
        rng2 = random.Random(int(seed))
        supplies = _place_supplies(graph, COLS, ROWS, rng2, reserved)
        return graph, entry, exit_a, exit_b, supplies

    fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1 = \
        get_facility(seed)
    return (
        fac_entry_v1,
        fac_exit_a_v1,
        fac_exit_b_v1,
        fac_graph_v1,
        fac_supplies_v1,
    )


@app.cell(hide_code=True)
def _(COLS, ROWS, mpatches, plt):
    # Define Draw Facility

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

    def draw_facility_v1(graph, entry, exit_a, exit_b, supplies,
                      highlight_path=None, title="Facility Layout",
                      node_colors=None, supply_collected=None,
                      figsize=(8, 8), legend=True):




        fig, ax = plt.subplots(figsize=figsize)
        ax.set_facecolor(COL_BG)
        fig.patch.set_facecolor(COL_BG)

        # Grid
        for c in range(COLS + 1):
            ax.plot([c, c], [0, ROWS], color=COL_GRID, lw=0.4, zorder=1)
        for r in range(ROWS + 1):
            ax.plot([0, COLS], [r, r], color=COL_GRID, lw=0.4, zorder=1)

        # Border
        for x0,y0,x1,y1 in [(0,0,COLS,0),(COLS,0,COLS,ROWS),(COLS,ROWS,0,ROWS),(0,ROWS,0,0)]:
            ax.plot([x0,x1],[y0,y1], color=COL_WALL, lw=2.2, zorder=3)

        # Internal walls
        for c in range(COLS):
            for r in range(ROWS):
                if c+1 < COLS and not graph.has_edge((c,r),(c+1,r)):
                    ax.plot([c+1,c+1],[r,r+1], color=COL_WALL, lw=1.6, zorder=3)
                if r+1 < ROWS and not graph.has_edge((c,r),(c,r+1)):
                    ax.plot([c,c+1],[r+1,r+1], color=COL_WALL, lw=1.6, zorder=3)

        # Highlighted nodes
        if node_colors:
            for node, color in node_colors.items():
                c, r = node
                rect = plt.Rectangle((c, r), 1, 1, color=color, alpha=0.50, zorder=2)
                ax.add_patch(rect)

        # Solution path
        if highlight_path and len(highlight_path) > 1:
            px = [c + 0.5 for c,r in highlight_path]
            py = [r + 0.5 for c,r in highlight_path]
            ax.plot(px, py, color=COL_PATH, lw=1.8, linestyle='--', alpha=0.75, zorder=4)

        # Supply markers
        for i, (sc, sr) in enumerate(supplies):
            already = supply_collected and (sc, sr) in supply_collected
            col = '#AAAAAA' if already else COL_SUPPLY
            mkr = 'x'      if already else '*'
            ax.plot(sc+0.5, sr+0.5, marker=mkr, markersize=14, color=col,
                    markeredgecolor=COL_ENTRY if not already else '#999',
                    markeredgewidth=0.8, zorder=5)
            ax.text(sc+0.62, sr+0.58, f'S{i+1}', fontsize=6, color=COL_WALL, zorder=6)

        # Entry circle
        ec, er = entry
        ax.add_patch(plt.Circle((ec+0.5,er+0.5), 0.22, color=COL_ENTRY, zorder=6))
        ax.text(ec+0.5, er+0.5, 'E', ha='center', va='center',
                fontsize=6, color='white', fontweight='bold', zorder=7)

        # Exit circles
        for lbl, node in [('A', exit_a), ('B', exit_b)]:
            xc, xr = node
            ax.add_patch(plt.Circle((xc+0.5,xr+0.5), 0.22, color=COL_EXIT, zorder=6))
            ax.text(xc+0.5, xr+0.5, lbl, ha='center', va='center',
                    fontsize=6, color='white', fontweight='bold', zorder=7)

        legend_items = [
            mpatches.Patch(color=COL_ENTRY,  label='Entry'),
            mpatches.Patch(color=COL_EXIT,   label='Exit A / B'),
            mpatches.Patch(color=COL_SUPPLY, label='Supply unit'),
        ]
        if node_colors:
            legend_items += [
                mpatches.Patch(color=COL_VISITED,  alpha=0.5, label='Visited'),
                mpatches.Patch(color=COL_FRONTIER, alpha=0.5, label='Frontier'),
                mpatches.Patch(color=COL_CURRENT,  alpha=0.7, label='Current'),
            ]
        if (legend):
            ax.legend(handles=legend_items, loc='upper left', fontsize=8, framealpha=0.9)
        ax.set_xlim(0, COLS); ax.set_ylim(0, ROWS)
        ax.set_aspect('equal'); ax.axis('off')
        ax.set_title(title, fontsize=11, fontweight='bold', color='#0B1F3B', pad=10)
        plt.tight_layout()
        return fig, ax

    return COL_PATH, draw_facility_v1


@app.cell(hide_code=True)
def _(
    COLS,
    ROWS,
    fac_entry_v1,
    fac_exit_a_v1,
    fac_exit_b_v1,
    fac_graph_v1,
    fac_supplies_v1,
    nx,
):
    # turn Mr Nielsens implimentation into mine :)


    def tup_to_flat_V1(a):
        return a[0] + COLS*a[1]

    def flat_to_tup_V1(a):
        return (a % COLS,int(( a- (a%COLS))/COLS))

    #def K_to_Mr(G, AS, SU, VP, EP, SUP, ASP, GP):



       # return fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1

    def Mr_to_K_V1(fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1):

        vertices = []
        G = nx.DiGraph()

        G.add_nodes_from([v for v in range(ROWS*COLS)])

        for edge in fac_graph_v1.edges():
            G.add_edge(tup_to_flat_V1(edge[0]),tup_to_flat_V1(edge[1]))
            G.add_edge(tup_to_flat_V1(edge[1]),tup_to_flat_V1(edge[0]))

        SU = {i for i in range(len(fac_supplies_v1))}

        AS = {0}


        VP: dict[dict[bool,bool,int]] = {i:{"is_entry":False, "is_exit": False, "supply_unit": None} for i in range(ROWS*COLS)}
        VP[tup_to_flat_V1(fac_entry_v1)]["is_entry"] = True
        VP[tup_to_flat_V1(fac_exit_a_v1)]["is_exit"] = True
        VP[tup_to_flat_V1(fac_exit_b_v1)]["is_exit"] = True
        for i in range(len(fac_supplies_v1)):
            VP[tup_to_flat_V1(fac_supplies_v1[i])]["supply_unit"] = i



        EP: dict[dict[float]] = {edge: {"cardinal_angle": 0}  for edge in G.edges}
        for edge in G.edges():
            if edge[0] == edge[1]-1:
                EP[edge]["cardinal_angle"] = 90
            elif edge[0] == edge[1]+1:
                EP[edge]["cardinal_angle"] = 270
            elif edge[0] == edge[1]-COLS:
                EP[edge]["cardinal_angle"] = 0
            elif edge[0] == edge[1]+COLS:
                EP[edge]["cardinal_angle"] = 180
            else:
                raise Exception("Something went wrong!")


        SUP: dict[dict[int]] = {i:{"location": tup_to_flat_V1(fac_supplies_v1[i])} for i in range(len(fac_supplies_v1))}

        ASP = {0:{"location":  tup_to_flat_V1(fac_entry_v1)}}

        GP = {}
        return G, AS, SU, VP, EP, SUP, ASP, GP


    G, AS, SU, VP, EP, SUP, ASP, GP = Mr_to_K_V1(fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1)
    return AS, ASP, EP, G, GP, SU, SUP, VP, flat_to_tup_V1


@app.cell(hide_code=True)
def _(VP, deque):
    # G = (V,E)

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
            walks.append(DFS_v1(G, entry, parent, sub_exit, sub_SU, i))

        #4. Calculating traversal_cost

        walk = shortest_walk(walks)
        length = len(walk) - 1

        #--------------------------------------------------
        #-----------------Return the output----------------
        #--------------------------------------------------

        #Outputing to the physical environment the instructions for the AS

        for i in range(length):
            _move(EP[(walk[i], walk[i+1])]["cardinal_angle"],1)
        _exit()

        return {"walk": walk, "length": length, "supply_units_recovered": SU}  

    def _move(a,b):
        #move at a angle b distance
        return
    def _exit():
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

    def DFS_v1(G, s, parent, sub_exit, sub_SU, i):
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
        min_index = 0
        min = len(walks[0])
        for i in range(len(walks)):
            if len(walks[i]) < min:
                min = len(walks[i])
                min_index = i

        return walks[min_index]



    return BFS, BFS_DFS, backtrace_tree, make_sub_exits


@app.cell(hide_code=True)
def _(AS, ASP, BFS_DFS, EP, G, GP, SU, SUP, VP, time, tracemalloc):
    # RUN BFS+DFS

    tracemalloc.start()
    tracemalloc.reset_peak()
    _size1, _peak1 = tracemalloc.get_traced_memory()

    _start_time = time.perf_counter()
    out_v1 = BFS_DFS(G, AS, SU, VP, EP, SUP, ASP, GP)
    BFS_DFS_time_taken = time.perf_counter() - _start_time
    _size2, _peak2 = tracemalloc.get_traced_memory()

    #print("size: "+str(_size2)+", peak:" + str(_peak2))
    #print("size: "+str(_size2-_size1)+", peak:" + str(_peak2-_peak1))
    memory_used = _peak2 - _size1
    walk_v1 = out_v1["walk"]

    tracemalloc.stop()
    # draw_facility_v1(fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1, highlight_path=[flat_to_tup_V1(v) for v in walk_v1], node_colors= { flat_to_tup_V1(walk_v1[len(walk_v1)-1]):"red"})
    return BFS_DFS_time_taken, memory_used, out_v1, walk_v1


@app.cell(hide_code=True)
def _(
    COL_PATH,
    draw_facility_v1,
    fac_entry_v1,
    fac_exit_a_v1,
    fac_exit_b_v1,
    fac_graph_v1,
    fac_supplies_v1,
    flat_to_tup_V1,
    imageio,
    os,
    plt,
    seed,
    walk_v1,
):
    #define make_gif_v1
    def front_focus_v1(_walk):
        leading = "#FF0000"
        base_col = '#58D4D3'

        _col_dict = {flat_to_tup_V1(v):base_col for v in _walk}

        _col_dict[flat_to_tup_V1(_walk[len(_walk)-1])] =  leading

        return _col_dict


    def make_gif_v1():
        if not os.path.exists("figs\\"):
           os.mkdir("figs\\")

        if (os.path.exists("figs\\"+ str(seed) + ".gif")):
            return False
    
        _fig, _ax= draw_facility_v1(fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1, legend = False)

        for _i in range(len(walk_v1)): 
            _highlight_path = [flat_to_tup_V1(v) for v in walk_v1[0:_i+1]]
            _node_colors = front_focus_v1(walk_v1[0:_i+1])

            if _highlight_path and len(_highlight_path) > 1:
                    px = [c + 0.5 for c,r in _highlight_path]
                    py = [r + 0.5 for c,r in _highlight_path]
                    path_plot, = _ax.plot(px, py, color=COL_PATH, lw=1.8, linestyle='--', alpha=0.75, zorder=4)


            if _node_colors:
                rectangles = []
                for node, color in _node_colors.items():
                    c, r = node
                    rect = plt.Rectangle((c, r), 1, 1, color=color, alpha=0.50, zorder=2)
                    rectangles.append(rect)
                    _ax.add_patch(rect)


            name = "figs\\"
            name += str(seed) + "_"
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
        for _i in range(len(walk_v1)): 
            _name = "figs\\"
            _name += str(seed) + "_"
            _name += str(_i)
            _name += ".png"
            list_of_im_paths.append(_name)

        path_to_save_gif = "figs\\"+ str(seed) + ".gif" 
        ims = [imageio.imread(f) for f in list_of_im_paths]
        dur = [0.1 for f in list_of_im_paths]
        dur[len(dur)-1] = 1.5
        imageio.mimsave(path_to_save_gif, ims, loop = 10000)

        for _i in range(len(list_of_im_paths)):
            if os.path.exists(list_of_im_paths[_i]):
                os.remove(list_of_im_paths[_i])

        return True



    return (make_gif_v1,)


@app.cell(disabled=True, hide_code=True)
def _(
    AS,
    ASP,
    BFS,
    EP,
    G,
    GP,
    SU,
    SUP,
    VP,
    backtrace_tree,
    draw_facility_v1,
    fac_entry_v1,
    fac_exit_a_v1,
    fac_exit_b_v1,
    fac_graph_v1,
    fac_supplies_v1,
    flat_to_tup_V1,
    make_sub_exits,
):
    # coloured graph for BFS+DFS
    def _get_sub_dicts(G, AS, SU, VP, EP, SUP, ASP, GP):
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
        return sub_exit, sub_SU

    _sub_exit, _sub_SU = _get_sub_dicts(G, AS, SU, VP, EP, SUP, ASP, GP)

    _node_colours = {}
    for _k in _sub_SU.keys():
        if not _sub_exit[_k] and not _sub_SU[_k]:
            _node_colours[flat_to_tup_V1(_k)] = "#000000"
        elif not _sub_exit[_k] and _sub_SU[_k]:
            _node_colours[flat_to_tup_V1(_k)] = "#D0D0E0"
            pass
        else :
            #_node_colours[flat_to_tup_V1(_k)] = "#58D4D3"
            pass

    draw_facility_v1(fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1,node_colors=_node_colours, legend= False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Problem Specification (Version 1):

    Seismic activity has destabilised the Emberlight Subterranean Research Complex (ESRC). Five critical supply units — designated S1 through S5 — remain scattered throughout the structure and are to be recovered.

    The ESRC is organised as a sector grid. Each sector is a discrete navigable unit. Sectors are connected by reinforced corridors. The sector grid can be seen below.

    The objective is to command CRUDY-1 (Corridor Reconnaissance and Utility Drone — Year 1)--an Autonomous System (AS)--to navigate the facility’s corridor network and transport recovered supply units to an extraction point while maximising recovered supply units and ensuring a safe extraction.

    (Nielsen, 2026)
    """)
    return


@app.cell
def _(
    draw_facility_v1,
    fac_entry_v1,
    fac_exit_a_v1,
    fac_exit_b_v1,
    fac_graph_v1,
    fac_supplies_v1,
):
    draw_facility_v1(fac_graph_v1, fac_entry_v1, fac_exit_a_v1, fac_exit_b_v1, fac_supplies_v1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This notebook explores the development of a design stratergy to complete this task, including
    1. deciding how the facility and mission should be represented computationally;
    2. identifing the constraints governing the AS's operation;
    3. designing an initial strategy and communicating it clearly;
    4. analysing efficiency and feasibility;
    5. refining and improving the design as new constraints emerge;
    6. justifing decisions and comparing alternatives with depth.

    (Nielsen, 2026)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Definitions:
    Spaces:
    - ESRC: The Emberlight Subterranean Research Complex, the scope of this problem.
    - Sector: A single unit of space, which can be occupied by an autonomous system (AS).
    - Sector Grid: A grid of sectors, joined by corridors and contained within the ESRC.


    Movement Options:
    - Corridor: Connects two adjacent sectors in the same sector grid that don't have a wall in-between them. Can be bidirectional or one-way.

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

    ## Assumptions:
    1.  An Autonomous System (AS) knows the layout of the ESRC sector grid before it navigates it (e.g. it has the blueprints).
    2.  The ASs can navigate in all directions without turning, and the AS knows its original orientation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part A - Problem Specification:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A1 - Algorithmic problem statement:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
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
def _(mo):
    mo.md("""
    #### Maps

    The following four ADTs are maps of maps, where the key gives you a map of properties of that object. The properties might have keys with values, such as 'weight: 1'. The final map gives properties of the whole ESRC.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### Map 1 - Edge Properties (EP):

    The first map, EP (Edge Properties), takes the edges as keys and returns a map that contains:

    - a real number indicating which direction this edge is pointing (cardinal angle). 0° faces north, 90° east, 180° south and 270° west.

    Beyond scope of version 1:

    - a real number indicating the cost to traverse (as it is all the same)
    - a real number indicating the stability of the corridor.
    - a real number indication the length of the corridor.

    In version 1, a possible implementation of this is:

    EP = {(u,v):{ "cardinal_angle": real number (cardinal angle from u to v)}
    	| u,v ∈ V ∧ (u,v) ∈ E}

    ##### Map 2 - Vertex Properties (VP):

    This map, VP (Vertex Properties), takes vertices (or sectors) as keys and returns a map that contains:

    - a string indicating what supply unit lies within the sector, or null if no supply unit is contained.
    - a Boolean value indicating whether it is an entry.
    - a Boolean value indicating whether it is an exit.

    Beyond scope of version 1:

    - a value indicating the stability of the sector.
    - size
    - shape

    In version 1, a possible implementation of this is:

    VP = {v : {
    	"supply_unit": nullable string (name of supply unit within the sector, null if it doesn't contain a supply unit),
    	"is_entry": Boolean (true if the sector is an entry, false otherwise) ,
    	"is_exit": Boolean (true if the sector is an extraction point, false otherwise )}
    	| v ∈ V}

    ##### Map 3 - Supply Unit Properties (SUP):

    This map, SUP (Supply Unit Properties), takes a supply unit as a key and returns a map that contains:

    - a sector (a vertex of graph G) indicating location (the sector on which the supply unit lies)

    Beyond scope of version 1:<br>
    In the version 1 problem scope, these properties of the supply units are irrelevant, so they won't be included in the map returned for each supply unit:
    - a real number indicating the weight of the supply unit (as in the version 1 problem, all supply unit weights are the same)
    - fragility
    - importance
    - size
    - lifespan

    In version 1, a possible implementation of this is:

    SUP = {s:{"location": v (the sector of the SU)} | v∈V∧s∈SU}

    ##### Map 4 - Autonomous System Properties (ASP):

    This map, ASP (Autonomous System Properties), takes Autonomous Systems (ASs) as keys and returns a map that contains:

    - a vertex which is the starting location (or entry) of the AS.

    Beyond scope of version 1:

    - a string indicating type (e.g. CRUDY-1) (as in version 1 there is only one type)
    - a real number indicating the total weight the AS can carry. (as in version 1 this equals the total supply units on the map)
    - a real number indicating how many supply units AS can carry at once. (that is different from the weight, right now they are the same so this is not necessary)
    - a real number indicating total energy of the AS.
    - a real number indicating how much energy a corridor takes.
    - a list of SUs that the AS has been assigned to extract.
    - a vertex indicating assigned extraction point for the AS.
    - a real number indicating speed of the AS.

    In version 1, a possible implementation of this is:

    ASP (Autonomous System Properties) = {x:{"entry": v (indicates entry for AS)}| x ∈ AS ∧ v ∈ V}

    ##### Map 5 - Graph Properties (GP):

    This map provides properties of the whole environment, such as:

    - a Boolean value indicating whether emergency lighting is operational
    - a time limit

    These are all beyond the version 1 problem scope, so:

    GP = {}

    ### Outputs

    #### Computational Outputs

    The output of the algorithm that the AS is running is a map containing:
    - A walk taken by the AS that maximises the number of supply units extracted. It starts at an entry and ends at an exit. (as a list)
    - Total energy expended (as a real number)
    - Supply Units recovered (as these are collected instantaneously) (as a set)

    It doesn't have to be a perfect solution, but it should aim to be an efficient one.

    so the output might look like:

    output = {"walk":  [$v_1$,,$v_2$,,$v_3$,...,,$v_n$],<br>
    "energy_expended": real number,<br>
    "supply_units_recovered": {$s_1$,$s_2$,$s_3$,...$s_m$}}

    #### Environmental Outputs

    It also has a continuous set of environmental outputs (controlling its actions) in the form of commands including:
    	1. move(a: angle, d: distance) → None         # allows the AS to move 'd' distance at 'a' cardinal angle.
    	2. exit() → None         # if at an exit (extraction point), it allows the AS to exit the sector grid.

    Note: There is no command that specifically orders to pickup a supply unit as that is automatically done when occupying the same sector as the supply unit.<br>
    Note: There is no command to scan the environment as it is assumed that the AS already knows the layout of the ESRC.


    ### Constraints

    1. The first vertex of the walk AS makes must be an entry.
    2. The last vertex of the walk AS makes must be an exit.
    3. $\forall i [i \in \mathbb{N} \land i \in [1,n] \implies v_i \in V]$
    - meaning all vertices in the walk must be vertices of graph G.
    4. $\forall i [i \in \mathbb{N} \land i \in [1,n-1] \implies e_i \in E \land e_i = (v_i,v_{i+1})]$
    - meaning all edges in the walk must be edges of graph G and that the edge $e_i$ must be from $v_i$ to $v_{i+1}$.

    *3 and 4 are simply ensuring the walk is indeed a walk on graph G.

    ### Objectives

    1. Maximise supply unit recovery.
    2. Minimise energy cost. In version 1, this is proportional to the number of edges traversed in the walk, so ||walk|| should be minimised. This is a lower priority compared to the first objective.
    3. Minimise computational time of the algorithm

    These three objectives mean that in the version 1 problem, the objective is to compute the shortest walk collecting all supply units and making it to the exit with a minimal computational time. This is as the version 1 problem is quite small and therefore even a bruteforce approach is relatively fast.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A2 - Salient Features:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Position
    1. The position of on object is defined as a vertex of the graph G, with edges describing its position relative to other vertices.
    2. The direct position (for example as GPS coordinates) is abstracted away and only shown in reference to that of the starting vertex (the entry), as the AS only needs to know where it is in the sector grid relative to other vertices.

    Direction
    1. This is modelled as a cardinal angle assigned to each edge of the graph G and the direction that the AS is facing. 0º doesn't have to be north, it only has to be consistent.
    2. The physically layout of the sector grid is abstracted away into this grid, as it only matters how to get from one sector to another sector to be able to traverse the whole grid. This can be calculated using the cardinal direction. (i.e. only relative space matters, not absolute.)

    Length
    1. The length of an edge (i.e. a corridor) can be abstracted away as in version 1, all corridors have the same length, meaning the AS only has to move in multiples of one edge length of the graph.

    Time
    1. Time is not modelled in the abstraction of version 1.
    2. This is a safe abstraction as conditions are stable.

    Mass
    1. Mass is modelled in units. The weight of supply units are all identical (weight = 1) so they can be abstracted away.
    2. As the AS can carry up to 5 units of weight, this is identical to saying the AS can carry up to 5 supply units.
    3. The unit is some weight, which is irrelative, it only matters relative to other masses.

    Corridors
    1. These are modelled as two edges between the sectors it is between, representing the two ways that one can pass through a corridor. The direction of the corridor is modelled as an cardinal angle.
    2. The shape of the corridor and the roughness of it is abstracted away as it is assumed that all corridors are traversable by the AS. This may or may not be a safe abstraction. The length of these corridors are abstracted away as they have the same length and the stability is abstracted away as it is assumed that conditions are stable in version 1.

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
        - total energy of the AS. (currently irrelevant in the version 1 problem scope, the AS has more than enough energy)
        - SUs that the AS has been assigned to extract. (all of them so doesn't need to be explicitly mentioned to the AS)
        - assigned extraction point for the AS. (doesn't matter as AS can exit at any extraction point)
        - speed of the AS. (doesn't matter as time is irrelevant in the version 1 problem scope)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A3 - ADTs for Modelling
    """)
    return


@app.cell(hide_code=True)
def _(mo):
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
    insert_at(l: list, i: Index, e: Element) → list<br>
    insert_at(l1: list, i: Index, l2: list) → list<br>
    append(l: list, e: Element) → list<br>
    append(l1: list, l2: List) → list<br>
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

    ### ADTs used <!--potential improvements to be made-->

    #### Inputs:

    - A Graph of the Sector Grid,
    - Maps of properties of the graph, vertices, edges, autonomous systems ASs and supply units SUs.
    - Sets of the ASs and the SUs.

    The graph is ideal to model a 2d space with discrite points where one can be, as graphs are well suited to finding paths and walks in space.<br>
    The sets are ideal to convey what is in the environment as order doesn't matter and it can store many items effectively.
    The maps are ideal to convey information about elements in the environment as they take an element and return a value (which can be made of multiple values) giving key information about said element.

    #### Outputs:

    map containing the whole output, including a:
    - List (of vertices and edges traversed in walk).
    - set (of supply units recovered)
    - integer (cost of walk)

    having these outputs all in a map allows for ease of use as they are packaged together.

    #### Within the Algorithm

    The algorithm is quite complicated with many ADTs used but some key ADTs used are:
    - A queue for BFS
    - A stack for DFS
    - Multiple maps to represent a tree, visited etc.
    - A list for the walk (ordered and allows for access to all locations without mutations.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B - Algorithm Design:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem properties
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Known properties of the version 1 problem:

    - all edges have the same weight, so it can be treated as an unweighted graph.
    - the graph is a tree
    - the maximum degree of any vertex is 4 as it is in a grid, meaning it is a 'sparse' graph for the sake of computation. (so an adjacency list is the way to go here).
    - There are 5 supply units
    - There are 2 exits.
    - There are ||V|| = 144 sectors.

    BFS is the best way to find the shortest path from a node to all nodes O(V+E) for an unweighted graph.

    Note: if edge traversal cost starts to differ (but stays positive) use Dijkstra's instead of BFS, O(log(V)(V+E)).

    Note: if there are negative edges (but not negative cycles), use Bellman Ford instead of BFS, O(VE).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Options
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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

    First: Finds all shortest paths between the supply units, the entry and the exits, put these into a (S+#entries + #exits) squared matrix.

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

    #### Algorithm:

    Overview:

    1. Do BFS retaining paths, number of children and leaf nodes O(V+E)
    2. Backwards trace the graph from the leaf nodes giving a property to each node whether it has a supply unit (SU) beneath it, and whether it has an exit beneath it. O(V)
    3. For each exit: O(#Exits(V+E))
    	1. Do DFS on the graph (retaining walk), where branches with SUs without exits are explored first. (ignore all branches without a SU or an exit)
    4. Find which of the walks is shortest and return that. O(#Exits V)

    Total time complexity O(V+E) + O(V) + O(#Exits(V+E)) + O(#Exits V) = O(#Exits(V+E))
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Discussion
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every option above has its merits and its drawbacks, but option 3 seems to be the most optimal for the version 1 problem as it balances speed with finding the optimal solution. Its time complexity is O(#Exits(V+E)), which is only always beaten by the DFS algorithm in terms of speed.

    Compared to the Brute force option, with time complexity O((V+E)S+S!) where S is #of supply units, the BFS + DFS solution is significantly faster for large values of S.

    A significant drawback of the BFS + DFS algorithm is that it relies on the graph being a tree which might not be the case in versions beyond version 1, leading to a potentially suboptimal solution for graphs with cycles.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part C - Pseudocode
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C1 - Algorithm in pseudocode (Nielsen, 2026)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pseudocode: (**Please note that marimo md renders indentation wrong for my pseudocode, please refer to the raw md**)

    ```
    //1 indexed.
    FUNCTION ember_rescue(G: Directed Unweighted Graph, SU: Set, AS: Set, VP: Map, EP: Map, SUP: Map, ASP: Map, GP: Map) -> Map
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C2 - Algorithm in python
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
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

        return {"walk": walk, "length": length, "supply_units_recovered": SU}

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
        min_index = 0
        min = len(walks[0])
        for i in range(len(walks)):
            if len(walks[i]) < min:
                min = len(walks[i])
                min_index = i

        return walks[min_index]


    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## C3 - Displaying the Process
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Inputs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    the inputs are: G, SU, AS, EP, VP, SUP, ASP, GP.
    - G: (Graph of a Sector Grid) = (V,E)
    - SU: (Supply Unit)
    - AS: (Autonomous System)
    - EP: (Edge Properties)
    - VP: (Vertex Properties)
    - SUP: (Supply Unit Properties)
    - ASP: (Autonomous Systems Properties)
    - GP: (Graph Properties)


    **Input values:**
    """)
    return


@app.cell
def _(AS, ASP, EP, G, GP, SU, SUP, VP, mo):
    _G = f"""
    ```python
    G = {G} = (in adjancey-list form) { {v:list(dict(G[v]).keys()) for v in G.nodes()} }
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
def _(mo):
    mo.md(r"""
    ### Outputs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is an animation showing the walk taken by the AS. The red node is the one currently occupied by the AS.

    Note: Creating the animation (stored at figs\\\\) often takes 1-2 minutes.
    """)
    return


@app.cell
def _(make_gif_v1, mo, seed, time):
    #DISPLAY GIF

    if(make_gif_v1()):
        time.sleep(10)
    mo.image("figs\\"+ str(seed) + ".gif")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Features of the walk:**
    """)
    return


@app.cell
def _(BFS_DFS_time_taken, memory_used, mo, out_v1):
    mo.callout(mo.hstack([
            mo.stat(label="Length",    value=str(out_v1["length"])),
            mo.stat(label="Time to Compute",    value=str(round(BFS_DFS_time_taken,4))+" sec"),
            mo.stat(label="Memory to Compute",    value=str(round(memory_used/1000,1))+" KB"),
            mo.stat(label="Supply Units Recovered",  value="All"),
        ], gap=0, wrap=True),kind = "info")
    return


@app.cell(hide_code=True)
def _(flat_to_tup_V1, mo, out_v1):
    mo.callout(mo.md(rf"""
    **walk list printed out in tuple form:**
    ```python
    {[flat_to_tup_V1(v) for v in out_v1["walk"]]}
    ```

    **raw output:**
    ```python
    {out_v1}
    ```
    """), kind = "info")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part D - Justification
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### DFS returns best walk proof
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Scope: undirected trees. (can be weighted)

    POI = Points of Interest, here meaning entries, exits and supply units.

    Conjecture: A shortest walk containing all POI (points of interest) ending at a specific node can be found utilising a modified DFS on a subtree with only POI as leaf nodes.

    Lemma 1: to visit all nodes and return to the source, DFS provides a shortest walk.
    1. Since to get to a node from another node there is only one path as G is a tree.
    2. To get to a single node and back to the source all edges in that path have to be traversed at least twice as there is only one path to go there and back.
    3. Each edge in the graph has to connect at least one node to the tree connected to the source meaning that all edges have to be traversed at least twice to visit all nodes and return to the source.
    4. Therefore the walk has to have length at <u>**least**</u> 2sum(E) (where sum(E) is the sum of all edge weights) as each edge is traversed twice.
    5. But DFS produces a walk of length 2sum(E) as it has to traverse all edges (in a tree) and then back again.
    6. This means DFS produces an optimal walk for its length is the shortest it could be.

    Lemma 2: DFS can produce a walk with length 2sum(E) - dist(source,v), if it has to visit all nodes from a source and end at v.
    1. Consider if DFS stacks the node with v as a decendant or v itself first at each iteration. Then DFS will explore all other branches before it pops v, and at that point it will explore the desendants of v. once it has explored all nodes, DFS will start returning to the source, and v has to be on that route as it (or a desendant of v) was explored last.
    2. Therefore as it will end at v having explored all nodes and on a direct path to the source with distance dist(source,v) and we know that a full DFS takes 2sum(E), the length of this walk must be 2sum(E) - dist(source,v).

    Lemma 3 There is no walk shorter that 2sum(E) - dist(source,v), if it has to visit all nodes from a source and end at v.
    1. Assume the opposite, there is a walk with length l < 2sum(E) - dist(source,v) that visits all nodes starting at the source and ending at v.
    2. Then l + dist(source,v) equals the return trip length of a walk visiting all nodes starting and ending at the source, as one just has to go from v to source and dist(source,v) = dist(v, source), which must be at least 2sum(E) from lemma 1.
    3. but l + dist(source,v) < 2sum(E) - dist(source,v) + dist(source,v) = 2sum(E).
    4. 2sum(E) $\leq$ l + dist(source,v) < 2sum(E) $\implies$ 2sum(E) < 2sum(E)
    5. There by contradiction Lemma 3 is true.

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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Proof Summary

    As the BFS+DFS algorithm utilises DFS in the manner discussed in the proof, BFS+DFS returns the shortest walk for the version 1 problem.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Suitability:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The ESRC is a **undirected, unweighted tree** meaning that my BFS+DFS algorithm--which requires an unweighted and undirected graph and returns an optimal solution for a tree--is a perfect match. It is also rather efficient (O((V+E)#Exits)), so for this particular problem (as #exits = 2 and it is sparse with ||E|| =143), it outperforms more general solutions, such as brute force and greedy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Coherence:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ADTs Used:
    - the map VP--for vertex properties--is called with VP[v]["supply_unit"] to check if a sector has a supply unit, in order to help build a subtree of G.
    - The graph G is used in BFS to find the neighbours of a vertex v, with G.vertices().
    Mismatch Problems between BFS+DFS algorithm and part A's ADTs.

    My ADT design is a bit over the top including lots of details in multiple places as well as some parts that aren't relevant to the version 1 problem, such as ASP, AS, SUP and GP as they are static, which my algorithm ignores.<br>
    In part A, I call the graph the combination of two sets--V and E--but then I call it its own ADT which I use in the pseudocode and python.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Constraints:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
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

    Therefore, all constraints are met!
    """)
    return


if __name__ == "__main__":
    app.run()
