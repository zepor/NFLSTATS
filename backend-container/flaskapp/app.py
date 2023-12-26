#IMPORT MODELS
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
#APIMAPPING IMPORTS
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
#DATABASE IMPORTS
from src.database.connections import get_mongodb_connection, connect_to_redis
from src.database.rediscache import clear_cache, FootballData
#NFLFETCHQUERIES IMPORTS
from src.nflfetchqueries.fetchallseasonsplayerstatdetails import fetch_AllSeasonsPlayerStatDetails
from src.nflfetchqueries.fetchallseasonsteamstatdetails import fetch_allseasonsteamstatdetails
from src.nflfetchqueries.fetchdatafrommongodb import fetch_data_from_mongodb
from src.nflfetchqueries.fetchlivegames import fetch_live_games_data
from src.nflfetchqueries.getseasoninfoandselected import get_season_info_and_selected
from src.nflfetchqueries.getteams import get_or_generate_teams
from src.nflfetchqueries.getyearseasoncombinations import get_year_season_combinations
#SPORTSRADAR IMPORTS
#BPSCHEDULAR IMPORTS
#from src.bpscheduler.bpschedule import schedule
#NFLFEAPI IMPORTS
from src.nflfeapi.default import serve, bp_default
from src.nflfeapi.getdata import get_data, bp_get_data
from src.nflfeapi.getlivegames import live_games, bp_live_games
from src.nflfeapi.gettop10 import structure_data_for_categories, bp_get_top10
from src.nflfeapi.getvenues import venues, bp_venues
from src.nflfeapi.populateseasons import populate_seasons, bp_populate_seasons
from src.nflfeapi.populateteams import populate_teams, bp_populate_teams
from src.nflfeapi.support_api import submit_support_request, bp_support_api

#ROUTERS IMPORTS

#UTILS IMPORTS
from src.utils.auth import auth_blueprint, init_oauth
from src.utils.log import be_logger
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.notfound import init_app

from config import (Config, DevelopmentConfig, ProductionConfig)
from flask import Flask, jsonify, request, session, redirect, url_for, render_template, make_response
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from dotenv import load_dotenv
import logging
import json 
from os import environ as env
import sys
import os
import os.path
load_dotenv()
sys.path.append('/ssweb')
sys.path.append('/ssweb/src')
app = Flask(__name__)
init_oauth(app)
CORS(app, origins=['https://0.0.0.0', 'https://loveoffootball.io', 'http://localhost:3000'], resources={r"/api/*": {"origins": "*"}})
mongodb_client = get_mongodb_connection()
db = MongoEngine(app)
redis_primary_host = 'redis'  # The host used in the development environment
redis_fallback_host = 'redis-service'
redis_port = 6379  # Default Redis port
r = connect_to_redis(redis_primary_host, redis_fallback_host, redis_port)
data_cache = FootballData()
app.debug = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['JSON_SORT_KEYS'] = False

FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'true')
if FLASK_DEBUG.lower() == 'true':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)
app.register_blueprint(bp_current_season_schedule)
app.register_blueprint(bp_league_hierarchy)
app.register_blueprint(bp_team_profile)
app.register_blueprint(bp_seasons)
app.register_blueprint(bp_seasonal_stats)
app.register_blueprint(bp_pbp, url_prefix='/pbp')
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(bp_default)
app.register_blueprint(bp_get_data)
app.register_blueprint(bp_live_games)
app.register_blueprint(bp_get_top10)
app.register_blueprint(bp_venues)
app.register_blueprint(bp_populate_seasons)
app.register_blueprint(bp_populate_teams)
app.register_blueprint(bp_support_api)
app.secret_key = 'sessionkey'
app.jinja_env.cache = {}

logger = logging.getLogger(__name__)
FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
be_logger.info(f"Current FLASK_DEBUG: {FLASK_DEBUG}")
if __name__ == "__main__":
    clear_cache()
    if FLASK_DEBUG == 'true' and os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        data = data or FootballData()
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
    elif FLASK_DEBUG != 'true':
        # In production mode, just initialize as usual
        data = data or FootballData()
        app.run()
