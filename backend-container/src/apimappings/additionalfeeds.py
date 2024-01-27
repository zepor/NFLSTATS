import itertools
import sys
import os
import time
from flask import Flask, jsonify, Blueprint
from datetime import datetime, timezone
from dotenv import load_dotenv
from src.utils.log import be_logger
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.sportsradar.workspace.datastore import save_data
from src.sportsradar.extract.additionalfeeds import AdditionalFeeds
from src.sportsradar.transform.additionalfeeds import AdditionalFeedsTransformer
from src.database.connections import get_mongodb_connection

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))

additionalfeeds_blueprint = Blueprint('additionalfeeds', __name__)

# Fetch the API key from the environment variable
api_key = os.getenv('APIKEY')
mongodb_url = os.getenv('MONGODB_URL')
mongodb_database = os.getenv('MONGODB_DATABASE')
class TestConstants:
    BASE_URL = "https://api.sportradar.us/nfl/official"
    ACCESS_LEVEL = "trial"
    VERSION = "v7"
    LANGUAGE_CODE = "en"
    FORMAT = "json"
    API_KEY = api_key
    MONGODB_URL = mongodb_url
    MONGODB_DATABASE = mongodb_database

@log_and_catch_exceptions
def fetch_nfl_season_week_info(year):
    be_logger.info(f"Fetching NFL season week information for year: {year}")
    client = get_mongodb_connection()
    if not client:
        be_logger.error("Failed to connect to MongoDB.")
        return {}

    db = client["Current_Season"]
    collection = db["LeagueInfo"]
    processed_info = {}

    # Query to find unique season types for the given year
    season_type_pipeline = [
        {"$match": {"season.year": year}},
        {"$group": {"_id": "$season.type"}}
    ]
    season_types = [doc['_id'] for doc in collection.aggregate(season_type_pipeline)]

    for season_type in season_types:
        pipeline = [
            {"$match": {"season.year": year, "season.type": season_type}},
            {"$unwind": "$leagueweek"},
            {"$group": {
                "_id": "$season.type",
                "weeks": {"$addToSet": "$leagueweek.sequence"}
            }}
        ]
        if result := list(collection.aggregate(pipeline)):
            # Ensuring data exists for the season type
            processed_info[season_type] = sorted(result[0]['weeks'])

    client.close()
    be_logger.info(f"Fetched season week information for year {year}: {processed_info}")
    return processed_info


@log_and_catch_exceptions
def process_weekly_depth_charts(year):
    season_week_info = fetch_nfl_season_week_info(year)
    additionalfeeds = AdditionalFeeds(TestConstants.BASE_URL)
    results = []

    for nfl_season, weeks in season_week_info.items():
        for week in weeks:
            be_logger.info(f"Processing weekly depth charts for year: {year}, season: {nfl_season}, week: {week}")
            try:
                if data := additionalfeeds.get_weekly_depth_charts(
                    access_level=TestConstants.ACCESS_LEVEL,
                    version=TestConstants.VERSION,
                    language_code=TestConstants.LANGUAGE_CODE,
                    year=year,
                    nfl_season=nfl_season,
                    nfl_season_week=week,
                    file_format=TestConstants.FORMAT,
                    api_key=TestConstants.API_KEY,
                ):
                    save_data(data, "Current_Season", "WeeklyDepthChartInfo")
                    results.append(data)
            except Exception as e:
                be_logger.error(f"Error processing data for year: {year}, season: {nfl_season}, week: {week}. Error: {e}")

            time.sleep(2)

    return results

@additionalfeeds_blueprint.route('/weekly_depth_charts/<int:year>', methods=['GET'])
@log_and_catch_exceptions
def get_weekly_depth_charts(year):
    be_logger.info(f"API Route '/weekly_depth_charts/{year}' accessed")
    data = process_weekly_depth_charts(year)
    serializable_data = [item.json() if hasattr(item, 'json') else item for item in data]
    return jsonify(serializable_data)


@log_and_catch_exceptions
def fetch_daily_transaction_dates(year):
    be_logger.info(f"Fetching daily transaction dates for the year: {year}")
    return [datetime(year, month, day) for month in range(1, 13) for day in range(1, 32)]

@log_and_catch_exceptions
def process_daily_transactions(year):
    be_logger.info(f"Processing daily transactions for the year: {year}")
    additionalfeeds = AdditionalFeeds(TestConstants.BASE_URL)
    results = []

    for month, day in itertools.product(range(1, 13), range(1, 32)):
        try:
            date = datetime(year, month, day)
            be_logger.info(f"Processing transactions for date: {date}")
            if data := additionalfeeds.get_daily_transactions(
                access_level=TestConstants.ACCESS_LEVEL,
                version=TestConstants.VERSION,
                language_code=TestConstants.LANGUAGE_CODE,
                year=year,
                month=month,
                day=day,
                file_format=TestConstants.FORMAT,
                api_key=TestConstants.API_KEY,
            ):
                save_data(data, "Current_Season", "TransactionInfo")
                results.append(data)
        except ValueError:
            # This exception occurs if the day is not valid for the month (e.g., February 30th)
            continue
        time.sleep(2)

    return results

@additionalfeeds_blueprint.route('/daily_transactions/<int:year>', methods=['GET'])
@log_and_catch_exceptions
def get_daily_transactions(year):
    be_logger.info(f"API Route '/daily_transactions/{year}' accessed")
    data = process_daily_transactions(year)
    return jsonify(data)

@log_and_catch_exceptions
def fetch_nfl_season_info(year):
    be_logger.info(f"Fetching NFL season information for year: {year}")
    client = get_mongodb_connection()
    if not client:
        be_logger.error("Failed to connect to MongoDB.")
        return []

    db = client["Current_Season"]
    collection = db["LeagueInfo"]

    query = {"season.year": year}
    projection = {"season.type": 1, "_id": 0}
    
    season_types = collection.find(query, projection)
    unique_types = {season['season']['type'] for season in season_types if 'season' in season}
    
    client.close()
    be_logger.info(f"Fetched season types for year {year}: {unique_types}")
    return list(unique_types)

@log_and_catch_exceptions
def process_postgame_standings(year):
    types = fetch_nfl_season_info(year)
    additionalfeeds = AdditionalFeeds(TestConstants.BASE_URL)
    results = []

    for type in types:
        be_logger.info(f"Processing postgame standings for year: {year}, type: {type}")
        if data := additionalfeeds.get_postgame_standings(
            access_level=TestConstants.ACCESS_LEVEL,
            version=TestConstants.VERSION,
            language_code=TestConstants.LANGUAGE_CODE,
            year=year,
            nfl_season=type,
            file_format=TestConstants.FORMAT,
            api_key=TestConstants.API_KEY,
        ):
            save_data(data, "Current_Season", "StandingsInfo")
            results.append(data)
        time.sleep(1)

    return results

@additionalfeeds_blueprint.route('/postgame_standings/<int:year>', methods=['GET'])
@log_and_catch_exceptions
def get_postgame_standings(year):
    be_logger.info(f"API Route '/postgame_standings/{year}' accessed")
    data = process_postgame_standings(year)

    # Convert the data to a serializable format if it's not already
    serializable_data = []
    for item in data:
        if hasattr(item, 'json'):
            serializable_data.append(item.json())
        elif isinstance(item, dict):
            serializable_data.append(item)
        else:
            # Convert other data types as needed
            serializable_data.append(str(item))

    return jsonify(serializable_data)

