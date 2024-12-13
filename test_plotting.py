import marimo

__generated_with = "0.9.34"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __():
    import altair as alt
    import pandas as pd
    from langchain_community.utilities import SQLDatabase
    return SQLDatabase, alt, pd


@app.cell
def __(SQLDatabase, pd):
    # Get Data from the SQLite store and then put it into a dataframe.
    db = SQLDatabase.from_uri("sqlite:///sniffer_data.db")
    df = pd.read_sql_query("""
        SELECT timestamp, temperature, humidity, carbon_dioxide, vpd
        FROM readings 
        ORDER BY timestamp
    """, db._engine)
    # First, let's see what columns we actually have
    print("DataFrame columns:", df.columns.tolist())
    return db, df


@app.cell
def __(mo, plot_variables):
    metrics = ["temperature", "humidity", "carbon_dioxide", "vpd"]
    checkboxes = {
        metric: mo.ui.checkbox(
            label=metric, 
            value=False,
            on_change=lambda _: on_checkbox_change()
        ) 
        for metric in metrics
    }
    def on_checkbox_change():
        to_plot = [m for m, cb in checkboxes.items() if cb.value]
        plot_variables(to_plot)
    # Display UI elements
    mo.hstack(list(checkboxes.values()))
    return checkboxes, metrics, on_checkbox_change


@app.cell
def __():
    def plot_variables(to_plot):
        print(f"in plot variables: {to_plot}")
    return (plot_variables,)


@app.cell
def __(alt, df, mo):
    # First, verify our data
    print("DataFrame head:")
    print(df.head())
    print("\nDataFrame info:")
    print(df.info())

    # Simple interactive chart with just timestamps and temperature
    chart = mo.ui.altair_chart(
        alt.Chart(df).mark_circle().encode(
            x='timestamp:T',
            y='temperature:Q'
        ).properties(
            width=600,
            height=400
        )
    )


    return (chart,)


@app.cell
def __(chart):
    # Display chart and show selected data
    chart
    return


if __name__ == "__main__":
    app.run()
