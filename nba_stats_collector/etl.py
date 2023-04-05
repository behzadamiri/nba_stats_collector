import logging
from sqlalchemy.orm import sessionmaker
from nba_stats_collector.models import (
    Team,
    GameHeaders,
    GameLineScore,
    GameLastMeeting,
    GameSeriesStandings,
    WestStandingByDate,
    EastStandingByDate,
    PlayerStatsByGame,
    TeamStarterBenchStatsByGame,
    TeamStatsByGame,
    Period,
    Jumpball,
    ThreePoint,
    Timeout,
    Turnover,
    TwoPoint,
    FreeThrow,
    Steal,
    Substitution,
    Foul,
    Rebound,
    Block,
    Violation,
    Game,
    Base,
)
from nba_stats_collector.config import DATABASE_URL
from nba_stats_collector.nba_api_client import (
    NBAGames,
    NBAGameStats,
    NBAPlayByPlay,
    get_team_data,
)
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NBAStatsETL:
    playbyplay_data_config = {
        "period": (Period, "get_period"),
        "jumpball": (Jumpball, "get_jumpball"),
        "turnover": (Turnover, "get_turnover"),
        "steal": (Steal, "get_steal"),
        "2pt": (TwoPoint, "get_2pt"),
        "foul": (Foul, "get_foul"),
        "freethrow": (FreeThrow, "get_freethrow"),
        "3pt": (ThreePoint, "get_3pt"),
        "rebound": (Rebound, "get_rebound"),
        "block": (Block, "get_block"),
        "timeout": (Timeout, "get_timeout"),
        "substitution": (Substitution, "get_substitution"),
        "violation": (Violation, "get_violation"),
        "game": (Game, "get_game"),
    }
    single_game_data_config = {
        "player_stats": (PlayerStatsByGame, "get_player_stats"),
        "team_stats": (TeamStatsByGame, "get_team_stats"),
        "starter_bench_stats": (TeamStarterBenchStatsByGame, "get_starter_bench_stats"),
    }

    game_day_data_config = {
        "headers": (GameHeaders, "get_game_header"),
        "line_score": (GameLineScore, "get_game_line_score"),
        "last_meeting": (GameLastMeeting, "get_last_meeting"),
        "series_standing": (GameSeriesStandings, "get_series_standings"),
        "east_standing": (EastStandingByDate, "get_east_standing"),
        "west_standing": (WestStandingByDate, "get_west_standing"),
    }

    def __init__(self, day_offset=-1):
        self.day_offset = day_offset
        self.games_stats = NBAGames(day_offset=self.day_offset)
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def commit_data(self, data_list, table_model):
        session = self.Session()
        team_columns = [column.name for column in table_model.__table__.columns]
        counter = 0
        for data in data_list:
            filtered_data = {
                key: value for key, value in data.items() if key in team_columns
            }
            team = table_model(**filtered_data)
            try:
                session.add(team)
                session.commit()
                counter += 1

            except Exception as e:
                logger.error(
                    f"Failed to commit data to {table_model.__tablename__} table. Data: {data}. Error: {e}"
                )
                continue

        logger.info(
            f"Successfully commited {counter} data points to {table_model.__tablename__} table."
        )

    def store_team_data(self):
        table_model = Team
        data_list = get_team_data()
        self.commit_data(data_list, table_model)

    def store_game_day_data(self, keyword):
        table_model, data_method_name = self.game_day_data_config[keyword]
        data_method = getattr(self.games_stats, data_method_name)
        data_list = data_method()
        self.commit_data(data_list, table_model)

    def store_single_game_data(self):
        for game_id in self.games_stats.get_games_list():
            ngs = NBAGameStats(game_id)

            for _, (
                table_model,
                data_method_name,
            ) in self.single_game_data_config.items():
                data_method = getattr(ngs, data_method_name)
                data_list = data_method()
                self.commit_data(data_list, table_model)

    def store_playbyplay_data(self):
        for game_id in self.games_stats.get_games_list():
            pbp = NBAPlayByPlay(game_id)

            for _, (
                table_model,
                data_method_name,
            ) in self.playbyplay_data_config.items():
                data_method = getattr(pbp, data_method_name)
                data_list = data_method()
                self.commit_data(data_list, table_model)
