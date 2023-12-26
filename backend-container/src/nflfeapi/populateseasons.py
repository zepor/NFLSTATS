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
bp_populate_seasons = Blueprint('populate_seasons', __name__)
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
@log_and_catch_exceptions
@bp_populate_seasons.route('/populate-seasons', methods=['GET'])
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