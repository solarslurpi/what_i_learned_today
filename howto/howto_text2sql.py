# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "duckdb==1.1.1",
#     "marimo",
#     "ollama==0.4.4",
#     "pandas==2.2.3",
#     "requests==2.32.3",
# ]
# ///

import marimo

__generated_with = "0.10.6"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import duckdb
    import marimo as mo
    return duckdb, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Explore text2sql

        The goal of this notebook is to explore methods of doing text2sql under the constraints of:

        - marimo is the IDE and UI.
        - The LLM that translates questions into SQL queries runs locally.
        - The results are not assumed to be accurate. The intent is to understand the workflow and how well this setup can perform on this task.

        ## Different Approaches

        Using marimo and Ollama stayed constant througout explorations.  I started out with a sqlite database but ended up using a DuckDB database for reasons I'll get into in a bit. Different approaches were tried.

        ### Langchain and LlamaIndex APIs

        Both have examples and code for text2sql.  A few lines of code and all should be spiffy.  Until it isn't.  While I could get both running, getting stuff to work became a chore.  It was not fun. I rapidly devolved into spelunking through their GitHub where I would lose focus rapidly as I tried to unravel the code.

        LLMs I tried included llama3.2 and nemo-mistral.  

        ### marimo's built in SQL support with calls to Ollama API

        It is extremely easy to use. `mo.sql()` uses a DuckDB interface when calling into a sqlite datbase.  This was great because it is super easy and has more features than a standard sqlite query has.  The challenge started coming in with the timestamps.  Ultimately, I am interested in analyzing timeseries data. DuckDB's native TIMESTAMP type allows straightforward datetime operations, while SQLite's lack of native support means datetimes are stored as text or real, requiring implicit conversions. I found the local LLMs struggled to recognize and translate SQLite's non-standard datetime storage, increasing the risk of errors in generating accurate SQL queries. This adds complexity to Text2SQL tasks.

        ### DuckDB-NSQL model with DuckDB database

        This led me down to replacing the sqlite database with a DuckDB database and pairing that with the [`DuckDB-NSQL` model](https://www.numbersstation.ai/duckdb-nsql-how-to-quack-in-sql/).  Up until this point, I was "fine tuning" Ollama with system prompts with many examples of text questions with the SQL answers. I found the more I mucked around, the worse the performance got.  

        How about using a model that was trained to translate text to DuckDB SQL? that's where th `DuckDB-nsql` model came in.  Although even in this case, examples that are in the documents capriciously returned different SQL results that worked roughly 75% of the time.

        #### Example Query 
        SQL Query: Get the longest trip in November 2022

        ##### First LLM answer

        SELECT list_slice(array_agg(trip_miles), -1, 1) FROM rideshare WHERE request_datetime BETWEEN '2022-11-01' AND '2022-11-30';

        Answer:
        []

        ##### Try Again

        SELECT MAX(trip_miles) FROM rideshare WHERE request_datetime BETWEEN '2022-11-01' AND '2022-11-30';

        Answer:
        59.4

        ### The code

        The code assumes Ollama is locally installed and the `DuckDB-nsql` model has been downloaded. The DuckDB python package is managed by marimo. I decided not to use any additional system prompting. 

        There is a python script, `create_db.py` that contains and loads the database discussed in the [DuckDB-NSQL: How to Quack in SQL article](https://www.numbersstation.ai/duckdb-nsql-how-to-quack-in-sql) article.  The user prompt is created in one of the cells and uses the schema.

        I am not that familiar with the content of the database other than the example queries that are found as chatbot prompts.  

        ## Conclusion
        In this exploration I learned: 

        - marimo has impressive easy SQL query support. However, when I moved to a DuckDB database and a small LLM that was fine tuned on DuckDB queries, it was better to use DuckDB's python apis.
        - I am a n00b when it comes to SQL. I am interested because I work with sensor data that is timeseries. I wanted to see how well I could use a small LLM to ask it questions in a natural language.

        - A feedback loop should be considered because there is a good chance a small LLM fine tuned on DuckDB SQL will get wrong SQL queries even if it has been trained on. I would like to explore more methods to improve results. However, I would need to research and discuss more with folks that are far smarter than I in this. Plus, doing so would be very time consuming. This is not my area of expertise, so unless there is more interest I'll just keep plugging away on....
        - DuckDB has additonal functionality that provides value over sqlite.
        - marimo can be a fun environment for exploration.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, ollama_sql_model):
    example_questions = [
        "Get passenger count, trip distance and fare amount from taxi table and order by all of them",
        "Get the longest trip in November 2022",
        "What's the longest trip in the dataset?",
        "Show summary statistics of rideshare table",
        "get violation_type field from other_violations json column in taxi table"
    ]
    chatbot = mo.ui.chat(
        ollama_sql_model,
        prompts= example_questions
    )
    mo.vstack([
        chatbot,
        mo.md("Try a sample prompt by clicking on the chat bubble.")
    ])
    return chatbot, example_questions


@app.cell
def _(DuckDBPyConnection):
    # see https://github.com/NumbersStationAI/DuckDB-NSQL/blob/main/examples/utils.py
    def get_schema(connection: DuckDBPyConnection) -> str:
        """Get schema from DuckDB connection."""
        tables = []
        information_schema = connection.execute(
            "SELECT * FROM information_schema.tables"
        ).fetchdf()
        for table_name in information_schema["table_name"].unique():
            table_df = connection.execute(
                f"SELECT * FROM information_schema.columns WHERE table_name = '{table_name}'"
            ).fetchdf()
            columns = []
            for _, row in table_df.iterrows():
                col_name = row["column_name"]
                col_dtype = row["data_type"]
                columns.append(f"{col_name} {col_dtype}")
            column_str = ",\n    ".join(columns)
            table = f"CREATE TABLE {table_name} (\n    {column_str}\n);"
            tables.append(table)
        return "\n\n".join(tables)
    return (get_schema,)


@app.cell
def _(duckdb):
    def validate_query(query, schemas):
        """Validates a SQL query against the given Tables in a schema.
        Raises:
            ParserException: If query cannot be parsed
            SyntaxException: If query has syntax errors
            BinderException: If query references invalid objects
            CatalogException: If schema objects cannot be created
            Exception: For other unexpected errors
        """
        with duckdb.connect('nyc.duckdb') as duckdb_conn:         
            # Execute the query to see if it is valid
            duckdb_conn.sql(query)

        return True  # Query is valid if we get here
    return (validate_query,)


@app.cell
def _(duckdb, get_schema):
    # Get the schema
    con = duckdb.connect('nyc.duckdb')
    schema = get_schema(con)
    return con, schema


@app.cell
def _(schema):

    def get_prompt(question: str) -> str:

        prompt = f"""Based on this DuckDB schema: {schema},
            Write the simplest DuckDB Query that will answer the user's question. If you do not understand how to make the simplest 
            DuckDB query or you cannot make the query, return null or None."

            Question: {question}
            SQL Query:"""
        return prompt

    return (get_prompt,)


@app.cell
def _(duckdb, get_prompt, mo, schema, validate_query):
    import ollama

    def ollama_sql_model(messages, config):
        question = messages[-1].content
        prompt = get_prompt(question)
        ollama_response = ollama.chat(model="duckdb-nsql", messages=[{"role": "user", "content": prompt}])
        sql_query = ollama_response["message"]["content"]
        try:
            validate_query(sql_query, schema)
            with duckdb.connect('nyc.duckdb') as duckdb_con:
                duckdb_answer = duckdb_con.sql(sql_query).fetchall()
                answer = duckdb_answer[0][0]
        except Exception as e:
            answer = f"ERROR: {str(e)}"
        results = response = mo.md(f"""
    ### {question}
    #### SQL Query: 

    {sql_query}

    #### Answer:

    {answer}
    """)
        return results
    return ollama, ollama_sql_model


if __name__ == "__main__":
    app.run()
