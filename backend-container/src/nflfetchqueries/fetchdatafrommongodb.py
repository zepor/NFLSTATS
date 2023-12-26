import sys
import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))  

@log_and_catch_exceptions
def fetch_data_from_mongodb(year, season_type, view_mode, team, stat_category):
    # Build your MongoDB query based on the filters
    if view_mode == "team":
        if stat_category == "passing":
            # Example: Fetching passing stats for teams
            records = SeasonStatTeam.objects(
                year=year, season_type=season_type, team=team).all()
            for record in records:
                fetched_data.append({
                    "team": record.team,
                    "passing_yards": record.passing.yards,
                    "passing_touchdowns": record.passing.touchdowns,
                    # ... add other relevant fields
                })
            headers = ["team", "passing_yards", "passing_touchdowns"]
            # ... add other relevant headers
        # Add more conditions for other stat categories
    elif view_mode == "player":
        # Similar logic for fetching player stats
        # ...
        # Always return a tuple (data, headers)
        return fetched_data, headers
    return [], []