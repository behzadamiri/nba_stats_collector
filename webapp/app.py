import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from webapp.callbacks import AppCallbacks
from webapp.db_queries import load_player_id_map, load_team_id_map
from webapp.layouts import AppLayouts

player_id_map = load_player_id_map()
team_id_map = load_team_id_map()

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Instantiate AppLayouts
app_layouts = AppLayouts(player_id_map, team_id_map)

# Define the app layout
app.layout = html.Div(
    [
        # Add a tabs component to display multiple graphs
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Shot Chart",
                    children=app_layouts.create_shot_chart_tab(),
                ),
                dcc.Tab(
                    label="Team FG % per Game",
                    children=app_layouts.create_team_fg_pct_tab(),
                ),
                # Add more tabs with different graphs as needed
            ]
        ),
    ]
)

app_callbacks = AppCallbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
