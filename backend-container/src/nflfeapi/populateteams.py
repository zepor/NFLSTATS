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
bp_populate_teams = Blueprint('populate_teams', __name__)
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
@log_and_catch_exceptions
@bp_populate_teams.route('/populate-teams', methods=['GET'])
def populate_teams():
    try:
        be_logger.info("/populate-teams being accessed)")
        # Debugging line:
        be_logger.debug(f"Args received from frontend: {str(request.args)}")
        selected_year_from_frontend = request.args.get(
            'year', default=data.selected_year, type=int)
        selected_season_type_from_frontend = request.args.get(
            'season_type', default=data.selected_season_type, type=str)
        # Debugging line:
        be_logger.debug("Selected year from frontend: " +
                        str(selected_year_from_frontend))
        be_logger.debug("Selected season type from frontend: " +
                        selected_season_type_from_frontend)
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

