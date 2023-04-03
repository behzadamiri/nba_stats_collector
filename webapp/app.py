import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
from nba_stats_collector.config import DATABASE_URL
import plotly.figure_factory as ff
import plotly.graph_objs as go
from webapp.db_queries import load_shotchart_data
from webapp.components import draw_court


shotchart_data = load_shotchart_data()
# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = html.Div(
    [
        # Add dropdowns, sliders, or other UI components for filtering here
        # Example: a dropdown for selecting a player
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="team-dropdown",
                            options=[
                                {"label": player, "value": player}
                                for player in shotchart_data["PLAYER_NAME"].unique()
                            ],
                            value=None,
                            placeholder="Select a player",
                        )
                    ]
                )
            ]
        ),
        # Add a graph to display the data
        dbc.Row(
            [
                dbc.Col(
                    [
                        # dcc.Graph(id="fg_pct_plot"),
                        # dcc.Graph(id="fg3_pct_plot"),
                        # dcc.Graph(id="points_plot"),
                        # dcc.Graph(id="rebounds_plot"),
                        # dcc.Graph(id="assists_plot"),
                        # dcc.Graph(id="home_away_plot"),
                        # dcc.Graph(id="points_quarter_plot"),
                        # dcc.Graph(id="points_overtime_plot"),
                        # dcc.Graph(id="heatmap"),
                        dcc.Graph(
                            id="shot-chart", style={"width": "180vh", "height": "90vh"}
                        )
                    ]
                )
            ]
        ),
    ]
)


@app.callback(Output("fg_pct_plot", "figure"), [Input("team-dropdown", "value")])
def update_fg_pct_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(
        filtered_data,
        x="game_number",
        y="fg_pct",
        title="Field Goal Percentage by Game",
    )
    return fig


@app.callback(Output("fg3_pct_plot", "figure"), [Input("team-dropdown", "value")])
def update_fg3_pct_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(
        filtered_data,
        x="game_number",
        y="fg3_pct",
        title="Three-Point Field Goal Percentage by Game",
    )
    return fig


@app.callback(Output("ft_pct_plot", "figure"), [Input("team-dropdown", "value")])
def update_ft_pct_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(
        filtered_data,
        x="game_number",
        y="ft_pct",
        title="Free Throw Percentage by Game",
    )
    return fig


@app.callback(Output("points_plot", "figure"), [Input("team-dropdown", "value")])
def update_points_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(filtered_data, x="game_number", y="pts", title="Points per Game")
    return fig


@app.callback(Output("rebounds_plot", "figure"), [Input("team-dropdown", "value")])
def update_rebounds_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(filtered_data, x="game_number", y="reb", title="Rebounds per Game")
    return fig


@app.callback(Output("assists_plot", "figure"), [Input("team-dropdown", "value")])
def update_assists_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(filtered_data, x="game_number", y="ast", title="Assists per Game")
    return fig


@app.callback(Output("home_away_plot", "figure"), [Input("team-dropdown", "value")])
def update_home_away_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(
        filtered_data,
        x="game_number",
        y="pts",
        color="home_or_away",
        title="Home vs. Away Performance",
    )
    return fig


@app.callback(
    Output("points_quarter_plot", "figure"), [Input("team-dropdown", "value")]
)
def update_points_quarter_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(
        filtered_data,
        x="game_number",
        y=["pts_qtr1", "pts_qtr2", "pts_qtr3", "pts_qtr4"],
        title="Points per Quarter",
    )
    return fig


@app.callback(
    Output("points_overtime_plot", "figure"), [Input("team-dropdown", "value")]
)
def update_points_overtime_plot(selected_team):
    filtered_data = (
        data[data["team_name"] == selected_team] if selected_team else pd.DataFrame()
    )
    fig = px.line(
        filtered_data,
        x="game_number",
        y="pts_total_ot",
        title="Points Scored in Overtime",
    )
    return fig


@app.callback(Output("heatmap", "figure"), [Input("team-dropdown", "value")])
def update_heatmap(selected_team):
    filtered_data = data[data["team_name"] == selected_team] if selected_team else data

    if not filtered_data.empty:
        # Calculate the mean values for various statistics
        mean_values = filtered_data[
            [
                "fg_pct",
                "fg3_pct",
                "ft_pct",
                "reb",
                "ast",
                "stl",
                "blk",
                "to",
                "pf",
                "pts",
            ]
        ].mean()

        # Create an annotated heatmap using Plotly's figure_factory
        fig = ff.create_annotated_heatmap(
            z=[mean_values],
            x=list(range(1, 11, 1)),
            y=list(data["team_name"].unique()),
            colorscale="Viridis",
            font_colors=["white"],
            annotation_text=[["{:.2f}".format(val) for val in mean_values]],
            showscale=True,
        )

        # Update the heatmap's title and axis labels
        fig.update_layout(
            title="Team Performance Overview (Averages)",
            xaxis_title="Statistic",
            yaxis_title="Team",
            yaxis=dict(autorange="reversed"),
        )

    else:
        fig = {}

    return fig


@app.callback(Output("bar-plot", "figure"), [Input("team-dropdown", "value")])
def update_bar_plot(selected_team):
    if selected_team:
        # Group the data by team and calculate the average points per game
        avg_pts_per_game = data.groupby("team_name")["pts"].mean().reset_index()

        # Create a bar plot using Plotly Express
        fig = px.bar(
            avg_pts_per_game,
            x="team_name",
            y="pts",
            title="Average Points Scored per Game by Team",
            labels={"team_name": "Team", "pts": "Average Points"},
        )

        # Highlight the selected team
        fig.update_traces(
            marker_color=[
                "red" if team == selected_team else "blue"
                for team in avg_pts_per_game["team_name"]
            ]
        )

        # Customize the plot's appearance
        fig.update_layout(
            showlegend=False,
            xaxis=dict(type="category", title="Team"),
            yaxis=dict(title="Average Points per Game"),
            plot_bgcolor="white",
        )

    else:
        fig = {}

    return fig


def create_shot_chart(data, title="Shot Chart"):
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


@app.callback(Output("shot-chart", "figure"), [Input("team-dropdown", "value")])
def update_shot_chart(selected_team):
    filtered_data = (
        shotchart_data[shotchart_data["PLAYER_NAME"] == selected_team]
        if selected_team
        else pd.DataFrame()
    )
    shot_chart = create_shot_chart(filtered_data, title="Shot Chart")
    return shot_chart


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
