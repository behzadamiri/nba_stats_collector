import pytest
from nba_stats_collector.nba_api_client import (
    NBAGames,
    NBAGameStats,
    NBAPlayByPlay,
    get_team_data,
)


@pytest.fixture
def nba_games():
    return NBAGames()


@pytest.fixture
def nba_game_stats():
    # Replace 'game_id' with a valid game ID from the NBA
    game_id = "0022201130"
    return NBAGameStats(game_id)


@pytest.fixture
def nba_play_by_play():
    # Replace 'game_id' with a valid game ID from the NBA
    game_id = "0022201130"
    return NBAPlayByPlay(game_id)


def test_get_game_header(nba_games):
    result = nba_games.get_game_header()
    assert isinstance(result, list)


def test_get_games_list(nba_games):
    result = nba_games.get_games_list()
    assert isinstance(result, list)


def test_get_player_stats(nba_game_stats):
    result = nba_game_stats.get_player_stats()
    assert isinstance(result, list)


def test_get_play_by_play(nba_play_by_play):
    result = nba_play_by_play.get_play_by_play()
    assert isinstance(result, list)


def test_get_team_data():
    result = get_team_data()
    assert isinstance(result, list)
