import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


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
    matplotlib.use('agg')
    return deque, imageio, mo, mpatches, nx, os, plt, random, time


@app.cell(hide_code=True)
def _():
    COLS, ROWS =12,12
    return COLS, ROWS


@app.cell(hide_code=True)
def _(COLS, ROWS, nx, random):
    seed = 596281

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

    fac_graph, fac_entry, fac_exit_a, fac_exit_b, fac_supplies = \
        get_facility(seed)
    return fac_entry, fac_exit_a, fac_exit_b, fac_graph, fac_supplies, seed


@app.cell(hide_code=True)
def _(COLS, ROWS, mpatches, plt):
    # Draw Facility

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

    def draw_facility(graph, entry, exit_a, exit_b, supplies,
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

    return COL_PATH, draw_facility


@app.cell(hide_code=True)
def _(
    COLS,
    ROWS,
    fac_entry,
    fac_exit_a,
    fac_exit_b,
    fac_graph,
    fac_supplies,
    nx,
):
    # turn Mr Nielsons implimentation into mine :)


    def tup_to_basic(a):
        return a[0] + COLS*a[1]

    def basic_to_tup(a):
        return (a % COLS,( a- (a%COLS))/COLS)

    #def K_to_Mr(G, AS, SU, VP, EP, SUP, ASP, GP):



       # return fac_graph, fac_entry, fac_exit_a, fac_exit_b, fac_supplies

    def Mr_to_K(fac_graph, fac_entry, fac_exit_a, fac_exit_b, fac_supplies):

        vertices = []
        G = nx.DiGraph()

        G.add_nodes_from([v for v in range(ROWS*COLS)])

        for edge in fac_graph.edges():
            G.add_edge(tup_to_basic(edge[0]),tup_to_basic(edge[1]))
            G.add_edge(tup_to_basic(edge[1]),tup_to_basic(edge[0]))

        SU = {i for i in range(len(fac_supplies))}

        AS = {0}


        VP: dict[dict[bool,bool,int]] = {i:{"is_entry":False, "is_exit": False, "supply_unit": None} for i in range(ROWS*COLS)}
        VP[tup_to_basic(fac_entry)]["is_entry"] = True
        VP[tup_to_basic(fac_exit_a)]["is_exit"] = True
        VP[tup_to_basic(fac_exit_b)]["is_exit"] = True
        for i in range(len(fac_supplies)):
            VP[tup_to_basic(fac_supplies[i])]["supply_unit"] = i



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


        SUP: dict[dict[int]] = {i:{"location": tup_to_basic(fac_supplies[i])} for i in range(len(fac_supplies))}

        ASP = {0:{"location":  tup_to_basic(fac_entry)}}

        GP = {}
        return G, AS, SU, VP, EP, SUP, ASP, GP


    G, AS, SU, VP, EP, SUP, ASP, GP = Mr_to_K(fac_graph, fac_entry, fac_exit_a, fac_exit_b, fac_supplies)
    return AS, ASP, EP, G, GP, SU, SUP, VP, basic_to_tup


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

        # 2. Backtrace Tree


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



    return (BFS_DFS,)


@app.cell
def _(AS, ASP, BFS_DFS, EP, G, GP, SU, SUP, VP):
    output_dict = BFS_DFS(G, AS, SU, VP, EP, SUP, ASP, GP)

    walk = output_dict["walk"]

    #draw_facility(fac_graph, fac_entry, fac_exit_a, fac_exit_b, fac_supplies, highlight_path=[basic_to_tup(v) for v in walk], node_colors= { basic_to_tup(walk[len(walk)-1]):"red"})
    return (walk,)


@app.cell(disabled=True, hide_code=True)
def _(basic_to_tup):
    #old
    def subtract_hex_col(str1,str2,min,times):
        r1 = str1[1:3]
        r2 = str2[1:3]
        g1 = str1[3:5]
        g2 = str2[3:5]
        b1 = str1[5:7]
        b2 = str2[5:7]

        rb = min[1:3] 
        gb = min[3:5]
        bb = min[5:7]


        num = hex_to_base10(r1) + hex_to_base10(r2)*times
        numb = hex_to_base10(rb)
        if(num > numb):
            num = numb
        r = base10_to_hex(num)
        num = hex_to_base10(g1) + hex_to_base10(g2)*times
        numb = hex_to_base10(gb)
        if(num > numb):
            num = numb
        g = base10_to_hex(num)
        num = hex_to_base10(b1) + hex_to_base10(b2)*times
        numb = hex_to_base10(bb)
        if(num > numb):
            num = numb
        b = base10_to_hex(num)

        return "#"+r+g+b

    def hex_to_base10(str):
        order = "0123456789ABCDEF"
        hex_to_int = {}
        for _i in range(len(order)):
           hex_to_int[order[_i]] = _i

        base10 = 0
        for _j in range(len(str)):
            _i = len(str)-1-_j
            base10 += (16**_j)*hex_to_int[str[_i]]

        return base10

    def base10_to_hex(_int):
        order = "0123456789ABCDEF"
        mag = 0
        while 16**(mag+1) <= _int:
            mag += 1

        hex = ''
        while(mag >= 0):

            hex += order[int((_int-_int%(16**mag))/(16**mag))]

            _int = _int%(16**mag)

            mag -= 1

        if(_int != 0):
            print("smth went wrong")

        if len(hex) == 1:
            hex = '0' + hex
        return hex

    def fade(_walk):
        _col_dict = {}

        leading = "#FF0000"
        front_col = "#58D4D3"
        take_away = '#063030'
        base_col = '#58D4D3'

        """ Distracting
        leading = "#000000"
        front_col = "#000000"
        take_away = '#070303'
        base_col = '#58D4D3'
        """

        """Clear grey front
        leading = "#000000"
        front_col = "#000000"
        take_away = '#063030'
        base_col = '#58D4D3'
        """

        """ Red front, grey trail, Cyan visisted
        leading = "#FF0000"
        front_col = "#000000"
        take_away = '#063030'
        base_col = '#58D4D3' 
        """





        for _j in range(len(_walk)):
            _i = len(_walk)-1-_j
            _col_dict[basic_to_tup( _walk[_j])] = subtract_hex_col(front_col,take_away,base_col,_i)


        _col_dict[basic_to_tup(_walk[len(_walk)-1])] =  leading


        return _col_dict

    return


@app.cell
def _(
    COL_PATH,
    basic_to_tup,
    draw_facility,
    fac_entry,
    fac_exit_a,
    fac_exit_b,
    fac_graph,
    fac_supplies,
    imageio,
    mo,
    os,
    plt,
    seed,
    time,
    walk,
):
    def front_focus(_walk):
        leading = "#FF0000"
        base_col = '#58D4D3'

        _col_dict = {basic_to_tup(v):base_col for v in _walk}

        _col_dict[basic_to_tup(_walk[len(_walk)-1])] =  leading

        return _col_dict


    def make_gif():
        if not os.path.exists("figs\\"):
           os.mkdir("figs\\")

        if (os.path.exists("figs\\"+ str(seed) + ".gif")):
            return False

        _fig, _ax= draw_facility(fac_graph, fac_entry, fac_exit_a, fac_exit_b, fac_supplies, legend = False)

        for _i in range(len(walk)): 
            _highlight_path = [basic_to_tup(v) for v in walk[0:_i+1]]
            _node_colors = front_focus(walk[0:_i+1])

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
        for _i in range(len(walk)): 
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

    if(make_gif()):
        time.sleep(10)
    mo.image("figs\\"+ str(seed) + ".gif")
    return


if __name__ == "__main__":
    app.run()
