from dash.dependencies import Input, Output

# Import other necessary modules and functions
from webapp.db_queries import load_shotchart_data, load_team_stats_per_game
from webapp.components import create_shot_chart

import plotly.express as px


class AppCallbacks:
    def __init__(self, app):
        self.app = app
        self.register_callbacks()

    def register_callbacks(self):
        self.shot_chart_callback()
        self.fg_pct_callback()
        # ... other callback registrations

    def shot_chart_callback(self):
        @self.app.callback(
            Output("shot-chart", "figure"), [Input("player-dropdown", "value")]
        )
        def _update_shot_chart(player_id):
            filtered_data = load_shotchart_data(player_id)
            shot_chart = create_shot_chart(filtered_data)
            return shot_chart

    def fg_pct_callback(self):
        @self.app.callback(
            Output("fg_pct_plot", "figure"), [Input("team-dropdown", "value")]
        )
        def update_fg_pct_plot(team_id):
            filtered_data = load_team_stats_per_game(team_id)
            fig = px.line(
                filtered_data,
                x="game_number",
                y="fg_pct",
                title="Field Goal Percentage by Game",
            )
            return fig

    # ... other callbacks
