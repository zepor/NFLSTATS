import sys
import os
import pickle
from datetime import datetime
from src.utils.log import be_logger
from src.database.connections import connect_to_redis

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root) 
sys.path.append(os.path.join(project_root, 'src'))

class FootballData:
    def __init__(self):
        self.livegames_cache = None
        self.get_AllSeasonsTeamStatDetails_cache = None
        self.current_year_season_cache = None
        self.year_season_combinations_cache = None
        self.teams_dict_cache = {}
        self.selected_teams_stats_cache = {}
        self.team_top_10_data_cache = {}
        self.selected_year = None
        self.selected_season_type = None
        self.selected_team = None
        self.selected_teams = {}
        self.last_refreshed = datetime.now()
data = FootballData()
cache_key = 'football_data_cache'
cache_expiration = 3600  # 1 hour in seconds
redis_primary_host = os.getenv('REDIS_PRIMARY_HOST', 'redis')
redis_fallback_host = os.getenv('REDIS_FALLBACK_HOST', 'redis-service')
redis_client = connect_to_redis(redis_primary_host, redis_fallback_host)
serialized_data = pickle.dumps(data)
redis_client.setex(cache_key, cache_expiration, serialized_data)
cached_data = redis_client.get(cache_key)
if cached_data is not None:
    try:
        data = pickle.loads(cached_data)
        be_logger.info("Successfully loaded data from cache.")
    except pickle.PickleError as e:
        be_logger.error("Failed to deserialize data from cache: %s", e)
def clear_cache(redis_client, cache_key):
    redis_client.delete(cache_key)
    be_logger.info("Cache cleared.")
