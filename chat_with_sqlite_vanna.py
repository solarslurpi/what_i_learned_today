import marimo

__generated_with = "0.9.32"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # Chatting with SQLite using Vanna
        I just finished a notebook where I used Langcha∈Langchain to convert natural language into a SQL Query using Ollama for loading and calling a local llm. In this notebook, I attempt the same thing - and then some - using Vanna. My goal is to explore a query that can be then plotted (like "plot the temperature values for December 10th") as well as an option to make suggestion queries that can appear as buttons in the UI.

        Let's DO THIS!
        """
    )
    return


@app.cell
def __():
    return


@app.cell
def __():
    from vanna.ollama import Ollama
    from vanna.chromadb import ChromaDB_VectorStore
    class MyVanna(ChromaDB_VectorStore, Ollama):
        def __init__(self, config=None):
            ChromaDB_VectorStore.__init__(self, config=config)
            Ollama.__init__(self, config=config)
    return ChromaDB_VectorStore, MyVanna, Ollama


@app.cell
def __(MyVanna):
    vn = MyVanna(config={'model': 'mistral'})

    vn.connect_to_sqlite('sniffer_data.db')
    return (vn,)


@app.cell
def __(vn):
    df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")
    df_ddl
    return (df_ddl,)


@app.cell
def __(df_ddl, vn):
    for ddl in df_ddl['sql'].to_list():
      vn.train(ddl=ddl)
    return (ddl,)


@app.cell
def __(vn):
    vn.ask(question="Plot the temperature values (not the average).")
    return


if __name__ == "__main__":
    app.run()
