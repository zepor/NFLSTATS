import os
import sys
import time
from datetime import datetime
from flask import Blueprint
from src.models.play_by_play_info import (quarter, location, possession, start_location, play, score)
from pymongo import MongoClient
from security import safe_requests

sys.path.append("os.getenv('LPATH')/src/")
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
bp = Blueprint('pbp', __name__)

def log_and_catch_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            be_logger.error(f"Error in {func.__name__}: {e}")
            raise Exception(f"Error in {func.__name__}: {e}")
    return func_wrapper

@log_and_catch_exceptions
def fetch_game_ids(season_year):
    print(f"Fetching game IDs for the season year: {season_year}")
    client = MongoClient(os.getenv('MONGODB_URL'))
    db = client.Current_Season
    collection = db.GameInfo
    # Define the start and end dates for the season year
    start_date = datetime(season_year - 1, 6,
                          1).strftime("%Y-%m-%dT%H:%M:%S.000+00:00")
    end_date = datetime(season_year, 5, 31, 23, 59, 59).strftime(
        "%Y-%m-%dT%H:%M:%S.000+00:00")
    query = {
        "gamegame.scheduled": {
            "$gte": start_date,
            "$lte": end_date
        }
    }
    games = collection.find(query, {"_id": 1})
    game_ids = [game["_id"] for game in games]
    game_count = collection.count_documents(query)
    print(f"Found {game_count} games for the season year: {season_year}")
    return game_ids, game_count

@log_and_catch_exceptions
def fetch_and_pbp_by_game(game_id):
    print("fetch_and_pbp_by_game")
    API_KEY = os.getenv('APIKEY')
    PLAY_BY_PLAY_API_URL = f"https://api.sportradar.us/nfl/official/trial/v7/en/games/{game_id}/pbp.json?api_key={api_key}"
    response = safe_requests.get(PLAY_BY_PLAY_API_URL, timeout=10)
    print("Response status code:", response.status_code)
    if response.status_code != 200:
        return f"GetCurrentSeasonScheduleError for {game_id} {year}: {response.status_code}"
    data = response.json()
    # print("data:", data)
    venue_info_dict = extract_venue_info(data)
    standings_info_dict = extract_standings_info(data)
    team_info_dict = extract_team_info(data)
    player_info_dict = extract_player_info(data)
    playstat_info_dict = extract_playstat_info(data)
    pbp_info_dict = extract_pbp_info(data)
    league_info_dict = extract_league_info(data)
    game_info_dict = extract_game_info(data)
    boxscore_info_dict = extract_boxscore_info(data)
    mapped_venues = map_venue_info(venue_info_dict)
    mapped_standings = map_standings_info(standings_info_dict)
    mapped_teams = map_team_info(team_info_dict)
    mapped_players = map_player_info(player_info_dict)
    mapped_playstats = map_playstat_info(playstat_info_dict)
    mapped_pbps = map_pbp_info(pbp_info_dict)
    mapped_leagues = map_league_info(league_info_dict)
    mapped_games = map_game_info(game_info_dict)
    mapped_boxscores = map_boxscore_info(boxscore_info_dict)
    save_to_database(mapped_venues, mapped_standings, mapped_teams, mapped_players, mapped_playstats, mapped_pbps, mapped_leagues, mapped_games, mapped_boxscores)
    time.sleep(2)
    return (f"Schedule data for {year} fetched and saved successfully")

@log_and_catch_exceptions
@bp.route('/pbpgames/<int:year>', methods=['GET'])
def process_games_for_year(year):
    print(f"Starting to process games for the year: {year}")
    game_ids, game_count = fetch_game_ids(year)
    counter = 0
    for game_id in game_ids:
        response = fetch_and_pbp_by_game(game_id)
        print(f"Processed game ID {game_id}: {response[:150]}")
        counter += 1
        time.sleep(2)
    return f"Processed {counter} games out of {game_count} for the year {year}"

@log_and_catch_exceptions
def extract_play_by_play_data(source):
    # Fetch play-by-play data from the source (API, database, file, etc.)
    # This is an example of extracting from an API
    response = safe_requests.get(source)
    return response.json()

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
            print("venue_info_dict:", venue_info_dict)
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
    print(len(mapped_venues))
    print("Mapped_Venues", mapped_venues)
    return mapped_venues


@log_and_catch_exceptions
def extract_standings_info(data):
    # Extract standings information from the play-by-play data
    standings_info = data["standings"]
    return standings_info_dict


@log_and_catch_exceptions
def map_standings_info(standings_info_dict):
    mapped_standings = {}
    for standings_id, standings_details in standings_info_dict.items():

        team_embedded = team(
            id=standings_details['id'],
            alias=standings_details['alias'],
            market=standings_details['market'],
            name=standings_details['name'],
            sr_id=standings_details['sr_id']
        )

        standings_info_instance = StandingsInfo(
            team=team_embedded
        )
        mapped_standings[standings_id] = standings_info_instance
    print(len(mapped_standings))
    print("Mapped_Standings", mapped_standings)
    return mapped_standings


@log_and_catch_exceptions
def extract_team_info(data):
    # Extract team information from the play-by-play data
    team_info = data["team"]
    return team_info_dict


@log_and_catch_exceptions
def map_team_info(team_info_dict):
    mapped_teams = {}
    for team_id, team_details in team_info_dict.items():

        team_embedded = team(
            id=team_details['id'],
            alias=team_details['alias'],
            market=team_details['market'],
            name=team_details['name'],
            sr_id=team_details['sr_id']
        )

        team_info_instance = TeamInfo(
            team=team_embedded
        )
        mapped_teams[team_id] = team_info_instance
    print(len(mapped_teams))
    print("Mapped_Teams", mapped_teams)
    return mapped_teams


@log_and_catch_exceptions
def extract_player_info(data):
    # Extract player information from the play-by-play data
    player_info = data["player"]
    return player_info_dict


@log_and_catch_exceptions
def map_player_info(player_info_dict):
    mapped_players = {}
    for player_id, player_details in player_info_dict.items():

        player_embedded = player(
            id=player_details['id'],
            active=player_details['active'],
            birth_date=player_details['birth_date'],
            birth_place=player_details['birth_place'],
            college=player_details['college'],
            country=player_details['country'],
            depth_chart_position=player_details['depth_chart_position'],
            depth_chart_order=player_details['depth_chart_order'],
            experience=player_details['experience'],
            first_name=player_details['first_name'],
            height=player_details['height'],
            jersey_number=player_details['jersey_number'],
            last_name=player_details['last_name'],
            middle_name=player_details['middle_name'],
            name_suffix=player_details['name_suffix'],
            position=player_details['position'],
            primary_position=player_details['primary_position'],
            pro_debut=player_details['pro_debut'],
            sr_id=player_details['sr_id'],
            status=player_details['status'],
            weight=player_details['weight']
        )

        player_info_instance = PlayerInfo(
            player=player_embedded
        )
        mapped_players[player_id] = player_info_instance
    print(len(mapped_players))
    print("Mapped_Players", mapped_players)
    return mapped_players


@log_and_catch_exceptions
def extract_playstat_info(data):
    # Extract playstat information from the play-by-play data
    playstat_info = data["playstat"]
    return playstat_info_dict


@log_and_catch_exceptions
def map_playstat_info(playstat_info_dict):
    mapped_playstats = {}
    for playstat_id, playstat_details in playstat_info_dict.items():

        team_embedded = team(
            id=playstat_details['id'],
            alias=playstat_details['alias'],
            market=playstat_details['market'],
            name=playstat_details['name'],
            sr_id=playstat_details['sr_id']
        )

        player_embedded = player(
            id=playstat_details['id'],
            active=playstat_details['active'],
            birth_date=playstat_details['birth_date'],
            birth_place=playstat_details['birth_place'],
            college=playstat_details['college'],
            country=playstat_details['country'],
            depth_chart_position=playstat_details['depth_chart_position'],
            depth_chart_order=playstat_details['depth_chart_order'],
            experience=playstat_details['experience'],
            first_name=playstat_details['first_name'],
            height=playstat_details['height'],
            jersey_number=playstat_details['jersey_number'],
            last_name=playstat_details['last_name'],
            middle_name=playstat_details['middle_name'],
            name_suffix=playstat_details['name_suffix'],
            position=playstat_details['position'],
            primary_position=playstat_details['primary_position'],
            pro_debut=playstat_details['pro_debut'],
            sr_id=playstat_details['sr_id'],
            status=playstat_details['status'],
            weight=playstat_details['weight']
        )

        playstat_embedded = playstat(
            id=playstat_details['id'],
            category=playstat_details['category'],
            sequence=playstat_details['sequence'],
            clock=playstat_details['clock'],
            updated=playstat_details['updated'],
            yards=playstat_details['yards'],
            team=team_embedded,
            player=player_embedded
        )

        playstat_info_instance = PlayStatInfo(
            playstat=playstat_embedded
        )
        mapped_playstats[playstat_id] = playstat_info_instance
    print(len(mapped_playstats))
    print("Mapped_Playstats", mapped_playstats)
    return mapped_playstats


@log_and_catch_exceptions
def extract_pbp_info(data):
    # Extract pbp information from the play-by-play data
    pbp_info = data["pbp"]
    return pbp_info_dict


@log_and_catch_exceptions
def map_pbp_info(pbp_info_dict):
    for pbp_id, pbp_details in pbp_info_dict.items():

        quarter_embedded = quarter(
            number=pbp_details['number'],
            sequence=pbp_details['sequence']
        )

        location_embedded = location(
            lat=pbp_details['lat'],
            lng=pbp_details['lng']
        )

        possession_embedded = possession(
            id=pbp_details['id'],
            name=pbp_details['name'],
            alias=pbp_details['alias'],
            market=pbp_details['market'],
            sr_id=pbp_details['sr_id']
        )

        start_location_embedded = start_location(
            lat=pbp_details['lat'],
            lng=pbp_details['lng']
        )

        play_embedded = play(
            id=pbp_details['id'],
            sequence=pbp_details['sequence'],
            updated=pbp_details['updated'],
            clock=pbp_details['clock'],
            type=pbp_details['type'],
            wall_clock=pbp_details['wall_clock'],
            description=pbp_details['description'],
            period=pbp_details['period'],
            down=pbp_details['down'],
            end_possession=pbp_details['end_possession'],
            end_yardline=pbp_details['end_yardline'],
            first_down=pbp_details['first_down'],
            gain=pbp_details['gain'],
            loss=pbp_details['loss'],
            net=pbp_details['net'],
            points=pbp_details['points'],
            pos_team_score=pbp_details['pos_team_score'],
            redzone=pbp_details['redzone'],
            start_possession=pbp_details['start_possession'],
            start_yardline=pbp_details['start_yardline'],
            yfd=pbp_details['yfd'],
            yards=pbp_details['yards'],
            yards_to_goal=pbp_details['yards_to_goal'],
            quarter=quarter_embedded,
            location=location_embedded,
            possession=possession_embedded,
            start_location=start_location_embedded
        )

        score_embedded = score(
            id=pbp_details['id'],
            sequence=pbp_details['sequence'],
            updated=pbp_details['updated'],
            clock=pbp_details['clock'],
            type=pbp_details['type'],
        )
    return {}


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
def extract_boxscore_info(data):
    # Extract general game information
    game_id = data['id']
    attendance = data.get('attendance')
    home_team = data['summary']['home']['alias']
    away_team = data['summary']['away']['alias']
    home_team_points = data['summary']['home']['points']
    away_team_points = data['summary']['away']['points']

    # Extract coin toss information
    coin_toss_info = extract_coin_toss_info(data)

    # Extract timeouts and challenges information
    timeouts_info = extract_timeouts_info(data)
    challenges_info = extract_challenges_info(data)

    # Extract quarter and overtime information
    quarters_info = extract_quarters_info(data)
    overtime_info = extract_overtime_info(data)

    return {
        game_id: {
            'game_id': game_id,
            'attendance': attendance,
            'home_team': home_team,
            'away_team': away_team,
            'home_team_points': home_team_points,
            'away_team_points': away_team_points,
            'coin_toss': coin_toss_info,
            'timeouts': timeouts_info,
            'challenges': challenges_info,
            'quarters': quarters_info,
            'overtimes': overtime_info,
        }
    }

# Helper functions to extract specific details

def extract_coin_toss_info(data):
    # Placeholder for coin toss data
    coin_toss_data = game_data.get('coin_toss', {})
    # Extracting coin toss information
    return coin_toss(
        awayteamcoincointossdecision='',  # extract this from data
        awayteamcoincointossdirection='',  # extract this from data
        awayteamcoincointossoutcome='',    # extract this from data
        hometeamcoincointossdecision='',   # extract this from data
        hometeamcoincointossdirection='',  # extract this from data
        hometeamcoincointossoutcome=''     # extract this from data
    )

def extract_timeouts_info(data):
    # Assuming timeout details are part of each play/event
    # Loop through plays/events to aggregate timeout info
    # Extract and aggregate timeout information
    return timeouts(
        awayteamtimeoutstimeoutsremaining=0,  # aggregate this from data
        awayteamtimeoutstimeoutsused=0,       # aggregate this from data
        hometeamtimeoutstimeoutsremaining=0,  # aggregate this from data
        hometeamtimeoutstimeoutsused=0        # aggregate this from data
    )
    
def extract_challenges_info(data):
    # Assuming challenge details are part of specific plays/events
    # Loop through plays/events to aggregate challenge info
    # Extract and aggregate challenge information
    return challenges(
        awayteamchallengeschallengesremaining=0,  # aggregate this from data
        awayteamchallengeschallengesused=0,       # aggregate this from data
        hometeamchallengeschallengesremaining=0,  # aggregate this from data
        hometeamchallengeschallengesused=0        # aggregate this from data
    )


def extract_quarters_info(data):
    return [
        quarter(
            quarter_id=quarter['id'],
            quarter_number=quarter['number'],
            quarter_sequence=quarter['sequence'],
            awayteampointsforquarter=quarter['scoring']['away']['points'],
            hometeampointsforquarter=quarter['scoring']['home']['points'],
        )
        for quarter in data['periods']
        if quarter['period_type'] == 'quarter'
    ]


def extract_overtime_info(data):
    return [
        overtime(
            overtime_id=quarter['id'],
            overtime_number=quarter['number'],
            overtime_sequence=quarter['sequence'],
            awayteamovertimepoints=quarter['scoring']['away']['points'],
            hometeamovertimepoints=quarter['scoring']['home']['points'],
        )
        for quarter in data['periods']
        if quarter['period_type'] == 'overtime'
    ]





@log_and_catch_exceptions
def map_boxscore_info(boxscore_info_dict):
    mapped_boxscores = {}
    for game_id, info in boxscore_info_dict.items():
        try:
            # Create instances of your embedded documents
            coin_toss_instance = coin_toss(...)
            challenges_instance = challenges(...)
            timeouts_instance = timeouts(...)
            quarters_instances = [quarter(...) for _ in info['quarters']]
            overtime_instances = [overtime(...) for _ in info['overtimes']]

            # Create main BoxscoreInfo instance
            boxscore_info_instance = BoxscoreInfo(
                gamebs=gamebs(id=info['game_id']),
                coin_toss=coin_toss_instance,
                challenges=challenges_instance,
                timeouts=timeouts_instance,
                quarters=quarters_instances,
                overtimes=overtime_instances,
            )
            mapped_boxscores[game_id] = boxscore_info_instance
        except Exception as e:
            print(f"Error processing game_id {game_id}: {e}")
            raise e

    return mapped_boxscores


def save_to_database(mapped_venues, mapped_standings, mapped_teams, mapped_players, mapped_playstats, mapped_pbps, mapped_leagues, mapped_games, mapped_boxscores):
    print("Saving to database")
    client = MongoClient(os.getenv('MONGODB_URL'))
    db = client.Current_Season
    collection = db.VenueInfo
    for venue_id in mapped_venues:
        venue_info_instance = mapped_venues[venue_id]
        venue_info_instance.save()
    collection = db.StandingsInfo
    for standings_id in mapped_standings:
        standings_info_instance = mapped_standings[standings_id]
        standings_info_instance.save()
    collection = db.TeamInfo
    for team_id in mapped_teams:
        team_info_instance = mapped_teams[team_id]
        team_info_instance.save()
    collection = db.PlayerInfo
    for player_id in mapped_players:
        player_info_instance = mapped_players[player_id]
        player_info_instance.save()
    collection = db.PlayStatInfo
    for playstat_id in mapped_playstats:
        playstat_info_instance = mapped_playstats[playstat_id]
        playstat_info_instance.save()
    collection = db.PlayByPlayInfo
    for pbp_id in mapped_pbps:
        pbp_info_instance = mapped_pbps[pbp_id]
        pbp_info_instance.save()
    collection = db.LeagueInfo
    for league_id in mapped_leagues:
        league_info_instance = mapped_leagues[league_id]
        league_info_instance.save()
    collection = db.GameInfo
    for game_id in mapped_games:
        game_info_instance = mapped_games[game_id]
        game_info_instance.save()
    collection = db.BoxscoreInfo
    for gamebs_id in mapped_boxscores:
        boxscore_info_instance = mapped_boxscores[gamebs_id]
        boxscore_info_instance.save()
    print("Saved to database")
