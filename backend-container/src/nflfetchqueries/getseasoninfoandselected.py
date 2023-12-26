import sys
import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from src.database.rediscache import data
from src.models.seasons import SeasonInfo
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))

@log_and_catch_exceptions
def get_season_info_and_selected(request):
    be_logger.info("Called get_season_info_and_selected function")
    if not data.current_year_season_cache:
        be_logger.info("get_season_info_and_selected: Data in Cache: NO")
        current_season = SeasonInfo.objects(status="inprogress").first()
        current_year = current_season.year
        current_season_type = current_season.type
        data.current_year_season_cache = current_year, current_season_type, None, None
    else:
        be_logger.info("get_season_info_and_selected: Data in Cache: Yes")
        current_year, current_season_type, _, _ = data.current_year_season_cache
    data.selected_year = request.args.get('year', default=current_year)
    data.selected_season_type = request.args.get(
        'season_type', default=current_season_type)
    be_logger.info(
        f"get_season_info_and_selected:Current Season:{current_year} {current_season_type}")
    data.current_year_season_cache = current_year, current_season_type, data.selected_year, data.selected_season_type
    be_logger.info("About to exit get_season_info_and_selected function")
    return data.current_year_season_cache







