import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))  
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Blueprint
bp_get_top10 = Blueprint('get_top10', __name__)
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
@log_and_catch_exceptions
@bp_get_top10.route('/get-top10-data', methods=['GET'])
def structure_data_for_categories():
    team_top_10_cache = {}
    team_top_10_data = {}
    try:
        be_logger.info("structure_data_for_categories: being accessed)")
        selected_year_from_frontend = request.args.get(
            'year', default=None, type=int)
        selected_season_type_from_frontend = request.args.get(
            'season_type', default=None, type=str)
        updated = False
        if selected_year_from_frontend is not None and selected_year_from_frontend != data.selected_year:
            data.selected_year = selected_year_from_frontend
            be_logger.info(
                f"structure_data_for_categories: updated via dropdown with {data.selected_year}")
            updated = True
        if selected_season_type_from_frontend is not None and selected_season_type_from_frontend != data.selected_season_type:
            data.selected_season_type = selected_season_type_from_frontend
            be_logger.info(
                f"structure_data_for_categories: updated via dropdown with {data.selected_season_type}")
            updated = True
        if not updated:
            be_logger.info(
                "structure_data_for_categories: with no updates from frontend")

        key = f"{data.selected_year}_{data.selected_season_type}"

        # Debugging code
        be_logger.debug(
            f"data.get_AllSeasonsTeamStatDetails_cache: {str(data.get_AllSeasonsTeamStatDetails_cache)[:200]}")

        filtered_items = [item for item in data.get_AllSeasonsTeamStatDetails_cache
                          if item['_id']['year'] == data.selected_year
                          ]
        be_logger.debug(
            f"Filtered data after applying year condition: {str(filtered_items)[:200]}")

        filtered_items = [item for item in data.get_AllSeasonsTeamStatDetails_cache
                          if item['_id']['year'] == data.selected_year
                          and item['_id']['season_type'] == data.selected_season_type
                          ]
        be_logger.debug(
            f"Filtered data after applying season_type condition: {str(filtered_items)[:200]}")

        # Original filtering
        data.selected_teams_stats_cache = [item for item in data.get_AllSeasonsTeamStatDetails_cache
                                           if item['_id']['year'] == data.selected_year
                                           and item['_id']['season_type'] == data.selected_season_type
                                           and 'seasonStatTeam' in item
                                           and 'games_played' in item['seasonStatTeam']
                                           and int(item['seasonStatTeam']['games_played']) > 0]

        be_logger.info(
            f"structure_data_for_categories: Data for year {data.selected_year} and season {data.selected_season_type} collected. Number of teams: {len(data.selected_teams_stats_cache)}")
        base_image_url = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/nfl/500/{TeamAlias}.png&w=40&h=40&cquality=40&scale=crop&location=origin&transparent=true"
        offensive_leaders, defensive_leaders = {}, {}

        def calculate_stat(x, mode='seasonStatTeam'):
            games_played = x[mode]['opponents_played'] if mode == 'seasonStatOppo' else x[mode]['games_played']
            try:
                return round((x[mode]['passing']['yards'] + x[mode]['rushing']['yards']) / games_played, 2)
            except ZeroDivisionError:
                be_logger.error(
                    "structure_data_for_categories: Division by zero encountered while calculating stat")
                return 0

        def build_leader_data(x, rank, mode='seasonStatTeam'):
            games_played = x['seasonStatOppo']['opponents_played'] if mode == 'seasonStatOppo' else x['seasonStatTeam']['games_played']
            return {
                'rank': rank,
                'team': f"{x['teamInfo']['team']['market']} {x['teamInfo']['team']['name']}",
                'games_played': games_played,
                'stat': calculate_stat(x, mode),
                'img': base_image_url.format(TeamAlias=x['teamInfo']['team']['alias'])
            }

        try:
            be_logger.info(
                "structure_data_for_categories: Preparing Offensive Leaders...")
            offensive_leaders = {
                'Total Yards': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatTeam'), reverse=True)[:10])],
                'Yards per Game': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatTeam'), reverse=True)[:10])],
                'Passing Yards': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatTeam']['passing']['yards'], reverse=True)[:10])],
                'Rushing Yards': [build_leader_data(x, i+1, 'seasonStatTeam') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatTeam']['rushing']['yards'], reverse=True)[:10])]
            }
            be_logger.info(
                "structure_data_for_categories: Offensive Leaders prepared.")
        except Exception as e:
            be_logger.error(
                f"structure_data_for_categories: Error preparing offensive leaders: {str(e)}")
            offensive_leaders = {}
            be_logger.error(
                f"structure_data_for_categories: Offensive Leaders Data: {offensive_leaders}")
        try:
            be_logger.info(
                "structure_data_for_categories: Preparing Defensive Leaders...")
            defensive_leaders = {
                'Total Yards Allowed': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatOppo'), reverse=False)[:10])],
                'Yards Allowed per Game': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: calculate_stat(x, 'seasonStatOppo'), reverse=False)[:10])],
                'Passing Yards Allowed': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatOppo']['passing']['yards'], reverse=False)[:10])],
                'Rushing Yards Allowed': [build_leader_data(x, i+1, 'seasonStatOppo') for i, x in enumerate(sorted(data.selected_teams_stats_cache, key=lambda x: x['seasonStatOppo']['rushing']['yards'], reverse=False)[:10])]
            }
            be_logger.info(
                "structure_data_for_categories: Defensive Leaders prepared.")
        except Exception as e:
            be_logger.error(
                f"structure_data_for_categories: Error preparing defensive leaders: {str(e)}")
            defensive_leaders = {}
            be_logger.error(
                f"structure_data_for_categories: Defensive Leaders Data: {defensive_leaders}")

        team_top_10_data = {
            'Offensive Leaders': offensive_leaders,
            'Defensive Leaders': defensive_leaders
        }

        be_logger.info(
            f"structure_data_for_categories: Preparing data for key: {key}")
        data.team_top_10_data_cache[key] = team_top_10_data

        team_top_10_cache = {}
        team_top_10_cache[key] = team_top_10_data

        if not bool(data.team_top_10_data_cache):
            be_logger.info(
                "get_data: Executed structure_data_for_categories function as top 10 data was not found in cache")

        try:
            sample_offensive_data = team_top_10_data['Offensive Leaders']['Yards per Game'][:2]
            be_logger.info(
                f"structure_data_for_categories: Sample 'Total Yards' for 'Offensive Leaders': {sample_offensive_data}")
        except (KeyError, TypeError) as e:
            be_logger.error(
                f"structure_data_for_categories:Error fetching 'Total Yards' for 'Offensive Leaders': {str(e)}")

        try:
            sample_defensive_data = team_top_10_data['Defensive Leaders']['Total Yards Allowed'][:2]
            be_logger.info(
                f"structure_data_for_categories: Sample 'Total Yards Allowed' for 'Defensive Leaders': {sample_defensive_data}")
        except (KeyError, TypeError) as e:
            be_logger.error(
                f"structure_data_for_categories: Error fetching 'Total Yards Allowed' for 'Defensive Leaders': {str(e)}")

        return jsonify(team_top_10_cache)

    except Exception as e:
        be_logger.error(
            f"Error in structure_data_for_categories: {str(e)}. Current state: team_top_10_data_cache: {data.team_top_10_data_cache}, team_top_10_cache: {team_top_10_cache}")

