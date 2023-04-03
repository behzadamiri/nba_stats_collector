from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Float,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False, unique=True)
    abbreviation = Column(String, nullable=False, unique=True)
    nickname = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    year_founded = Column(Integer, nullable=False)


class GameHeaders(Base):
    __tablename__ = "game_headers"

    game_date_est = Column(DateTime, nullable=False)
    game_sequence = Column(Integer, nullable=False)
    game_id = Column(String, nullable=False, unique=True, primary_key=True)
    game_status_id = Column(Integer, nullable=False)
    game_status_text = Column(String, nullable=False)
    gamecode = Column(String, nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    visitor_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    season = Column(String, nullable=False)
    live_period = Column(Integer, nullable=False)
    live_pc_time = Column(String, nullable=True)
    natl_tv_broadcaster_abbreviation = Column(String, nullable=True)
    live_period_time_bcast = Column(String, nullable=True)
    wh_status = Column(Integer, nullable=False)

    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id])
    visitor_team = relationship("Team", foreign_keys=[visitor_team_id])
    line_scores = relationship("GameLineScore", back_populates="game")
    series_standings = relationship("GameSeriesStandings", back_populates="game")
    last_meeting = relationship("GameLastMeeting", back_populates="game")
    player_stats = relationship("PlayerStatsByGame", back_populates="game")
    team_stats = relationship("TeamStatsByGame", back_populates="game")
    team_starter_bench_stats = relationship(
        "TeamStarterBenchStatsByGame", back_populates="game"
    )


class GameLineScore(Base):
    __tablename__ = "game_line_scores"

    game_date_est = Column(DateTime, nullable=False)
    game_sequence = Column(Integer, nullable=False)
    game_id = Column(
        String, ForeignKey("game_headers.game_id"), nullable=False, primary_key=True
    )
    team_id = Column(Integer, nullable=False, primary_key=True)
    team_abbreviation = Column(String, nullable=False)
    team_city_name = Column(String, nullable=False)
    team_wins_losses = Column(String, nullable=False)
    pts_qtr1 = Column(Integer, nullable=False)
    pts_qtr2 = Column(Integer, nullable=False)
    pts_qtr3 = Column(Integer, nullable=False)
    pts_qtr4 = Column(Integer, nullable=False)
    pts_ot1 = Column(Integer, nullable=False)
    pts_ot2 = Column(Integer, nullable=False)
    pts_ot3 = Column(Integer, nullable=False)
    pts_ot4 = Column(Integer, nullable=False)
    pts_ot5 = Column(Integer, nullable=False)
    pts_ot6 = Column(Integer, nullable=False)
    pts_ot7 = Column(Integer, nullable=False)
    pts_ot8 = Column(Integer, nullable=False)
    pts_ot9 = Column(Integer, nullable=False)
    pts_ot10 = Column(Integer, nullable=False)
    pts = Column(Integer, nullable=False)
    fg_pct = Column(Float, nullable=False)
    ft_pct = Column(Float, nullable=False)
    fg3_pct = Column(Float, nullable=False)
    ast = Column(Integer, nullable=False)
    reb = Column(Integer, nullable=False)
    tov = Column(Integer, nullable=False)

    # Relationships
    game = relationship("GameHeaders", back_populates="line_scores")


class GameSeriesStandings(Base):
    __tablename__ = "game_series_standings"

    game_date_est = Column(DateTime, nullable=False)
    game_id = Column(
        String, ForeignKey("game_headers.game_id"), nullable=False, primary_key=True
    )
    home_team_id = Column(Integer, nullable=False)
    visitor_team_id = Column(Integer, nullable=False)
    home_team_wins = Column(Integer, nullable=False)
    home_team_losses = Column(Integer, nullable=False)
    series_leader = Column(String, nullable=False)

    # Relationships
    game = relationship("GameHeaders", back_populates="series_standings")


class GameLastMeeting(Base):
    __tablename__ = "game_last_meeting"

    last_game_date_est = Column(DateTime, nullable=False)
    game_id = Column(
        String, ForeignKey("game_headers.game_id"), nullable=False, primary_key=True
    )
    last_game_id = Column(String, nullable=False)
    last_game_home_team_id = Column(Integer, nullable=False)
    last_game_visitor_team_id = Column(Integer, nullable=False)
    last_game_home_team_points = Column(Integer, nullable=False)
    last_game_visitor_team_points = Column(Integer, nullable=False)

    # Relationships
    game = relationship("GameHeaders", back_populates="last_meeting")


class EastStandingByDate(Base):
    __tablename__ = "east_standing_by_date"

    standingsdate = Column(DateTime, nullable=False, primary_key=True)
    team_id = Column(Integer, nullable=False, primary_key=True)
    g = Column(Integer, nullable=False)
    w = Column(Integer, nullable=False)
    w = Column(Integer, nullable=False)
    w_pct = Column(Float, nullable=False)
    home_record = Column(String, nullable=False)
    road_record = Column(String, nullable=False)


class WestStandingByDate(Base):
    __tablename__ = "west_standing_by_date"

    standingsdate = Column(DateTime, nullable=False, primary_key=True)
    team_id = Column(Integer, nullable=False, primary_key=True)
    g = Column(Integer, nullable=False)
    w = Column(Integer, nullable=False)
    w = Column(Integer, nullable=False)
    w_pct = Column(Float, nullable=False)
    home_record = Column(String, nullable=False)
    road_record = Column(String, nullable=False)


class PlayerStatsByGame(Base):
    __tablename__ = "player_stats_by_game"

    game_id = Column(
        String, ForeignKey("game_headers.game_id"), nullable=False, primary_key=True
    )
    player_id = Column(Integer, nullable=False, primary_key=True)
    team_id = Column(Integer, nullable=False)
    player_name = Column(String, nullable=False)
    start_position = Column(String, nullable=False)
    comment = Column(String, nullable=False)
    min = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    to = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Float)

    # Relationships
    game = relationship("GameHeaders", back_populates="player_stats")


class TeamStatsByGame(Base):
    __tablename__ = "team_stats_by_game"

    game_id = Column(
        String, ForeignKey("game_headers.game_id"), nullable=False, primary_key=True
    )
    team_id = Column(Integer, nullable=False, primary_key=True)
    min = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    to = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Float)

    # Relationships
    game = relationship("GameHeaders", back_populates="team_stats")


class TeamStarterBenchStatsByGame(Base):
    __tablename__ = "team_starter_bench_stats_by_game"

    game_id = Column(
        String, ForeignKey("game_headers.game_id"), nullable=False, primary_key=True
    )
    team_id = Column(Integer, nullable=False, primary_key=True)
    starters_bench = Column(String, nullable=False, primary_key=True)
    min = Column(String)
    fgm = Column(Integer)
    fga = Column(Integer)
    fg_pct = Column(Float)
    fg3m = Column(Integer)
    fg3a = Column(Integer)
    fg3_pct = Column(Float)
    ftm = Column(Integer)
    fta = Column(Integer)
    ft_pct = Column(Float)
    oreb = Column(Integer)
    dreb = Column(Integer)
    reb = Column(Integer)
    ast = Column(Integer)
    stl = Column(Integer)
    blk = Column(Integer)
    to = Column(Integer)
    pf = Column(Integer)
    pts = Column(Integer)
    plus_minus = Column(Float)

    # Relationships
    game = relationship("GameHeaders", back_populates="team_starter_bench_stats")


class Period(Base):
    __tablename__ = "period"
    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(String)
    period = Column(Integer)
    periodType = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(String)
    orderNumber = Column(Integer)
    xLegacy = Column(Float)
    yLegacy = Column(Float)
    isFieldGoal = Column(Integer)
    side = Column(String)
    description = Column(String)
    personIdsFilter = Column(String)


class Jumpball(Base):
    __tablename__ = "jumpball"
    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(String)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    descriptor = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(String)
    orderNumber = Column(Integer)
    xLegacy = Column(Float)
    yLegacy = Column(Float)
    isFieldGoal = Column(Integer)
    jumpBallRecoveredName = Column(String)
    jumpBallRecoverdPersonId = Column(Integer)
    side = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)
    jumpBallWonPlayerName = Column(String)
    jumpBallWonPersonId = Column(Integer)
    description = Column(String)
    jumpBallLostPlayerName = Column(String)
    jumpBallLostPersonId = Column(Integer)


class Turnover(Base):
    __tablename__ = "turnover"
    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(String)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    area = Column(String)
    areaDetail = Column(String)
    side = Column(String)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(String)
    orderNumber = Column(Integer)
    xLegacy = Column(Float)
    yLegacy = Column(Float)
    isFieldGoal = Column(Integer)
    turnoverTotal = Column(Integer)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)
    stealPlayerName = Column(String)
    stealPersonId = Column(Integer)
    officialId = Column(Integer)
    descriptor = Column(String)


class Steal(Base):
    __tablename__ = "steal"
    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(String)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    area = Column(String)
    areaDetail = Column(String)
    side = Column(String)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(String)
    orderNumber = Column(Integer)
    subType = Column(String)
    xLegacy = Column(Float)
    yLegacy = Column(Float)
    isFieldGoal = Column(Boolean)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)

    stealPlayerName = Column(String)
    stealPersonId = Column(Integer)


class TwoPoint(Base):
    __tablename__ = "two_point"
    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(String)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    descriptor = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    area = Column(String)
    areaDetail = Column(String)
    side = Column(String)
    shotDistance = Column(Float)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(String)
    orderNumber = Column(Integer)
    xLegacy = Column(Float)
    yLegacy = Column(Float)
    isFieldGoal = Column(Boolean)
    shotResult = Column(String)
    pointsTotal = Column(Integer)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)

    assistPlayerNameInitial = Column(String)
    assistPersonId = Column(Integer)
    assistTotal = Column(Integer)
    blockPlayerName = Column(String)
    blockPersonId = Column(Integer)


class Foul(Base):
    __tablename__ = "foul"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    descriptor = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    area = Column(String)
    areaDetail = Column(String)
    side = Column(String)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    officialId = Column(Integer)
    orderNumber = Column(Integer)
    xLegacy = Column(Float)
    yLegacy = Column(Float)
    isFieldGoal = Column(Integer)
    foulPersonalTotal = Column(Integer)
    foulTechnicalTotal = Column(Integer)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)
    foulDrawnPlayerName = Column(String)
    foulDrawnPersonId = Column(Integer)


class FreeThrow(Base):
    __tablename__ = "freethrow"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    side = Column(String)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    orderNumber = Column(Integer)
    xLegacy = Column(Float)
    yLegacy = Column(Float)
    isFieldGoal = Column(Integer)
    shotResult = Column(String)
    pointsTotal = Column(Integer)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)
    descriptor = Column(String)


class ThreePoint(Base):
    __tablename__ = "threepoint"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(String)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    area = Column(String)
    areaDetail = Column(String)
    side = Column(String)
    shotDistance = Column(Float)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(String)
    orderNumber = Column(Integer)
    xLegacy = Column(Integer)
    yLegacy = Column(Integer)
    isFieldGoal = Column(Integer)
    shotResult = Column(String)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)
    descriptor = Column(String)
    pointsTotal = Column(Integer)
    assistPlayerNameInitial = Column(String)
    assistPersonId = Column(Integer)
    assistTotal = Column(Integer)
    blockPlayerName = Column(String)
    blockPersonId = Column(Integer)


class Rebound(Base):
    __tablename__ = "rebound"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(String)
    y = Column(String)
    area = Column(String)
    areaDetail = Column(String)
    side = Column(String)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    orderNumber = Column(Integer)
    xLegacy = Column(String)
    yLegacy = Column(String)
    isFieldGoal = Column(Integer)
    shotActionNumber = Column(Integer)
    reboundTotal = Column(Integer)
    reboundDefensiveTotal = Column(Integer)
    reboundOffensiveTotal = Column(Integer)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)


class Block(Base):
    __tablename__ = "block"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(String)
    y = Column(String)
    area = Column(String)
    areaDetail = Column(String)
    side = Column(String)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    orderNumber = Column(Integer)
    xLegacy = Column(String)
    yLegacy = Column(String)
    isFieldGoal = Column(Integer)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)


class Timeout(Base):
    __tablename__ = "timeout"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(String)
    y = Column(String)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    orderNumber = Column(Integer)
    xLegacy = Column(String)
    yLegacy = Column(String)
    isFieldGoal = Column(Integer)
    side = Column(String)
    description = Column(String)
    personIdsFilter = Column(String)


class Substitution(Base):
    __tablename__ = "substitution"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    orderNumber = Column(Integer)
    xLegacy = Column(Integer)
    yLegacy = Column(Integer)
    isFieldGoal = Column(Integer)
    side = Column(String)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)


class Violation(Base):
    __tablename__ = "violation"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    teamId = Column(Integer)
    teamTricode = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    officialId = Column(Integer)
    orderNumber = Column(Integer)
    xLegacy = Column(Integer)
    yLegacy = Column(Integer)
    isFieldGoal = Column(Integer)
    side = Column(String)
    description = Column(String)
    playerName = Column(String)
    playerNameI = Column(String)
    personIdsFilter = Column(String)


class Game(Base):
    __tablename__ = "game"

    game_id = Column(String, primary_key=True)
    actionNumber = Column(Integer, primary_key=True)
    clock = Column(String)
    timeActual = Column(DateTime)
    period = Column(Integer)
    periodType = Column(String)
    actionType = Column(String)
    subType = Column(String)
    qualifiers = Column(String)
    personId = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    possession = Column(Integer)
    scoreHome = Column(String)
    scoreAway = Column(String)
    edited = Column(DateTime)
    orderNumber = Column(Integer)
    xLegacy = Column(Integer)
    yLegacy = Column(Integer)
    isFieldGoal = Column(Integer)
    side = Column(String)
    description = Column(String)
    personIdsFilter = Column(String)
