import marimo

__generated_with = "0.9.34"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import altair as alt
    import pandas as pd
    from langchain_community.utilities import SQLDatabase
    return SQLDatabase, alt, mo, pd


@app.cell
def __(SQLDatabase, pd):
    # Get Data from the SQLite store and then put it into a dataframe.
    db = SQLDatabase.from_uri("sqlite:///sniffer_data.db")
    df = pd.read_sql_query("""
        SELECT timestamp, temperature, humidity, carbon_dioxide, vpd
        FROM readings 
        ORDER BY timestamp
    """, db._engine)
    return db, df


@app.cell
def __(alt, df, mo):
    # All in one cell
    # Create checkboxes and plot function
    metrics = ["temperature", "humidity", "carbon_dioxide", "vpd"]

    def on_checkbox_change():
        to_plot = [m for m, cb in checkboxes.items() if cb.value]
        
        base = alt.Chart(df).encode(x='timestamp:T')
        layers = [
            base.mark_line().encode(
                y=alt.Y(f'{m}:Q', scale=alt.Scale(zero=False))
            )
            for m in to_plot
        ]
        return alt.layer(*layers) if layers else base

    checkboxes = {
        metric: mo.ui.checkbox(
            label=metric, 
            value=False,
            on_change=lambda _: on_checkbox_change()
        ) 
        for metric in metrics
    }

    # Display UI
    mo.hstack(list(checkboxes.values()))
    mo.ui.altair_chart(alt.Chart(df).encode(x='timestamp:T').properties(width=600, height=400))
    return checkboxes, metrics, on_checkbox_change


@app.cell(hide_code=True)
def __(checkboxes):
    def on_checkbox_change():
        to_plot = [m for m, cb in checkboxes.items() if cb.value]
        print(to_plot)
    return (on_checkbox_change,)


if __name__ == "__main__":
    app.run()
