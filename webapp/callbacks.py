from dash.dependencies import Input, Output

from webapp.figure_generators import create_shot_chart_figure, create_fg_pct_figure


class AppCallbacks:
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.register_callbacks()

    @staticmethod
    def _generate_inputs(tab_id, dropdowns):
        return [
            Input(f"{tab_id}_{dropdown}-dropdown", "value") for dropdown in dropdowns
        ]

    def register_callbacks(self):
        for tab_config in self.config:
            tab_id = tab_config["tab_name"].lower().replace(" ", "_")
            for graph_name in tab_config["graphs"]:
                graph_id = f"{tab_id}_{graph_name}"
                match graph_name:
                    case "shot_chart":
                        self.shot_chart_callback(
                            tab_id, graph_id, tab_config["dropdowns"]
                        )
                    case "team_fg_pct":
                        self.fg_pct_callback(tab_id, graph_id, tab_config["dropdowns"])

    def shot_chart_callback(self, tab_id, graph_id, dropdowns):
        @self.app.callback(
            Output(graph_id, "figure"),
            self._generate_inputs(tab_id, dropdowns),
        )
        def _update_shot_chart(player_id):
            return create_shot_chart_figure(player_id)

    def fg_pct_callback(self, tab_id, graph_id, dropdowns):
        @self.app.callback(
            Output(graph_id, "figure"),
            self._generate_inputs(tab_id, dropdowns),
        )
        def _update_fg_pct_plot(team_id):
            return create_fg_pct_figure(team_id)

    # ... other callbacks
