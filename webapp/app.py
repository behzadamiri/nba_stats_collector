import dash
from dash import html
import dash_bootstrap_components as dbc
from webapp.callbacks import AppCallbacks
from webapp.layouts import AppLayouts


config_path = "webapp/app_config.json"

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Instantiate AppLayouts
app_layouts = AppLayouts(config_path)

# Define the app layout
app.layout = html.Div([app_layouts.create_tabs()])

app_callbacks = AppCallbacks(app, app_layouts.config)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
