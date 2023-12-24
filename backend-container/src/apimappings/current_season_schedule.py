from src.models.boxscore_info import (
    gamebs, quarter, overtime, BoxscoreInfo)
import json
import pandas
from src.models.game_info import (
    gamegame, awayteam, hometeam, broadcast, weather, wind, GameInfo)
from src.models.league_info import (
    game, season, changelog, leagueweek, LeagueInfo)
from src.models.venue_info import (venue1, location, VenueInfo)
import time
import os
import requests
from bson import ObjectId
from mongoengine import DecimalField, EmbeddedDocumentField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
from uuid import UUID
from datetime import datetime
from flask import Blueprint, jsonify, Flask
import sys
sys.path.append("os.getenv('LPATH')/src/")
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
bp = Blueprint('current_season_schedule', __name__)


def log_and_catch_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            be_logger.error(f"Error in {func.__name__}: {e}")
            raise Exception(f"Error in {func.__name__}: {e}")
    return func_wrapper


@log_and_catch_exceptions
@bp.route('/fetchAndSaveAllSeasonsSchedule', methods=['GET'])
def fetch_and_save_all_seasons_schedule():
    print("fetch_and_save_all_seasons_schedule called")
    API_KEY = os.getenv('APIKEY')
    SEASONS_API_URL = "http://api.sportradar.us/nfl/official/trial/v7/en/games/{year}/{season_type}/schedule.json?api_key={API_KEY}"
    for year in range(2016, 2024):
        for season_type in ['REG', 'PST']:
            url = SEASONS_API_URL.format(
                year=year, season_type=season_type, API_KEY=API_KEY)
            print(datetime.now(), "Requesting URL:", url)
            response = requests.get(url)
            print("Response status code:", response.status_code)
            if response.status_code != 200:
                return f"GetCurrentSeasonScheduleError for {year} {season_type}: {response.status_code}"
            data = response.json()
            venue_info_dict = extract_venue_info(data)
            league_info_dict = extract_league_info(data)
            game_info_dict = extract_game_info(data)
            boxscore_info_dict = extract_boxscore_info(data)
            mapped_venues = map_venue_info(venue_info_dict)
            mapped_leagues = map_league_info(league_info_dict)
            mapped_games = map_game_info(game_info_dict)
            mapped_boxscores = map_boxscore_info(boxscore_info_dict)
            save_to_database(mapped_venues, mapped_leagues,
                             mapped_games, mapped_boxscores)
            print("Games saved to database")
            time.sleep(2)
    return "Schedule data for all seasons fetched and saved successfully."

@log_and_catch_exceptions
@bp.route('/fetchAndSaveWeeklySchedule', methods=['GET'])
def fetch_and_save_weekly_schedule():
    print("fetch_and_save_weekly_schedule called")
    API_KEY = os.getenv('APIKEY')
    season_year = datetime.now().year
    season_type = 'REG'  # or 'PRE' or 'POST' depending on the current season
    # adjust this calculation as needed
    week_number = datetime.now().isocalendar()[1] - 34
    WEEKLY_SCHEDULE_API_URL = 'http://api.sportradar.us/nfl/official/trial/v7/en/games/{season_year}/{season_type}/{week_number}/schedule.json?api_key={API_KEY}'
    url = WEEKLY_SCHEDULE_API_URL.format(
        season_year=season_year, season_type=season_type, week_number=week_number, API_KEY=API_KEY)
    print(datetime.now(), "Requesting URL:", url)
    response = requests.get(url)
    print("Response status code:", response.status_code)
    if response.status_code != 200:
        return f"GetCurrentSeasonScheduleError for {season_year} {season_type} {week_number}: {response.status_code}"
    data = response.json()
    # print("data:", data)
    venue_info_dict = extract_venue_info(data)
    league_info_dict = extract_league_info(data)
    game_info_dict = extract_game_info(data)
    boxscore_info_dict = extract_boxscore_info(data)
    mapped_venues = map_venue_info(venue_info_dict)
    mapped_leagues = map_league_info(league_info_dict)
    mapped_games = map_game_info(game_info_dict)
    mapped_boxscores = map_boxscore_info(boxscore_info_dict)
    save_to_database(mapped_venues, mapped_leagues,
                     mapped_games, mapped_boxscores)

    time.sleep(2)
    return ("Schedule data for all seasons fetched and saved successfully")


@log_and_catch_exceptions
def extract_boxscore_info(data):
    boxscore_info_dict = {}
    weeks_or_week = data.get('weeks') or data.get('week')
    if not weeks_or_week:
        return boxscore_info_dict
    if isinstance(weeks_or_week, dict):
        weeks_or_week = [weeks_or_week]
    for week in weeks_or_week:
        for game in week['games']:
            boxscore_info = {
                'game_id': game['id'],
                'attendance': game.get('attendance', None),
            }
            boxscore_info['home_teambs'] = game['home']['alias']
            boxscore_info['away_teambs'] = game['away']['alias']
            scoring = game.get('scoring', {})
            boxscore_info['home_team_total_points'] = scoring.get(
                'home_points')
            boxscore_info['away_team_total_points'] = scoring.get(
                'away_points')
            boxscore_info['quarters'] = []
            for quarter in scoring.get('periods', []):
                quarter_info = {
                    'quarter_id': quarter['id'],
                    'quarter_number': quarter['number'],
                    'quarter_sequence': quarter['sequence'],
                    'away_points_for_quarter': quarter['away_points'],
                    'home_points_for_quarter': quarter['home_points'],
                }
                boxscore_info['quarters'].append(quarter_info)
            boxscore_info['overtime'] = []
            for overtime in scoring.get('overtime', []):
                overtime_info = {
                    'overtime_id': overtime['id'],
                    'overtime_number': overtime['number'],
                    'overtime_sequence': overtime['sequence'],
                    'away_points_for_overtime': overtime['away_points'],
                    'home_points_for_overtime': overtime['home_points'],
                }
                boxscore_info['overtime'].append(overtime_info)
            boxscore_info_dict[game['id']] = boxscore_info
    return boxscore_info_dict


@log_and_catch_exceptions
def map_boxscore_info(boxscore_info_dict):
    if boxscore_info_dict is None:
        return {}
    mapped_boxscores = {}
    for gamebs_id in boxscore_info_dict:
        try:
            gamebs_details = boxscore_info_dict[gamebs_id]
            game_embeded = gamebs(
                id=gamebs_details['game_id'],
                attendance=gamebs_details['attendance'],
                hometeam=gamebs_details['home_teambs'],
                hometeamtotalpoints=gamebs_details['home_team_total_points'],
                awayteam=gamebs_details['away_teambs'],
                awayteamtotalpoints=gamebs_details['away_team_total_points']
            )
            quarters_embedded_list = []
            for quarter_data in gamebs_details.get('quarters', []):
                quarter_embedded = quarter(
                    quarter_id=quarter_data['quarter_id'],
                    quarter_number=quarter_data['quarter_number'],
                    quarter_sequence=quarter_data['quarter_sequence'],
                    awayteampointsforquarter=quarter_data['away_points_for_quarter'],
                    hometeampointsforquarter=quarter_data['home_points_for_quarter']
                )
                quarters_embedded_list.append(quarter_embedded)

            overtime_embedded_list = []
            for overtime_data in gamebs_details.get('overtime', []):
                overtime_embedded = overtime(
                    overtime_id=overtime_data['overtime_id'],
                    overtime_number=overtime_data['overtime_number'],
                    overtime_sequence=overtime_data['overtime_sequence'],
                    awayteamovertimepoints=overtime_data['away_points_for_overtime'],
                    hometeamovertimepoints=overtime_data['home_points_for_overtime']
                )
                overtime_embedded_list.append(overtime_embedded)

            boxscore_info_instance = BoxscoreInfo(
                gamebs=game_embeded,
                overtimes=overtime_embedded_list,
                quarters=quarters_embedded_list
            )
            mapped_boxscores[gamebs_id] = boxscore_info_instance
        except Exception as e:
            print(f"Error processing gamebs_id {gamebs_id}: {e}")
            raise e
    # print("Mapped Boxscore Info:", mapped_boxscores)
    return mapped_boxscores


@log_and_catch_exceptions
def extract_game_info(data):
    game_info_dict = {}
    weeks_or_week = data.get('weeks') or data.get('week')
    if not weeks_or_week:
        return game_info_dict
    if isinstance(weeks_or_week, dict):
        weeks_or_week = [weeks_or_week]  # make it a list so we can iterate
    for week in weeks_or_week:
        for game in week['games']:
            game_ginfo = {'season_id': data.get('id', None)}
            game_ginfo['week_id'] = week.get('id', None)
            game_ginfo['venue_id'] = game['venue']['id']
            game_ginfo['game_id'] = game['id']
            game_ginfo['status'] = game['status']
            game_ginfo['scheduled'] = game['scheduled']
            game_ginfo['attendance'] = game.get(
                'attendance', None)  # or some default value
            game_ginfo['entry_mode'] = game.get(
                'entry_mode', None)  # or some default value
            game_ginfo['sr_id'] = game.get('sr_id')
            game_ginfo['neutral_site'] = game.get(
                'neutral_site', None)  # or some default value
            game_ginfo['game_type'] = game.get(
                'game_type', None)  # or some default value
            game_ginfo['conference_game'] = game.get(
                'conference_game', None)  # or some default value
            game_ginfo['title'] = game.get(
                'title', None)  # or some default value
            game_ginfo['duration'] = game.get(
                'duration', None)  # or some default value
            game_ginfo['home_id'] = game['home']['id']
            game_ginfo['home_name'] = game['home']['name']
            game_ginfo['home_alias'] = game['home']['alias']
            game_ginfo['home_game_number'] = game['home'].get('game_number')
            game_ginfo['home_sr_id'] = game['home'].get('sr_id')
            game_ginfo['away_id'] = game['away']['id']
            game_ginfo['away_name'] = game['away']['name']
            game_ginfo['away_alias'] = game['away']['alias']
            game_ginfo['away_game_number'] = game['away'].get('game_number')
            game_ginfo['away_sr_id'] = game['away'].get('sr_id')
            game_ginfo['broadcast_network'] = game.get('broadcast', {}).get(
                'network', None)  # or some default value
            game_ginfo['broadcast_channel'] = game.get(
                'broadcast', {}).get('channel', None)
            game_ginfo['broadcast_satellite'] = game.get(
                'broadcast', {}).get('satellite', None)
            game_ginfo['broadcast_internet'] = game.get(
                'broadcast', {}).get('internet', None)
            game_ginfo['weather_condition'] = game.get(
                'weather', {}).get('condition', None)
            game_ginfo['weather_humidity'] = game.get(
                'weather', {}).get('humidity', None)
            game_ginfo['weather_temp'] = game.get(
                'weather', {}).get('temp', None)
            game_ginfo['wind_speed'] = game.get(
                'weather', {}).get('wind', {}).get('speed', None)
            game_ginfo['wind_direction'] = game.get(
                'weather', {}).get('wind', {}).get('direction', None)
            game_info_dict[game['id']] = game_ginfo
            # print("game_info_dict:", game_info_dict)
    return game_info_dict


@log_and_catch_exceptions
def map_game_info(game_info_dict):
    mapped_games = {}
    for game_id in game_info_dict:
        game_details = game_info_dict[game_id]
        # print("game_details:", game_details)
        # Convert integer IDs to string UUIDs if needed
        game_embedded1 = gamegame(
            id=game_details['game_id'],
            # number=None,
            conference_game=game_details['conference_game'],
            # coverage=None,
            duration=game_details['duration'],
            entry_mode=game_details['entry_mode'],
            game_type=game_details['game_type'],
            sr_id=game_details['sr_id'],
            # last_modified=None,
            scheduled=game_details['scheduled'],
            status=game_details['status'],
            title=game_details['title'],
            neutral_site=game_details['neutral_site'],
            seasonid=game_details['season_id'],
            leagueweek=game_details['week_id'],
            venueid=game_details['venue_id']
            # season_id=None
        )
        away_embedded1 = awayteam(
            alias=game_details['away_alias'],
            id=game_details['away_id'],
            name=game_details['away_name'],
            game_number=game_details['away_game_number'],
            sr_id=game_details['away_sr_id'],
            # market=None
        )
        home_embedded1 = hometeam(
            alias=game_details['home_alias'],
            id=game_details['home_id'],
            name=game_details['home_name'],
            game_number=game_details['home_game_number'],
            sr_id=game_details['home_sr_id'],
            # market=None
        )
        broadcast_embedded = broadcast(
            channel=game_details['broadcast_channel'],
            internet=game_details['broadcast_internet'],
            network=game_details['broadcast_network'],
            satellite=game_details['broadcast_satellite']
        )
        weather_embedded = weather(
            condition=game_details['weather_condition'],
            humidity=game_details['weather_humidity'],
            temp=game_details['weather_temp']
        )
        wind_embedded = wind(
            direction=game_details['wind_direction'],
            speed=game_details['wind_speed']
        )
        game_info_instance = GameInfo(
            gamegame=game_embedded1,
            awayteam=away_embedded1,
            hometeam=home_embedded1,
            broadcast=broadcast_embedded,
            weather=weather_embedded,
            wind=wind_embedded
        )
        mapped_games[game_id] = game_info_instance
    # print("Mapped Game Info:", mapped_games)
    return mapped_games


@log_and_catch_exceptions
def extract_league_info(data):
    league_info_dict = {}
    season = data  # Assuming there's only one season in the list
    weeks_or_week = season.get('weeks') or season.get('week')
    if not weeks_or_week:
        return league_info_dict
    if isinstance(weeks_or_week, dict):
        weeks_or_week = [weeks_or_week]  # make it a list so we can iterate
    for week in weeks_or_week:
        league_info = {
            'Season Id': season['id'],
            'Season Year': season['year'],
            'Season Type': season['type'],
            'Season Name': season['name'],
            'Week Id': week['id'],
            'Week Sequence': week['sequence'],
            'Week Title': week['title'],
        }
        bye_week_teams = week.get('bye_week', [])
        bye_week_team_info = []
        for team in bye_week_teams:
            team_info = team.get('team', {})  # Get the team details
            team_id = team_info.get('id')
            team_name = team_info.get('name')
            team_alias = team_info.get('alias')
            # Set a default value if 'sr_id' is missing
            team_sr_id = team_info.get('sr_id', None)
            bye_week_team_info.append(
                {'id': team_id, 'name': team_name, 'alias': team_alias, 'sr_id': team_sr_id})
        league_info['Bye Week Team Info'] = bye_week_team_info
        league_info_dict[league_info['Week Id']] = league_info
    return league_info_dict


@log_and_catch_exceptions
def map_league_info(league_info_dict):
    mapped_leagues = {}
    for weekid, league_details in league_info_dict.items():
        season_embedded = season(
            weekid=league_details['Week Id'],
            id=league_details['Season Id'],
            name=league_details['Season Name'],
            type=league_details['Season Type'],
            year=league_details['Season Year']
        )
        week_embedded_list = []  # List to store leagueweek instances
        if bye_week_team_info_list := league_details['Bye Week Team Info']:
            for team_info in bye_week_team_info_list:
                week_embedded = leagueweek(
                    id=league_details['Week Id'],
                    sequence=league_details['Week Sequence'],
                    title=league_details['Week Title'],
                    byeweekteamalias=team_info.get('alias', None),
                    byeweekteamid=team_info.get('id', None),
                    byeweekteamname=team_info.get('name', None),
                    byeweekteamsrid=team_info.get('sr_id', None)
                )
                week_embedded_list.append(week_embedded)
        else:
            week_embedded = leagueweek(
                id=league_details['Week Id'],
                sequence=league_details['Week Sequence'],
                title=league_details['Week Title']
            )
            week_embedded_list.append(week_embedded)

        # Create a new dictionary for each LeagueInfo instance
        league_info_instance = LeagueInfo(
            season=season_embedded,
            leagueweek=week_embedded_list
        )
        mapped_leagues[weekid] = league_info_instance
    print("Mapped Leagues:", mapped_leagues)
    return mapped_leagues


@log_and_catch_exceptions
def extract_venue_info(data):
    venue_info_dict = {}
    weeks_or_week = data.get('weeks') or data.get('week')
    if not weeks_or_week:
        return venue_info_dict
    if isinstance(weeks_or_week, dict):
        weeks_or_week = [weeks_or_week]  # make it a list so we can iterate
    for week in weeks_or_week:
        for game in week['games']:
            venue_info = {
                'id': game['venue']['id'],
                'name': game['venue']['name'],
                'city': game['venue']['city'],
                'state': game['venue'].get('state'),
            }
            venue_info['country'] = game['venue'].get('country')
            venue_info['zip'] = game['venue'].get('zip')
            venue_info['address'] = game['venue']['address']
            venue_info['capacity'] = game['venue']['capacity']
            venue_info['surface'] = game['venue']['surface']
            venue_info['roof_type'] = game['venue']['roof_type']
            venue_info['sr_id'] = game['venue']['sr_id']
            venue_info['lat'] = game.get('venue', {}).get(
                'location', {}).get('lat', None)
            venue_info['lng'] = game.get('venue', {}).get(
                'location', {}).get('lng', None)
            venue_info_dict[game['venue']['id']] = venue_info
                    # print("venue_info_dict:", venue_info_dict)
    return venue_info_dict


@log_and_catch_exceptions
def map_venue_info(venue_info_dict):
    mapped_venues = {}
    for venue_id, venue_details in venue_info_dict.items():

        venue_embedded = venue1(
            id=venue_details['id'],
            address=venue_details['address'],
            capacity=venue_details['capacity'],
            city=venue_details['city'],
            country=venue_details['country'],
            name=venue_details['name'],
            sr_id=venue_details['sr_id'],
            roof_type=venue_details['roof_type'],
            state=venue_details['state'],
            surface=venue_details['surface'],
            zip=venue_details['zip']
        )

        location_embedded = location(
            lat=venue_details['lat'],
            lng=venue_details['lng']
        )

        venue_info_instance = VenueInfo(
            venue1=venue_embedded,
            location=location_embedded
        )
        mapped_venues[venue_id] = venue_info_instance
    # print(len(mapped_venues))
    # print("Mapped_Venues", mapped_venues)
    return mapped_venues

@log_and_catch_exceptions
def save_to_database(mapped_venues, mapped_leagues, mapped_games, mapped_boxscores):
    print("save_to_database called")

    def update_collection(model_cls, mapped_data, collection_name):
        updated_count = 0
        new_count = 0
        for mapped_entry_info in mapped_data:
            mapped_entry = mapped_entry_info
            mapped_entry_id = mapped_entry.id  # Extract the ID from the mapped entry
            existing_entry = model_cls.objects(id=mapped_entry_id).first()

            # Print the ID being checked
            print(f"Checking {collection_name} with ID: {mapped_entry_id}")

            if existing_entry:
                updated_fields = []
                for field_name in existing_entry._fields.keys():
                    existing_value = getattr(existing_entry, field_name)
                    mapped_value = getattr(mapped_entry, field_name)
                    if existing_value != mapped_value:
                        setattr(existing_entry, field_name, mapped_value)
                        updated_fields.append(field_name)
                if updated_fields:
                    existing_entry.save()
                    updated_count += 1
                    print(
                        f"Updated {collection_name} {mapped_entry_id}: Updated fields: {', '.join(updated_fields)}")
                else:
                    print(
                        f"No updates needed for {collection_name} {mapped_entry_id}")
            else:
                mongo_representation = mapped_entry.to_mongo()
                print(
                    f"Mapped entry: {mapped_entry}, Mongo representation: {mongo_representation}")
                new_entry = model_cls(**mapped_entry.to_mongo())
                new_entry.save()
                new_count += 1
                print(f"Added new {collection_name} with id {mapped_entry_id}")

        print(
            f"Updated {updated_count} {collection_name}s and added {new_count} new {collection_name}s.")

    update_collection(VenueInfo, mapped_venues.values(), "venue")
    update_collection(LeagueInfo, mapped_leagues.values(), "league")
    update_collection(GameInfo, mapped_games.values(), "game")
    update_collection(BoxscoreInfo, mapped_boxscores.values(), "boxscore")