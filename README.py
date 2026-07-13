import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    #RUN THIS NOTEBOOK AND PUT IT INTO APP VIEW
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
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


@app.cell
def _():
    from memo_1 import app as app_memo_1
    from memo_1_to_A1 import app as app_memo_1_to_A1 
    from memo_A1 import app as app_memo_A1
    from memo_A1_to_A2 import app as app_memo_A1_to_A2
    from memo_A2 import app as app_memo_A2
    from Side_Memos import app as app_side


    return (
        app_memo_1,
        app_memo_1_to_A1,
        app_memo_A1,
        app_memo_A1_to_A2,
        app_memo_A2,
        app_side,
    )


@app.cell
async def _(
    app_memo_1,
    app_memo_1_to_A1,
    app_memo_A1,
    app_memo_A1_to_A2,
    app_memo_A2,
    app_side,
):
    result_1 = await app_memo_1.embed()
    result_1_to_A1 = await app_memo_1_to_A1.embed()
    result_A1 = await app_memo_A1.embed()
    result_A1_to_A2 = await app_memo_A1_to_A2.embed()
    result_A2 = await app_memo_A2.embed()
    result_side = await app_side.embed()
    return (
        result_1,
        result_1_to_A1,
        result_A1,
        result_A1_to_A2,
        result_A2,
        result_side,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Choose a Memo
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    README_text = mo.md("""
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

    Hi Mr Nielsen. I hope your doing well. Sorry for the big document. 

    # Outline

    - From the tab above, you can select between each iteration of the solution, with Memo 1, Memo A1 and Memo A2. 

    - The Memo 'x' to 'y' shows an approximate dif file, highlighting changes made from file to file. 

    - The 'Memos' start at the 'Problem Outline (memo _ )' heading, everything before then is a review of the changes and adjustments made from memo to memo. 

    - The side memos tab contains all the side memos explored.

    # Thing to Know

    - As this notebook is relatively large, I would recommend running it in the cloud on Molab or just a beefy computer. Use the pyproject.toml to avoid the 'too large output' error from this notebook. Otherwise open the memo files individually

    - The figs/ folder contains the animations of walks taken by the different algorithms. Each time a new algorithm for a different seed is explored, the animations are saved there. For speed, I recommend not deleting this folder as it will have to be generated again.
    """)

    Bibliography_text = mo.md("""

    Abstract Data Type. (2025). Pages.Dev. https://quartz-akz.pages.dev/Abstract-Data-Type

    App - marimo. (2026). Marimo.Io. https://docs.marimo.io/api/app/#marimo.appmeta.theme

    Biconnected_components — NetworkX 3.6.1 documentation. (2025a). Networkx.Org. 
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.biconnected_components.html

    Chris, K. (2022, April 14). Dot Symbol – Bullet Point in HTML Unicode. freeCodeCamp.Org. https://www.freecodecamp.org/news/dot-symbol-bullet-point-in-html-unicode/

    CSS text-decoration property. (n.d.-a). Www.W3schools.Com. https://www.w3schools.com/cssref/pr_text_text-decoration.php

    DiGraph—Directed graphs with self loops — NetworkX 2.8.7 documentation. (n.d.-b). Networkx.Org.
    https://networkx.org/documentation/stable/reference/classes/digraph.html

    GeeksforGeeks. (2013, May 21). Articulation Points (or Cut Vertices) in a Graph. GeeksforGeeks.
    https://www.geeksforgeeks.org/dsa/articulation-points-or-cut-vertices-in-a-graph/

    GeeksforGeeks. (2017, December 8). Reversing a List in Python. GeeksforGeeks. https://www.geeksforgeeks.org/python/python-reversing-list/

    GeeksforGeeks. (2018, November 20). Get the Last Element of List in Python. GeeksforGeeks. 
    https://www.geeksforgeeks.org/python/python-how-to-get-the-last-element-of-list/

    GeeksforGeeks. (2019a, April 18). time.perf_counter() function in Python. GeeksforGeeks. https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python/

    GeeksforGeeks. (2019b, November 25). Create a directory in Python. GeeksforGeeks. https://www.geeksforgeeks.org/python/create-a-directory-in-python/

    GIF-FI Static and animated gif (FreeImage) — imageio 2.9.0 documentation. (2020). Readthedocs.Io. 
    https://imageio.readthedocs.io/en/v2.9.0/format_gif-fi.html

    Graph.subgraph — NetworkX 3.6.1 documentation. (2025b). Networkx.Org. 
    https://networkx.org/documentation/stable/reference/classes/generated/networkx.Graph.subgraph.html

    Image - marimo. (2026a). Marimo.Io. https://docs.marimo.io/api/media/image/#marimo.image

    marimo. (2024). Marimo.Io. https://docs.marimo.io/

    matplotlib.axes.Axes.remove — Matplotlib 3.10.9 documentation. (2026b). Matplotlib.Org.
    https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.remove.html

    matplotlib.pyplot.savefig — Matplotlib 3.7.1 documentation. (n.d.-c). Matplotlib.Org. 
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html

    Maxim Khesin. (2012, August 18). Python: pickling nested functions. Stack Overflow. 
    https://stackoverflow.com/questions/12019961/python-pickling-nested-functions

    MyBib Contributors. (n.d.). MyBib Citation Manager. MyBib. https://www.mybib.com/

    Nielson, K. (2026a). Marimo Memo 01.

    Nielson, K. (2026b). Task Description.

    os.path — Common pathname manipulations — Python 3.9.1 documentation. (n.d.-d). Docs.Python.Org. 
    https://docs.python.org/3/library/os.path.html

    patches. (2020). Matplotlib remove patches from figure. Stack Overflow. https://stackoverflow.com/questions/21687571/matplotlib-remove-patches-from-figure

    Python. (n.d.). multiprocessing — Process-based parallelism — Python 3.8.3rc1 documentation. Docs.Python.Org. 
    https://docs.python.org/3/library/multiprocessing.html

    Reddit - Please wait for verification. (2026c). Reddit.Com. 
    https://www.reddit.com/r/learnpython/comments/1j4o1i3/is_there_a_simple_way_to_run_a_loop_in_parallel/

    Shlomif. (2020, May 10). Creating an animation out of Matplotlib .pngs. Stack Overflow. 
    https://stackoverflow.com/questions/61716066/creating-an-animation-out-of-matplotlib-pngs

    Spring_layout — NetworkX 2.8.7 documentation. (n.d.). Networkx.Org. Retrieved July 7, 2026, from https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html

    tracemalloc — Trace memory allocations — Python 3.11.0 documentation. (n.d.-e). Docs.Python.Org. https://docs.python.org/3/library/tracemalloc.html

    Tutorial — NetworkX 2.5 documentation. (n.d.-f). Networkx.Org. https://networkx.org/documentation/stable/tutorial.html

    Welker, E. (2009, October 13). Can Python print a function definition? Stack Overflow. https://stackoverflow.com/questions/1562759/can-python-print-a-function-definition

    (2026d). Mintlify.App. https://marimo-team-marimo.mintlify.app/interactive-elements
    """)

    choose_version = mo.ui.tabs({"README":README_text,"Memo 1": "", "Memo 1 to A1": "", "Memo A1": "", "Memo A1 to A2":"", "Memo A2":"", "Side Memos": "", "References": Bibliography_text}, value = "README")
    choose_version
    return (choose_version,)


@app.cell
def _(choose_version, mo, result_1):
    mo.stop(choose_version.value != "Memo 1")

    result_1.output
    return


@app.cell
def _(choose_version, mo, result_1_to_A1):
    mo.stop(choose_version.value != "Memo 1 to A1")

    result_1_to_A1.output
    return


@app.cell
def _(choose_version, mo, result_A1):
    mo.stop(choose_version.value != "Memo A1")

    result_A1.output
    return


@app.cell
def _(choose_version, mo, result_A1_to_A2):
    mo.stop(choose_version.value != "Memo A1 to A2")

    result_A1_to_A2.output
    return


@app.cell
def _(choose_version, mo, result_A2):
    mo.stop(choose_version.value != "Memo A2")

    result_A2.output
    return


@app.cell(hide_code=True)
def _(choose_version, mo, result_side):
    mo.stop(choose_version.value != "Side Memos")

    result_side.output
    return


if __name__ == "__main__":
    app.run()
