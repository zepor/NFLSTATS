import sys
import os
from src.database.rediscache import data
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))  

@log_and_catch_exceptions
def get_year_season_combinations(current_year, current_season_type):
    if data.year_season_combinations_cache:
        be_logger.info("get_year_season_combinations: Data in Cache: Yes")
    else:
        be_logger.info("get_year_season_combinations: Data in Cache: No")
        season_type_mapping = {
            "PRE": "Pre-Season",
            "REG": "Regular Season",
            "PST": "Playoffs"
        }
        season_type_order = {"PRE": 0, "REG": 1, "PST": 2}
        year_season_combinations = set()
        current_combo = {
            "year": current_year,
            "season_type": season_type_mapping[current_season_type]
        }
        for item in data.get_AllSeasonsTeamStatDetails_cache:
            if all(k in item["_id"] for k in ("year", "season_type")) and "games_played" in item["seasonStatTeam"] and item["seasonStatTeam"]["games_played"] > 1:
                season_type_db = item["_id"]["season_type"]
                year = item["_id"]["year"]
                if year != current_year or season_type_db != current_season_type:
                    season_type = season_type_mapping.get(
                        season_type_db, season_type_db)
                    combo = {"year": year, "season_type": season_type}
                    year_season_combinations.add(frozenset(combo.items()))
        year_season_combinations = [
            dict(combo) for combo in sorted(
                year_season_combinations,
                key=lambda x: (x['year'], season_type_order[x['season_type']]),
                reverse=True
            )
        ]
        year_season_combinations.insert(0, current_combo)
        be_logger.info(
            f"get_year_season_combinations:Number Items in Season Dropdown:{len(year_season_combinations)}")
        be_logger.debug(
            f"get_year_season_combinations:Sample year-season combinations: {year_season_combinations[:4]}")
        data.year_season_combinations_cache = year_season_combinations
    return data.year_season_combinations_cache