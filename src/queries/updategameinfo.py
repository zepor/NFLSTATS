import sys
sys.path.append('..')
from pymongo import MongoClient
from bson.binary import Binary
import base64
from mongoengine import connect
from dotenv import load_dotenv
load_dotenv()


# Setup MongoDB
mongodb_service_name = os.getenv('MONGODB_SERVICE_NAME', 'localhost')
mongodb_url = os.getenv('MONGODB_URL', f"mongodb://{mongodb_service_name}:27017/current_season")
client = MongoClient(mongodb_url, connectTimeoutMS=30000, socketTimeoutMS=None)
db = MongoEngine(app)
gameinfo_collection = db['GameInfo']
league_info = db['league_info'].find_one()

for season in league_info['season']:
    seasonid = Binary(base64.b64decode(season['id']['$binary']['base64']))
    for week in league_info['leagueweek']:s
        leagueweek = Binary(base64.b64decode(week['id']['$binary']['base64']))
        # update all GameInfo documents for the given season and week
        gameinfo_collection.update_many(
            {
                "gamegame.scheduled": {
                    "$gte": datetime.datetime(season['year'], 1, 1),
                    "$lt": datetime.datetime(season['year'] + 1, 1, 1)
                }
            },
            {
                "$set": {
                    "seasonid": seasonid,
                    "leagueweek": leagueweek
                }
            }
        )
