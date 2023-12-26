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
from flask import request, jsonify, Blueprint
bp_support_api = Blueprint('support_api', __name__)
from src.database.connections import get_mongodb_connection
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
load_dotenv()
ip_timestamps = {}
@bp_support_api.route('/api/submit-support', methods=['OPTIONS', 'POST'])
def submit_support_request():
    if request.method == 'OPTIONS':
        return handle_preflight_request()
    
    data = request.get_json()
    client = get_mongodb_connection()
    db = client['Current_Season']
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')
    if not email or "@" not in email:
        return jsonify({"error": "Invalid email address"}), 400
    user_ip = request.remote_addr
    if last_timestamp := ip_timestamps.get(user_ip):
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
        db.SupportEmails.insert_one(support_request)
    except Exception as e:
        return jsonify({"error": "Error inserting support request"}), 500
    ip_timestamps[user_ip] = datetime.now()
    return jsonify({"message": "Support request submitted successfully"}), 200

def handle_preflight_request():
    response = jsonify({})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
