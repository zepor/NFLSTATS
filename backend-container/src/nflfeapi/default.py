import sys
import os
import pickle 
from flask import request, jsonify, Blueprint

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))  

bp_default = Blueprint('default', __name__)
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
from src.nflfetchqueries.fetchlivegames import fetch_live_games_data
from src.nflfetchqueries.getseasoninfoandselected import get_season_info_and_selected
from src.nflfetchqueries.fetchallseasonsteamstatdetails import fetch_allseasonsteamstatdetails
from src.database.rediscache import data
from src.database.connections import r
from src.nflfeapi.default import ( 
    fetch_live_games_data,
    get_season_info_and_selected,
    fetch_allseasonsteamstatdetails,
)


@log_and_catch_exceptions
@bp_default.route('/', defaults={'path': ''})
@bp_default.route('/<path:path>')
def serve(path):
    try:
        be_logger.info("Fetching live games data...")
        fetched_data = fetch_live_games_data()
        live_games_data = fetched_data.get("upcominggames", [])
        if live_games_data:
            live_games_cache_key = "livegames_cache"
            r.set(live_games_cache_key, pickle.dumps(live_games_data))
            be_logger.info(
                "Live games data was fetched and cached successfully.")
        else:
            be_logger.warning("No live games data was fetched.")
        be_logger.info("Fetching current year and season type...")
        current_year, current_season_type, _, _ = get_season_info_and_selected(
            request)
        data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
        be_logger.info(
            f"Current year: {current_year}, Current season type: {current_season_type}")
        be_logger.info("Fetching AllSeasonsTeamStatDetails cache...")
        cached_data = r.get("get_AllSeasonsTeamStatDetails_cache")
        if cached_data is None:
            be_logger.info("Cache is empty, fetching data...")
            query_allteamstats = fetch_allseasonsteamstatdetails()
            results_data = list(
                SeasonStatTeam.objects.aggregate(*query_allteamstats))
            be_logger.debug(
                "Total number of documents fetched: %s", len(results_data))
            redis_data = pickle.dumps(results_data)
            r.set("get_AllSeasonsTeamStatDetails_cache", redis_data)
            be_logger.debug("First 200 chars of cached data: %s",
                            str(redis_data)[:200])
            data.get_AllSeasonsTeamStatDetails_cache = results_data
            be_logger.info(
                "AllSeasonsTeamStatDetails cache was fetched and cached successfully.")
        else:
            be_logger.info("Cache hit, loading cached data...")
            cached_results = pickle.loads(cached_data)
            data.get_AllSeasonsTeamStatDetails_cache = cached_results
            be_logger.info(
                "AllSeasonsTeamStatDetails cache was loaded successfully.")
        be_logger.info(
            f"Count of documents in data.get_AllSeasonsTeamStatDetails_cache: {len(data.get_AllSeasonsTeamStatDetails_cache)}")
        response_data = {
            "live_games": live_games_data,
            "year": current_year,
            "season_type": current_season_type,
            "team_stats": data.get_AllSeasonsTeamStatDetails_cache
        }
        be_logger.info("Returning JSON response...")
        return jsonify(response_data)
    except Exception as e:
        be_logger.error(f"Error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
