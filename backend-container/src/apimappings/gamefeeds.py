import sys
import os
import time
from flask import Flask, jsonify, Blueprint
from datetime import datetime, timezone
from dotenv import load_dotenv
from src.utils.log import be_logger
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.sportsradar.workspace.datastore import save_data
from src.sportsradar.extract.gamefeeds import GameFeeds
from src.database.connections import get_mongodb_connection

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))

gamefeeds_blueprint = Blueprint('gamefeeds', __name__)
# Fetch the API key from the environment variable
api_key = os.getenv('APIKEY')
mongodb_url = os.getenv('MONGODB_URL')
mongodb_database = os.getenv('MONGODB_DATABASE')
# Constants used for the Sportradar API
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
def get_game_ids_for_year(year):
    be_logger.info(f"Fetching game IDs for the year: {year}")
    client = get_mongodb_connection()
    if not client:
        be_logger.error("Failed to connect to MongoDB.")
        return []

    db = client["Current_Season"]
    collection = db["GameInfo"]

    start_date = datetime(year, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)

    query = {"gamegame.scheduled": {"$gte": start_date, "$lt": end_date}}
    projection = {"gamegame._id": 1}

    game_ids = [doc["gamegame"]["_id"] for doc in collection.find(query, projection)]
    client.close()
    be_logger.info(f"Number of game IDs fetched: {len(game_ids)}")
    return game_ids

@log_and_catch_exceptions
def process_game_feeds(year):
    game_ids = get_game_ids_for_year(year)
    gamefeeds = GameFeeds(TestConstants.BASE_URL)
    results = []
    
    for game_id in game_ids:
        be_logger.info(f"Processing game ID: {game_id}")
        try:
            if boxscore_data := gamefeeds.get_game_boxscore(
                game_id=game_id,
                access_level=TestConstants.ACCESS_LEVEL,
                language_code=TestConstants.LANGUAGE_CODE,
                version=TestConstants.VERSION,
                file_format=TestConstants.FORMAT,
                api_key=TestConstants.API_KEY,
            ):
                be_logger.info(f"Data retrieved for game ID {game_id}: {boxscore_data}")
                save_data(
                    response=boxscore_data,
                    collection="GameFeed",
                    database=mongodb_database
                )
                results.append(boxscore_data)
            else:
                be_logger.warning(f"No data retrieved for game ID {game_id}")
            time.sleep(2)
        except Exception as e:
            be_logger.error(f"Error processing game ID {game_id}: {e}")
    return results

@gamefeeds_blueprint.route('/<int:year>', methods=['GET'])
def get_game_feeds(year):
    try:
        data = process_game_feeds(year)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
