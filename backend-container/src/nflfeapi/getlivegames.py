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
bp_live_games = Blueprint('live_games', __name__)
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
@log_and_catch_exceptions
@bp_live_games.route("/livegames", methods=['GET'])
def live_games():
    if games_data := fetch_live_games_data():
        return jsonify(games_data)
    else:
        return Response(json.dumps({"error": "Query is already running or an error occurred"}), status=500, mimetype='application/json')
