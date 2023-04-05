# webapp/layouts.py
import json
import dash_bootstrap_components as dbc
from dash import html, dcc
from webapp.db_queries import load_player_id_map, load_team_id_map

dropdown_map = {
    "player": {"id_map": load_player_id_map(), "default": 2544},
    "team": {"id_map": load_team_id_map(), "default": "1610612737"},
}


class AppLayouts:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)

    def _load_config(self, config_path):
        with open(config_path, "r") as file:
            config = json.load(file)
        return config

    def create_tabs(self):
        tabs = [Tab(tab_config).create_tab() for tab_config in self.config]
        return dcc.Tabs(tabs)


class Tab:
    def __init__(self, config):
        self.tab_name = config["tab_name"]
        self.dropdown_list = config["dropdowns"]
        self.graph_list = config["graphs"]
        self.tab_id = self.tab_name.lower().replace(" ", "_")

    def create_tab(self):
        dropdowns = self._create_dropdowns()
        graphs = self._create_graphs()
        tab_content = html.Div([dbc.Row(dropdowns), dbc.Row(graphs)])
        return dcc.Tab(label=self.tab_name, children=tab_content, id=self.tab_id)

    def _create_dropdowns(self):
        dropdowns = [
            dbc.Col(
                Dropdown(
                    self._generate_dropdown_id(name),
                    dropdown_map[name]["id_map"],
                    dropdown_map[name]["default"],
                ).create()
            )
            for name in self.dropdown_list
        ]
        return dropdowns

    def _create_graphs(self):
        graphs = [
            dbc.Col(Figure(f"{self.tab_id}_{name}").create())
            for name in self.graph_list
        ]
        return graphs

    def _generate_dropdown_id(self, dropdown_name):
        return f"{self.tab_id}_{dropdown_name}-dropdown"


class Dropdown:
    def __init__(self, dropdown_id, id_map, default=None):
        self.dropdown_id = dropdown_id
        self.id_map = id_map
        self.default = default

    def create(self):
        return dcc.Dropdown(
            id=self.dropdown_id,
            options=[
                {"label": name, "value": id}
                for id, name in zip(self.id_map["id"], self.id_map["name"])
            ],
            value=self.default,
        )


class Figure:
    def __init__(self, figure_id):
        self.figure_id = figure_id

    def create(self):
        return dcc.Graph(
            id=self.figure_id,
            style={"width": "180vh", "height": "90vh"},
        )
