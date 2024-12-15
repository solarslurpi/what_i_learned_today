# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "duckdb==1.1.1",
#     "marimo",
#     "ollama==0.4.4",
#     "pandas==2.2.3",
# ]
# ///

import marimo

__generated_with = "0.10.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""## 💽 Step 1: Connect to the sqlite db.""")
    return


@app.cell
def _(INFORMATION_SCHEMA, TABLES, mo):
    _df = mo.sql(
        f"""
        -- Boilerplate: detach the database so this cell works when you re-run it
        DETACH DATABASE IF EXISTS snifferdata;

        -- Attach the database; omit READ_ONLY if you want to write to the database.
        ATTACH '../data/sniffer_data.db' as snifferdata (TYPE SQLITE, READ_ONLY);

        -- This query lists all the tables in the database
        SELECT table_name FROM INFORMATION_SCHEMA.TABLES;
        """
    )
    return (snifferdata,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 🦙 Step 2: Connect to Ollama
        To connect to Ollama:

        - ✅ Define a function to create the prompt.
        - Define a function that is used by marimo when using a "custom" llm.
        - Define a function that is called when the llm is to perform a query.
        """
    )
    return


@app.cell
def _(mo, sqlite_master):
    def get_schema() -> str:
        schema_df = mo.sql("""
            SELECT sql 
            FROM memory.sqlite_master 
            WHERE type='table' and name='readings';
            """)
            # Extract the CREAE TABLE statement from the DataFrame
        schema_str = schema_df.iloc[0]['sql']
        return schema_str
    return (get_schema,)


@app.cell
def _():
    # Defing the prompt
    def get_prompt(question: str) -> str:
        schema_str = """CREATE TABLE snifferdata.readings(id BIGINT PRIMARY KEY, "timestamp" VARCHAR NOT NULL, light_on BIGINT, carbon_dioxide BIGINT, eco2 BIGINT, temperature DOUBLE, humidity DOUBLE, dew_point DOUBLE, vpd DOUBLE, temp_unit VARCHAR);"""
        prompt = f"""Based on the snifferdata.readings table schema that you have been given,
            Write a SQLite Query that will answer the user's question. 
            Write only the SQLite Query, no additional text. Review your answer to make sure it is correct. If you cannot make the SQL query from the question, say so.  Do not answer with SQL if the question cannot be answered with SQL.

            Question: {question}
            SQL Query:"""
        return prompt
    prompt = get_prompt("QUESTION")
    prompt
    return get_prompt, prompt


@app.cell
def _():
    import ollama
    return (ollama,)


@app.cell
def _(get_prompt, mo, ollama):

    def ollama_sql_model(messages, config):
        """This chatbot echoes what the user says."""
        # messages is a list of chatbot messages
        question = messages[-1]
        prompt = get_prompt(question)
        print(f"Question:\n {question}")
        response = ollama.chat(model="sql_with_mistral_nemo", messages=[{"role": "user", "content": prompt}])
        # Each message has two fields:
        #   message.role, which may be "user", "assistant", or "system"
        #   message.content: the content of the message
        print(f"SQL :\n {response.message.content}")
        answer = mo.sql(response.message.content, output=False)
        print(f"Answer:\n {answer}")
        value = answer.squeeze()
        print(f"Answer squeezed:\n {value}")
        # print(f"Response: {answer}")
        return value

    chatbot = mo.ui.chat(
        ollama_sql_model,
        prompts=["Hello", "How are you?"],
        show_configuration_controls=False
    )
    chatbot

    return chatbot, ollama_sql_model


if __name__ == "__main__":
    app.run()
