from src.models.season_stat_player_info import (SeasonStatPlayer, intreturns,
                                            passing, receiving, defense, fieldgoals, punts, rushing, extrapoints,
                                            kickreturns, puntreturns, conversions, kickoffs, fumbles, penalties)
from src.models.franchise_info import (FranchiseInfo)
from src.models.boxscore_info import (gamebs, quarter, overtime, BoxscoreInfo)
from src.models.season_stat_team_info import (SeasonStatTeam, intreturns, passing,
                                          receiving, defense, thirddown, fourthdown, goaltogo, redzone, kicks, fieldgoals, punts,
                                          rushing, kickreturns, puntreturns, record, conversions, kickoffs, fumbles, penalties,
                                          touchdowns, interceptions, firstdowns)
from src.models.season_stat_oppo_info import (SeasonStatOppo, intreturns, passing, receiving,
                                          defense, receiving, defense, thirddown, fourthdown, goaltogo, redzone, kicks, fieldgoals,
                                          punts, rushing, kickreturns, puntreturns, miscreturns, record,  conversions,
                                          kickoffs, fumbles, penalties, touchdowns, interceptions, firstdowns)
from src.models.seasons import SeasonInfo
from src.models.player_DCI_info import (
    player, prospect, primary, position, practice, injury, PlayerDCIinfo)
from src.models.changelog import ChangelogEntry
from src.models.team_info import (coach, rgb_color, team, team_color, TeamInfo)
from src.models.leaguehierarchy import (
    teams, division, conference, league, typeleague, LeagueHierarchy)
from src.models.game_info import (
    gamegame, awayteam, hometeam, broadcast, weather, wind, GameInfo)
from src.models.league_info import (
    game, season, changelog, leagueweek, LeagueInfo)
from src.models.venue_info import (venue1, location, VenueInfo)
from config import (Config, DevelopmentConfig, ProductionConfig)
from src.apimappings.Seasons import bp as bp_seasons
from src.apimappings.SeasonalStats import bp as bp_seasonal_stats
from src.apimappings.SeasonalStats import fetch_and_save_seasonal_stats
from src.apimappings.TeamProfile import bp as bp_team_profile
from src.apimappings.TeamProfile import fetch_and_save_team_profile
from src.apimappings.LeagueHierarchy import bp as bp_league_hierarchy
from src.apimappings.LeagueHierarchy import fetchandsaveLeagueHierarchy
from src.apimappings.current_season_schedule import bp as bp_current_season_schedule
from src.apimappings.current_season_schedule import fetch_and_save_weekly_schedule
from src.apimappings.PBP import bp as bp_pbp
from src.apimappings.PBP import process_games_for_year
from fastapi import FastAPI
from src.routers import seasons_router
from src.Database.rediscache import FootballData
data_cache = FootballData()
#NFLFEAPI IMPORTS
from src.nflfeapi.default import serve
from src.nflfeapi.getdata import get_data
from src.nflfeapi.getlivegames import live_games
from src.nflfeapi.gettop10 import structure_data_for_categories
from src.nflfeapi.getvenues import venues
from src.nflfeapi.populateseasons import populate_seasons
from src.nflfeapi.populateteams import populate_teams
from src.nflfeapi.support_api import submit_support_request


from fastapi import FastAPI
from dotenv import load_dotenv
import sys
import os
load_dotenv()
sys.path.append('/src')
sys.path.append('/src/models')

app = FastAPI()

app.include_router(seasons_router.router)
