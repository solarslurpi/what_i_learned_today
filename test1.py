import marimo

__generated_with = "0.9.34"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import altair as alt
    from vega_datasets import data

    source = data.movies.url

    heatmap = alt.Chart(source).mark_rect().encode(
        alt.X('IMDB_Rating:Q').bin(),
        alt.Y('Rotten_Tomatoes_Rating:Q').bin(),
        alt.Color('count()').scale(scheme='greenblue')
    )

    points = alt.Chart(source).mark_circle(
        color='black',
        size=5,
    ).encode(
        x='IMDB_Rating:Q',
        y='Rotten_Tomatoes_Rating:Q',
    )

    heatmap + points
    return alt, data, heatmap, mo, points, source


if __name__ == "__main__":
    app.run()
