from models.season_stat_player_info import (SeasonStatPlayer, intreturns,
                                            passing, receiving, defense, fieldgoals, punts, rushing, extrapoints,
                                            kickreturns, puntreturns, conversions, kickoffs, fumbles, penalties)
from models.franchise_info import (FranchiseInfo)
from models.boxscore_info import (gamebs, quarter, overtime, BoxscoreInfo)
from models.season_stat_team_info import (SeasonStatTeam, intreturns, passing,
                                          receiving, defense, thirddown, fourthdown, goaltogo, redzone, kicks, fieldgoals, punts,
                                          rushing, kickreturns, puntreturns, record, conversions, kickoffs, fumbles, penalties,
                                          touchdowns, interceptions, firstdowns)
from models.season_stat_oppo_info import (SeasonStatOppo, intreturns, passing, receiving,
                                          defense, receiving, defense, thirddown, fourthdown, goaltogo, redzone, kicks, fieldgoals,
                                          punts, rushing, kickreturns, puntreturns, miscreturns, record,  conversions,
                                          kickoffs, fumbles, penalties, touchdowns, interceptions, firstdowns)
from models.seasons import (SeasonInfo)
from models.player_DCI_info import (
    player, prospect, primary, position, practice, injury, PlayerDCIinfo)
from models.changelog import ChangelogEntry
from models.team_info import (coach, rgb_color, team, team_color, TeamInfo)
from models.leaguehierarchy import (
    teams, division, conference, league, typeleague, LeagueHierarchy)
from models.game_info import (
    gamegame, awayteam, hometeam, broadcast, weather, wind, GameInfo)
from models.league_info import (
    game, season, changelog, leagueweek, LeagueInfo)
from models.venue_info import (venue1, location, VenueInfo)
from config import (Config, DevelopmentConfig, ProductionConfig)
from apimappings.Seasons import bp as bp_seasons
from apimappings.SeasonalStats import bp as bp_seasonal_stats
from apimappings.SeasonalStats import fetch_and_save_seasonal_stats
from apimappings.TeamProfile import bp as bp_team_profile
from apimappings.TeamProfile import fetch_and_save_team_profile
from apimappings.LeagueHierarchy import bp as bp_league_hierarchy
from apimappings.LeagueHierarchy import fetchandsaveLeagueHierarchy
from apimappings.current_season_schedule import bp as bp_current_season_schedule
from apimappings.current_season_schedule import fetch_and_save_weekly_schedule
from dotenv import load_dotenv
from mongoengine import connect
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from waitress import serve
from apscheduler.schedulers.background import BackgroundScheduler
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask import Flask, Blueprint, render_template, request, jsonify, make_response, session
from bson import Binary
from operator import itemgetter
from json import JSONEncoder
from itertools import groupby
import redis
import time
import json
import base64
from dateutil.parser import parse
from datetime import datetime, timedelta
import pymongo
import requests
from logging.handlers import RotatingFileHandler
import logging
import sys
import os
from dotenv import load_dotenv  # Import this if you're using load_dotenv
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
load_dotenv()  # Load environment variables from .env file
LPATH = os.getenv('LPATH')
# Append paths to sys.path
sys.path.append(os.path.join(LPATH, '.venv', 'lib', 'site-packages'))
sys.path.append(LPATH)
sys.path.append('/src')
sys.path.append('/src/models')
# from models import AllSeasonsTeamStatDetails, SeasonInfo, SeasonStatTeam
# from src.apimappings.SeasonalStats import bp as bp_seasonal_stats
# Setup MongoDB testing azure provider
mongodb_service_name = os.getenv('MONGODB_SERVICE_NAME', 'localhost')
mongodb_url = os.getenv(
    'MONGODB_URL', f"mongodb://{mongodb_service_name}:27017/current_season")
client = MongoClient(mongodb_url, connectTimeoutMS=30000, socketTimeoutMS=None)
try:
    client.admin.command('ismaster')
except ConnectionFailure:
    logging.error("MongoDB server not available")
# Initialize Flask
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'templates', 'static'))
# Initialize logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log_dir = './logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'app.log')
# Set up the 'backend-logger' to log to both the file and the console
be_logger = logging.getLogger('backend-logger')
be_logger.setLevel(logging.DEBUG)  # Capture all logs at DEBUG level and above
# File handler
file_handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
be_logger.addHandler(file_handler)
# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
be_logger.addHandler(console_handler)
# Initialize CORS
CORS(app, origins='https://198.168.0.116')
# Initialize scheduler
scheduler = BackgroundScheduler()
# Initialize MongoDB settings
app.config['MONGODB_SETTINGS'] = {
    'db': 'current_season',  # Replace with your database name
    'host': mongodb_url
}
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# MongoDB and logging settings
db = MongoEngine(app)
# Determine the environment from the FLASK_ENV variable
flask_env = os.environ.get('FLASK_ENV', 'development')
# Use different configurations based on the environment
if flask_env == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)
# JSON sorting settings
app.config['JSON_SORT_KEYS'] = False
# Register your blueprints
app.register_blueprint(bp_current_season_schedule)
app.register_blueprint(bp_league_hierarchy)
app.register_blueprint(bp_team_profile)
app.register_blueprint(bp_seasons)
app.register_blueprint(bp_seasonal_stats)
# Set Flask secret key
app.secret_key = 'sessionkey'
# Error Handling


@app.errorhandler(Exception)
def handle_exception(e):
    be_logger.exception("An error occurred: %s", e)
    return str(e), 500


def log_and_catch_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            be_logger.error(f"Error in {func.__name__}: {e}")
            raise Exception(f"Error in {func.__name__}: {e}")
    return func_wrapper


class FootballData:
    def __init__(self):
        self.all_season_team_stat_details_cache = None
        self.current_year_season_cache = None
        self.year_season_combinations_cache = None
        self.teams_dict_cache = {}
        self.selected_teams_stats_cache = {}
        self.team_top_10_data_cache = {}
        self.selected_year = None
        self.selected_season_type = None
        self.selected_team = None
        self.selected_teams = {}

    @staticmethod
    @log_and_catch_exceptions
    def get_AllSeasonsTeamStatDetails():
        return [
            {
                '$lookup': {
                    'from': 'TeamInfo',
                    'localField': 'teamid',
                    'foreignField': '_id',
                    'as': 'teamInfo'
                }
            }, {
                '$unwind': '$teamInfo'
            }, {
                '$lookup': {
                    'from': 'FranchiseInfo',
                    'localField': 'teamid',
                    'foreignField': 'teamid',
                    'as': 'franchiseInfo'
                }
            }, {
                '$unwind': '$franchiseInfo'
            }, {
                '$lookup': {
                    'from': 'SeasonInfo',
                    'localField': 'seasonid',
                    'foreignField': '_id',
                    'as': 'seasonInfo'
                }
            }, {
                '$unwind': '$seasonInfo'
            }, {
                '$lookup': {
                    'from': 'SeasonStatOppo',
                    'let': {
                        'team_id': '$teamid',
                        'season_id': '$seasonid'
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {
                                            '$eq': [
                                                '$teamid', '$$team_id'
                                            ]
                                        }, {
                                            '$eq': [
                                                '$seasonid', '$$season_id'
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'seasonStatOppo'
                }
            }, {
                '$unwind': '$seasonStatOppo'
            }, {
                '$lookup': {
                    'from': 'SeasonStatTeam',
                    'let': {
                        'team_id': '$teamid',
                        'season_id': '$seasonid'
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {
                                            '$eq': [
                                                '$teamid', '$$team_id'
                                            ]
                                        }, {
                                            '$eq': [
                                                '$seasonid', '$$season_id'
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'seasonStatTeam'
                }
            }, {
                '$unwind': '$seasonStatTeam'
            }, {
                '$group': {
                    '_id': {
                        'year': '$seasonInfo.year',
                        'season_type': '$seasonInfo.type',
                        'team': '$teamInfo.team.name'
                    },
                    'teamInfo': {
                        '$first': '$teamInfo'
                    },
                    'franchiseInfo': {
                        '$first': '$franchiseInfo'
                    },
                    'seasonStatOppo': {
                        '$first': '$seasonStatOppo'
                    },
                    'seasonStatTeam': {
                        '$first': '$seasonStatTeam'
                    }
                }
            }, {
                '$sort': {
                    '_id.year': -1,
                    '_id.season_type': 1
                }
            }
        ]

    @staticmethod
    @log_and_catch_exceptions
    def get_AllSeasonsPlayerStatDetails():
        return [
            {
                '$lookup': {
                    'from': 'TeamInfo',
                    'localField': 'teamid',
                    'foreignField': '_id',
                    'as': 'teamInfo'
                }
            }, {
                '$unwind': '$teamInfo'
            }, {
                '$lookup': {
                    'from': 'FranchiseInfo',
                    'localField': 'teamid',
                    'foreignField': 'teamid',
                    'as': 'franchiseInfo'
                }
            }, {
                '$unwind': '$franchiseInfo'
            }, {
                '$lookup': {
                    'from': 'SeasonInfo',
                    'localField': 'seasonid',
                    'foreignField': '_id',
                    'as': 'seasonInfo'
                }
            }, {
                '$unwind': '$seasonInfo'
            }, {
                '$lookup': {
                    'from': 'SeasonStatPlayer',
                    'let': {
                        'team_id': '$teamid',
                        'season_id': '$seasonid'
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {
                                            '$eq': [
                                                '$teamid', '$$team_id'
                                            ]
                                        }, {
                                            '$eq': [
                                                '$seasonid', '$$season_id'
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'seasonstatplayer'
                }
            }, {
                '$unwind': '$seasonstatplayer'
            }, {
                '$group': {
                    '_id': {
                        'year': '$seasonInfo.year',
                        'season_type': '$seasonInfo.type',
                        'team': '$teamInfo.team.name'
                    },
                    'teamInfo': {
                        '$first': '$teamInfo'
                    },
                    'franchiseInfo': {
                        '$first': '$franchiseInfo'
                    },
                    'seasonInfo': {
                        '$first': '$seasonInfo'
                    },
                    'seasonstatplayer': {
                        '$first': '$seasonstatplayer'
                    }
                }
            }, {
                '$sort': {
                    '_id.year': -1,
                    '_id.season_type': 1
                }
            }
        ]

    @staticmethod
    @log_and_catch_exceptions
    def alldetailcurrentseasonplaybyplay():
        return [
            {
                '$lookup': {
                    'from': 'BoxscoreInfo',
                    'localField': 'gamegame._id',
                    'foreignField': 'gamebs._id',
                    'as': 'Boxscoreinfo'
                }
            }, {
                '$lookup': {
                    'from': 'SeasonInfo',
                    'localField': 'gamegame.seasonid',
                    'foreignField': '_id',
                    'as': 'season_info'
                }
            }
        ]
         
data = FootballData()


@app.before_first_request
@log_and_catch_exceptions
def initialization():
    time.sleep(2)
    if not data.all_season_team_stat_details_cache:
        data.fetch_all_season_team_stat_details()
        be_logger.info("inital query load")  # called during initialization


@app.route('/')
@log_and_catch_exceptions
def index():
    # Check if the cache data already exists
    if not data.all_season_team_stat_details_cache:
        be_logger.debug("Accessing / and log_and_catch_exceptions")
        data.fetch_all_season_team_stat_details()
    current_year, current_season_type, _, _ = get_season_info_and_selected(
        request)
    data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
    year_season_combinations_cache = get_year_season_combinations(
        current_year, current_season_type)
    data.selected_teams = get_or_generate_teams()
    # Render the HTML template with necessary variables
    html_content = render_template(
        'index.html',
        year_season_combinations=year_season_combinations_cache,
        selected_year=data.selected_year,
        selected_season_type=data.selected_season_type,
        teams=data.selected_teams,
        teams_dict=data.teams_dict_cache,
    )
    renderindexresponse = make_response(html_content)
    renderindexresponse.headers['Access-Control-Allow-Origin'] = '*'
    return renderindexresponse


@app.errorhandler(404)
@log_and_catch_exceptions
def not_found(e):
    return jsonify(error=str(e)), 404


@log_and_catch_exceptions
def get_season_info_and_selected(request):
    be_logger.info("Called get_season_info_and_selected function")
    if not data.current_year_season_cache:
        be_logger.info("get_season_info_and_selected: Data in Cache: NO")
        current_season = SeasonInfo.objects(status="inprogress").first()
        current_year = current_season.year
        current_season_type = current_season.type
        data.current_year_season_cache = current_year, current_season_type, None, None
    else:
        be_logger.info("get_season_info_and_selected: Data in Cache: Yes")
        current_year, current_season_type, _, _ = data.current_year_season_cache
    data.selected_year = request.args.get('year', default=current_year)
    data.selected_season_type = request.args.get(
        'season_type', default=current_season_type)
    be_logger.info(
        f"get_season_info_and_selected:Current Season:{current_year} {current_season_type}")
    data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
    be_logger.info("About to exit get_season_info_and_selected function")
    return data.current_year_season_cache


@log_and_catch_exceptions
def get_year_season_combinations(current_year, current_season_type):
    if data.year_season_combinations_cache:
        be_logger.info("get_year_season_combinations: Data in Cache: Yes")
    else:
        be_logger.info("get_year_season_combinations: Data in Cache: No")
        season_type_mapping = {
            "PRE": "Pre-Season",
            "REG": "Regular Season",
            "PST": "Playoffs"
        }
        year_season_combinations = []
        current_combo = {
            "year": current_year,
            "season_type": season_type_mapping[current_season_type]
        }
        for item in data.all_season_team_stat_details_cache:
            if "_id" in item and "year" in item["_id"] and "season_type" in item["_id"] and "games_played" in item["seasonStatTeam"]:
                year = item["_id"]["year"]
                season_type_db = item["_id"]["season_type"]
                # Only include seasons with more than 1 game played
                if item["seasonStatTeam"]["games_played"] > 1:
                    season_type = season_type_mapping.get(
                        season_type_db, season_type_db)
                    if not (year == current_year and season_type_db == current_season_type):
                        combo = {"year": year, "season_type": season_type}
                        if combo not in year_season_combinations:
                            year_season_combinations.append(combo)
        ordered_seasons = ["PRE", "REG", "PST"]
        year_season_combinations.sort(key=lambda x: (x['year'], ordered_seasons.index(
            [k for k, v in season_type_mapping.items() if v == x['season_type']][0])), reverse=True)
        if current_combo in year_season_combinations:
            year_season_combinations.remove(current_combo)
        year_season_combinations.insert(0, current_combo)
        be_logger.info(
            f"get_year_season_combinations:Number Items in Season Dropdown:{len(year_season_combinations)}")
        be_logger.debug(
            f"get_year_season_combinations:Sample year-season combinations: {year_season_combinations[:4]}")
        data.year_season_combinations_cache = year_season_combinations
    return data.year_season_combinations_cache


@log_and_catch_exceptions
def get_or_generate_teams():
    base_image_url = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/{TeamAlias}.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true"
    default_team_entry = {"name": "All Teams",
                          "imageLink": ""}
    teams = data.all_season_team_stat_details_cache
    cache = {}
    for team in teams:
        year = team["_id"]["year"]
        season_type = team["_id"]["season_type"]
        if f"{year}_{season_type}" not in cache:
            matched_data = [team for team in teams if (team["_id"]["year"] == year and team["_id"]["season_type"] == season_type
                            and ('seasonStatTeam' in team and 'games_played' in team['seasonStatTeam'] and int(team['seasonStatTeam']['games_played']) > 0))]
            teams_for_combo = [{"name": f"{team['teamInfo']['team']['market']} {team['teamInfo']['team']['name']}" if team['teamInfo']['team']['name'] and team['teamInfo']['team']['market'] else "",
                                "imageLink": base_image_url.format(TeamAlias=team['teamInfo']['team']['alias'])}
                               for team in matched_data]
            teams_for_combo = sorted(
                teams_for_combo, key=lambda x: x["name"].split(" ")[0])
            teams_for_combo.insert(0, default_team_entry)
            cache[f"{year}_{season_type}"] = teams_for_combo
    data.teams_dict_cache = cache
    return data.teams_dict_cache


@log_and_catch_exceptions
@app.route('/get-top10-data', methods=['GET'])
def structure_data_for_categories():
    try:
        be_logger.info("structure_data_for_categories: being accessed)")
        selected_year_from_frontend = request.args.get(
            'year', default=None, type=int)
        selected_season_type_from_frontend = request.args.get(
            'season_type', default=None, type=str)
        updated = False
        if selected_year_from_frontend is not None and selected_year_from_frontend != data.selected_year:
            data.selected_year = selected_year_from_frontend
            be_logger.info(
                f"structure_data_for_categories: updated via dropdown with {data.selected_year}")
            updated = True
        if selected_season_type_from_frontend is not None and selected_season_type_from_frontend != data.selected_season_type:
            data.selected_season_type = selected_season_type_from_frontend
            be_logger.info(
                f"structure_data_for_categories: updated via dropdown with {data.selected_season_type}")
            updated = True
        if not updated:
            be_logger.info(
                "structure_data_for_categories: with no updates from frontend")
        # Filter records from data.all_season_team_stat_details_cache using selected year and season type
        key = f"{data.selected_year}_{data.selected_season_type}"
        data.selected_teams_stats_cache = [item for item in data.all_season_team_stat_details_cache
                                           if item['_id']['year'] == data.selected_year
                                           and item['_id']['season_type'] == data.selected_season_type
                                           and 'seasonStatTeam' in item
                                           and 'games_played' in item['seasonStatTeam']
                                           and int(item['seasonStatTeam']['games_played']) > 0]
        be_logger.info(
            f"structure_data_for_categories: Data for year {data.selected_year} and season {data.selected_season_type} collected. Number of teams: {len(data.selected_teams_stats_cache)}")
        base_image_url = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/{TeamAlias}.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true"
        offensive_leaders, defensive_leaders = {}, {}

        def calculate_stat(x, mode='seasonStatTeam'):
            games_played = x[mode]['opponents_played'] if mode == 'seasonStatOppo' else x[mode]['games_played']
            try:
                return round((x[mode]['passing']['yards'] + x[mode]['rushing']['yards']) / games_played, 2)
            except ZeroDivisionError:
                be_logger.error(
                    "structure_data_for_categories: Division by zero encountered while calculating stat")
                return 0

        def build_leader_data(x, rank, mode='seasonStatTeam'):
            games_played = x['seasonStatOppo']['opponents_played'] if mode == 'seasonStatOppo' else x['seasonStatTeam']['games_played']
            return {
                'rank': rank,
                'team': f"{x['teamInfo']['team']['market']} {x['teamInfo']['team']['name']}",
                'games_played': games_played,
                'stat': calculate_stat(x, mode),
                'img': base_image_url.format(TeamAlias=x['teamInfo']['team']['alias'])
            }
        try:
            be_logger.info(
                "structure_data_for_categories: Preparing Offensive Leaders...")
            offensive_leaders = {
                'Total Yards': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatTeam'), reverse=True)[:10])],
                'Yards per Game': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatTeam'), reverse=True)[:10])],
                'Passing Yards': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatTeam']['passing']['yards'], reverse=True)[:10])],
                'Rushing Yards': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatTeam']['rushing']['yards'], reverse=True)[:10])]
            }
            be_logger.info(
                "structure_data_for_categories: Offensive Leaders prepared.")
        except Exception as e:
            be_logger.error(
                f"structure_data_for_categories: Error preparing offensive leaders: {str(e)}")
            offensive_leaders = {}
            be_logger.error(
                f"structure_data_for_categories: Offensive Leaders Data: {offensive_leaders}")
        try:
            be_logger.info(
                "structure_data_for_categories: Preparing Defensive Leaders...")
            defensive_leaders = {
                'Total Yards Allowed': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatOppo'), reverse=False)[:10])],
                'Yards Allowed per Game': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatOppo'), reverse=False)[:10])],
                'Passing Yards Allowed': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatOppo']['passing']['yards'], reverse=False)[:10])],
                'Rushing Yards Allowed': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatOppo']['rushing']['yards'], reverse=False)[:10])]
            }
            be_logger.info(
                "structure_data_for_categories: Defensive Leaders prepared.")
        except Exception as e:
            be_logger.error(
                f"structure_data_for_categories: Error preparing defensive leaders: {str(e)}")
            defensive_leaders = {}
            be_logger.error(
                f"structure_data_for_categories: Defensive Leaders Data: {defensive_leaders}")
        team_top_10_data = {
            'Offensive Leaders': offensive_leaders,
            'Defensive Leaders': defensive_leaders
        }
        be_logger.info(
            f"structure_data_for_categories: Preparing data for key: {key}")
        data.team_top_10_data_cache[key] = team_top_10_data
        team_top_10_cache = {}
        team_top_10_cache[key] = team_top_10_data
        if not bool(data.team_top_10_data_cache):
            be_logger.info(
                "get_data: Executed structure_data_for_categories function as top 10 data was not found in cache")
        try:
            sample_offensive_data = team_top_10_data['Offensive Leaders']['Yards per Game'][:2]
            be_logger.info(
                f"structure_data_for_categories: Sample 'Total Yards' for 'Offensive Leaders': {sample_offensive_data}")
        except (KeyError, TypeError) as e:
            be_logger.error(
                f"structure_data_for_categories:Error fetching 'Total Yards' for 'Offensive Leaders': {str(e)}")
        try:
            sample_defensive_data = team_top_10_data['Defensive Leaders']['Total Yards Allowed'][:2]
            be_logger.info(
                f"structure_data_for_categories: Sample 'Total Yards Allowed' for 'Defensive Leaders': {sample_defensive_data}")
        except (KeyError, TypeError) as e:
            be_logger.error(
                f"structure_data_for_categories: Error fetching 'Total Yards Allowed' for 'Defensive Leaders': {str(e)}")
        return jsonify(team_top_10_cache)
    except Exception as e:
        be_logger.error(
            f"Error in structure_data_for_categories: {str(e)}. Current state: team_top_10_data_cache: {data.team_top_10_data_cache}, team_top_10_cache: {team_top_10_cache}")
        return jsonify({"error": str(e)}), 500


@log_and_catch_exceptions
@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        # Log the input from the frontend
        selected_year_from_frontend = request.args.get(
            'year', default=None, type=int)
        selected_season_type_from_frontend = request.args.get(
            'season_type', default=None, type=str)
        selected_team_from_frontend = request.args.get(
            'single_team', default=None, type=str)
        be_logger.info(
            f"get_data: From frontend - Year: {selected_year_from_frontend}, Season: {selected_season_type_from_frontend}, Team: {selected_team_from_frontend}")
        updated = False
        if data.current_year_season_cache:
            current_year, current_season_type, _, _ = data.current_year_season_cache
            be_logger.info(
                f"get_data: Using cached year and season: {current_year} {current_season_type}")
        else:
            current_year, current_season_type, _, _ = get_season_info_and_selected(
                request)
            data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
            be_logger.info(
                "get_data: Data fetched with get_season_info_and_selected and saved to cache")
        key = f"{data.selected_year}_{data.selected_season_type}"
        be_logger.info(
            f"get_data: Generated key for selected year and season: {key}")
        # Check and flag if updates are needed
        if selected_year_from_frontend is not None and selected_year_from_frontend != data.selected_year:
            data.selected_year = selected_year_from_frontend
            updated = True
        if selected_season_type_from_frontend is not None and selected_season_type_from_frontend != data.selected_season_type:
            data.selected_season_type = selected_season_type_from_frontend
            updated = True
        if selected_team_from_frontend is not None and selected_team_from_frontend != data.selected_team:
            data.selected_team = selected_team_from_frontend
            updated = True
        be_logger.info(f"get_data: Updated flag: {updated}")
        # Data fetch/update operations
        team_top_10_data_cache_json = structure_data_for_categories()
        be_logger.info(
            "get_data: Fetched data with structure_data_for_categories as it was not found in cache")
        if not data.year_season_combinations_cache:
            data.year_season_combinations_cache = get_year_season_combinations(
                data.selected_year, data.selected_season_type)
            be_logger.info(
                f"get_data: Number of Documents returned to year_season_combinations_cache: {len(data.year_season_combinations_cache)}")
        if key in data.teams_dict_cache:
            be_logger.debug("get_data: Teams_dict_cache content: {}".format(
                data.teams_dict_cache[key][1:4]))
        else:
            be_logger.warning(
                f"get_data: Key {key} not found in data.teams_dict_cache")
        # Get data from teams dict cache
        data.selected_teams = data.teams_dict_cache.get(key, [])
        be_logger.info(
            f"get_data: Selected Teams (first 2): {data.selected_teams[:3]}")
        # Prepare top 10 data for UI
        team_top_10_data = data.team_top_10_data_cache.get(key)
        offensive_leaders = team_top_10_data.get('Offensive Leaders', {})
        defensive_leaders = team_top_10_data.get('Defensive Leaders', {})
        for category_name, stats_list in offensive_leaders.items():
            be_logger.info(
                f"Offensive Leaders - {category_name}: Number of Teams {len(stats_list)}")
        for category_name, stats_list in defensive_leaders.items():
            be_logger.info(
                f"Defensive Leaders - {category_name}: Number of Teams {len(stats_list)}")
        return render_template('DynamicSeasonStats.html',
                               team_top_10_data=data.team_top_10_data_cache[key],
                               selected_year=data.selected_year,
                               selected_season_type=data.selected_season_type,
                               teams=data.selected_teams,
                               year_season_combinations=data.year_season_combinations_cache
                               )
    except Exception as e:
        be_logger.error(f"get_data: Error occurred: {str(e)}")
        return jsonify(error=str(e)), 500


@log_and_catch_exceptions
def fetch_data_from_mongodb(year, season_type, view_mode, team, stat_category):
    # Build your MongoDB query based on the filters
    if view_mode == "team":
        if stat_category == "passing":
            # Example: Fetching passing stats for teams
            records = SeasonStatTeam.objects(
                year=year, season_type=season_type, team=team).all()
            for record in records:
                fetched_data.append({
                    "team": record.team,
                    "passing_yards": record.passing.yards,
                    "passing_touchdowns": record.passing.touchdowns,
                    # ... add other relevant fields
                })
            headers = ["team", "passing_yards", "passing_touchdowns"]
            # ... add other relevant headers
        # Add more conditions for other stat categories
    elif view_mode == "player":
        # Similar logic for fetching player stats
        # ...
        # Always return a tuple (data, headers)
        return fetched_data, headers
    return [], []


@log_and_catch_exceptions
@app.route('/populate-teams', methods=['GET'])
def populate_teams():
    try:
        be_logger.info("/populate-teams being accessed)")
        selected_year_from_frontend = request.args.get(
            'year', default=data.selected_year, type=int)
        selected_season_type_from_frontend = request.args.get(
            'season_type', default=data.selected_season_type, type=str)
        if selected_season_type_from_frontend == data.selected_season_type and selected_year_from_frontend == data.selected_year:
            be_logger.info("/populate-teams: No change in Team Dropdown List")
        key = f"{selected_year_from_frontend}_{selected_season_type_from_frontend}"
        be_logger.info({key})
        be_logger.info(
            f"/populate-teams: Received request to populate teams for year: {selected_year_from_frontend} and season type: {selected_season_type_from_frontend}")
        data.selected_teams = data.teams_dict_cache.get(key, {})
        be_logger.info(
            f"/populate-teams: Team List New Season: {str(data.selected_teams)[:100]}")
        return jsonify({'teams': data.selected_teams})
    except Exception as e:
        be_logger.error(f"Error in populate_teams: {e}")
        return jsonify({"error": str(e)}), 500


@log_and_catch_exceptions
@app.route('/populate-seasons', methods=['GET'])
def populate_seasons():
    try:
        be_logger.info(
            f"/populate-seasons List: {str(data.year_season_combinations_cache)[:100]}")
        return jsonify({
            'seasons': data.year_season_combinations_cache
        })
    except Exception as e:
        be_logger.error(f"Error in populate_teams: {e}")
        return jsonify({"error": str(e)}), 500


@log_and_catch_exceptions
@app.route('/venues')
def venues():
    be_logger.debug("Accessing /venues")
    # Fetch all venues from the database
    venue_infos = VenueInfo.objects.all()
    # Extract the venue1 dictionaries from each document and add lat and lng
    venues = []
    for venue_info in venue_infos:
        # Use the instance 'venue_info.venue1', not the class definition
        venue = venue_info.venue1.to_mongo().to_dict()
        # Use the instance 'venue_info.location', not the class definition
        location_dict = venue_info.location.to_mongo().to_dict()
        if location_dict.get('lat') and location_dict.get('lng'):
            venue.update(location_dict)
            venues.append(venue)
    return render_template('venues.html', venues=venues)


@log_and_catch_exceptions
@app.route('/livegames', methods=['GET', 'POST'])
def livegames():
    be_logger.debug("Accessing /livegames")
    now = datetime.now()
    week = request.form.get('week')
    team = request.form.get('team')
    year = request.form.get('year')
    # Fetch weeks and teams from the database
    league_info = LeagueInfo.objects.first()
    weeks = [week['title'] for week in league_info.leagueweek]
    years = list(range(2001, 2024))
    selected_year = 2023
    # Determine the current NFL week
    current_date = now.date()
    selected_week = None
    for start_date, week in nfl_weeks.items():
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = start_date + timedelta(days=6)
        if start_date <= current_date <= end_date:
            selected_week = week
            break
    selected_team = None
    if year:
        selected_year = int(year)
    if week:
        selected_week = week
    query = GameInfo.objects.all()
    teams = query.distinct('gamegame.team')
    if selected_week:
        start_date = [date for date, week in nfl_weeks.items()
                      if week == selected_week][0]
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = start_date + timedelta(days=6)
        query = query.filter(gamegame__scheduled__gte=start_date,
                             gamegame__scheduled__lte=end_date)
    if team:
        selected_team = team
        query = query.filter(gamegame__team__icontains=selected_team)
    game_infos = query
    game_ids = []
    for game_info in game_infos:
        try:
            game_id = game_info.gamegame['_id']
        except KeyError:
            try:
                game_id = game_info.gamegame['gamegame']['_id']
            except KeyError:
                continue
        game_ids.append(game_id)
    boxscore_infos = BoxscoreInfo.objects(gamebs__id__in=game_ids)
    games = []
    for game_info in game_infos:
        game = json.loads(game_info.to_json())
        try:
            game_id = game['gamegame']['_id']
        except KeyError:
            try:
                game_id = game['gamegame']['gamegame']['_id']
            except KeyError:
                continue
        game_bs_info = boxscore_infos.filter(gamebs__id=game_id).first()
        if game_bs_info:
            game_bs_info_dict = json.loads(game_bs_info.to_json())
            game_bs_info_dict['gamebs']['_id'] = game_id
            for quarter in game_bs_info_dict['quarters']:
                quarter['id'] = base64.b64encode(
                    quarter['id']['$binary']['base64']).decode('utf-8')
            game['boxscore_info'] = game_bs_info_dict
        # Convert 'scheduled' field to 'Thursday, September 7, 2023' format
        scheduled = game_info.gamegame['scheduled']
        game['gamegame']['scheduled'] = scheduled.strftime('%A, %B %d, %Y')
        games.append(game)
    # Group games by day
    games_grouped = {k: list(v) for k, v in groupby(
        games, key=lambda x: x['gamegame']['scheduled'])}
    return render_template('livegames.html', games_grouped=games_grouped, weeks=weeks, years=years, teams=teams, selected_week=selected_week, selected_year=selected_year, selected_team=selected_team)


@log_and_catch_exceptions
def generate_nfl_weeks(year):
    be_logger.debug("Accessing generate_nfl_weeks")
    # start date of the NFL season in the given year
    start_date = datetime(year, 9, 1)
    # dictionary to hold the date ranges for each week
    nfl_weeks = {}
    # generate date ranges for each week of the regular season
    for week in range(1, 18):
        end_date = start_date + timedelta(days=6)
        nfl_weeks[start_date.strftime('%Y-%m-%d')] = f'WEEK {week}'
        start_date += timedelta(days=7)
    return nfl_weeks


@app.route('/scores')
def scores():
    # Query your MongoDB collections to get the data. Sample query is shown below, replace it with your own
    # data = MongoClient('mongodb://localhost:27017/').mydb.mycollection.find()

    # If you can structure your data in the format {game1: {...}, game2: {...}, ...}
    # then you can pass the whole data dictionary to your template and use game_info to access each game's info
    # If your data isn't structured like this, modify the following code as needed

    # This should be replaced with actual function to get data
    data = get_data_from_database()

    return render_template('scores.html', games=data)

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    if flask_env == 'development':
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context="adhoc")
    else:
        app.run()
