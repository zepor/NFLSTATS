import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))  
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Blueprint
bp_get_data = Blueprint('get_data', __name__)
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
@log_and_catch_exceptions
@bp_get_data.route('/get-data', methods=['GET'])
def get_data():
    try:
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
            be_logger.error(
                "get_data: structure_data_for_categories() returned None")
            return jsonify({"error": "Error in getting top 10 data"}), 500
        else:
            be_logger.info(
                "get_data: Fetched data with structure_data_for_categories as it was not found in cache")
        if not data.year_season_combinations_cache:
            data.year_season_combinations_cache = get_year_season_combinations(
                data.selected_year, data.selected_season_type)
            be_logger.info(
                f"get_data: Number of Documents returned to year_season_combinations_cache: {len(data.year_season_combinations_cache)}")
        if key in data.teams_dict_cache:
            be_logger.debug(
                f"get_data: Teams_dict_cache content: {data.teams_dict_cache[key][1:4]}"
            )
        else:
            be_logger.warning(
                f"get_data: Key {key} not found in data.teams_dict_cache")
        data.selected_teams = data.teams_dict_cache.get(key, [])
        be_logger.info(
            f"get_data: Selected Teams (first 2): {data.selected_teams[:2]}")
        team_top_10_data = data.team_top_10_data_cache.get(key)
        if team_top_10_data is None:  # Add this check
            be_logger.error(
                f"get_data: No team top 10 data Cache: {data.team_top_10_data_cache}")
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