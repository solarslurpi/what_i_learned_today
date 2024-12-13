import marimo

__generated_with = "0.9.34"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # Explore Plotting with Altair
        I was browsing the marimo examples looking at what plotting packages are commonly used. There are several. The one that was new to me and looked intriguing is Altair. The goal of this notebook is to get a fundamental understanding of Altair.
        """
    )
    return


@app.cell
def __():
    # Cell 1: Imports
    import altair as alt
    import pandas as pd
    import numpy as np
    return alt, np, pd


@app.cell
def __(alt, mo):
    from vega_datasets import data
    # Load some data
    cars = data.cars()

    # Create an Altair chart
    _chart = alt.Chart(cars).mark_point().encode(
        x='Horsepower',
        y='Miles_per_Gallon',
        color='Origin',
    ).properties(height=300)

    # Make it reactive ⚡
    chart1 = mo.ui.altair_chart(_chart)
    return cars, chart1, data


@app.cell
def __(chart1):
    chart1
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Panda Dataframes
        Panda dataframes are used as the input format.
        """
    )
    return


@app.cell
def __(pd):
    data_pd = pd.DataFrame({
        'x': range(10),
        'y': [2, 5, 3, 8, 6, 10, 4, 7, 9, 8]
    })
    return (data_pd,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # Chart
        The chart() method is used to make a plot.
        e.g.: 
        - alt.Chart(data)  -> start with the data
        - mark_line()      -> choose the plot type.
        - encode()         -> map the data to the x and y axis.

        The example below explores the property settings for the different plot features.  We are able to make the plot as ugly as possible!!!
        """
    )
    return


@app.cell
def __(alt, data, mo):
    _chart = alt.Chart(data).mark_line(
        point=True,
        color='green',         # Line color
        strokeWidth=2          # Optional: make line thicker
    ).encode(
        x=alt.X('x', axis=alt.Axis(
            labelColor='#666666',      # Axis label color
            titleColor='white',      # Axis title color
            gridColor='black',       # Grid line color
            domainColor='purple'      # Axis line color
        )),
        y=alt.Y('y', axis=alt.Axis(
            labelColor='#666666',      # Axis label color
            titleColor='yellow',      # Axis title color
            gridColor='blue',       # Grid line color
            domainColor='purple'      # Axis line color
        )),
        tooltip=[
            alt.Tooltip('x', title='Position'),
            alt.Tooltip('y', title='Value', format='.2f'),
            # Add any other columns you want to show
        ]
    ).properties(
        width=500,
        height=300,
        title='Simple Line Plot'
    ).configure_title(
        color='yellow',              # Title color
        fontSize=20                   # Optional: make title larger
    ).configure_view(
        fillOpacity=.8,
        stroke='green',
        strokeWidth=5,               # Remove border
        fill='purple')

    chart = mo.ui.altair_chart(_chart)
    return (chart,)


@app.cell
def __(chart):
    chart
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Explore a Time Series Chart
        This chart includes the pan and zoom feature.
        """
    )
    return


@app.cell
def __(alt, np, pd):
    # Create sample time series data with minutes and seconds
    dates = pd.date_range(
        start='2023-01-01 00:00:00',
        end='2023-12-31 23:59:59',
        freq='h'
    )
    data_timeseries = pd.DataFrame({
        'date': dates,
        'value': np.random.randn(len(dates)).cumsum()
    })

    # Line chart with points on hover
    chart_timeseries = alt.Chart(data_timeseries).mark_line(
        color='steelblue',
        strokeWidth=2,
        point=True  # Add points that appear on hover
    ).encode(
        x=alt.X(
            'date:T',
            axis=alt.Axis(
                title='Date',
                format='%Y-%m-%d %H:%M:%S',
                labelAngle=-45
            )
        ),
        y=alt.Y(
            'value:Q',
            axis=alt.Axis(
                title='Value'
            )
        ),
        tooltip=[
            alt.Tooltip('date:T', format='%Y-%m-%d %H:%M:%S'),
            alt.Tooltip('value:Q', format='.2f')
        ]
    ).properties(
        width=700,
        height=400,
        title='Interactive Time Series Plot'
    ).interactive()

    chart_timeseries
    return chart_timeseries, data_timeseries, dates


@app.cell
def __(mo):
    mo.md(
        r"""
        # Explore Time Series 2
        This chart features interval selection.
        """
    )
    return


@app.cell
def __(alt, np, pd):
    # Create sample time series data with minutes and seconds
    dates_timeseries2 = pd.date_range(
        start='2023-01-01 00:00:00',
        end='2023-12-31 23:59:59',
        freq='h'
    )
    data_timeseries2 = pd.DataFrame({
        'date': dates_timeseries2,
        'value': np.random.randn(len(dates_timeseries2)).cumsum()
    })

    # Create the selection
    brush = alt.selection_interval(encodings=['x'])

    # Main detail view
    detail = alt.Chart(data_timeseries2).mark_line(
        color='steelblue',
        strokeWidth=2
    ).encode(
        x=alt.X('date:T',
            scale=alt.Scale(domain=brush),  # This makes the brush actually work
            axis=alt.Axis(title='Date', format='%Y-%m-%d %H:%M:%S', labelAngle=-45)
        ),
        y=alt.Y('value:Q', axis=alt.Axis(title='Value')),
        tooltip=[
            alt.Tooltip('date:T', format='%Y-%m-%d %H:%M:%S'),
            alt.Tooltip('value:Q', format='.2f')
        ]
    ).properties(
        width=700,
        height=300,
        title='Time Series Detail View'
    )

    # Overview with brush selection
    overview = alt.Chart(data_timeseries2).mark_area(
        color='lightblue'
    ).encode(
        x='date:T',
        y='value:Q'
    ).properties(
        width=700,
        height=60
    ).add_params(brush)

    # Combine charts
    chart_timeseries2 = alt.vconcat(detail, overview)

    chart_timeseries2
    return (
        brush,
        chart_timeseries2,
        data_timeseries2,
        dates_timeseries2,
        detail,
        overview,
    )


@app.cell
def __():
    return


@app.cell
def __(mo, np, pd):
    # Create data and UI elements
    dates_timeseries3 = pd.date_range(
        start='2023-01-01 00:00:00',
        end='2023-12-31 23:59:59',
        freq='h'
    )
    data_timeseries3 = pd.DataFrame({
        'date': dates_timeseries3,
        'value': np.random.randn(len(dates_timeseries3)).cumsum()
    })

    # Create time resolution selector
    resolution_ts3 = mo.ui.dropdown(
        options=['Year', 'Month', 'Day', 'Hour'],
        value='Day',
        label="Time Resolution"
    )
    return data_timeseries3, dates_timeseries3, resolution_ts3


@app.cell
def __(alt, data_timeseries3, mo, pd, resolution_ts3):
    # Create visualization
    brush_ts3 = alt.selection_interval(encodings=['x'])

    # Main detail view
    detail_ts3 = alt.Chart(data_timeseries3).mark_line(
        color='steelblue',
        strokeWidth=2
    ).encode(
        x=alt.X('date:T',
            scale=alt.Scale(domain=brush_ts3),
            axis=alt.Axis(
                title='Date', 
                format={'Year': '%Y', 'Month': '%b %Y', 
                       'Day': '%Y-%m-%d', 'Hour': '%Y-%m-%d %H:%M'}[resolution_ts3.value],
                labelAngle=-45
            )
        ),
        y=alt.Y('value:Q', axis=alt.Axis(title='Value')),
        tooltip=[
            alt.Tooltip('date:T', format='%Y-%m-%d %H:%M:%S'),
            alt.Tooltip('value:Q', format='.2f')
        ]
    ).properties(
        width=700,
        height=300,
        title='Time Series Detail View'
    )

    # Create statistics DataFrame
    stats_df = pd.DataFrame({
        'Metric': ['Mean', 'Max', 'Min', 'Std Dev'],
        'Value': [
            f"{data_timeseries3['value'].mean():.2f}",
            f"{data_timeseries3['value'].max():.2f}",
            f"{data_timeseries3['value'].min():.2f}",
            f"{data_timeseries3['value'].std():.2f}"
        ]
    })

    # Combine everything and display
    mo.hstack([
        mo.vstack([
            mo.md("### Controls"),
            resolution_ts3,
            mo.md("### Statistics"),
            mo.md(stats_df.to_markdown())  # Convert DataFrame to markdown table
        ]),
        alt.vconcat(
            detail_ts3,
            alt.Chart(data_timeseries3).mark_area(
                color='lightblue',
                opacity=0.5
            ).encode(
                x=alt.X('date:T', axis=alt.Axis(format='%b %Y', title='')),
                y=alt.Y('value:Q', axis=alt.Axis(title=''))
            ).properties(
                width=700,
                height=60
            ).add_params(brush_ts3)
        )
    ])
    return brush_ts3, detail_ts3, stats_df


@app.cell
def __():
    return


@app.cell
def __(mo, np, pd):
    # Create sample temperature data with 20-second intervals
    dates_temp = pd.date_range(
        start='2023-01-01 00:00:00',
        end='2023-12-31 23:59:59',
        freq='20s'  # 20-second intervals
    )
    data_temp = pd.DataFrame({
        'date': dates_temp,
        'temperature': 20 + 5 * np.sin(np.pi * len(dates_temp) / (24 * 365)) + 
                      2 * np.sin(np.pi * len(dates_temp) / (60 * 30)) +  
                      0.5 * np.random.randn(len(dates_temp))
    })

    # Create start and end date pickers
    start_date = mo.ui.date(
        value="2023-01-01",
        label="Start Date"
    )

    end_date = mo.ui.date(
        value="2023-01-01",  # Default to single day
        label="End Date"
    )
    return data_temp, dates_temp, end_date, start_date


@app.cell
def __(alt, data_temp, end_date, mo, pd, start_date):
    # Convert picker dates to pandas datetime
    selected_start = pd.to_datetime(start_date.value)
    selected_end = pd.to_datetime(end_date.value) + pd.Timedelta(days=1)

    # Filter data for the selected date range
    filtered_data = data_temp[
        (data_temp['date'] >= selected_start) & 
        (data_temp['date'] < selected_end)
    ].copy()

    # Add formatted datetime strings for tooltips
    filtered_data['datetime_str'] = filtered_data['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    filtered_data['temp_str'] = filtered_data['temperature'].round(2).astype(str) + '°C'

    # Determine if we're looking at a single day
    is_single_day = (selected_end - selected_start).days <= 1

    # Create the chart
    base_ts4 = alt.Chart(filtered_data).encode(
        x=alt.X('date:T',
            axis=alt.Axis(
                title='Time',
                format='%H:%M' if is_single_day else '%Y-%m-%d %H:%M',
                labelAngle=-45,
                tickCount=24 if is_single_day else 'day'
            )
        ),
        y=alt.Y(
            'temperature:Q',
            axis=alt.Axis(title='Temperature (°C)')
        )
    )

    # Main line
    line_ts4 = base_ts4.mark_line(color='orangered', strokeWidth=1).encode(
        tooltip=['datetime_str:N', 'temp_str:N']
    )

    # Points for hover
    nearest_ts4 = alt.selection_point(nearest=True, on='mouseover', fields=['date'])
    points_ts4 = line_ts4.mark_point().encode(
        opacity=alt.condition(nearest_ts4, alt.value(1), alt.value(0))
    ).add_params(nearest_ts4)

    # Average temperature text
    avg_temp_ts4 = base_ts4.transform_aggregate(
        avg_temp='mean(temperature)'
    ).transform_calculate(
        text="'Avg: ' + format(datum.avg_temp, '.2f') + '°C'"
    ).mark_text(
        align='right',
        baseline='top',
        dx=-5,
        dy=5,
        fontSize=12
    ).encode(
        x=alt.value(780),
        y=alt.value(0),
        text='text:N'
    )

    # Combine all layers
    chart_ts4 = (line_ts4 + points_ts4 + avg_temp_ts4).properties(
        width=800,
        height=400,
        title=f'Temperature Reading for {selected_start.strftime("%Y-%m-%d")}'
    ).interactive()

    # Display
    mo.hstack([
        mo.vstack([
            mo.md("### Date Range"),
            start_date,
            end_date
        ]),
        chart_ts4
    ])
    return (
        avg_temp_ts4,
        base_ts4,
        chart_ts4,
        filtered_data,
        is_single_day,
        line_ts4,
        nearest_ts4,
        points_ts4,
        selected_end,
        selected_start,
    )


if __name__ == "__main__":
    app.run()
