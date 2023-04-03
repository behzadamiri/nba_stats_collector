import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from webapp.callbacks import AppCallbacks
from webapp.db_queries import load_player_id_map


player_id_map = load_player_id_map()

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
                            id="player-dropdown",
                            options=[
                                {"label": player, "value": id}
                                for id, player in zip(
                                    player_id_map["player_id"],
                                    player_id_map["player_name"],
                                )
                            ],
                            value=2544,  # Lebron James as default selection
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
app_callbacks = AppCallbacks(app)


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
