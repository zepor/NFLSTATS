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
from threading import Thread
import redis
import pickle
import time
import json
import base64
from dateutil.parser import parse
from datetime import datetime, timedelta
import pymongo
import requests
import redis
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
import os.path
sys.path.append(os.path.join(str(LPATH), '.venv', 'lib', 'site-packages'))
sys.path.append(str(LPATH))
sys.path.append('/src')
sys.path.append('/src/models')
mongodb_service_name = os.getenv('MONGODB_SERVICE_NAME', 'localhost')
mongodb_url = os.getenv(
    'MONGODB_URL', f"mongodb://{mongodb_service_name}:27017/current_season")
client = MongoClient(mongodb_url, connectTimeoutMS=30000, socketTimeoutMS=None)
try:
    client.admin.command('ismaster')
except ConnectionFailure:
    logging.error("MongoDB server not available")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'templates', 'static'))
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
log_dir = './logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'app.log')
be_logger = logging.getLogger('backend-logger')
be_logger.setLevel(logging.DEBUG)  
file_handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
be_logger.addHandler(file_handler)
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
be_logger.addHandler(console_handler)
be_logger.info(os.getenv('FLASK_APP'))
be_logger.info(os.getenv('FLASK_ENV'))
for key, value in app.config.items():
    be_logger.info(f"{key}: {value}")
CORS(app, origins='https://0.0.0.0')
scheduler = BackgroundScheduler()
try:
    r = redis.Redis(host='127.0.0.1', port=6379, db=0) # replace with your Redis' host and port
    r.ping() # this will raise an ConnectionError if the Redis server is not available
    be_logger.info("Connected to Redis")
except redis.exceptions.ConnectionError as ex:
    be_logger.info("Could not connect to Redis:", str(ex))
app.config['MONGODB_SETTINGS'] = {
    'db': 'current_season',  # Replace with your database name
    'host': mongodb_url
}
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['JSON_SORT_KEYS'] = False
db = MongoEngine(app)
flask_env = os.environ.get('FLASK_ENV', 'development')
if flask_env == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)
app.register_blueprint(bp_current_season_schedule)
app.register_blueprint(bp_league_hierarchy)
app.register_blueprint(bp_team_profile)
app.register_blueprint(bp_seasons)
app.register_blueprint(bp_seasonal_stats)
app.secret_key = 'sessionkey'
app.jinja_env.cache = {}

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
        self.get_AllSeasonsTeamStatDetails_cache = None
        self.current_year_season_cache = None
        self.year_season_combinations_cache = None
        self.teams_dict_cache = {}
        self.selected_teams_stats_cache = {}
        self.team_top_10_data_cache = {}
        self.selected_year = None
        self.selected_season_type = None
        self.selected_team = None
        self.selected_teams = {}
        self.last_refreshed = datetime.now()
data = FootballData()

@log_and_catch_exceptions
def fetch_AllSeasonsTeamStatDetails():
    be_logger.info("Starting fetch for fetch_AllSeasonsTeamStatDetails...")
    return[
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


def clear_cache():
    r.flushdb()  # Caution, this clears the entire Redis database. Only use if your Redis db is dedicated to caching.
    be_logger.info("Cache cleared.")
    

@log_and_catch_exceptions
@app.route('/')
def index():
    # Try getting the data from the cache
    cached_data = r.get("get_AllSeasonsTeamStatDetails_cache")
    be_logger.info(f"Type of data: {type(data)}")  # Debug be_logger.info: type of data
    be_logger.info(f"Type of cached_data: {type(cached_data)}")  # Debug be_logger.info: type of cached_data
    current_year, current_season_type, _, _ = get_season_info_and_selected(request)
    data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
    cache_key = f"seasons_{current_year}_{current_season_type}_statdetails"
    cached_data = r.get(cache_key)
    if cached_data is None:
        be_logger.info("Cache is empty, fetching data...")
        query_allteamstats = fetch_AllSeasonsTeamStatDetails()
        results_data = list(SeasonStatTeam.objects.aggregate(*query_allteamstats))
        be_logger.debug("Total number of documents fetched: %s", len(results_data))
        redis_data = pickle.dumps(results_data)
        r.set("get_AllSeasonsTeamStatDetails_cache", redis_data)
        be_logger.debug("First 200 chars of cached data: %s", str(redis_data)[:200])
        data.get_AllSeasonsTeamStatDetails_cache = results_data
    else:
        be_logger.info("Cache hit, loading cached data...")
        try:
            cached_results = pickle.loads(cached_data)
        except pickle.UnpicklingError:
            # This will handle old cache entries that were stored as JSON
            cached_results = json.loads(cached_data.decode())
        data.get_AllSeasonsTeamStatDetails_cache = cached_results
    be_logger.info(f"data.get_AllSeasonsTeamStatDetails_cache: {data.get_AllSeasonsTeamStatDetails_cache[:200]}")  
    current_year, current_season_type, _, _ = get_season_info_and_selected(request)
    data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
    year_season_combinations_cache = get_year_season_combinations(
        current_year, current_season_type) 
    data.selected_teams = get_or_generate_teams()
    be_logger.debug(f"Total number of documents from cache: {len(data.get_AllSeasonsTeamStatDetails_cache)}")
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
        for item in data.get_AllSeasonsTeamStatDetails_cache:
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
    default_team_entry = {"name": "All Teams", "imageLink": ""}
    teams = data.get_AllSeasonsTeamStatDetails_cache
    cache = {}
    for team in teams:
        if "_id" in team and "year" in team["_id"] and "season_type" in team["_id"]:  # Check if keys exist before accessing
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
                
                key = f"{year}_{season_type}"
                cache[key] = teams_for_combo
                
                # Debugging log to print the key and the list of teams for this year and season type
                be_logger.debug(f"Key: {key}, Teams: {teams_for_combo}")
    data.teams_dict_cache = cache
    return data.teams_dict_cache


@log_and_catch_exceptions
@app.route('/get-top10-data', methods=['GET'])
def structure_data_for_categories():
    team_top_10_cache = {}
    team_top_10_data = {} 
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
        
        key = f"{data.selected_year}_{data.selected_season_type}"

        # Debugging code
        be_logger.debug(f"data.get_AllSeasonsTeamStatDetails_cache: {str(data.get_AllSeasonsTeamStatDetails_cache)[:200]}")

        filtered_items = [item for item in data.get_AllSeasonsTeamStatDetails_cache
                           if item['_id']['year'] == data.selected_year
                        ]
        be_logger.debug(f"Filtered data after applying year condition: {str(filtered_items)[:200]}")

        filtered_items = [item for item in data.get_AllSeasonsTeamStatDetails_cache
                           if item['_id']['year'] == data.selected_year
                           and item['_id']['season_type'] == data.selected_season_type
                        ]
        be_logger.debug(f"Filtered data after applying season_type condition: {str(filtered_items)[:200]}")

        # Original filtering
        data.selected_teams_stats_cache = [item for item in data.get_AllSeasonsTeamStatDetails_cache
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
        be_logger.error(f"Error in structure_data_for_categories: {str(e)}. Current state: team_top_10_data_cache: {data.team_top_10_data_cache}, team_top_10_cache: {team_top_10_cache}")

@log_and_catch_exceptions
@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        selected_year_from_frontend = request.args.get('year', default=None, type=int)
        selected_season_type_from_frontend = request.args.get('season_type', default=None, type=str)
        selected_team_from_frontend = request.args.get('single_team', default=None, type=str)
        be_logger.info(f"get_data: From frontend - Year: {selected_year_from_frontend}, Season: {selected_season_type_from_frontend}, Team: {selected_team_from_frontend}")
        updated = False
        if data.current_year_season_cache:
            current_year, current_season_type, _, _ = data.current_year_season_cache
            be_logger.info(f"get_data: Using cached year and season: {current_year} {current_season_type}")
        else:
            current_year, current_season_type, _, _ = get_season_info_and_selected(request)
            data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
            be_logger.info("get_data: Data fetched with get_season_info_and_selected and saved to cache")
        key = f"{data.selected_year}_{data.selected_season_type}"
        be_logger.info(f"get_data: Generated key for selected year and season: {key}")
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
        team_top_10_data_cache_json = structure_data_for_categories()
        if team_top_10_data_cache_json is None:  
            be_logger.error(f"get_data: structure_data_for_categories() returned None")
            return jsonify({"error": "Error in getting top 10 data"}), 500
        else:
            be_logger.info("get_data: Fetched data with structure_data_for_categories as it was not found in cache")
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
        data.selected_teams = data.teams_dict_cache.get(key, [])
        be_logger.info(f"get_data: Selected Teams (first 2): {data.selected_teams[:2]}")
        team_top_10_data = data.team_top_10_data_cache.get(key)
        if team_top_10_data is None:  # Add this check
            be_logger.error(f"get_data: No team top 10 data Cache: {data.team_top_10_data_cache}")
            return jsonify({"error": "No team top 10 data found"}), 500
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
        return jsonify({"error": str(e)}), 500


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
        # Debugging line:
        be_logger.debug("Args received from frontend: " + str(request.args))
        selected_year_from_frontend = request.args.get(
            'year', default=data.selected_year, type=int)
        selected_season_type_from_frontend = request.args.get(
            'season_type', default=data.selected_season_type, type=str)
        # Debugging line:
        be_logger.debug("Selected year from frontend: " + str(selected_year_from_frontend))
        be_logger.debug("Selected season type from frontend: " + selected_season_type_from_frontend)
        if selected_season_type_from_frontend == data.selected_season_type and selected_year_from_frontend == data.selected_year:
            be_logger.info("/populate-teams: No change in Team Dropdown List")
        key = f"{selected_year_from_frontend}_{selected_season_type_from_frontend}"
        be_logger.info({key})
        be_logger.info(
            f"/populate-teams: Received request to populate teams for year: {selected_year_from_frontend} and season type: {selected_season_type_from_frontend}")
        data.selected_teams = data.teams_dict_cache.get(key, {})
        # Debugging line: Check if any data found for the constructed key
        if not data.selected_teams:
            be_logger.debug(f"No team data found in cache for key: {key}")
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
@app.route("/livegames", methods=['GET'])
def live_games():
    now = datetime.now()
    in_three_days = now + timedelta(days=3)
    be_logger.debug("Accessing /livegames")
    thisweeksgames = [
        {
            "$match": {
                "gamegame.scheduled": { 
                    "$gte": now,
                    "$lt": in_three_days
                }
            }
        },
        {
            "$group": {
                "_id": None, 
                "distinctLeagueWeeks": { "$addToSet": "$gamegame.leagueweek" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "distinctLeagueWeeks": 1
            }
        },
        {
            "$unwind": "$distinctLeagueWeeks"
        },
        {
            "$lookup": {
                "from": "GameInfo",
                "localField": "distinctLeagueWeeks",
                "foreignField": "gamegame.leagueweek",
                "as": "games"
            }
        },
        {
            "$unwind": "$games"
        },  
        {
            "$lookup": {
                "from": "BoxscoreInfo",
                "localField": "games._id",
                "foreignField": "_id",
                "as": "games.boxscore_info"
            }
        },
        {
            "$unwind": "$games.boxscore_info"
        },
        {
            "$lookup": {
                "from": "LeagueInfo",
                "localField": "games.gamegame.leagueweek",
                "foreignField": "_id",
                "as": "games.league_info"
            }
        },
        {
            "$unwind": "$games.league_info"
        },
        {
            "$lookup": {
                "from": "SeasonStatPlayer",
                "localField": "games.hometeam.id",
                "foreignField": "teamid",
                "as": "games.season_stat_player"
            }
        }, 
        {
            "$unwind": "$games.season_stat_player"
        },
        {
            "$lookup": {
                "from": "SeasonStatTeam",
                "localField": "games.hometeam.id",
                "foreignField": "teamid",
                "as": "games.season_stat_team"
            }
        },
        {
            "$unwind": "$games.season_stat_team"
        },
        {
            "$lookup": {
                "from": "TeamInfo",
                "localField": "games.hometeam.id",
                "foreignField": "_id",
                "as": "games.team_info"
            }
        },
        {
            "$unwind": "$games.team_info"
        },
        {
            "$replaceRoot": {
              "newRoot": "$games"
            }
        }
    ]
    be_logger.debug(f"thisweeksgames: {thisweeksgames}")
    games = list(GameInfo.objects.aggregate(*thisweeksgames))

    return jsonify({"upcominggames": games})

logger = logging.getLogger(__name__)
flask_env = os.environ.get('FLASK_ENV')
be_logger.info(f"Current FLASK_ENV: {flask_env}")
if __name__ == "__main__":
    clear_cache()
    if flask_env == 'development' and os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        data = data if data else FootballData()
        app.run(host='localhost', port=5000, debug=True, ssl_context="adhoc", use_reloader=True)
    elif flask_env != 'development':
        # In production mode, just initialize as usual
        data = data if data else FootballData()
        app.run()