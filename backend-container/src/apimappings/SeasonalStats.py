import sys
sys.path.append('..')
import requests, pandas, json
from requests.exceptions import RequestException
from flask import Blueprint, jsonify, Flask
import os, time
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
from pymongo import MongoClient
from datetime import datetime
from uuid import UUID
import json
from mongoengine import connect
from models.seasons import(SeasonInfo) 
from models.player_DCI_info import(player, prospect, primary, position, practice, injury, PlayerDCIinfo)
from models.season_stat_oppo_info import(SeasonStatOppo, intreturns, passing, receiving,
defense, receiving, defense, thirddown,fourthdown,goaltogo, redzone, kicks, fieldgoals,
punts, rushing, kickreturns, puntreturns, miscreturns, record,  conversions,
kickoffs, fumbles, penalties, touchdowns, interceptions, firstdowns)
from models.season_stat_team_info import(SeasonStatTeam, intreturns, passing,
receiving, defense, thirddown,fourthdown,goaltogo, redzone, kicks, fieldgoals, punts, 
rushing, kickreturns, puntreturns, record, conversions, kickoffs, fumbles, penalties,
touchdowns, interceptions, firstdowns)
from models.season_stat_player_info import(SeasonStatPlayer, intreturns, 
passing, receiving, defense, fieldgoals, punts, rushing, extrapoints, 
kickreturns, puntreturns, conversions, kickoffs, fumbles, penalties)                                        
from models.team_info import(coach, rgb_color, team, team_color, TeamInfo)
from flask_mongoengine import MongoEngine
from mongoengine import (DoesNotExist, DecimalField, EmbeddedDocumentField, Document,
 StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, 
 EmbeddedDocumentListField)
from bson import ObjectId
import logging
from dotenv import load_dotenv
load_dotenv()

bp = Blueprint('SeasonalStats', __name__)
@bp.route('/SeasonalStats', methods=['GET'])
def fetch_and_save_seasonal_stats():
    logging.basicConfig(filename='SeasonalStats.log', level=logging.INFO)
    logger = logging.getLogger('SeasonalStats')
    logger.info("SeasonalStats called")
    logging.info("SeasonalStats called")
    API_KEY = os.getenv('APIKEY')
    URL = "http://api.sportradar.us/nfl/official/trial/v7/en/seasons/{SEASONYEAR}/{SEASONTYPE}/teams/{TEAMID}/statistics.json?api_key={API_KEY}"
    TEAMID =  list(set([team.id for team in TeamInfo.objects.only("id")]))
    SEASONYEAR = [2023]
    #list(set([season.year for season in SeasonInfo.objects.only("year")]))
    SEASONTYPE = ['REG']
    #list(set([season["type"] for season in SeasonInfo.objects.only("type")]))
    def make_api_call(url):
        MAX_RETRIES = 3
        RETRY_DELAY = 10  # wait 10 seconds before retrying in case of a 403 error
        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.HTTPError as http_err:
                if response.status_code == 403:
                    logger.error(f"API call to {url} returned status code 403. Retrying in {RETRY_DELAY} seconds.")
                    time.sleep(RETRY_DELAY)
                    retries += 1
                else:
                    logger.error(f"HTTP error occurred: {http_err}")
                    raise
            except Exception as err:
                logger.error(f"Other error occurred: {err}")
                raise
        logger.error(f"Max retries reached for URL: {url}. Skipping...")
        return None
    total_mapped_seasons = 0
    total_mapped_players = 0
    total_mapped_opposeasonalstats = 0
    total_mapped_player_seasonal_stat = 0
    total_mapped_team_seasonal_stat = 0
    total_mapped_teams = 0
    try:
        for team_id in TEAMID:
            for year in SEASONYEAR:
                for season_type in SEASONTYPE:
                    constructed_url = URL.format(SEASONYEAR=year, SEASONTYPE=season_type, TEAMID=team_id)
                    logging.info(f"{datetime.now()} - Requesting URL: {constructed_url}")
                    try:
                        response = requests.get(constructed_url)
                        logging.info(f"Response status code: {response.status_code}")
                        if response.status_code != 200:
                            logger.error(f"API call to {constructed_url} returned status code: {response.status_code}")
                            # Continue to the next iteration if this URL fails
                            continue 
                    except RequestException as req_e:
                        logger.error(f"API request error for {constructed_url}. Error: {req_e}")
                        continue  # Continue to the next iteration if there's an error making the request
                    data = response.json()    
                    logger.info(f"Team Profile Data for TeamID {TEAMID},Year {SEASONYEAR}, SeaosnType {SEASONTYPE} fetched and saved successfully")         
                    # Extract and map season info
                    mapped_seasons = {}  # Initialize an empty dictionary
                    season_info = extract_season_info(data)
                    mapped_season = map_season_info(season_info)
                    mapped_seasons[season_info['id']] = mapped_season
                    total_mapped_seasons += len(mapped_seasons)
                    # Extract and map player info
                    player_info = extract_player_info(data)
                    mapped_players = map_player_info(player_info)
                    total_mapped_players += len(mapped_players)
                    # Extract and map OpponenetSeasonalTeamStats
                    opponenetseasondata = extract_oppo_seasonal_stats_info(data)
                    total_mapped_opposeasonalstats += len(opponenetseasondata)
                    # Extract and map player season stat info
                    playerseasondata = extract_player_seasonal_stat_info(data)
                    total_mapped_player_seasonal_stat += len(playerseasondata)
                    # Extract and map team stat info
                    teamseasondata = extract_team_seasonal_stat_info(data)
                    total_mapped_team_seasonal_stat += len(teamseasondata)
                    # Extract and map team info
                    team_info_dict = extract_team_info(data)
                    total_mapped_teams += len(team_info_dict)
                    # Log keys of data being passed to save_to_database
                    #logger.info(f"Keys being passed to save_to_database for team_id: {team_id}, year: {year}, season_type: {season_type}:")
                    #logger.info(f"mapped_seasons keys: {list(mapped_seasons.keys())}")
                    #logger.info(f"mapped_players keys: {list(mapped_players.keys())}")
                    #logger.info(f"opponenetseasondata keys: {list(opponenetseasondata.keys())}")
                    #logger.info(f"teamseasondata keys: {list(teamseasondata.keys())}")
                    #logger.info(f"playerseasondata keys: {list(playerseasondata.keys())}")
                    #logger.info(f"team_info_dict keys: {list(team_info_dict.keys())}")
                    logger.info(f"Keys being passed to save_to_database for team_id: {team_id}, year: {year}, season_type: {season_type}:")
                    logger.info(f"mapped_seasons keys count: {len(mapped_seasons.keys())}")
                    logger.info(f"mapped_players keys count: {len(mapped_players.keys())}")
                    logger.info(f"opponenetseasondata keys count: {len(opponenetseasondata.keys())}")
                    logger.info(f"teamseasondata keys count: {len(teamseasondata.keys())}")
                    logger.info(f"playerseasondata keys count: {len(playerseasondata.keys())}")
                    logger.info(f"team_info_dict keys count: {len(team_info_dict.keys())}")
                    # Save mapped data to the database
                    save_to_database(mapped_seasons, mapped_players, opponenetseasondata, teamseasondata, playerseasondata, team_info_dict)     
                    # Add a delay between requests to avoid rate limiting
                    time.sleep(2)
        logger.info(f"Total mapped Seasons: {total_mapped_seasons}")
        logger.info(f"Total mapped Players: {total_mapped_players}")
        logger.info(f"Total mapped Opponenent Team Season Stats: {total_mapped_opposeasonalstats}")
        logger.info(f"Total mapped Player Season Stats: {total_mapped_player_seasonal_stat}")
        logger.info(f"Total mapped Team Season Stats: {total_mapped_team_seasonal_stat}")
        logger.info(f"Total mapped Teams: {total_mapped_teams}")
        return "Team Profile Data Fetched and Saved Successfully"
    except Exception as e:
        logger.exception("An error occurred:")
        return f"Error: {str(e)}", 500
def extract_season_info(data):
    season_data = {
        "id": data.get("season", {}).get("id"),
        "year": data.get("season", {}).get("year"),
        "type": data.get("season", {}).get("type")
    }
    logging.info("Extracted season data:", season_data)
    return season_data
def map_season_info(season_data):
    # Print the type and value of season_data for debugging
    logging.info(f"Type of season_data: {type(season_data)}")
    logging.info("Value of season_data:", season_data)
    # Directly mapping the season_data without iterating over its items
    season_instance = SeasonInfo(
        _id=season_data["id"],
        year=season_data["year"],
        type=season_data["type"]
    )
    # Print the mapped season_instance for debugging
    logging.info("Mapped season instance: %s", season_instance)  
    return season_instance
def extract_player_info(data):
    players_data = data.get('players', [])
    extracted_players = {}
    for player_data in players_data:
        player_id = player_data.get("id")  # Based on your sample data
        if not player_id:
            logging.info(f"Debug: Player without ID: {player_data}")
            continue
        extracted_players[player_id] = {
            "fullname": player_data.get("name"),  # Changed based on your sample data
            "id": player_id,
            "jersey": player_data.get("jersey"),
            "position": player_data.get("position")
        }
    logging.info(f"Number of players extracted: {len(extracted_players)}")
    return extracted_players
def map_player_info(extracted_players):
    mapped_players = {}
    for player_id, player_data in extracted_players.items():
        if not player_id:
            logging.info(f"Debug: Player data without ID during mapping: {player_data}")
            continue
        player_instance = player(
                fullname=player_data["fullname"],
                id=player_data["id"],
                jersey=player_data["jersey"],
                position=player_data["position"]
        )
        player_dci_info_instance = PlayerDCIinfo(playerinfo=player_instance)
        mapped_players[player_id] = player_dci_info_instance
    logging.info(f"Number of players mapped: {len(mapped_players)}")
    return mapped_players
def extract_oppo_seasonal_stats_info(data):
    teamid = str(data.get("id"))
    seasonid = str(data.get("season", {}).get("id"))
    oppo_stats = data.get('opponents', {})
    key = (teamid, seasonid)
    opponenetseasondata = {key: {}}
    opponenetseasondata_main = opponenetseasondata[key]
    opponenetseasondata_main.update({
        "teamid": teamid,
        "seasonid": seasonid,
        "opponents_played": oppo_stats.get("games_played"),
        "touchdowns": {
            "passing": oppo_stats.get("touchdowns", {}).get("pass"),
            "rush": oppo_stats.get("touchdowns", {}).get("rush"),
            "totalreturn": oppo_stats.get("touchdowns", {}).get("total_return"),
            "total": oppo_stats.get("touchdowns", {}).get("total"),
            "fumblereturn": oppo_stats.get("touchdowns", {}).get("fumble_return"),
            "intreturn": oppo_stats.get("touchdowns", {}).get("int_return"),
            "kickreturn": oppo_stats.get("touchdowns", {}).get("kick_return"),
            "puntreturn": oppo_stats.get("touchdowns", {}).get("punt_return"),
            "other": oppo_stats.get("touchdowns", {}).get("other")
        },
        "rushing": {
            "avgyards": oppo_stats.get("rushing", {}).get("avg_yards"),
            "attempts": oppo_stats.get("rushing", {}).get("attempts"),
            "touchdowns": oppo_stats.get("rushing", {}).get("touchdowns"),
            "tlost": oppo_stats.get("rushing", {}).get("tlost"),
            "tlostyards": oppo_stats.get("rushing", {}).get("tlost_yards"),
            "yards": oppo_stats.get("rushing", {}).get("yards"),
            "longest": oppo_stats.get("rushing", {}).get("longest"),
            "longesttouchdown": oppo_stats.get("rushing", {}).get("longest_touchdown"),
            "redzoneattempts": oppo_stats.get("rushing", {}).get("redzone_attempts"),
            "brokentackles": oppo_stats.get("rushing", {}).get("broken_tackles"),
            "kneeldowns": oppo_stats.get("rushing", {}).get("kneel_downs"),
            "scrambles": oppo_stats.get("rushing", {}).get("scrambles"),
            "yardsaftercontact": oppo_stats.get("rushing", {}).get("yards_after_contact")
        },
        "receiving": {
            "targets": oppo_stats.get("receiving", {}).get("targets"),
            "receptions": oppo_stats.get("receiving", {}).get("receptions"),
            "avgyards": oppo_stats.get("receiving", {}).get("avg_yards"),
            "yards": oppo_stats.get("receiving", {}).get("yards"),
            "touchdowns": oppo_stats.get("receiving", {}).get("touchdowns"),
            "yardsaftercatch": oppo_stats.get("receiving", {}).get("yards_after_catch"),
            "longest": oppo_stats.get("receiving", {}).get("longest"),
            "longesttouchdown": oppo_stats.get("receiving", {}).get("longest_touchdown"),
            "redzonetargets": oppo_stats.get("receiving", {}).get("redzone_targets"),
            "airyards": oppo_stats.get("receiving", {}).get("air_yards"),
            "brokentackles": oppo_stats.get("receiving", {}).get("broken_tackles"),
            "droppedpasses": oppo_stats.get("receiving", {}).get("dropped_passes"),
            "catchablepasses": oppo_stats.get("receiving", {}).get("catchable_passes"),
            "yardsaftercontact": oppo_stats.get("receiving", {}).get("yards_after_contact")
        },
        "punts": {
            "attempts": oppo_stats.get("punts", {}).get("attempts"),
            "yards": oppo_stats.get("punts", {}).get("yards"),
            "netyards": oppo_stats.get("punts", {}).get("net_yards"),
            "blocked": oppo_stats.get("punts", {}).get("blocked"),
            "touchbacks": oppo_stats.get("punts", {}).get("touchbacks"),
            "inside20": oppo_stats.get("punts", {}).get("inside_20"),
            "returnyards": oppo_stats.get("punts", {}).get("return_yards"),
            "avgnetyards": oppo_stats.get("punts", {}).get("avg_net_yards"),
            "avgyards": oppo_stats.get("punts", {}).get("avg_yards"),
            "longest": oppo_stats.get("punts", {}).get("longest"),
            "hangtime": oppo_stats.get("punts", {}).get("hang_time"),
            "avghangtime": oppo_stats.get("punts", {}).get("avg_hang_time")
        },
        "puntreturns":{
            "avgyards": oppo_stats.get("punt_returns", {}).get("avg_yards"),
            "returns": oppo_stats.get("punt_returns", {}).get("returns"),
            "yards": oppo_stats.get("punt_returns", {}).get("yards"),
            "longest": oppo_stats.get("punt_returns", {}).get("longest"),
            "touchdowns": oppo_stats.get("punt_returns", {}).get("touchdowns"),
            "longesttouchdown": oppo_stats.get("punt_returns", {}).get("longest_touchdown"),
            "faircatches": oppo_stats.get("punt_returns", {}).get("faircatches")
        },
        "penalties":{
            "penalties": oppo_stats.get("penalties", {}).get("penalties"),
            "yards": oppo_stats.get("penalties", {}).get("yards")
        },
        "passing":{
            "attempts": oppo_stats.get("passing", {}).get("attempts"),
            "completions": oppo_stats.get("passing", {}).get("completions"),
            "comppct": oppo_stats.get("passing", {}).get("cmp_pct"),
            "interceptions": oppo_stats.get("passing", {}).get("interceptions"),
            "sackyards": oppo_stats.get("passing", {}).get("sack_yards"),
            "rating": oppo_stats.get("passing", {}).get("rating"),
            "touchdowns": oppo_stats.get("passing", {}).get("touchdowns"),
            "avgyards": oppo_stats.get("passing", {}).get("avg_yards"),
            "sacks": oppo_stats.get("passing", {}).get("sacks"),
            "longest": oppo_stats.get("passing", {}).get("longest"),
            "longesttouchdown": oppo_stats.get("passing", {}).get("longest_touchdown"),
            "airyards": oppo_stats.get("passing", {}).get("air_yards"),
            "redzoneattempts": oppo_stats.get("passing", {}).get("redzone_attempts"),
            "netyards": oppo_stats.get("passing", {}).get("net_yards"),
            "yards": oppo_stats.get("passing", {}).get("yards"),
            "grossyards": oppo_stats.get("passing", {}).get("gross_yards"),
            "inttouchdowns": oppo_stats.get("passing", {}).get("int_touchdowns"),
            "throwaways": oppo_stats.get("passing", {}).get("throw_aways"),
            "poorthrows": oppo_stats.get("passing", {}).get("poor_throws"),
            "defendedpasses": oppo_stats.get("passing", {}).get("defended_passes"),
            "droppedpasses": oppo_stats.get("passing", {}).get("dropped_passes"),
            "spikes": oppo_stats.get("passing", {}).get("spikes"),
            "blitzes": oppo_stats.get("passing", {}).get("blitzes"),
            "hurries": oppo_stats.get("passing", {}).get("hurries"),
            "knockdowns": oppo_stats.get("passing", {}).get("knockdowns"),
            "pockettime": oppo_stats.get("passing", {}).get("pocket_time"),
            "battedpasses": oppo_stats.get("passing", {}).get("batted_passes"),
            "ontargetthrows": oppo_stats.get("passing", {}).get("on_target_throws")
        },
        "kickoffs":{
            "endzone": oppo_stats.get("kickoffs", {}).get("endzone"),
            "inside20": oppo_stats.get("kickoffs", {}).get("inside_20"),
            "returnyards": oppo_stats.get("kickoffs", {}).get("return_yards"),
            "returned": oppo_stats.get("kickoffs", {}).get("returned"),
            "touchbacks": oppo_stats.get("kickoffs", {}).get("touchbacks"),
            "yards": oppo_stats.get("kickoffs", {}).get("yards"),
            "outofbounds": oppo_stats.get("kickoffs", {}).get("out_of_bounds"),
            "kickoffs": oppo_stats.get("kickoffs", {}).get("kickoffs"),
            "onsideattempts": oppo_stats.get("kickoffs", {}).get("onside_attempts"),
            "onsidesuccesses": oppo_stats.get("kickoffs", {}).get("onside_successes"),
            "squibkicks": oppo_stats.get("kickoffs", {}).get("squib_kicks")
        },
        "kickreturns":{
            "avgyards": oppo_stats.get("kick_returns", {}).get("avg_yards"),
            "yards": oppo_stats.get("kick_returns", {}).get("yards"),
            "longest": oppo_stats.get("kick_returns", {}).get("longest"),
            "touchdowns": oppo_stats.get("kick_returns", {}).get("touchdowns"),
            "longesttouchdown": oppo_stats.get("kick_returns", {}).get("longest_touchdown"),
            "faircatches": oppo_stats.get("kick_returns", {}).get("faircatches"),
            "returns": oppo_stats.get("kick_returns", {}).get("returns")
        },
        "interceptions":{
            "returnyards": oppo_stats.get("interceptions", {}).get("return_yards"),
            "returned": oppo_stats.get("interceptions", {}).get("returned"),
            "interceptions": oppo_stats.get("interceptions", {}).get("interceptions"),
        },
        "intreturns": {
            "avgyards": oppo_stats.get("int_returns", {}).get("avg_yards"),
            "yards": oppo_stats.get("int_returns", {}).get("yards"),
            "longest": oppo_stats.get("int_returns", {}).get("longest"),
            "touchdowns": oppo_stats.get("int_returns", {}).get("touchdowns"),
            "longesttouchdown": oppo_stats.get("int_returns", {}).get("longest_touchdown"),
            "returns": oppo_stats.get("int_returns", {}).get("returns")
        },
        "fumbles": {
            "fumbles": oppo_stats.get("fumbles", {}).get("fumbles"),
            "lostfumbles": oppo_stats.get("fumbles", {}).get("lost_fumbles"),
            "ownrec": oppo_stats.get("fumbles", {}).get("own_rec"),
            "ownrecyards": oppo_stats.get("fumbles", {}).get("own_rec_yards"),
            "opprec": oppo_stats.get("fumbles", {}).get("opp_rec"),
            "opprecyards": oppo_stats.get("fumbles", {}).get("opp_rec_yards"),
            "outofbounds": oppo_stats.get("fumbles", {}).get("out_of_bounds"),
            "forcedfumbles": oppo_stats.get("fumbles", {}).get("forced_fumbles"),
            "ownrectds": oppo_stats.get("fumbles", {}).get("own_rec_tds"),
            "opprectds": oppo_stats.get("fumbles", {}).get("opp_rec_tds"),
            "ezrectds": oppo_stats.get("fumbles", {}).get("ez_rec_tds")
        },
        "firstdowns": {
            "passing": oppo_stats.get("first_downs", {}).get("pass"),
            "penalty": oppo_stats.get("first_downs", {}).get("penalty"),
            "rush": oppo_stats.get("first_downs", {}).get("rush"),
            "total": oppo_stats.get("first_downs", {}).get("total")
        },
        "fieldgoals": {
            "attempts": oppo_stats.get("field_goals", {}).get("attempts"),
            "made": oppo_stats.get("field_goals", {}).get("made"),
            "blocked": oppo_stats.get("field_goals", {}).get("blocked"),
            "yards": oppo_stats.get("field_goals", {}).get("yards"),
            "avgyards": oppo_stats.get("field_goals", {}).get("avg_yards"),
            "longest": oppo_stats.get("field_goals", {}).get("longest"),
            "missed": oppo_stats.get("field_goals", {}).get("missed"),
            "pct": oppo_stats.get("field_goals", {}).get("pct"),
            "attempts19": oppo_stats.get("field_goals", {}).get("attempts_19"),
            "attempts29": oppo_stats.get("field_goals", {}).get("attempts_29"),
            "attempts39": oppo_stats.get("field_goals", {}).get("attempts_39"),
            "attempts49": oppo_stats.get("field_goals", {}).get("attempts_49"),
            "attempts50": oppo_stats.get("field_goals", {}).get("attempts_50"),
            "made19": oppo_stats.get("field_goals", {}).get("made_19"),
            "made29": oppo_stats.get("field_goals", {}).get("made_29"),
            "made39": oppo_stats.get("field_goals", {}).get("made_39"),
            "made49": oppo_stats.get("field_goals", {}).get("made_49"),
            "made50": oppo_stats.get("field_goals", {}).get("made_50")
        },
        "defense": {
            "tackles": oppo_stats.get("defense", {}).get("tackles"),
            "assists": oppo_stats.get("defense", {}).get("assists"),
            "combined": oppo_stats.get("defense", {}).get("combined"),
            "sacks": oppo_stats.get("defense", {}).get("sacks"),
            "sackyards": oppo_stats.get("defense", {}).get("sack_yards"),
            "interceptions": oppo_stats.get("defense", {}).get("interceptions"),
            "passesdefended": oppo_stats.get("defense", {}).get("passes_defended"),
            "forcedfumbles": oppo_stats.get("defense", {}).get("forced_fumbles"),
            "fumblerecoveries": oppo_stats.get("defense", {}).get("fumble_recoveries"),
            "qbhits": oppo_stats.get("defense", {}).get("qb_hits"),
            "tloss": oppo_stats.get("defense", {}).get("tloss"),
            "tlossyards": oppo_stats.get("defense", {}).get("tloss_yards"),
            "safeties": oppo_stats.get("defense", {}).get("safeties"),
            "sptackles": oppo_stats.get("defense", {}).get("sp_tackles"),
            "spassists": oppo_stats.get("defense", {}).get("sp_assists"),
            "spforcedfumbles": oppo_stats.get("defense", {}).get("sp_forced_fumbles"),
            "spfumblerecoveries": oppo_stats.get("defense", {}).get("sp_fumble_recoveries"),
            "spblocks": oppo_stats.get("defense", {}).get("sp_blocks"),
            "misctackles": oppo_stats.get("defense", {}).get("misc_tackles"),
            "miscassists": oppo_stats.get("defense", {}).get("misc_assists"),
            "miscforcedfumbles": oppo_stats.get("defense", {}).get("misc_forced_fumbles"),
            "miscfumblerecoveries": oppo_stats.get("defense", {}).get("misc_fumble_recoveries"),
            "deftargets": oppo_stats.get("defense", {}).get("def_targets"),
            "defcomps": oppo_stats.get("defense", {}).get("def_comps"),
            "blitzes": oppo_stats.get("defense", {}).get("blitzes"),
            "hurries": oppo_stats.get("defense", {}).get("hurries"),
            "knockdowns": oppo_stats.get("defense", {}).get("knockdowns"),
            "missedtackles": oppo_stats.get("defense", {}).get("missed_tackles"),
            "battedpasses": oppo_stats.get("defense", {}).get("batted_passes"),
            "threeandoutsforced": oppo_stats.get("defense", {}).get("three_and_outs_forced"),
            "fourthdownstops": oppo_stats.get("defense", {}).get("fourth_down_stops")
        },
        "extra_points": {
            "conversions": {
                "passattempts": oppo_stats.get("extra_points", {}).get("conversions", {}).get("pass_attempts"),
                "passsuccesses": oppo_stats.get("extra_points", {}).get("conversions", {}).get("pass_successes"),
                "rushattempts": oppo_stats.get("extra_points", {}).get("conversions", {}).get("rush_attempts"),
                "rushsuccesses": oppo_stats.get("extra_points", {}).get("conversions", {}).get("rush_successes"),
                "defenseattempts": oppo_stats.get("extra_points", {}).get("conversions", {}).get("defense_attempts"),
                "defensesuccesses": oppo_stats.get("extra_points", {}).get("conversions", {}).get("defense_successes"),
                "turnoversuccesses": oppo_stats.get("extra_points", {}).get("conversions", {}).get("turnover_successes")
            },
            "kicks": {
                "attempts": oppo_stats.get("extra_points", {}).get("kicks", {}).get("attempts"),
                "blocked": oppo_stats.get("extra_points", {}).get("kicks", {}).get("blocked"),
                "made": oppo_stats.get("extra_points", {}).get("kicks", {}).get("made"),
                "pct": oppo_stats.get("extra_points", {}).get("kicks", {}).get("pct")
            },
        },
        "efficiency": {
            "goaltogo": {
                "attempts": oppo_stats.get("efficiency", {}).get("goaltogo", {}).get("attempts"),
                "successes": oppo_stats.get("efficiency", {}).get("goaltogo", {}).get("successes"),
                "pct": oppo_stats.get("efficiency", {}).get("goaltogo", {}).get("pct")
            },
            "redzone": {
                "attempts": oppo_stats.get("efficiency", {}).get("redzone", {}).get("attempts"),
                "successes": oppo_stats.get("efficiency", {}).get("redzone", {}).get("successes"),
                "pct": oppo_stats.get("efficiency", {}).get("redzone", {}).get("pct")
            },
            "thirddown": {
                "attempts": oppo_stats.get("efficiency", {}).get("thirddown", {}).get("attempts"),
                "successes": oppo_stats.get("efficiency", {}).get("thirddown", {}).get("successes"),
                "pct": oppo_stats.get("efficiency", {}).get("thirddown", {}).get("pct")
            },
            "fourthdown": {
                "attempts": oppo_stats.get("efficiency", {}).get("fourthdown", {}).get("attempts"),
                "successes": oppo_stats.get("efficiency", {}).get("fourthdown", {}).get("successes"),
            },
        },
    })
    if 'efficiency' in oppo_stats:
        efficiencydata = oppo_stats['efficiency']
        for key, value in efficiencydata.items():
            opponenetseasondata_main[key] = value

    if 'extra_points' in oppo_stats:
        extrapointsdata = oppo_stats['extra_points']
        for key, value in extrapointsdata.items():
            opponenetseasondata_main[key] = value
    #logging.info("Extracted OpponenetData data:", opponenetseasondata)
    logging.info(f"Number of OpponenetData extracted: {len(opponenetseasondata)}")
    return opponenetseasondata
def extract_team_seasonal_stat_info(data):
    teamid = str(data.get("id"))
    seasonid = str(data.get("season", {}).get("id"))
    team_stats = data.get('record', {})
    key = (teamid, seasonid)
    teamseasondata = {key:{}}
    teamseasondata_main = teamseasondata[key]
    teamseasondata_main.update({
        "teamid": teamid,
        "seasonid": seasonid,
        "intreturns":{
            "avgyards": team_stats.get("int_returns", {}).get("avg_yards"),
            "yards": team_stats.get("int_returns", {}).get("yards"),
            "longest": team_stats.get("int_returns", {}).get("longest"),
            "touchdowns": team_stats.get("int_returns", {}).get("touchdowns"),
            "longesttouchdown": team_stats.get("int_returns", {}).get("longest_touchdown"),
            "returns": team_stats.get("int_returns", {}).get("returns")
        },
        "passing":{
            "attempts": team_stats.get("passing", {}).get("attempts"),
            "completions": team_stats.get("passing", {}).get("completions"),
            "cmppct": team_stats.get("passing", {}).get("cmp_pct"),
            "interceptions": team_stats.get("passing", {}).get("interceptions"),
            "sackyards": team_stats.get("passing", {}).get("sack_yards"),
            "rating": team_stats.get("passing", {}).get("rating"),
            "touchdowns": team_stats.get("passing", {}).get("touchdowns"),
            "avgyards": team_stats.get("passing", {}).get("avg_yards"),
            "sacks": team_stats.get("passing", {}).get("sacks"),
            "longest": team_stats.get("passing", {}).get("longest"),
            "longesttouchdown": team_stats.get("passing", {}).get("longest_touchdown"),
            "airyards": team_stats.get("passing", {}).get("air_yards"),
            "redzoneattempts": team_stats.get("passing", {}).get("redzone_attempts"),
            "netyards": team_stats.get("passing", {}).get("net_yards"),
            "yards": team_stats.get("passing", {}).get("yards"),
            "grossyards": team_stats.get("passing", {}).get("gross_yards"),
            "inttouchdowns": team_stats.get("passing", {}).get("int_touchdowns"),
            "throwaways": team_stats.get("passing", {}).get("throw_aways"),
            "poorthrows": team_stats.get("passing", {}).get("poor_throws"),
            "defendedpasses": team_stats.get("passing", {}).get("defended_passes"),
            "droppedpasses": team_stats.get("passing", {}).get("dropped_passes"),
            "spikes": team_stats.get("passing", {}).get("spikes"),
            "blitzes": team_stats.get("passing", {}).get("blitzes"),
            "hurries": team_stats.get("passing", {}).get("hurries"),
            "knockdowns": team_stats.get("passing", {}).get("knockdowns"),
            "pockettime": team_stats.get("passing", {}).get("pocket_time"),
            "battedpasses": team_stats.get("passing", {}).get("batted_passes"),
            "ontargetthrows": team_stats.get("passing", {}).get("on_target_throws")
        },
        "receiving":{
            "targets": team_stats.get("receiving", {}).get("targets"),
            "receptions": team_stats.get("receiving", {}).get("receptions"),
            "avgyards": team_stats.get("receiving", {}).get("avg_yards"),
            "yards": team_stats.get("receiving", {}).get("yards"),
            "touchdowns": team_stats.get("receiving", {}).get("touchdowns"),
            "yardsaftercatch": team_stats.get("receiving", {}).get("yards_after_catch"),
            "longest": team_stats.get("receiving", {}).get("longest"),
            "longesttouchdown": team_stats.get("receiving", {}).get("longest_touchdown"),
            "redzonetargets": team_stats.get("receiving", {}).get("redzone_targets"),
            "airyards": team_stats.get("receiving", {}).get("air_yards"),
            "brokentackles": team_stats.get("receiving", {}).get("broken_tackles"),
            "droppedpasses": team_stats.get("receiving", {}).get("dropped_passes"),
            "catchablepasses": team_stats.get("receiving", {}).get("catchable_passes"),
            "yardsaftercontact": team_stats.get("receiving", {}).get("yards_after_contact")
        },
        "defense": {
            "tackles": team_stats.get("defense", {}).get("tackles"),
            "assists": team_stats.get("defense", {}).get("assists"),
            "combined": team_stats.get("defense", {}).get("combined"),
            "sacks": team_stats.get("defense", {}).get("sacks"),
            "sackyards": team_stats.get("defense", {}).get("sack_yards"),
            "interceptions": team_stats.get("defense", {}).get("interceptions"),
            "passesdefended": team_stats.get("defense", {}).get("passes_defended"),
            "forcedfumbles": team_stats.get("defense", {}).get("forced_fumbles"),
            "fumblerecoveries": team_stats.get("defense", {}).get("fumble_recoveries"),
            "qbhits": team_stats.get("defense", {}).get("qb_hits"),
            "tloss": team_stats.get("defense", {}).get("tloss"),
            "tlossyards": team_stats.get("defense", {}).get("tloss_yards"),
            "safeties": team_stats.get("defense", {}).get("safeties"),
            "sptackles": team_stats.get("defense", {}).get("sp_tackles"),
            "spassists": team_stats.get("defense", {}).get("sp_assists"),
            "spblocks": team_stats.get("defense", {}).get("sp_blocks"),
            "spforcedfumbles": team_stats.get("defense",{}).get("sp_forced_fumbles"),
            "spfumblerecoveries": team_stats.get("defense",{}).get("sp_fumble_recoveries"),
            "misctackles": team_stats.get("defense",{}).get("misc_tackles"),
            "miscassists": team_stats.get("defense",{}).get("misc_assists"),
            "miscforcedfumbles": team_stats.get("defense",{}).get("misc_forced_fumbles"),
            "miscfumblerecoveries": team_stats.get("defense",{}).get("misc_fumble_recoveries"),
            "deftargets": team_stats.get("defense", {}).get("def_targets"),
            "defcomps": team_stats.get("defense", {}).get("def_comps"),
            "blitzes": team_stats.get("defense", {}).get("blitzes"),
            "hurries": team_stats.get("defense", {}).get("hurries"),
            "knockdowns": team_stats.get("defense", {}).get("knockdowns"),
            "missedtackles": team_stats.get("defense", {}).get("missed_tackles"),
            "battedpasses": team_stats.get("defense", {}).get("batted_passes"),
            "threeandoutsforced": team_stats.get("defense", {}).get("three_and_outs_forced"),
            "fourthdownstops": team_stats.get("defense", {}).get("fourth_down_stops")
        },
        "efficiency": {
            "goaltogo": {
                "attempts": team_stats.get("efficiency", {}).get("goaltogo", {}).get("attempts"),
                "successes": team_stats.get("efficiency", {}).get("goaltogo", {}).get("successes"),
                "pct": team_stats.get("efficiency", {}).get("goaltogo", {}).get("pct")
            },
            "redzone": {
                "attempts": team_stats.get("efficiency", {}).get("redzone", {}).get("attempts"),
                "successes": team_stats.get("efficiency", {}).get("redzone", {}).get("successes"),
                "pct": team_stats.get("efficiency", {}).get("redzone", {}).get("pct")
            },
            "thirddown": {
                "attempts": team_stats.get("efficiency", {}).get("thirddown", {}).get("attempts"),
                "successes": team_stats.get("efficiency", {}).get("thirddown", {}).get("successes"),
                "pct": team_stats.get("efficiency", {}).get("thirddown", {}).get("pct")
            },
            "fourthdown": {
                "attempts": team_stats.get("efficiency", {}).get("fourthdown", {}).get("attempts"),
                "successes": team_stats.get("efficiency", {}).get("fourthdown", {}).get("successes"),
                "pct": team_stats.get("efficiency", {}).get("fourthdown", {}).get("pct")
            },
        },
        "fieldgoals": {
            "attempts": team_stats.get("field_goals", {}).get("attempts"),
            "made": team_stats.get("field_goals", {}).get("made"),
            "blocked": team_stats.get("field_goals", {}).get("blocked"),
            "yards": team_stats.get("field_goals", {}).get("yards"),
            "avgyards": team_stats.get("field_goals", {}).get("avg_yards"),
            "longest": team_stats.get("field_goals", {}).get("longest"),
            "missed": team_stats.get("field_goals", {}).get("missed"),
            "pct": team_stats.get("field_goals", {}).get("pct"),
            "attempts19": team_stats.get("field_goals", {}).get("attempts_19"),
            "attempts29": team_stats.get("field_goals", {}).get("attempts_29"),
            "attempts39": team_stats.get("field_goals", {}).get("attempts_39"),
            "attempts49": team_stats.get("field_goals", {}).get("attempts_49"),
            "attempts50": team_stats.get("field_goals", {}).get("attempts_50"),
            "made19": team_stats.get("field_goals", {}).get("made_19"),
            "made29": team_stats.get("field_goals", {}).get("made_29"),
            "made39": team_stats.get("field_goals", {}).get("made_39"),
            "made49": team_stats.get("field_goals", {}).get("made_49"),
            "made50": team_stats.get("field_goals", {}).get("made_50")
        },
        "punts":{
            "attempts": team_stats.get("punts", {}).get("attempts"),
            "yards": team_stats.get("punts", {}).get("yards"),
            "netyards": team_stats.get("punts", {}).get("net_yards"),
            "blocked": team_stats.get("punts", {}).get("blocked"),
            "touchbacks": team_stats.get("punts", {}).get("touchbacks"),
            "inside20": team_stats.get("punts", {}).get("inside_20"),
            "returnyards": team_stats.get("punts", {}).get("return_yards"),
            "avgnetyards": team_stats.get("punts", {}).get("avg_net_yards"),
            "avgyards": team_stats.get("punts", {}).get("avg_yards"),
            "longest": team_stats.get("punts", {}).get("longest"),
            "hangtime": team_stats.get("punts", {}).get("hang_time"),
            "avghangtime": team_stats.get("punts", {}).get("avg_hang_time")
        },
        "rushing": {
            "avgyards": team_stats.get("rushing", {}).get("avg_yards"),
            "attempts": team_stats.get("rushing", {}).get("attempts"),
            "touchdowns": team_stats.get("rushing", {}).get("touchdowns"),
            "tlost": team_stats.get("rushing", {}).get("tlost"),
            "tlostyards": team_stats.get("rushing", {}).get("tlost_yards"),
            "yards": team_stats.get("rushing", {}).get("yards"),
            "longest": team_stats.get("rushing", {}).get("longest"),
            "longesttouchdown": team_stats.get("rushing", {}).get("longest_touchdown"),
            "redzoneattempts": team_stats.get("rushing", {}).get("redzone_attempts"),
            "brokentackles": team_stats.get("rushing", {}).get("broken_tackles"),
            "kneeldowns": team_stats.get("rushing", {}).get("kneel_downs"),
            "scrambles": team_stats.get("rushing", {}).get("scrambles"),
            "yardsaftercontact": team_stats.get("rushing", {}).get("yards_after_contact")
        },
        "kickreturns":{
            "avgyards": team_stats.get("kick_returns", {}).get("avg_yards"),
            "yards": team_stats.get("kick_returns", {}).get("yards"),
            "longest": team_stats.get("kick_returns", {}).get("longest"),
            "touchdowns": team_stats.get("kick_returns", {}).get("touchdowns"),
            "longesttouchdown": team_stats.get("kick_returns", {}).get("longest_touchdown"),
            "faircatches": team_stats.get("kick_returns", {}).get("faircatches"),
            "returns": team_stats.get("kick_returns", {}).get("returns")
        },
        "puntreturns":{
            "avgyards": team_stats.get("punt_returns", {}).get("avg_yards"),
            "returns": team_stats.get("punt_returns", {}).get("returns"),
            "yards": team_stats.get("punt_returns", {}).get("yards"),
            "longest": team_stats.get("punt_returns", {}).get("longest"),
            "touchdowns": team_stats.get("punt_returns", {}).get("touchdowns"),
            "longesttouchdown": team_stats.get("punt_returns", {}).get("longest_touchdown"),
            "faircatches": team_stats.get("punt_returns", {}).get("faircatches")
        },
        "miscreturns":{
            "yards": team_stats.get("misc_returns", {}).get("yards"),
            "touchdowns": team_stats.get("misc_returns", {}).get("touchdowns"),
            "longesttouchdown": team_stats.get("misc_returns", {}).get("longest_touchdown"),
            "blkfgtouchdowns": team_stats.get("misc_returns", {}).get("blk_fg_touchdowns"),
            "blkpattouchdowns": team_stats.get("misc_returns", {}).get("blk_pat_touchdowns"),
            "fgreturntouchdowns": team_stats.get("misc_returns", {}).get("fg_return_touchdowns"),
            "ezrectouchdowns": team_stats.get("misc_returns", {}).get("ez_rec_touchdowns"),
            "returns": team_stats.get("misc_returns", {}).get("returns")
        },
        "games_played": team_stats.get("games_played"),
        "extra_points": {
            "conversions": {
                "passattempts": team_stats.get("extra_points", {}).get("conversions", {}).get("pass_attempts"),
                "passsuccesses": team_stats.get("extra_points", {}).get("conversions", {}).get("pass_successes"),
                "rushattempts": team_stats.get("extra_points", {}).get("conversions", {}).get("rush_attempts"),
                "rushsuccesses": team_stats.get("extra_points", {}).get("conversions", {}).get("rush_successes"),
                "defenseattempts": team_stats.get("extra_points", {}).get("conversions", {}).get("defense_attempts"),
                "defensesuccesses": team_stats.get("extra_points", {}).get("conversions", {}).get("defense_successes"),
                "turnoversuccesses": team_stats.get("extra_points", {}).get("conversions", {}).get("turnover_successes")
            },
            "kicks": {
                "attempts": team_stats.get("extra_points", {}).get("kicks", {}).get("attempts"),
                "blocked": team_stats.get("extra_points", {}).get("kicks", {}).get("blocked"),
                "made": team_stats.get("extra_points", {}).get("kicks", {}).get("made"),
                "pct": team_stats.get("extra_points", {}).get("kicks", {}).get("pct")
            },
        },
        "kickoffs":{
            "endzone": team_stats.get("kickoffs", {}).get("endzone"),
            "inside20": team_stats.get("kickoffs", {}).get("inside_20"),
            "returnyards": team_stats.get("kickoffs", {}).get("return_yards"),
            "returned": team_stats.get("kickoffs", {}).get("returned"),
            "touchbacks": team_stats.get("kickoffs", {}).get("touchbacks"),
            "yards": team_stats.get("kickoffs", {}).get("yards"),
            "outofbounds": team_stats.get("kickoffs", {}).get("out_of_bounds"),
            "kickoffs": team_stats.get("kickoffs", {}).get("kickoffs"),
            "onsideattempts": team_stats.get("kickoffs", {}).get("onside_attempts"),
            "onsidesuccesses": team_stats.get("kickoffs", {}).get("onside_successes"),
            "squibkicks": team_stats.get("kickoffs", {}).get("squib_kicks")
        },
        "fumbles": {
            "fumbles": team_stats.get("fumbles", {}).get("fumbles"),
            "lostfumbles": team_stats.get("fumbles", {}).get("lost_fumbles"),
            "ownrec": team_stats.get("fumbles", {}).get("own_rec"),
            "ownrecyards": team_stats.get("fumbles", {}).get("own_rec_yards"),
            "opprec": team_stats.get("fumbles", {}).get("opp_rec"),
            "opprecyards": team_stats.get("fumbles", {}).get("opp_rec_yards"),
            "outofbounds": team_stats.get("fumbles", {}).get("out_of_bounds"),
            "forcedfumbles": team_stats.get("fumbles", {}).get("forced_fumbles"),
            "ownrectds": team_stats.get("fumbles", {}).get("own_rec_tds"),
            "opprectds": team_stats.get("fumbles", {}).get("opp_rec_tds"),
            "ezrectds": team_stats.get("fumbles", {}).get("ez_rec_tds")
        },
        "penalties":{
            "penalties": team_stats.get("penalties", {}).get("penalties"),
            "yards": team_stats.get("penalties", {}).get("yards")
        },
        "touchdowns": {
            "passing": team_stats.get("touchdowns", {}).get("pass"),
            "rush": team_stats.get("touchdowns", {}).get("rush"),
            "totalreturn": team_stats.get("touchdowns", {}).get("total_return"),
            "total": team_stats.get("touchdowns", {}).get("total"),
            "fumblereturn": team_stats.get("touchdowns", {}).get("fumble_return"),
            "intreturn": team_stats.get("touchdowns", {}).get("int_return"),
            "kickreturn": team_stats.get("touchdowns", {}).get("kick_return"),
            "puntreturn": team_stats.get("touchdowns", {}).get("punt_return"),
            "other": team_stats.get("touchdowns", {}).get("other")
        },
        "interceptions":{
            "returnyards": team_stats.get("interceptions", {}).get("return_yards"),
            "returned": team_stats.get("interceptions", {}).get("returned"),
            "interceptions": team_stats.get("interceptions", {}).get("interceptions"),
        },        
        "firstdowns": {
            "passing": team_stats.get("first_downs", {}).get("pass"),
            "penalty": team_stats.get("first_downs", {}).get("penalty"),
            "rush": team_stats.get("first_downs", {}).get("rush"),
            "total": team_stats.get("first_downs", {}).get("total")
        },
    })
    if 'efficiency' in team_stats:
        efficiencydata = team_stats['efficiency']
        for key, value in efficiencydata.items():
            teamseasondata_main[key] = value
    if 'extra_points' in team_stats:
        extrapointsdata = team_stats['extra_points']
        for key, value in extrapointsdata.items():
            teamseasondata_main[key] = value
    #logging.info("Extracted TEAM SEASON data:", teamseasondata)
    logging.info(f"Number of TEAM SEASON extracted: {len(teamseasondata)}")
    return  teamseasondata
def extract_player_seasonal_stat_info(data):
    teamid = str(data.get("id"))
    seasonid = str(data.get("season", {}).get("id"))
    players_data = data.get("players", [])
    # This will be a list to store data for all players
    playerseasondata = {}
    for player_stats in players_data:
        playerid = str(player_stats.get("id"))
        key = (playerid, teamid, seasonid)
        playerseasondata[key] = ({
            "playerid": playerid,
            "teamid": teamid,
            "seasonid": seasonid,
            "playername": player_stats.get("name"),
            "position": player_stats.get("position"),
            "jersey": player_stats.get("jersey"),
            "gamesplayed": player_stats.get("games_played"),
            "gamesstarted": player_stats.get("games_started"),
            "intreturns":{
                "longest": player_stats.get("int_returns",{}).get("longest"),
                "longesttouchdown": player_stats.get("int_returns",{}).get("longest_touchdown"),
                "avgyards": player_stats.get("int_returns",{}).get("avg_yards"),
                "returns": player_stats.get("int_returns",{}).get("returns"),
                "touchdowns": player_stats.get("int_returns",{}).get("touchdowns"),
                "yards": player_stats.get("int_returns",{}).get("yards")
            },
            "passing":{
                "attempts": player_stats.get("passing",{}).get("attempts"),
                "longest": player_stats.get("passing",{}).get("longest"),
                "longesttouchdown": player_stats.get("passing",{}).get("longest_touchdown"),
                "airyards": player_stats.get("passing",{}).get("air_yards"),
                "avgpockettime": player_stats.get("passing",{}).get("avg_pocket_time"),
                "avgyards": player_stats.get("passing",{}).get("avg_yards"),
                "battedpasses": player_stats.get("passing",{}).get("batted_passes"),
                "blitzes": player_stats.get("passing",{}).get("blitzes"),
                "cmppct": player_stats.get("passing",{}).get("cmp_pct"),
                "completions": player_stats.get("passing",{}).get("completions"),
                "defendedpasses": player_stats.get("passing",{}).get("defended_passes"),
                "droppedpasses": player_stats.get("passing",{}).get("dropped_passes"),
                "firstdowns": player_stats.get("passing",{}).get("first_downs"),
                "grossyards": player_stats.get("passing",{}).get("gross_yards"),
                "hurries": player_stats.get("passing",{}).get("hurries"),
                "inttouchdowns": player_stats.get("passing",{}).get("int_touchdowns"),
                "interceptions": player_stats.get("passing",{}).get("interceptions"),
                "knockdowns": player_stats.get("passing",{}).get("knockdowns"),
                "netyards": player_stats.get("passing",{}).get("net_yards"),
                "ontargetthrows": player_stats.get("passing",{}).get("on_target_throws"),
                "pockettime": player_stats.get("passing",{}).get("pocket_time"),
                "poorthrows": player_stats.get("passing",{}).get("poor_throws"),
                "rating": player_stats.get("passing",{}).get("rating"),
                "redzoneattempts": player_stats.get("passing",{}).get("redzone_attempts"),
                "sackyards": player_stats.get("passing",{}).get("sack_yards"),
                "sacks": player_stats.get("passing",{}).get("sacks"),
                "spikes": player_stats.get("passing",{}).get("spikes"),
                "throwaways": player_stats.get("passing",{}).get("throw_aways"),
                "touchdowns": player_stats.get("passing",{}).get("touchdowns"),
                "yards": player_stats.get("passing",{}).get("yards")
            },
            "receiving":{
                "longest": player_stats.get("receiving",{}).get("longest"),
                "longesttouchdown": player_stats.get("receiving",{}).get("longest_touchdown"),
                "airyards": player_stats.get("receiving",{}).get("air_yards"),
                "avgyards": player_stats.get("receiving",{}).get("avg_yards"),
                "brokentackles": player_stats.get("receiving",{}).get("broken_tackles"),
                "catchablepasses": player_stats.get("receiving",{}).get("catchable_passes"),
                "droppedpasses": player_stats.get("receiving",{}).get("dropped_passes"),
                "firstdowns": player_stats.get("receiving",{}).get("first_downs"),
                "receptions": player_stats.get("receiving",{}).get("receptions"),
                "redzonetargets": player_stats.get("receiving",{}).get("redzone_targets"),
                "targets": player_stats.get("receiving",{}).get("targets"),
                "touchdowns": player_stats.get("receiving",{}).get("touchdowns"),
                "yards": player_stats.get("receiving",{}).get("yards"),
                "yardsaftercatch": player_stats.get("receiving",{}).get("yards_after_catch"),
                "yardsaftercontact": player_stats.get("receiving",{}).get("yards_after_contact")
            },
            "defense":{
                "assists": player_stats.get("defense",{}).get("assists"),
                "battedpasses": player_stats.get("defense",{}).get("batted_passes"),
                "blitzes": player_stats.get("defense",{}).get("blitzes"),
                "combined": player_stats.get("defense",{}).get("combined"),
                "defcomps": player_stats.get("defense",{}).get("def_comps"),
                "deftargets": player_stats.get("defense",{}).get("def_targets"),
                "forcedfumbles": player_stats.get("defense",{}).get("forced_fumbles"),
                "fumblerecoveries": player_stats.get("defense",{}).get("fumble_recoveries"),
                "hurries": player_stats.get("defense",{}).get("hurries"),
                "interceptions": player_stats.get("defense",{}).get("interceptions"),
                "knockdowns": player_stats.get("defense",{}).get("knockdowns"),
                "miscassists": player_stats.get("defense",{}).get("misc_assists"),
                "miscfumblesforced": player_stats.get("defense",{}).get("misc_forced_fumbles"),
                "miscfumblerecoveries": player_stats.get("defense",{}).get("misc_fumble_recoveries"),
                "misctackles": player_stats.get("defense",{}).get("misc_tackles"),
                "missedtackles": player_stats.get("defense",{}).get("missed_tackles"),
                "passesdefended": player_stats.get("defense",{}).get("passes_defended"),
                "qbhits": player_stats.get("defense",{}).get("qb_hits"),
                "sackyards": player_stats.get("defense",{}).get("sack_yards"),
                "sacks": player_stats.get("defense",{}).get("sacks"),
                "safeties": player_stats.get("defense",{}).get("safeties"),
                "spassists": player_stats.get("defense",{}).get("sp_assists"),
                "spblocks": player_stats.get("defense",{}).get("sp_blocks"),
                "spforcedfumbles": player_stats.get("defense",{}).get("sp_forced_fumbles"),
                "spfumblerecoveries": player_stats.get("defense",{}).get("sp_fumble_recoveries"),
                "sptackles": player_stats.get("defense",{}).get("sp_tackles"),
                "tackles": player_stats.get("defense",{}).get("tackles"),
                "tloss": player_stats.get("defense",{}).get("tloss"),
                "tlossyards": player_stats.get("defense",{}).get("tloss_yards")
                },
            "fieldgoals":{
                "longest": player_stats.get("field_goals",{}).get("longest"),
                "attempts": player_stats.get("field_goals",{}).get("attempts"),
                "attempt19": player_stats.get("field_goals",{}).get("attempts_19"),
                "attempt29": player_stats.get("field_goals",{}).get("attempts_29"),
                "attempt39": player_stats.get("field_goals",{}).get("attempts_39"),
                "attempt49": player_stats.get("field_goals",{}).get("attempts_49"),
                "attempt50": player_stats.get("field_goals",{}).get("attempts_50"),
                "avgyards": player_stats.get("field_goals",{}).get("avg_yards"),
                "blocked": player_stats.get("field_goals",{}).get("blocked"),
                "made": player_stats.get("field_goals",{}).get("made"),
                "made19": player_stats.get("field_goals",{}).get("made_19"),
                "made29": player_stats.get("field_goals",{}).get("made_29"),
                "made39": player_stats.get("field_goals",{}).get("made_39"),
                "made49": player_stats.get("field_goals",{}).get("made_49"),
                "made50": player_stats.get("field_goals",{}).get("made_50"),
                "missed": player_stats.get("field_goals",{}).get("missed"),
                "pct": player_stats.get("field_goals",{}).get("pct"),
                "yards": player_stats.get("field_goals",{}).get("yards")
            },
            "punts":{
                "longest": player_stats.get("punts",{}).get("longest"),
                "attempt": player_stats.get("punts",{}).get("attempts"),
                "avghangtime": player_stats.get("punts",{}).get("avg_hang_time"),
                "avgnetyards": player_stats.get("punts",{}).get("avg_net_yards"),
                "avgyards": player_stats.get("punts",{}).get("avg_yards"),
                "blocked": player_stats.get("punts",{}).get("blocked"),
                "hangtime": player_stats.get("punts",{}).get("hang_time"),
                "inside20": player_stats.get("punts",{}).get("inside_20"),
                "netyards": player_stats.get("punts",{}).get("net_yards"),
                "returnyards": player_stats.get("punts",{}).get("return_yards"),
                "touchbacks": player_stats.get("punts",{}).get("touchbacks"),
                "yards": player_stats.get("punts",{}).get("yards")
            },
            "rushing":{
                "longest": player_stats.get("rushing",{}).get("longest"),
                "longesttouchdown": player_stats.get("rushing",{}).get("longest_touchdown"),
                "attempt": player_stats.get("rushing",{}).get("attempts"),
                "avgyards": player_stats.get("rushing",{}).get("avg_yards"),
                "brokentackles": player_stats.get("rushing",{}).get("broken_tackles"),
                "firstdowns": player_stats.get("rushing",{}).get("first_downs"),
                "kneeldowns": player_stats.get("rushing",{}).get("kneel_downs"),
                "redzoneattempts": player_stats.get("rushing",{}).get("redzone_attempts"),
                "scrambles": player_stats.get("rushing",{}).get("scrambles"),
                "tlost": player_stats.get("rushing",{}).get("tlost"),
                "tlostyards": player_stats.get("rushing",{}).get("tlost_yards"),
                "touchdowns": player_stats.get("rushing",{}).get("touchdowns"),
                "yards": player_stats.get("rushing",{}).get("yards"),
                "yardsaftercontact": player_stats.get("rushing",{}).get("yards_after_contact")
            },
            "extra_points":{
                "attempts": player_stats.get("extra_points",{}).get("attempts"),
                "blocked": player_stats.get("extra_points",{}).get("blocked"),
                "made": player_stats.get("extra_points",{}).get("made"),
                "missed": player_stats.get("extra_points",{}).get("missed"),
                "pct": player_stats.get("extra_points",{}).get("pct")
            },
            "kickreturns":{
                "longest": player_stats.get("kick_returns",{}).get("longest"),
                "longesttouchdown": player_stats.get("kick_returns",{}).get("longest_touchdown"),
                "avgyards": player_stats.get("kick_returns",{}).get("avg_yards"),
                "faircatches": player_stats.get("kick_returns",{}).get("faircatches"),
                "returns": player_stats.get("kick_returns",{}).get("returns"),
                "touchdowns": player_stats.get("kick_returns",{}).get("touchdowns"),
                "yards": player_stats.get("kick_returns",{}).get("yards")
            },
            "puntreturns":{
                "longest": player_stats.get("punt_returns",{}).get("longest"),
                "longesttouchdown": player_stats.get("punt_returns",{}).get("longest_touchdown"),
                "avgyards": player_stats.get("punt_returns",{}).get("avg_yards"),
                "faircatches": player_stats.get("punt_returns",{}).get("faircatches"),
                "returns": player_stats.get("punt_returns",{}).get("returns"),
                "touchdowns": player_stats.get("punt_returns",{}).get("touchdowns"),
                "yards": player_stats.get("punt_returns",{}).get("yards")
            },
            "conversions":{
                "defenseattempts": player_stats.get("conversions",{}).get("defense_attempts"),
                "defensesuccesses": player_stats.get("conversions",{}).get("defense_successes"),
                "passattempts": player_stats.get("conversions",{}).get("pass_attempts"),
                "passsuccesses": player_stats.get("conversions",{}).get("pass_successes"),
                "receiveattempts": player_stats.get("conversions",{}).get("receive_attempts"),
                "receivesuccesses": player_stats.get("conversions",{}).get("receive_successes"),
                "rushattempts": player_stats.get("conversions",{}).get("rush_attempt"),
                "rushsuccesses": player_stats.get("conversions",{}).get("rush_successes")
            },
            "kickoffs":{
                "endzone":player_stats.get("kickoffs",{}).get("endzone"),
                "inside20":player_stats.get("kickoffs",{}).get("inside_20"),
                "kickoffs":player_stats.get("kickoffs",{}).get("kickoffs"),
                "onsideattempts":player_stats.get("kickoffs",{}).get("onside_attempts"),
                "onsidesuccesses":player_stats.get("kickoffs",{}).get("onside_successes"),
                "outofbounds":player_stats.get("kickoffs",{}).get("out_of_bounds"),
                "returnyards":player_stats.get("kickoffs",{}).get("return_yards"),
                "squibkicks":player_stats.get("kickoffs",{}).get("squib_kicks"),
                "touchbacks":player_stats.get("kickoffs",{}).get("touchbacks"),
                "yards":player_stats.get("kickoffs",{}).get("yards")
            },
            "fumbles": {
                "fumbles":player_stats.get("fumbles",{}).get("fumbles"),
                "lostfumbles": player_stats.get("fumbles",{}).get("lost_fumbles"),
                "ownrec": player_stats.get("fumbles",{}).get("own_rec"),
                "ownrecyards": player_stats.get("fumbles",{}).get("own_rec_yards"),
                "opprec": player_stats.get("fumbles",{}).get("opp_rec"),
                "opprecyards": player_stats.get("fumbles",{}).get("opp_rec_yards"),
                "outofbounds": player_stats.get("fumbles",{}).get("out_of_bounds"),
                "forcedfumbles": player_stats.get("fumbles",{}).get("forced_fumbles"),
                "ownrectds": player_stats.get("fumbles",{}).get("own_rec_tds"),
                "opprectds": player_stats.get("fumbles",{}).get("opp_rec_tds"),
                "ezrectds": player_stats.get("fumbles",{}).get("ez_rec_tds")
            },
            "penalties": {
                "penalties": player_stats.get("penalties", {}).get("penalties"),
                "yards": player_stats.get("penalties", {}).get("yards"),
                "firstdowns": player_stats.get("penalties", {}).get("first_downs")
            },
         })
    #logging.info("Extracted PlayerData data:", playerseasondata)
    logging.info(f"Number of PlayersData extracted: {len(playerseasondata)}")
    return playerseasondata     
def extract_team_info(data):
    team_id = data.get("id")
    team_info = {
        "id": team_id,
        "name": data.get("name"),
        "market": data.get("market"),
        "alias": data.get("alias"),
        "sr_id": data.get("sr_id"),
    }
    team_info_dict = {team_id: team_info}
    #logging.info("Extracted TeamInfo data:", team_info_dict)
    return team_info_dict
def truncate_dict(d, max_items=5):
    """Truncates dictionary to a certain number of items."""
    truncated = dict(list(d.items())[:max_items])
    if len(d) > max_items:
        truncated["..."] = "..."
    return truncated
def map_dict_to_model(data_dict, model_class):
    if not isinstance(data_dict, dict):
        logging.info(f"Error: Expected dictionary but received {type(data_dict)} with value {data_dict}")
        return None
    # Check if the model expects 'id' and map 'playerid' to 'id' accordingly
    if 'id' not in data_dict and 'playerid' in data_dict:
        data_dict['id'] = data_dict['playerid']
    # Ensure that 'teamid' and 'seasonid' are strings
    for key in ['teamid', 'seasonid', 'id']:
        if key in data_dict and not isinstance(data_dict[key], str):
            logging.info(f"Warning: {key} is not a string. Converting to string.")
            data_dict[key] = str(data_dict[key])
    # Handle EmbeddedDocumentField
    if isinstance(model_class, EmbeddedDocumentField):
        model_instance = model_class.document_type()
    else:
        model_instance = model_class()
    # Print conversion data only for opponentseasondata and teamseasondata
    if (
        hasattr(model_instance, 'opponentseasondata') 
        and 'conversions' in data_dict.get('opponentseasondata', {})
    ):
        logging.info(f"Conversions Data for opponentseasondata: {data_dict['opponentseasondata']['conversions']}")
    if (
        hasattr(model_instance, 'teamseasondata') 
        and 'conversions' in data_dict.get('teamseasondata', {})
    ):
        logging.info(f"Conversions Data for teamseasondata: {data_dict['teamseasondata']['conversions']}")
    for key, value in data_dict.items():
        # Skip the current iteration if the value is None
        if value is None:
            continue
        if hasattr(model_instance, key):  # Check if the model instance has the attribute/key
            field_type = type(getattr(model_class, key))
            # Handle EmbeddedDocumentListField for lists of embedded documents
            if field_type == EmbeddedDocumentListField:
                if isinstance(value, list):
                    nested_model_class = getattr(model_class, key).field.document_type
                    nested_model_instances = [map_dict_to_model(item, nested_model_class) for item in value]
                    setattr(model_instance, key, nested_model_instances)
                else:
                    logging.info(f"Warning: Expected a list for {key} but got {type(value)}. Wrapping in a list.")
                    nested_model_class = getattr(model_class, key).field.document_type
                    nested_model_instance = map_dict_to_model(value, nested_model_class)
                    setattr(model_instance, key, [nested_model_instance])
            # Handle EmbeddedDocumentField for embedded documents
            elif field_type == EmbeddedDocumentField:
                nested_model_class = getattr(model_class, key).document_type
                nested_model_instance = map_dict_to_model(value, nested_model_class)
                setattr(model_instance, key, nested_model_instance)
            # Handle nested dictionaries
            elif isinstance(value, dict):
                logging.info(f"Mapping nested dictionary for {key}: {value}")
                nested_model_class = (
                    getattr(model_class, key).document_type 
                    if field_type == EmbeddedDocumentField 
                    else getattr(model_class, key)
                )
                nested_model_instance = map_dict_to_model(value, nested_model_class)
                setattr(model_instance, key, nested_model_instance)
            else:
                setattr(model_instance, key, value)
    return model_instance
def save_to_database(mapped_seasons, mapped_players,  opponenetseasondata, teamseasondata, playerseasondata, team_info_dict):
    logging.info("save_to_database called")
    if isinstance(opponenetseasondata, tuple):
        opponenetseasondata = opponenetseasondata[0]
    def handle_non_dict_entry(entry_id, mapped_entry, model_cls):
        """
        Handle the non-dictionary entry and possibly convert or format it.
        Returns the handled entry which can then be saved to the database.
        """
        if isinstance(mapped_entry, model_cls):
            return mapped_entry
        logging.warning(f"Received unexpected non-dict type {type(mapped_entry)} for {entry_id}. Defaulting to a new model instance.")
        return model_cls()
    def is_effectively_empty(document):
        """Determine if a document is effectively empty"""
        for value in document.values():
            if value not in [None, 0, "", []]:
                return False
        return True    
    def update_collection(model_cls, mapped_data, collection_name):
        logging.info(f"save_to_database called for {collection_name}")
        # Adjust for TeamInfo which is a single dictionary, not a dictionary of dictionaries
        if collection_name == "TeamInfo":
            team_id = mapped_data.get("id")
            mapped_data = {team_id: mapped_data}
        updated_count = 0
        new_count = 0
        for entry_id, mapped_entry in mapped_data.items():
            if not isinstance(mapped_entry, dict):
                mapped_entry = handle_non_dict_entry(entry_id, mapped_entry, model_cls)
            new_entry = map_dict_to_model(mapped_entry, model_cls) if not isinstance(mapped_entry, model_cls) else mapped_entry
            # Specify query condition based on collection_name
            if collection_name in ["SeasonStatOppo", "SeasonStatTeam"]:
                query_condition = {"seasonid": entry_id[0], "teamid": entry_id[1]}
            elif collection_name == "SeasonStatPlayer":
                query_condition = {"playerid": entry_id[0], "seasonid": entry_id[1], "teamid": entry_id[2]}
            elif collection_name == "SeasonInfo":
                query_condition = {"_id": entry_id}
            else:
                query_condition = {"id": entry_id}
            existing_entry = model_cls.objects(**query_condition).first()
            if existing_entry:
                update_data = {}
                for field_name in existing_entry._fields.keys():
                    existing_value = getattr(existing_entry, field_name)
                    mapped_value = getattr(new_entry, field_name, None)
                    if existing_value != mapped_value and mapped_value is not None:
                        update_data[field_name] = mapped_value
                if update_data:
                    model_cls.objects(**query_condition).update_one(**{"set__" + key: value for key, value in update_data.items()})
                    updated_count += 1
                    logging.info(f"Updated {collection_name} {entry_id}: Updated fields: {', '.join(update_data.keys())}")
            else:
                try:
                    mongo_representation = new_entry.to_mongo().to_dict()
                    if '_id' in mongo_representation:
                        mongo_representation['id'] = mongo_representation.pop('_id')
                    if is_effectively_empty(mongo_representation):
                        logging.info(f"Skipping saving an effectively empty document for {collection_name} with id {entry_id}")
                        continue
                    new_entry = model_cls(**mongo_representation)
                    logging.debug(f"Trying to save {collection_name} with data: {mongo_representation}")
                    new_entry.save()
                    logging.info(f"Added new {collection_name} with id {new_entry.id}")
                    new_count += 1
                except Exception as e:
                    logging.error(f"Error while saving {collection_name} with data: {mongo_representation if mongo_representation else 'Failed before mongo representation'}")
                    raise e
        logging.info(f"Updated {updated_count} {collection_name}s and added {new_count} new {collection_name}s.")
    update_collection(SeasonInfo, mapped_seasons, "SeasonInfo")
    update_collection(PlayerDCIinfo, mapped_players, "PlayerDCIinfo")
    update_collection(SeasonStatOppo, opponenetseasondata, "SeasonStatOppo")
    update_collection(SeasonStatTeam, teamseasondata, "SeasonStatTeam")
    update_collection(SeasonStatPlayer, playerseasondata, "SeasonStatPlayer")
    update_collection(TeamInfo, team_info_dict, "TeamInfo")