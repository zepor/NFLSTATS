import os
from security import safe_requests

if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
from mongoengine import connect
from src.models.seasons import(SeasonInfo)
from src.models.team_info import(TeamInfo)
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
from dotenv import load_dotenv
load_dotenv()
connection_string = os.getenv('MONGODB_URL')
if not connection_string:
    raise Exception("MONGO_CONNECTION_STRING must be set")
connect(db='Current_Season', host=connection_string)

from datetime import datetime
import requests
API_KEY = os.getenv('APIKEY')
URL = "http://api.sportradar.us/nfl/official/trial/v7/en/seasons/{SEASONYEAR}/{SEASONTYPE}/teams/{TeamID}/statistics.json?api_key={API_KEY}"
TEAMID = list({team.id for team in TeamInfo.objects.only("id")})
SEASONYEAR = list({season.year for season in SeasonInfo.objects.only("year")})
SEASONTYPE = list(
    {season["type"] for season in SeasonInfo.objects.only("type")}
)
print(SEASONYEAR)
print(TEAMID)
print(SEASONTYPE)

counter = 0
try:
    for team_id in TEAMID:
        for year in SEASONYEAR:
            for season_type in SEASONTYPE:
                constructed_url = URL.format(SEASONYEAR=year, SEASONTYPE=season_type, TeamID=team_id)
                print(datetime.now(), "Constructed URL:", constructed_url)
                try:
                    response = safe_requests.get(constructed_url)
                    if response.status_code != 200:
                        print(f"Error: API call to {constructed_url} returned status code: {response.status_code}")
                except requests.exceptions.RequestException as req_e:
                    print(f"API request error for {constructed_url}. Error: {req_e}")
                counter += 1
                if counter >= 40:
                    break
            if counter >= 40:
                break
        if counter >= 40:
            break
except Exception as e:
    print(f"Error: {str(e)}")
