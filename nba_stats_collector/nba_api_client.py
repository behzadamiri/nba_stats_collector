from nba_api.stats.endpoints import scoreboard, boxscoretraditionalv2
from nba_api.live.nba.endpoints import playbyplay
from nba_api.stats.static import teams


class StatsEndpoints:
    def process_endpoint_data(self, index):
        result_data = self.endpoint_result_dict[index]

        games_data_list = []
        for game in result_data["rowSet"]:
            single_game_data = {}
            for stat, value in zip(result_data["headers"], game):
                single_game_data[stat.lower()] = value
            games_data_list.append(single_game_data)

        return games_data_list


class NBAGames(StatsEndpoints):
    def __init__(self, day_offset=0):
        self.endpoint_result_dict = scoreboard.Scoreboard(
            day_offset=day_offset
        ).get_dict()["resultSets"]

    def get_game_header(self):
        return self.process_endpoint_data(0)

    def get_game_line_score(self):
        return self.process_endpoint_data(1)

    def get_series_standings(self):
        return self.process_endpoint_data(2)

    def get_last_meeting(self):
        return self.process_endpoint_data(3)

    def get_east_standing(self):
        return self.process_endpoint_data(4)

    def get_west_standing(self):
        return self.process_endpoint_data(5)

    def get_games_list(self):
        return [game["game_id"] for game in self.get_game_header()]


class NBAGameStats(StatsEndpoints):
    def __init__(self, game_id):
        self.endpoint_result_dict = boxscoretraditionalv2.BoxScoreTraditionalV2(
            game_id=game_id
        ).get_dict()["resultSets"]

    def get_player_stats(self):
        return self.process_endpoint_data(0)

    def get_team_stats(self):
        return self.process_endpoint_data(1)

    def get_starter_bench_stats(self):
        return self.process_endpoint_data(2)


class NBAPlayByPlay:
    def __init__(self, game_id):
        self.game_id = game_id
        self.actions = playbyplay.PlayByPlay(game_id=self.game_id).get_dict()["game"][
            "actions"
        ]
        self.get_play_by_play()

    def get_play_by_play(self):
        self.game_actions = []

        for action in self.actions:
            mod_action = {"game_id": self.game_id}
            mod_action.update(action)
            self.game_actions.append(mod_action)

    def get_specific_action(self, action_type):
        return [play for play in self.game_actions if play["actionType"] == action_type]

    def get_period(self):
        return self.get_specific_action("period")

    def get_jumpball(self):
        return self.get_specific_action("jumpball")

    def get_turnover(self):
        return self.get_specific_action("turnover")

    def get_steal(self):
        return self.get_specific_action("steal")

    def get_2pt(self):
        return self.get_specific_action("2pt")

    def get_foul(self):
        return self.get_specific_action("2pt")

    def get_freethrow(self):
        return self.get_specific_action("freethrow")

    def get_3pt(self):
        return self.get_specific_action("3pt")

    def get_rebound(self):
        return self.get_specific_action("rebound")

    def get_block(self):
        return self.get_specific_action("block")

    def get_timeout(self):
        return self.get_specific_action("timeout")

    def get_substitution(self):
        return self.get_specific_action("substitution")

    def get_violation(self):
        return self.get_specific_action("violation")

    def get_game(self):
        return self.get_specific_action("game")


def get_team_data():
    return teams.get_teams()
