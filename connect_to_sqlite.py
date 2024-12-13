# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "duckdb==1.1.1",
#     "marimo",
#     "pandas==2.2.3",
#     "requests==2.32.3",
# ]
# ///

import marimo

__generated_with = "0.9.34"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        r"""
        # Connect to SQLite

        You can use marimo's SQL cells to read from and write to SQLite databases.

        The first step is to attach a SQLite database. We attach to a sample database in a read-only mode below.

        For advanced usage, see [duckdb's documentation](https://duckdb.org/docs/extensions/sqlite).
        """
    )
    return


@app.cell(hide_code=True)
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(INFORMATION_SCHEMA, TABLES, mo):
    _df = mo.sql(
        f"""
        -- Boilerplate: detach the database so this cell works when you re-run it
        DETACH DATABASE IF EXISTS snifferdata;

        -- Attach the database; omit READ_ONLY if you want to write to the database.
        ATTACH 'sniffer_data.db' as snifferdata (TYPE SQLITE, READ_ONLY);

        -- This query lists all the tables in the Chinook database
        SELECT table_name FROM INFORMATION_SCHEMA.TABLES;

        """
    )
    return (snifferdata,)


@app.cell
def __(mo, readings, snifferdata):
    df = mo.sql("SELECT * from snifferdata.readings ")
    return (df,)


@app.cell
def __(df):
    # Transform data to long format for just temperature and humidity
    df_long = df.melt(
        id_vars=['timestamp'],
        value_vars=['temperature', 'humidity'],
        var_name='metric',
        value_name='value'
    )
    return (df_long,)


@app.cell
def __(df, mo):
    import altair as alt
    # Create temperature chart
    temp_chart = mo.ui.altair_chart(
        alt.Chart(df).mark_line(color='red').encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('temperature:Q', 
                   title='Temperature (°C)',
                   scale=alt.Scale(zero=False))
        ).properties(
            width=300,  # Made smaller to fit in horizontal layout
            height=300
        )
    )
    # Create humidity chart
    humidity_chart = mo.ui.altair_chart(
        alt.Chart(df).mark_line(color='blue').encode(
            x=alt.X('timestamp:T', title='Time'),
            y=alt.Y('humidity:Q', 
                   title='Humidity (%)',
                   scale=alt.Scale(zero=False))
        ).properties(
            width=300,
            height=300
        )
    )
    # Create horizontal layout
    layout = mo.hstack([
        temp_chart,humidity_chart
        # We'll add more charts here later
    ])
        
    layout
    return alt, humidity_chart, layout, temp_chart


if __name__ == "__main__":
    app.run()
