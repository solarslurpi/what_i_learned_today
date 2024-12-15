import marimo

__generated_with = "0.9.34"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import ollama
    return mo, ollama


@app.cell
def __(mo):
    def connect_to_sqlite(db_path: str="sniffer_data.db"):
        mo.sql(
            f"""
            -- Boilerplate: detach the database so this cell works when you re-run it
            DETACH DATABASE IF EXISTS snifferdata;

            -- Attach the database; omit READ_ONLY if you want to write to the database.
            """
        )
    return (connect_to_sqlite,)


app._unparsable_cell(
    r"""
    def get_schema(db_path: str=\"sniffer_data.db\") -> str:
        
    """,
    name="__"
)


@app.cell
def __():
    def prompt(question: str, schema: str):
        prompt = f"""Based on the table schema below: \n
            Schema: {schema}\n
            Write a SQLite Query that will answer the user's question. 
            Write only the SQLite Query, no additional text.
            
            Question: {question}
            SQL Query:"""
        return prompt
    return (prompt,)


app._unparsable_cell(
    r"""
    def query_llm(prompt, config):
        # Use ollama to query the model.
    """,
    name="__"
)


@app.cell
def __(find_relevant_docs, messages, mo, query_llm):
    def my_model(message, config):
        question = messages[-1].content
        docs = find_relevant_docs(question)
        context = "\n".join(docs)
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        # Query your own model or third-party models
        response = query_llm(prompt, config)
        return response

    mo.ui.chat(my_model)
    return (my_model,)


if __name__ == "__main__":
    app.run()
