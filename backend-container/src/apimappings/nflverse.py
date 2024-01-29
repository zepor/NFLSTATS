import sys
import os
from flask import Flask, jsonify, Blueprint
from pymongo import MongoClient
from dotenv import load_dotenv
from src.utils.log import be_logger
from src.database.connections import get_mongodb_connection
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri, r

# Flask and MongoDB Setup
os.environ['R_LIBS_USER'] = '/usr/local/lib/R/site-library'
load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))

nflverse_blueprint = Blueprint('nflverse', __name__)
mongodb_url = os.getenv('MONGODB_URL')
mongodb_database = 'NFLVerse'

flask_app = Flask(__name__)
client = MongoClient(mongodb_url)  # MongoDB connection setup
db = client[mongodb_database]  # Database selection

# Enable DataFrame conversion from R to Pandas
pandas2ri.activate()

# Import the 'nflreadr' R package
nflreadr = importr('nflreadr', lib_loc="/usr/local/lib/R/site-library/")

# Definition for fetching and storing data
def fetch_and_store(load_function_name, collection_name, year=None):
    if year:
        rdf = getattr(nflreadr, load_function_name)(year)
    else:
        rdf = getattr(nflreadr, load_function_name)()
    
    with localconverter(ro.default_converter + pandas2ri.converter):
        df = ro.conversion.rpy2py(rdf)
    # Data conversion and logging
    be_logger.info(str(df.head()))
    data_dict = df.to_dict("records")
    # MongoDB insertion
    collection = db[collection_name]
    collection.insert_many(data_dict)

# Load functions with details: (MongoDB Collection Name, Requires Year, Description)
load_functions = {
    'load_pfr_advstats': ('PFRAdvStats', True, 'Advanced Stats from PFR'),
    'load_ff_playerids': ('FantasyPlayerIDs', False, 'Fantasy Player IDs'),
    'load_ff_rankings': ('FantasyProsRankings', False, 'Latest FantasyPros Rankings'),
    'load_ff_opportunity': ('ExpectedFantasyPoints', False, 'Expected Fantasy Points'),
    'load_teams': ('NFLTeams', False, 'NFL Team Graphics, Colors, and Logos')
}

# Adjust year range for load_pfr_advstats and call fetch_and_store accordingly
for load_func_name, (collection_name, requires_year, description) in load_functions.items():
    year_range = range(2018, 2023) if load_func_name == 'load_pfr_advstats' else range(1999, 2023)
    
    if requires_year:
        for year in year_range:
            try:
                fetch_and_store(load_func_name, collection_name, year)
            except Exception as e:
                print(f"Error fetching {description} ({load_func_name}) for year {year}: {str(e)}")
    else:
        try:
            fetch_and_store(load_func_name, collection_name)
        except Exception as e:
            print(f"Error fetching {description} ({load_func_name}): {str(e)}")

if __name__ == '__main__':
    flask_app.run(debug=True)