import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from memo1 import app as app_memo1
    from memo1toA1 import app as app_memo1_to_A1 
    from memoA1 import app as app_memoA1


    return app_memo1, app_memo1_to_A1, app_memoA1


@app.cell
async def _(app_memo1, app_memo1_to_A1, app_memoA1):
    result_1 = await app_memo1.embed()
    result_1_to_A1 = await app_memo1_to_A1.embed()
    result_A1 = await app_memoA1.embed()
    return result_1, result_1_to_A1, result_A1


@app.cell
def _(mo):
    choose_version = mo.ui.tabs({"Memo 1": "", "Memo 1 to A1": "", "Memo A1": ""})
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


if __name__ == "__main__":
    app.run()
