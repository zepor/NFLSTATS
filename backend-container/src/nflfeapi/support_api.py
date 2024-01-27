import sys
import os
from datetime import datetime
from flask import request, jsonify, Blueprint, Flask
from flask_cors import CORS, cross_origin
from src.database.connections import get_mongodb_connection
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))  
from pymongo import MongoClient
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
bp_support_api = Blueprint('support_api', __name__)
ip_timestamps = {}
api_key = os.getenv('APIKEY')
mongodb_url = os.getenv('MONGODB_URL')
mongodb_database = os.getenv('MONGODB_DATABASE')

@bp_support_api.route('/submit-support', methods=['OPTIONS', 'POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type', 'Authorization']) # type: ignore
@log_and_catch_exceptions
def submit_support_request():
    if request.method != 'POST':
        return
    data = request.get_json()
    client = get_mongodb_connection()
    if not client:
        be_logger.error("Failed to connect to MongoDB.")
        return make_response(jsonify({"error": "Database connection failed"}), 500)
    db = client["Current_Season"]
    collection = db["SupportEmails"]
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

    if not email or "@" not in email:
        return jsonify({"error": "Invalid email address"}), 400
    user_ip = request.remote_addr
    if user_ip in ip_timestamps:
        last_timestamp = ip_timestamps[user_ip]
        days_diff = (datetime.now() - last_timestamp).days
        if days_diff < 1:
            return jsonify({"error": "You have already submitted today. Please try again tomorrow."}), 400
    support_request = {
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "timestamp": datetime.now()
    }
    try:
        collection.insert_one(support_request)
    except Exception as e:
        be_logger.error("Error inserting suppoert request: %s", str(e))
        return jsonify({"error": "Error inserting support request"}), 500
    ip_timestamps[user_ip] = datetime.now()
    return jsonify({"message": "Support request submitted successfully"}), 200

