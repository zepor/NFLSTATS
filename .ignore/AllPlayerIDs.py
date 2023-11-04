import sys
sys.path.append('..')
sys.path.append('D:\\Program Files\\Server\\Apache24\\htdocs')
from pymongo import MongoClient
from mongoengine import connect
from dotenv import load_dotenv
load_dotenv()
import datetime
import uuid 
from src.models.team_info import(coach, rgb_color, team, team_color, TeamInfo)

mongodb_service_name = os.getenv('MONGODB_SERVICE_NAME', 'localhost')
mongodb_url = os.getenv('MONGODB_URL', f"mongodb://{mongodb_service_name}:27017/current_season")
client = MongoClient(mongodb_url, connectTimeoutMS=30000, socketTimeoutMS=None)
db = MongoEngine(app)

player_ids_cursor = db.PlayerDCIinfo.find({}, {"_id": 1})

# To print them out
for player in player_ids_cursor:
    print(player.get('_id'))





