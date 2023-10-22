import sys
sys.path.append('..')
from pymongo import MongoClient
from mongoengine import connect
import datetime
import uuid 
from dotenv import load_dotenv
load_dotenv()
# Setup MongoDB
mongodb_service_name = os.getenv('MONGODB_SERVICE_NAME', 'localhost')
mongodb_url = os.getenv('MONGODB_URL', f"mongodb://{mongodb_service_name}:27017/current_season")
client = MongoClient(mongodb_url, connectTimeoutMS=30000, socketTimeoutMS=None)
db = MongoEngine(app)
nfl_weeks = {}
start_date = datetime.datetime(2001, 1, 1)
end_date = datetime.datetime(2024, 12, 31)

# Extract year, type, title, and sequence from league_info collection
league_info = db['league_info'].find({}, {"season.year": 1, "season.type": 1, "leagueweek.title": 1, "leagueweek.sequence": 1})

for info in league_info:
    for season in info['season']:
        year = season['year']
        type_ = season['type']
        
        for week in info['leagueweek']:
            title = week['title']
            sequence = week['sequence']
            if year not in nfl_weeks:
                nfl_weeks[year] = []
            nfl_weeks[year].append({
                'year': year,
                'season_type': type_,
                'week': sequence,
                'title': title,
                'min_date': '',
                'max_date': ''
            })

        pipeline = [
    {
        "$addFields": {
            "gamegame.seasonid": { "$toString": "$gamegame.seasonid" },
            "gamegame.leagueweek": { "$toString": "$gamegame.leagueweek" }
        }
    },
    {
        "$lookup": {
            "from": "league_info",
            "let": { "seasonid": "$gamegame.seasonid", "leagueweek": "$gamegame.leagueweek" },
            "pipeline": [
                { "$unwind": "$season" },
                { "$unwind": "$leagueweek" },
                {
                    "$match": {
                        "$expr": {
                            "$and": [
                                { "$eq": ["$season._id", "$$seasonid"] },
                                { "$eq": ["$leagueweek._id", "$$leagueweek"] }
                            ]
                        }
                    }
                }
            ],
            "as": "league_info"
        }
    },
    {
        "$unwind": "$league_info"
    },
    {
        "$group": {
            "_id": {
                "year": "$league_info.season.year",
                "season_type": "$league_info.season.type",
                "week": "$league_info.leagueweek.sequence"
            },
            "min_date": { "$min": "$gamegame.scheduled" },
            "max_date": { "$max": "$gamegame.scheduled" }
        }
    },
    {
        "$addFields": {
            "min_date_month": {
                "$let": {
                    "vars": {
                        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                    },
                    "in": {
                        "$arrayElemAt": ["$$months", { "$subtract": [{ "$month": "$min_date" }, 1] }]
                    }
                }
            },
            "min_date_day": { "$dayOfMonth": "$min_date" },
            "max_date_month": {
                "$let": {
                    "vars": {
                        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                    },
                    "in": {
                        "$arrayElemAt": ["$$months", { "$subtract": [{ "$month": "$max_date" }, 1] }]
                    }
                }
            },
            "max_date_day": { "$dayOfMonth": "$max_date" }
        }
    },
    {
        "$project": {
            "year": "$_id.year",
            "season_type": "$_id.season_type",
            "week": "$_id.week",
            "min_date": {
                "$concat": ["$min_date_month", "/", { "$toString": "$min_date_day" }]
            },
            "max_date": {
                "$concat": ["$max_date_month", "/", { "$toString": "$max_date_day" }]
            },
            "_id": 0
        }
    },
    {
        "$sort": {
            "year": 1,
            "week": 1
        }
    }
]



result = db.GameInfo.aggregate(pipeline)
for doc in result:
    year = doc['year']
    season_type = doc['season_type']
    week = doc['week']
    min_date = doc['min_date']
    max_date = doc['max_date']
    
    if year in nfl_weeks:
        for entry in nfl_weeks[year]:
            if entry['season_type'] == season_type and entry['week'] == week:
                entry['min_date'] = min_date
                entry['max_date'] = max_date
                break

# Print the nfl_weeks dictionary
for year, weeks in nfl_weeks.items():
    print(f'Year: {year}')
    for week in weeks:
        print(week)



