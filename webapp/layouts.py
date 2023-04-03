# webapp/layouts.py
import dash_bootstrap_components as dbc
from dash import html, dcc


class AppLayouts:
    def __init__(self, player_id_map, team_id_map):
        self.player_id_map = player_id_map
        self.team_id_map = team_id_map

    @staticmethod
    def _create_dropdown(dropdown_id, id_column, name_column, default=None):
        return dcc.Dropdown(
            id=dropdown_id,
            options=[
                {"label": name, "value": id}
                for id, name in zip(
                    id_column,
                    name_column,
                )
            ],
            value=default,
        )

    @staticmethod
    def _create_tab(dropdowns_list, graph_list):
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dropdowns_list),
                        dbc.Col(graph_list),
                    ]
                ),
            ]
        )

    def create_shot_chart_tab(self):
        dropdown_list = [
            self._create_dropdown(
                dropdown_id="player-dropdown",
                id_column=self.player_id_map["player_id"],
                name_column=self.player_id_map["player_name"],
                default=2544,
            ),
        ]
        graph_list = [
            dcc.Graph(
                id="shot-chart",
                style={
                    "width": "180vh",
                    "height": "90vh",
                },
            )
        ]
        return self._create_tab(dropdowns_list=dropdown_list, graph_list=graph_list)

    def create_team_fg_pct_tab(self):
        dropdown_list = [
            self._create_dropdown(
                dropdown_id="team-dropdown",
                id_column=self.team_id_map["team_id"],
                name_column=self.team_id_map["team_name"],
                default="1610612737",
            ),
        ]
        graph_list = [
            dcc.Graph(
                id="fg_pct_plot",
                style={
                    "width": "180vh",
                    "height": "90vh",
                },
            )
        ]
        return self._create_tab(dropdowns_list=dropdown_list, graph_list=graph_list)
