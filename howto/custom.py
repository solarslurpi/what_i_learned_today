# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.10.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # Custom chatbot

        This example shows how to make a custom chatbot: just supply a function that takes two arguments,
        `messages` and `config`, and returns the chatbot's response. This response can be any object; it
        doesn't have to be a string!
        """
    )
    return


@app.cell
def _(get_prompt, mo, ollama):
    def simple_echo_model(messages, config):
        """This chatbot echoes what the user says."""
        # messages is a list of chatbot messages
        question = messages[-1]
        prompt = get_prompt(question)
        print(f"Prompt: {prompt}")
        response = ollama.chat(model="sql_with_modelfile", messages=[{"role": "user", "content": prompt}])
        print(f"Response: {response.message}")
        # Each message has two fields:
        #   message.role, which may be "user", "assistant", or "system"
        #   message.content: the content of the message
        return response.content
        
    def my_model(messages, config):
        print(f"Config: {config}.\n\n Messages: {messages}")
        question = messages[-1].content
        prompt = get_prompt(question)
          # Query your own model or third-party models
        response = ollama.chat(model="sql_with_modelfile", messages=[{"role": "user", "content": prompt}])
        print(f"Response: {response.message}")
        return response.message
    chatbot = mo.ui.chat(
        simple_echo_model,
        prompts=["Hello", "How are you?"],
        show_configuration_controls=False
    )
    chatbot
    return chatbot, my_model, simple_echo_model


@app.cell
def _(mo):
    mo.md("""Access the chatbot's historical messages with `chatbot.value`.""")
    return


@app.cell
def _(chatbot):
    # chatbot.value is the list of chat messages
    chatbot.value
    return


if __name__ == "__main__":
    app.run()
