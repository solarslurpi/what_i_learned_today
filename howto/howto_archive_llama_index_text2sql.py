# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "duckdb==1.1.1",
#     "llama-index==0.12.5",
#     "llama-index-llms-ollama",
#     "marimo",
#     "pandas==2.2.3",
#     "requests==2.32.3",
#     "sentence-transformers==3.3.1",
#     "sqlalchemy==2.0.36",
# ]
# ///

import marimo

__generated_with = "0.10.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # The Purpose
        I was exploring evaluating text2sql using LlamaIndex. I found during the exploration that the LlamaIndex implementation is very heavy weight. It just made me feel sad there was all this code goop.  So many packages to install and get right.  So much code to have to load and debug. So I decided to stick to just using a LLM that was focused on text2sql then trying to abstract all these rules on top of it.  Thus, this notebook is more of an artifact. I keep it because it shows how to set up Llamaindex in this environment.
        """
    )
    return


@app.cell
def _():
    from llama_index.core.query_engine import NLSQLTableQueryEngine
    from llama_index.core import SQLDatabase
    from llama_index.llms.ollama import Ollama
    from sentence_transformers import SentenceTransformer
    from sqlalchemy import create_engine

    db_uri = "sqlite:///data/sniffer_data.db"
    engine = create_engine(db_uri)
    sql_database = SQLDatabase(engine)
    return (
        NLSQLTableQueryEngine,
        Ollama,
        SQLDatabase,
        SentenceTransformer,
        create_engine,
        db_uri,
        engine,
        sql_database,
    )


@app.cell
def _():
    import os
    print(os.getcwd())
    print("Files in directory:", os.listdir())
    return (os,)


@app.cell
def _(engine):
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Available tables:", tables)

    # If you want more details about each table, you can do:
    for table_name in tables:
        columns = inspector.get_columns(table_name)
        print(f"\nTable: {table_name}")
        for column in columns:
            print(f"  {column['name']}: {column['type']}")
    return column, columns, inspect, inspector, table_name, tables


@app.cell
def _(NLSQLTableQueryEngine, Ollama, SentenceTransformer, sql_database):
    embed_model = SentenceTransformer('multi-qa-mpnet-base-cos-v1')
    llm = Ollama(model="sql_with_duckdb_nsql")

    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, 
        llm=llm,
        embed_model=embed_model
    )
    query_str = "What is the average humidity value for the last 5 readings2?"
    response = query_engine.query(query_str)
    response
    return embed_model, llm, query_engine, query_str, response


@app.cell
def _(mo):
    mo.md(
        r"""
        # Not Using LlamaIndex
        LlamaIndex provides all these gooey extractions that add additional oomph to text2sql. Like checking if the SQL is valid (I think because when I used the strict to SQL llm, it seemed to always give llm) and immediately going to an english like language.

        Using built in marimo features and going directly to ollama however is much, much less heavy weight.
        """
    )
    return


if __name__ == "__main__":
    app.run()
