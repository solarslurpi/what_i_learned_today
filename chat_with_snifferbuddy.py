import marimo

__generated_with = "0.9.32"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    # Initialize Marimo app
    app = mo.App()
    return (app,)


@app.cell
def __(app, mo):
    # Add a text input widget for user questions.
    @app.cell
    def user_input():
        return mo.ui.text(label="Enter your question:")
    return (user_input,)


@app.cell
def __(mo):
    text = mo.ui.text(placeholder="Search...", label="Filter")
    return (text,)


@app.cell
def __(mo, text):
    mo.hstack([text, mo.md(f"Has value: {text.value}")])
    return


@app.cell
def __(mo, respond_to_question):
    # Functions in cells are called using .run()
    # Two values are returned, outputs = dict of cell's outputs. defs = set of names defined in the cell.
    test_text = mo.ui.text(label="Enter your question:",on_change=respond_to_question)

    mo.hstack([test_text])
    return (test_text,)


@app.cell
def __():
    def respond_to_question(question):
        print(f"The question was:  {question}")
    return (respond_to_question,)


@app.cell
def __():
    def test_chat_model(messages,config):
        question = messages[-1].content
        response = "Hello World!"
        return response
    return (test_chat_model,)


@app.cell
def __(alt):
    data = [
        {'adtype': 'SEO', 'roi': 68.9},
        {'adtype': 'Email', 'roi': 56.7},
        {'adtype': 'PPC', 'roi': 52.4},
        {'adtype': 'PR', 'roi': 48.5},
        {'adtype': 'Direct Mail', 'roi': 37.4},
        {'adtype': 'OMB', 'roi': 19.9}
    ]

    # Create the bar chart
    chart = alt.Chart(alt.Data(values=data)).mark_bar().encode(
        x=alt.X('adtype:N', title='Ad Type'),
        y=alt.Y('roi:Q', title='ROI'),
        color='adtype:N'
    )
    return chart, data


@app.cell
def __(alt, mo):
    def bar_chart():

        # Your data
        data = [
            {'adtype': 'SEO', 'roi': 68.9},
            {'adtype': 'Email', 'roi': 56.7},
            {'adtype': 'PPC', 'roi': 52.4},
            {'adtype': 'PR', 'roi': 48.5},
            {'adtype': 'Direct Mail', 'roi': 37.4},
            {'adtype': 'OMB', 'roi': 19.9}
        ]
        
        # Create the chart
        chart = alt.Chart(alt.Data(values=data)).mark_bar().encode(
            x=alt.X('adtype:N', title='Ad Type'),
            y=alt.Y('roi:Q', title='ROI'),
            color='adtype:N'
        )
        
        # Return the chart (assuming this is inside a function)
        return mo.ui.altair_chart(chart, label="test")
    return (bar_chart,)


@app.cell
def __():
    import altair as alt
    return (alt,)


@app.cell
def __(bar_chart):
    bar_chart()
    return


@app.cell
def __(bar_chart, mo):
    def echo_model(messages, config):
        print(messages)
        # return f"Echo: {messages[-1].content} and all of messages{messages} and config {config}"
        return bar_chart()

    chat1 = mo.ui.chat(echo_model, prompts=["Hello", "How are you?"])
    chat1
    return chat1, echo_model


@app.cell
def __(mo, test_chat_model):
    chat = mo.ui.chat(test_chat_model)
    chat
    return (chat,)


if __name__ == "__main__":
    app.run()
