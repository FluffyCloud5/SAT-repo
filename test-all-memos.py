import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from memo_1 import app as app_memo_1
    from memo_1_to_A1 import app as app_memo_1_to_A1 
    from memo_A1 import app as app_memo_A1
    from memo_A1_to_A2 import app as app_memo_A1_to_A2
    from memo_A2 import app as app_memo_A2


    return (
        app_memo_1,
        app_memo_1_to_A1,
        app_memo_A1,
        app_memo_A1_to_A2,
        app_memo_A2,
    )


@app.cell
async def _(
    app_memo_1,
    app_memo_1_to_A1,
    app_memo_A1,
    app_memo_A1_to_A2,
    app_memo_A2,
):
    result_1 = await app_memo_1.embed()
    result_1_to_A1 = await app_memo_1_to_A1.embed()
    result_A1 = await app_memo_A1.embed()
    result_A1_to_A2 = await app_memo_A1_to_A2.embed()
    result_A2 = await app_memo_A2.embed()
    return result_1, result_1_to_A1, result_A1, result_A1_to_A2, result_A2


@app.cell
def _(mo):
    choose_version = mo.ui.tabs({"Memo 1": "", "Memo 1 to A1": "", "Memo A1": "", "Memo A1 to A2":"", "Memo A2":""})
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


if __name__ == "__main__":
    app.run()
