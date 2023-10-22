import json
import requests
import time

import deserialize
import jsonpickle

from flask import Blueprint, Response, jsonify, request
from functools import wraps

import config

from orgs import DepthChart, Response, Team

backend_blueprint = Blueprint(name="backend_blueprint", import_name=__name__)

# =========================================|
# Decorator to restrict specific endpoints |
# to `localhost`-only:                     |
# =========================================|
def local_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if request.remote_addr == "127.0.0.1":
            return f(*args, **kwargs)
        else:
            return abort(403)   

    return wrapped

# ==================================|
# Default endpoint request wrapper: |
# ==================================|
def request_endpoint(url):
    body = requests.get(url).text
    return json.loads(body)

# ==============================|
# /league.json request wrapper: |
# ==============================|
def request_league_details(api_key):
    url = f"{config.base_uri}{config.league_endpoint}".replace(
        "{api_key}", api_key)

    return request_endpoint(url)

# ===================================|
# /full-roster.json request wrapper: |
# ===================================|
def request_team_details(api_key, team_id):
    url = f"{config.base_uri}{config.team_roster_endpoint}".replace(
        "{api_key}", api_key).replace("{id}", team_id)

    return request_endpoint(url)

# ===================================|
# /depth_chart.json request wrapper: |
# ===================================|
def request_depth_chart(api_key, year, season, week):
    url = f"{config.base_uri}{config.depth_chart_endpoint}".replace(
        "{api_key}", api_key).replace("{year}", year).replace(
        "{nfl_season_type}", season).replace("{nfl_season_week}", week)

    return request_endpoint(url)

# ================================================|
# Append eligible players by position & max depth |
# to overall players list:                        |
# ================================================|
def search_for_eligible_players(depth_section):
    players = []

    for depth_category in depth_section:
        if depth_category.position.name in config.allowed_positions:
            for player in depth_category.position.players:
                max_depth = config.max_depth_by_position[config.allowed_positions.
                    index(depth_category.position.name)]

                if player.depth <= max_depth:
                    players.append(player)

    return players

# ====================================================|
# Open (or re-open) the locally cached NFL data file: |
# ====================================================|
def open_cache():
    with open("export.json", "r") as file:
        data = deserialize.deserialize(Response,
            json.load(file))

    return data

# ========================|
# Refresh Local Cache API |
# ========================|
@backend_blueprint.route("refresh_cache")
@local_only
def refresh_cache():
    data = deserialize.deserialize(Response,
        request_league_details(config.api_key))

    # Intentionally throttle API call speed:
    time.sleep(1)

    depth_chart = deserialize.deserialize(DepthChart,
        request_depth_chart(config.api_key, config.depth_year,
        config.depth_nfl_season_type, config.depth_nfl_season_week))

    for conference in data.conferences:
        for division in conference.divisions:
            for team in division.teams:
                # Parse out desired depth by position per team:
                for depth_chart_team in depth_chart.teams:
                    if team.id == depth_chart_team.id:
                        # Reset the equivalent team's player list status
                        # status before compiling valid players to add:
                        team.players = []

                        # Check OFF, DEF, & ST for players in eligible
                        # positions & depth by configuration definition:
                        team.players.extend(search_for_eligible_players(depth_chart_team.offense))
                        team.players.extend(search_for_eligible_players(depth_chart_team.defense))
                        team.players.extend(search_for_eligible_players(depth_chart_team.special_teams))
                        
                        break
                    else:
                        print(f'Team not found for {team.name}?')

    serializedData = jsonpickle.encode(data, unpicklable=False)

    with open("export.json", "w") as file:
        file.write(json.dumps(json.loads(serializedData)))
