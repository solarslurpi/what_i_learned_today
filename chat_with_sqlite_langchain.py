import marimo

__generated_with = "0.9.33"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        # Chat with sqlite using Langchain
        In a previous `what_i_learned_today` notebook, I explored using Anthropic's `mcp` protocol to extract data by sending a SQL query through `mcp`'s `RPC` mechanism.  In this notebook, I explore using an LLM to convert natural language into a SQL Query.  I am interested in doing the queries locally so I'll be using Ollama to load and run the LLMs.

        There are several Open Source ways to do this.

        - [Vanna.AI](vanna.ai) `Vanna` appears to be a high level abstraction.  I did not install it because it brought in more code than I wanted. I felt inevitably there would be too many layers of `Vanna` code to deal with.  There is [an interesting paper on the challenges of using an LLM to convert to SQL](https://vanna.ai/blog/ai-sql-accuracy.html).
        - [Langchain](https://python.langchain.com/docs/tutorials/sql_qa/) which I use in this notebook following the steps outlined in the YouTube video titled [Chat with MySQL Database with Python | LangChain Tutorial](https://youtu.be/9ccl1_Wu24Q).  Watch this video to follow along with the notebook.  The differences are Ollama is used instead of OpenAI and sqlite is used instead of MySQL.

        After getting this to work, I am getting intrigued by Vanna because it includes additional features such as plotting/graphing and coming up with questions based on the database. So I am going to write a notebook using Vanna.
        """
    )
    return


@app.cell
def __():
    import marimo as mo
    from langchain_core.prompts import ChatPromptTemplate
    return ChatPromptTemplate, mo


@app.cell
def __(ChatPromptTemplate):
    template = """Based on the table schema below: \n
    Schema: {schema}\n\nwrite a SQLite Query that will answer the user's question. Do not write any additional text. Write only the SQLite Query.
    \n
    Question: {question}\n
    SQL Query:>>>
    ----------------------------------
    Examples:

    Question: "What is the average temperature?"\n
    Answer: SELECT AVG(temperature) FROM readings;

    Question: "What is the average humidity for the last hour?"\n
    Answer: SELECT AVG(humidity) FROM readings WHERE timestamp > datetime('now', '-1 hour');

    Question: "Where is Milwalkie?"\n
    Answer: "I'm sorry, I cannot write a SQL Statement."

    Question: "What is the average cost of grapes?"
    Answer: "I'm sorry, there is no information about grapes in the database."

    Question: "Is the light on?"
    Answer: SELECT light_on FROM readings ORDER BY id DESC LIMIT 1;
    ------------------------------------------------------------------
    Reread the Examples to make sure queries like "Is the light on?" Can be done correctly. Also make sure to pay attention to what the data in the readings file contains.  Questions that do not fit the table should be answered with "I'm sorry, I cannot write a SQL Statement."
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt, template


@app.cell
def __():
    from langchain_community.utilities import SQLDatabase
    db = SQLDatabase.from_uri("sqlite:///sniffer_data.db")
    type(db)
    return SQLDatabase, db


@app.cell
def __(db):
    def get_schema(_):
        return db.get_table_info()
    return (get_schema,)


@app.cell
def __(get_schema):
    get_schema(None)
    return


@app.cell
def __():
    from langchain_ollama import ChatOllama
    llm = ChatOllama(model="sql_with_modelfile")
    return ChatOllama, llm


@app.cell
def __(get_schema, llm, prompt):
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    sql_chain = (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm.bind(stop=["\nSQL Result:"])
        | StrOutputParser()
     )
    return RunnablePassthrough, StrOutputParser, sql_chain


@app.cell
def __(sql_chain):
    sql_chain.invoke({"question": "Can i have pizzadfjakldjfasklfjsdlkfjd?"})
    return


if __name__ == "__main__":
    app.run()
