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


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def __(INFORMATION_SCHEMA, TABLES, mo, readings, snifferdata):
    # Load the sqlite database that has the readings table.
    mo.sql(
            f"""
            -- Boilerplate: detach the database so this cell works when you re-run it
            DETACH DATABASE IF EXISTS snifferdata;

            -- Attach the database; omit READ_ONLY if you want to write to the database.
            ATTACH 'sniffer_data.db' as snifferdata (TYPE SQLITE, READ_ONLY);

            -- This query lists all the tables in the Chinook database
            SELECT table_name FROM INFORMATION_SCHEMA.TABLES;
            """
        )
    df = mo.sql("""
        SELECT 
            CAST(timestamp AS TIMESTAMP) as timestamp,
            temperature,
            humidity,
            vpd,
            carbon_dioxide
        FROM snifferdata.readings
    """)
    return df, snifferdata


@app.cell
def __():
    import altair as alt
    return (alt,)


@app.cell
def __():
    humidity_color = "#8ecae6"
    temperature_color = '#0a9396'
    vpd_color = "#219ebc"
    co2_color = "#ffb703"


    return co2_color, humidity_color, temperature_color, vpd_color


@app.cell(hide_code=True)
def __(alt, df, humidity_color, mo, temperature_color, vpd_color):
    # Base chart with common x-axis
    base = alt.Chart(df).encode(
        x='timestamp:T'
    ).properties(
        width=600,
        height=200
    )

    # Left axis for temperature and humidity
    left = alt.layer(
        base.mark_point(color=temperature_color).encode(
            y=alt.Y('temperature:Q', 
                    scale=alt.Scale(domain=[20, 100]),
                    axis=alt.Axis(title='Temperature (°F) / Humidity (%)'))),
        base.mark_point(color=humidity_color).encode(
            y=alt.Y('humidity:Q', scale=alt.Scale(domain=[0, 100])))
    )

    # Right axis for VPD
    right = base.mark_point(color=vpd_color).encode(
        y=alt.Y('vpd:Q', 
                axis=alt.Axis(
                    values=[0, 0.5, 1.0, 1.5, 2.0],  # Explicit tick values
                    format='.1f'  # One decimal place
                ),
                title='VPD (kPa)')
    )

    # Combine with proper scale resolution
    brush = alt.selection_interval()
    _chart = alt.layer(left, right).resolve_scale(
        y='independent'
    ).add_params(brush)

    chart_ref = mo.ui.altair_chart(_chart)
    return base, brush, chart_ref, left, right


@app.cell(hide_code=True)
def __(chart_ref):
    chart_ref
    return


@app.cell(hide_code=True)
def __(chart_ref, df, mo):

    # Check if DataFrame has data - use df when chart_ref.value is empty
    dataframe = df if chart_ref.value.empty else chart_ref.value

    temp_avg = dataframe['temperature'].mean()
    humid_avg = dataframe['humidity'].mean()
    vpd_avg = dataframe['vpd'].mean()
    co2_avg = dataframe['carbon_dioxide'].mean()

    grid = mo.hstack([
        mo.stat(
            label="Total", 
            value=f"{len(df)}", 
            bordered=True,
        ),
        mo.stat(
            label="Selected", 
            value=f"{len(chart_ref.value)}", 
            bordered=True
        ),
        mo.stat(
            label=f"{dataframe['timestamp'].min().strftime('%Y-%m-%d')}", 
            value=f" {dataframe['timestamp'].min().strftime('%H:%M:%S')}", 
            bordered=True
        ),
        mo.stat(
            label=f"{dataframe['timestamp'].max().strftime('%Y-%m-%d')}", 
            value=f"{dataframe['timestamp'].max().strftime('%H:%M:%S')}", 
            bordered=True
        ),
        mo.stat(label="Temperature", value=f"{temp_avg:.1f}°C", bordered=True),
        mo.stat(label="Humidity", value=f"{humid_avg:.1f}%", bordered=True),
        mo.stat(label="VPD", value=f"{vpd_avg:.2f} kPa", bordered=True),
        mo.stat(label="CO₂", value=f"{co2_avg:.0f} ppm", bordered=True),
    ], justify="start")
    grid
    return co2_avg, dataframe, grid, humid_avg, temp_avg, vpd_avg


@app.cell(hide_code=True)
def __(
    alt,
    chart_ref,
    co2_color,
    humidity_color,
    mo,
    temperature_color,
    vpd_color,
):

    mo.stop(chart_ref.value.empty, "No data selected")

    # First reshape the data with unique name
    metrics_df = chart_ref.value.melt(
        id_vars=['timestamp'],
        value_vars=['temperature', 'humidity', 'vpd', 'carbon_dioxide'],
        var_name='metric',
        value_name='value'
    )

    # Temperature graph with unique names
    temperature_chart = mo.ui.altair_chart(
        alt.Chart(metrics_df.query("metric == 'temperature'")).mark_point(color=temperature_color).encode(
            x=alt.X('timestamp:T', axis=alt.Axis(labelColor=temperature_color, titleColor=temperature_color)),
            y=alt.Y('value:Q', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(labelColor=temperature_color, titleColor=temperature_color))
        ).properties(
            title=alt.TitleParams(
                text='Temperature',  # The title text
                color=temperature_color,    # Title color
                fontSize=20         # Optional: title font size
            ),
            width=300, height=200)
    )

    # Humidity graph with unique names
    humidity_chart = mo.ui.altair_chart(
        alt.Chart(metrics_df.query("metric == 'humidity'")).mark_point(color=humidity_color).encode(
            x=alt.X('timestamp:T', axis=alt.Axis(labelColor=humidity_color, titleColor=humidity_color)),
            y=alt.Y('value:Q', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(labelColor=humidity_color, titleColor=humidity_color))
        ).properties(
            title=alt.TitleParams(
                text='Humidity',  # The title text
                color=humidity_color,    # Title color
                fontSize=20         # Optional: title font size
            ),
            width=300, height=200)
    )

    # VPD graph with unique names
    vpd_metrics_chart = mo.ui.altair_chart(
        alt.Chart(metrics_df.query("metric == 'vpd'")).mark_point(color=vpd_color).encode(
            x=alt.X('timestamp:T', axis=alt.Axis(labelColor=vpd_color, titleColor=vpd_color)),

            y=alt.Y('value:Q', scale=alt.Scale(domain=[0, 2]), axis=alt.Axis(labelColor=vpd_color, titleColor=vpd_color))
        ).properties(
                title=alt.TitleParams(
                text='vpd',  # The title text
                color=vpd_color,    # Title color
                fontSize=20         # Optional: title font size
            ),
            width=300, height=200)
    )

    # CO2 graph with unique names
    co2_metrics_chart = mo.ui.altair_chart(
        alt.Chart(metrics_df.query("metric == 'carbon_dioxide'")).mark_point(color=co2_color).encode(
            x=alt.X('timestamp:T', axis=alt.Axis(labelColor=co2_color, titleColor=co2_color)),
            y=alt.Y('value:Q', scale=alt.Scale(domain=[0, 2000]), axis=alt.Axis(labelColor=co2_color, titleColor=co2_color))
        ).properties(          
                title=alt.TitleParams(
                text='CO2',  # The title text
                color=co2_color,    # Title color
                fontSize=20         # Optional: title font size
            ),
            width=300, height=200)
    )


    # Create 2x2 grid using marimo's layout
    charts = mo.hstack([
        mo.vstack([temperature_chart, vpd_metrics_chart]),
        mo.vstack([humidity_chart, co2_metrics_chart])
    ],justify="start")

    charts
    return (
        charts,
        co2_metrics_chart,
        humidity_chart,
        metrics_df,
        temperature_chart,
        vpd_metrics_chart,
    )


if __name__ == "__main__":
    app.run()
