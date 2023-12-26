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
def get_or_generate_teams():
    base_image_url = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/{TeamAlias}.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true"
    default_team_entry = {"name": "All Teams", "imageLink": ""}
    teams = data.get_AllSeasonsTeamStatDetails_cache
    cache = {}
    for team in teams:
        # Check if keys exist before accessing
        if "_id" in team and "year" in team["_id"] and "season_type" in team["_id"]:
            year = team["_id"]["year"]
            season_type = team["_id"]["season_type"]
            if f"{year}_{season_type}" not in cache:
                matched_data = [team for team in teams if (team["_id"]["year"] == year and team["_id"]["season_type"] == season_type
                                                           and ('seasonStatTeam' in team and 'games_played' in team['seasonStatTeam'] and int(team['seasonStatTeam']['games_played']) > 0))]
                teams_for_combo = [{"name": f"{team['teamInfo']['team']['market']} {team['teamInfo']['team']['name']}" if team['teamInfo']['team']['name'] and team['teamInfo']['team']['market'] else "",
                                    "imageLink": base_image_url.format(TeamAlias=team['teamInfo']['team']['alias'])}
                                   for team in matched_data]
                teams_for_combo = sorted(
                    teams_for_combo, key=lambda x: x["name"].split(" ")[0])
                teams_for_combo.insert(0, default_team_entry)

                key = f"{year}_{season_type}"
                cache[key] = teams_for_combo

                # Debugging log to print the key and the list of teams for this year and season type
                be_logger.debug(
                    f"Key: {key}, Team Count: {len(teams_for_combo)}")
    data.teams_dict_cache = cache
    return data.teams_dict_cache