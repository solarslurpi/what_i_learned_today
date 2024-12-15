import marimo

__generated_with = "0.10.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from llama_index.llms.ollama import Ollama
    return (Ollama,)


@app.cell
def _():
    import sys
    print(sys.executable)
    return (sys,)


if __name__ == "__main__":
    app.run()
