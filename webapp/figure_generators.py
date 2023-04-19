import plotly.graph_objs as go
from webapp.db_queries import load_shotchart_data, load_team_stats_per_game
import plotly.express as px


def draw_court(fig):
    # Add lines for the court
    court_shapes = [
        dict(
            type="rect",
            x0=0,
            x1=100,
            y0=0,
            y1=50,
            line=dict(color="black"),
            layer="below",
        ),
        dict(
            type="circle",
            x0=42.5,
            x1=57.5,
            y0=22.5,
            y1=27.5,
            line=dict(color="black"),
            layer="below",
        ),
        dict(
            type="rect",
            x0=18,
            x1=82,
            y0=0,
            y1=6,
            line=dict(color="black"),
            layer="below",
        ),
        dict(
            type="rect",
            x0=18,
            x1=82,
            y0=44,
            y1=50,
            line=dict(color="black"),
            layer="below",
        ),
    ]

    court_shapes = [
        {
            "x0": 0,
            "x1": 94,
            "y0": 0,
            "y1": 50,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 4,
            "x1": 4,
            "y0": 22,
            "y1": 28,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "line",
        },
        {
            "x0": 90,
            "x1": 90,
            "y0": 22,
            "y1": 28,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "line",
        },
        {
            "x0": 0,
            "x1": 19,
            "y0": 17,
            "y1": 33,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 0,
            "x1": 19,
            "y0": 19,
            "y1": 31,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 75,
            "x1": 94,
            "y0": 17,
            "y1": 33,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 75,
            "x1": 94,
            "y0": 19,
            "y1": 31,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 0,
            "x1": 14,
            "y0": 47,
            "y1": 47,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 0,
            "x1": 14,
            "y0": 3,
            "y1": 3,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 80,
            "x1": 94,
            "y0": 47,
            "y1": 47,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 80,
            "x1": 94,
            "y0": 3,
            "y1": 3,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 47,
            "x1": 47,
            "y0": 0,
            "y1": 50,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "rect",
        },
        {
            "x0": 6.1,
            "x1": 4.6,
            "y0": 25.75,
            "y1": 24.25,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "circle",
        },
        {
            "x0": 89.4,
            "x1": 87.9,
            "y0": 25.75,
            "y1": 24.25,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "circle",
        },
        {
            "x0": 25,
            "x1": 13,
            "y0": 31,
            "y1": 19,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "circle",
        },
        {
            "x0": 81,
            "x1": 69,
            "y0": 31,
            "y1": 19,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "circle",
        },
        {
            "x0": 53,
            "x1": 41,
            "y0": 31,
            "y1": 19,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "circle",
        },
        {
            "x0": 49,
            "x1": 45,
            "y0": 27,
            "y1": 23,
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "type": "circle",
        },
        {
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "path": "M 14,47 Q 45,25 14,3",
            "type": "path",
        },
        {
            "line": {"color": "rgba(0,0,0,1)", "width": 1},
            "path": "M 80,47 Q 49,25 80,3",
            "type": "path",
        },
    ]

    for shape in court_shapes:
        fig.add_shape(shape)

    return fig


def create_shot_chart(data):
    made_shots = data[data["SHOT_MADE_FLAG"] == "Made"]
    missed_shots = data[data["SHOT_MADE_FLAG"] == "Missed"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=made_shots["LOC_X"] * 0.94,
            y=made_shots["LOC_Y"] / 2,
            mode="markers",
            marker=dict(color="green", size=5),
            name="Made",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=missed_shots["LOC_X"] * 0.94,
            y=missed_shots["LOC_Y"] / 2,
            mode="markers",
            marker=dict(color="red", size=5),
            name="Missed",
        )
    )

    # Draw court
    fig = draw_court(fig)

    return fig


def create_shot_chart_figure(player_id):
    filtered_data = load_shotchart_data(player_id)
    shot_chart = create_shot_chart(filtered_data)
    return shot_chart


def create_team_stat_figure(team_id, stat, title=None):
    filtered_data = load_team_stats_per_game(team_id)
    fig = px.line(
        filtered_data,
        x="game_number",
        y=stat,
        title=title if title else stat,
    )
    return fig
