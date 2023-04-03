import pandas as pd
from sqlalchemy import create_engine
from nba_stats_collector.config import DATABASE_URL

# Connect to your nba_stats database
engine = create_engine(DATABASE_URL)


# Load data from the database into a pandas DataFrame
def load_player_id_map():
    with engine.connect() as connection:
        query = """
        select distinct player_id, player_name
        from public.player_stats_by_game
        """
        data = pd.read_sql(query, connection)
    return data


# Load data from the database into a pandas DataFrame
def load_team_stats_per_game():
    with engine.connect() as connection:
        query = """
        with all_teams_in_games as
        (
            select game_date_est,
                game_id,
                home_team_id as team_id,
                'home' as home_or_away
            from public.game_headers
            union
            select game_date_est,
                game_id,
                visitor_team_id as team_id,
                'away' as home_or_away
            from public.game_headers
        )
        select all_teams_in_games.game_date_est,
            all_teams_in_games.game_id,
            all_teams_in_games.team_id,
            all_teams_in_games.home_or_away,
            row_number() over(partition by all_teams_in_games.team_id order by all_teams_in_games.game_date_est) as game_number,
            sum(case when all_teams_in_games.home_or_away = 'home' then 1 else 0 end) over(partition by all_teams_in_games.team_id order by all_teams_in_games.game_date_est rows between unbounded preceding and current row) as home_games_count,
            sum(case when all_teams_in_games.home_or_away = 'away' then 1 else 0 end) over(partition by all_teams_in_games.team_id order by all_teams_in_games.game_date_est rows between unbounded preceding and current row) as away_games_count,
            tsbg.fgm,
            tsbg.fga,
            tsbg.fg_pct,
            tsbg.fg3m,
            tsbg.fg3a,
            tsbg.fg3_pct,
            tsbg.ftm,
            tsbg.fta,
            tsbg.ft_pct,
            tsbg.oreb,
            tsbg.dreb,
            tsbg.reb,
            tsbg.ast,
            tsbg.stl,
            tsbg.blk,
            tsbg.to,
            tsbg.pf,
            tsbg.pts,
            tsbg.plus_minus,
            gls.team_abbreviation as team_name,
            gls.pts_qtr1,
            gls.pts_qtr2,
            gls.pts_qtr3,
            gls.pts_qtr4,
            gls.pts_ot1+gls.pts_ot2+gls.pts_ot3+gls.pts_ot4+gls.pts_ot5+gls.pts_ot6+gls.pts_ot7+gls.pts_ot8+gls.pts_ot9+gls.pts_ot10 as pts_total_ot
        from all_teams_in_games
        join public.team_stats_by_game tsbg
        on tsbg.game_id = all_teams_in_games.game_id and
        tsbg.team_id = all_teams_in_games.team_id
        join public.game_line_scores gls
        on gls.game_id = all_teams_in_games.game_id and
        gls.team_id = all_teams_in_games.team_id
        """
        data = pd.read_sql(query, connection)
    return data


def load_shotchart_data(player_id):
    with engine.connect() as connection:
        query = """
        with get_all_shots as
        (
        select "personId" as player_id,
                "x" as "LOC_X", 
                "y" as "LOC_Y", 
                "shotResult"  as "SHOT_MADE_FLAG"
        from public.two_point
        union 
        select "personId" as player_id,
                "x" as "LOC_X", 
                "y" as "LOC_Y", 
                "shotResult"  as "SHOT_MADE_FLAG"
        from public.threepoint
        )
        , player_id_map as
        (
        select distinct player_id, player_name
        from public.player_stats_by_game
        )
        select get_all_shots.*,
            player_id_map.player_name
        from get_all_shots
        join player_id_map
        on player_id_map.player_id = get_all_shots.player_id
        where get_all_shots.player_id = {}
        """.format(
            player_id
        )
        data = pd.read_sql(query, connection)
    return data
