import sys
sys.path.append('..')
sys.path.append("os.getenv('LPATH')/src/")
import requests, pandas, json
from flask import Blueprint, jsonify, Flask
import os, time
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
from pymongo import MongoClient
from datetime import datetime
from uuid import UUID
from models.franchise_info import(FranchiseInfo) 
from models.venue_info import(venue1, location, VenueInfo)
from models.leaguehierarchy import(teams, division, conference, league,typeleague, LeagueHierarchy)
from models.team_info import(coach, rgb_color, team, team_color, TeamInfo)
from models.player_DCI_info import(player, prospect, primary, position, practice, injury, PlayerDCIinfo)
from mongoengine import DoesNotExist, DecimalField, EmbeddedDocumentField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
from bson import ObjectId
import logging
bp = Blueprint('TeamProfile', __name__)
@bp.route('/TeamProfile', methods=['GET'])
def fetch_and_save_team_profile():
    logging.basicConfig(filename='fetch_and_save.log', level=logging.INFO)
    logger = logging.getLogger('fetch_and_save_team_profile')
    logger.info("fetch_and_save_team_profile called")
    API_KEY = os.getenv('APIKEY')
    URL = "http://api.sportradar.us/nfl/official/trial/v7/en/teams/{TeamID}/profile.json?api_key={API_KEY}"
    team_ids =  [
        "ce92bd47-93d5-4fe9-ada4-0fc681e6caa0"	,
        "1f6dcffb-9823-43cd-9ff4-e7a8466749b5"	,
        "6680d28d-d4d2-49f6-aace-5292d3ec02c2"	,
        "7d4fcc64-9cb5-4d1b-8e75-8a906d1e1576"	,
        "768c92aa-75ff-4a43-bcc0-f2798c2e1724"	,
        "4809ecb0-abd3-451d-9c4a-92a90b83ca06"	,
        "5fee86ae-74ab-4bdd-8416-42a9dd9964f3"	,
        "97354895-8c77-4fd4-a860-32e62ea7382a"	,
        "82cf9565-6eb9-4f01-bdbd-5aa0d472fcd9"	,
        "f7ddd7fa-0bae-4f90-bc8e-669e4d6cf2de"	,
        "82d2d380-3834-4938-835f-aec541e5ece7"	,
        "d26a1ca5-722d-4274-8f97-c92e49c96315"	,
        "ad4ae08f-d808-42d5-a1e6-e9bc4e34d123"	,
        "d5a2eb42-8065-4174-ab79-0a6fa820e35e"	,
        "ebd87119-b331-4469-9ea6-d51fe3ce2f1c"	,
        "cb2f9f1f-ac67-424e-9e72-1475cb0ed398"	,
        "4254d319-1bc7-4f81-b4ab-b5e6f3402b69"	,
        "e6aa13a4-0055-48a9-bc41-be28dc106929"	,
        "f14bf5cc-9a82-4a38-bc15-d39f75ed5314"	,
        "0d855753-ea21-4953-89f9-0e20aff9eb73"	,
        "f0e724b0-4cbf-495a-be47-013907608da9"	,
        "de760528-1dc0-416a-a978-b510d20692ff"	,
        "2eff2a03-54d4-46ba-890e-2bc3925548f3"	,
        "3d08af9e-c767-4f88-a7dc-b920c6d2b4a8"	,
        "22052ff7-c065-42ee-bc8f-c4691c50e624"	,
        "e627eec7-bbae-4fa4-8e73-8e1d6bc5c060"	,
        "386bdbf9-9eea-4869-bb9a-274b0bc66e80"	,
        "04aa1c9d-66da-489d-b16a-1dee3f2eec4d"	,
        "7b112545-38e6-483c-a55c-96cf6ee49cb8"	,
        "c5a59daa-53a7-4de0-851f-fb12be893e9e"	,
        "a20471b4-a8d9-40c7-95ad-90cc30e46932"	,
        "33405046-04ee-4058-a950-d606f8c30852"	
        ]
    total_mapped_franchises = 0
    total_mapped_leaguehierarchy = 0
    total_mapped_players = 0
    total_mapped_teams = 0
    total_mapped_venues = 0
    
    try:
        for TeamID in team_ids:
            logger.info(f"{datetime.now()} Requesting URL: {URL.format(TeamID=TeamID)}")
            response = requests.get(URL.format(TeamID=TeamID))
            logger.info(f"Response status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"API request failed for TeamID {TeamID}. Status code: {response.status_code}")
                continue
            
            data = response.json()
            
            # Extract and map franchise info
            franchise_info = extract_franchise_info(data)
            mapped_franchises = map_franchise_info(franchise_info)
            total_mapped_franchises += 1
            
            # Extract and map league hierarchy
            league_hierarchy_dict = extract_league_hierarchy(data)
            mapped_leaguehierarchy = map_leaguehierarchy(league_hierarchy_dict)
            total_mapped_leaguehierarchy += len(mapped_leaguehierarchy['conferences'])
            
            # Extract and map player info
            player_info_dict = extract_player_info(data)
            mapped_players = map_player_info(player_info_dict)
            total_mapped_players += len(mapped_players)
            
            # Extract and map team info
            team_info_dict = extract_team_info(data)
            mapped_teams = map_team_info(team_info_dict)
            total_mapped_teams += 1
            
            # Extract and map venue info
            venue_info_dict = extract_venue_info(data)
            mapped_venues = map_venue_info(venue_info_dict)
            total_mapped_venues += 1
            
            # Save mapped data to the database
            save_to_database(mapped_leaguehierarchy, mapped_franchises, mapped_players, mapped_teams, mapped_venues)
            logger.info(f"Team Profile Data for TeamID {TeamID} fetched and saved successfully")
            
            # Add a delay between requests to avoid rate limiting
            time.sleep(2)
        
        logger.info(f"Total mapped franchises: {total_mapped_franchises}")
        logger.info(f"Total mapped league hierarchy items: {total_mapped_leaguehierarchy}")
        logger.info(f"Total mapped players: {total_mapped_players}")
        logger.info(f"Total mapped teams: {total_mapped_teams}")
        logger.info(f"Total mapped venues: {total_mapped_venues}")
        return "Team Profile Data Fetched and Saved Successfully"
    except Exception as e:
        logger.exception("An error occurred:")
        return f"Error: {str(e)}", 500
def extract_franchise_info(data):
    franchise_info = {
        'id': data['id'],
        'falias': data['franchise']['alias'],
        'fid': data['franchise']['id'],
        'fname': data['franchise']['name'],
    }
    return franchise_info
def map_franchise_info(franchise_info):
    franchise_id = franchise_info['fid']
    mapped_franchise = FranchiseInfo(
        teamid=franchise_info['id'],
        alias=franchise_info['falias'],
        id=franchise_id,
        name=franchise_info['fname']
    )
    return {franchise_id: mapped_franchise}
def extract_league_hierarchy(data):
    # Extract conference and division data from raw data
    conference_data = data['conference']
    division_data = data['division']
    
    # Extract specific data points
    extracted_conference = {
        'calias': conference_data['alias'],
        'cid': conference_data['id'],
        'cname': conference_data['name'],
        'divisions': [
            {
                'dalias': division_data['alias'],
                'did': division_data['id'],
                'dname': division_data['name']
            }
        ]
    }
    
    league_hierarchy_dict = {
        'conferences': [extracted_conference]
    }
    
    #logging.info("League Hierarchy Dict:", league_hierarchy_dict)
    return league_hierarchy_dict
def map_leaguehierarchy(league_hierarchy_dict):
    # Manually set the static ID for the mapped_leaguehierarchy
    static_id = "3c6d318a-6164-4290-9bbc-bf9bb21cc4b8"
    # Create a league embedded document instance
    mapped_league = {
        'id': static_id,
        'alias': "NFL",
        'name': "National Football League",
        'conferences': []
    }
    mapped_leaguehierarchy = {
        'id': static_id,
        'league_id': static_id,  # Set league_id to the same value as id
        'conferences': {}
    } 
    for conference_dict in league_hierarchy_dict.get('conferences', []):
        cid = conference_dict.get('cid')
        calias = conference_dict.get('calias')
        cname = conference_dict.get('cname')
        for division_dict in conference_dict.get('divisions', []):
            did = division_dict.get('did')
            dalias = division_dict.get('dalias')
            dname = division_dict.get('dname')
            division_key = (cid, did)
            mapped_division = {
                'did': did,
                'dalias': dalias,
                'dname': dname,
            }
            if division_key not in mapped_leaguehierarchy['conferences']:
                mapped_leaguehierarchy['conferences'][division_key] = {
                    'cid': cid,
                    'calias': calias,
                    'cname': cname,
                    'divisions': [mapped_division],
                }
            else:
                mapped_leaguehierarchy['conferences'][division_key]['divisions'].append(mapped_division)
    # Assign the league embedded document instance to the league attribute
    mapped_leaguehierarchy['league'] = mapped_league
    logging.info("Mapped League Hierarchy:", mapped_leaguehierarchy)
    return mapped_leaguehierarchy
def extract_player_info(data):
    players_info = data.get("players", [])
    extracted_players = {}
    for player_info in players_info:
        logging.info(f"Raw player data: {player_info}")
        player_id = player_info.get('id')
        logging.info(f"Extracted player ID: {player_id}")
        extracted_player = {
            "abbrname": player_info.get("abbr_name"),
            "birthdate": player_info.get("birth_date"),
            "birthplace": player_info.get("birth_place"),
            "college": player_info.get("college"),
            "collegeconf": player_info.get("college_conf"),
            "draftinfonumber": player_info.get("draft", {}).get("number"),
            "draftinfo_round": player_info.get("draft", {}).get("round"),
            "draftinfo_year": player_info.get("draft", {}).get("year"),
            "draftteamalias": player_info.get("draft", {}).get("team", {}).get("alias"),
            "draftteamid": player_info.get("draft", {}).get("team", {}).get("id"),
            "draftteammarket": player_info.get("draft", {}).get("team", {}).get("market"),
            "draftteamname": player_info.get("draft", {}).get("team", {}).get("name"),
            "draftteamsrid": player_info.get("draft", {}).get("team", {}).get("sr_id"),
            "experience": player_info.get("experience"),
            "firstname": player_info.get("first_name"),
            "fullname": f"{player_info.get('first_name')} {player_info.get('last_name')}",  # Constructed fullname
            "height": player_info.get("height"),
            "highschool": player_info.get("high_school"),
            "id": player_info.get("id"),
            "jerseynumber": player_info.get("jersey"),
            "lastname": player_info.get("last_name"),
            "namesuffix": player_info.get("name_suffix"),
            "position": player_info.get("position"),
            "preferredname": player_info.get("name"),
            "srid": player_info.get("sr_id"),
            "status": player_info.get("status"),
            "weight": player_info.get("weight"),
        }   
        extracted_players[player_id] = extracted_player
    logging.info(f"Number of players extracted: {len(extracted_players)}")
    return extracted_players
def map_player_info(extracted_players):
    mapped_players = {}
    for player_id, player_details in extracted_players.items():
        try:
            playerembedded = player(
                abbrname=player_details.get('abbrname', ''),
                age=player_details.get('age', None),
                birthdate=player_details.get('birthdate', ''),
                birthplace=player_details.get('birthplace', ''),
                id=player_details.get('id', ''),
                college=player_details.get('college', ''),
                collegeconf=player_details.get('collegeconf', ''),
                depth=player_details.get('depth', None),
                experience=player_details.get('experience', 0),
                firstname=player_details.get('firstname', ''),
                fullname=player_details.get('fullname', ''),
                height=player_details.get('height', 0),
                highschool=player_details.get('highschool', ''),
                srid=player_details.get('srid', ''),
                ingamestatus=player_details.get('ingamestatus', None),
                jersey=player_details.get('jersey', ''),
                lastmodified=player_details.get('lastmodified', None),
                lastname=player_details.get('lastname', ''),
                status=player_details.get('status', ''),
                namesuffix=player_details.get('namesuffix', None),
                position=player_details.get('position', ''),
                preferredname=player_details.get('preferredname', ''),
                role=player_details.get('role', None),
                sourceid=player_details.get('sourceid', None),
                weight=player_details.get('weight', 0),
                draftyear=player_details.get('draftyear', None),
                draftround=player_details.get('draftround', None),
                draftnumber=player_details.get('draftnumber', None),
                draftteamid=player_details.get('draftteamid', None),
                draftteamname=player_details.get('draftteamname', None),
                draftteamalias=player_details.get('draftteamalias', None),
                draftteamsrid=player_details.get('draftteamsrid', None),
                draftteammarket=player_details.get('draftteammarket', None)
            )
            player_info_instance = PlayerDCIinfo(
                playerinfo=playerembedded,
                prospectinfo=None,
                primaryposition=None,
                positioninfo=None,
                practiceinfo=None,
                injuryinfo=None
            )
            mapped_players[player_id] = player_info_instance
        except Exception as e:
            logging.info(f"Error mapping player ID {player_id}. Error: {e}")

    logging.info(f"Number of mapped players: {len(mapped_players)}")
    logging.info("mapped_players:", mapped_players)
    return mapped_players
def extract_team_info(data):
    team_colors = data.get('team_colors', []) 
    team_info = {
        'alias': data['alias'],
        'coaches': [],
        'id': data['id'],
        'market': data['market'],
        'name': data['name'],
        'sr_id': data['sr_id'],
        'team_colors': [],  # Placeholder for colors information
        'conference_id': data['conference']['id'],  # Extract conference id
        'division_id': data['division']['id']       # Extract division id
    }
    # Extract coach information
    for coach in data['coaches']:
        coach_info = {
            'coach_first_name': coach['first_name'],
            'coach_full_name': coach['full_name'],
            'coach_id': coach['id'],
            'coach_last_name': coach['last_name'],
            'coach_name_suffix': coach.get('name_suffix', ''),
            'coach_position': coach['position']
        }
        team_info['coaches'].append(coach_info)
    # Extract team color information if available
    for color in team_colors:
        color_info = {
            'color_type': color.get('type', ''),
            'color_hex': color.get('hex_color', ''),
            'color_alpha': color.get('alpha', ''),
            'color_rgb_blue': color.get('rgb_color', {}).get('blue', ''),
            'color_rgb_green': color.get('rgb_color', {}).get('green', ''),
            'color_rgb_red': color.get('rgb_color', {}).get('red', ''),
        }
        team_info['team_colors'].append(color_info)
    return team_info
def map_team_info(team_info):
    team_id = team_info['id']
    # Mapping coaches
    mapped_coaches = [coach(
        first_name=coach_data['coach_first_name'],
        full_name=coach_data['coach_full_name'],
        id=coach_data['coach_id'],
        last_name=coach_data['coach_last_name'],
        name_suffix=coach_data['coach_name_suffix'],
        position=coach_data['coach_position']
    ) for coach_data in team_info['coaches']]
    # Mapping RGB colors
    mapped_rgb_colors = [rgb_color(
        blue=color_data['color_rgb_blue'],
        green=color_data['color_rgb_green'],
        red=color_data['color_rgb_red']
    ) for color_data in team_info['team_colors']]
    # Mapping team colors
    mapped_team_colors = [team_color(
        alpha=color_data['color_alpha'],
        hex_color=color_data['color_hex'],
        type=color_data['color_type']
    ) for color_data in team_info['team_colors']]
    # Mapping team
    mapped_team = team(
        alias=team_info['alias'],
        id=team_id,
        market=team_info['market'],
        name=team_info['name'],
        sr_id=team_info['sr_id']
    )
    team_dict = {
        team_id: {
            "team": mapped_team,
            "coachs": mapped_coaches,
            "rgb_colors": mapped_rgb_colors,
            "team_colors": mapped_team_colors,
            "conference_id": team_info.get('conference_id', None),
            "division_id": team_info.get('division_id', None),
        }
    }
    return team_dict
def extract_venue_info(data):
    venue_data = data.get('venue', {})
    # Debug: Print the type and content of venue_data to check its structure
    logging.info("Type of venue data:", type(venue_data))
    logging.info("Content of venue data:", venue_data)
    venue_info = {
        'id': venue_data.get('id'),
        'name': venue_data.get('name'),
        'city': venue_data.get('city'),
        'state': venue_data.get('state'),
        'country': venue_data.get('country'),
        'zip': venue_data.get('zip'),
        'address': venue_data.get('address'),
        'capacity': venue_data.get('capacity'),
        'surface': venue_data.get('surface'),
        'roof_type': venue_data.get('roof_type'),
        'sr_id': venue_data.get('sr_id'),
        'location': venue_data.get('location', {}),
    }
    # Debug: Print the type and content of venue_info
    logging.info("Type of venue info:", type(venue_info))
    logging.info("Content of venue info:", venue_info)
    return venue_info
def map_venue_info(venue_info_dict):
    mapped_venues = {}
    # No need to loop; just extract the details from venue_info_dict directly
    venue_details = venue_info_dict
    # Debug: Print the type and content of venue_details
    logging.info("Type of venue details:", type(venue_details))
    logging.info("Content of venue details:", venue_details)
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
        lat=venue_details['location']['lat'],
        lng=venue_details['location']['lng']
    )
    venue_info_instance = VenueInfo(
        venue1=venue_embedded,
        location=location_embedded
    )
    mapped_venues[venue_details['id']] = venue_info_instance  
    # Debug: Print the number of mapped venues and their content
    logging.info(f"Number of mapped venues: {len(mapped_venues)}")
    logging.info("Mapped_Venues:", mapped_venues)
    return mapped_venues
def map_league_hierarchy(league_hierarchy_dict):
    # Create an empty LeagueHierarchy instance
    mapped_league_hierarchy = LeagueHierarchy()
    # Create a list to store mapped conferences
    mapped_conferences_list = []
    for conference_dict in league_hierarchy_dict.get('conferences', []):
        # Extract conference details
        cid = conference_dict.get('cid')
        calias = conference_dict.get('calias')
        cname = conference_dict.get('cname')
        # Create a list to store mapped divisions for this conference
        mapped_divisions_list = []
        for division_dict in conference_dict.get('divisions', []):
            # Extract division details
            did = division_dict.get('did')
            dalias = division_dict.get('dalias')
            dname = division_dict.get('dname')
            # Create division instance
            mapped_division = division(did=did, dalias=dalias, dname=dname)
            # Append to the divisions list
            mapped_divisions_list.append(mapped_division)
        # Create conference instance with the divisions list
        mapped_conference = conference(cid=cid, calias=calias, cname=cname, divisions=mapped_divisions_list)
        # Append to the conferences list
        mapped_conferences_list.append(mapped_conference)
    # Assign the mapped conferences list to the LeagueHierarchy instance
    mapped_league_hierarchy.conferences = mapped_conferences_list
    return mapped_league_hierarchy
def save_to_database(mapped_leaguehierarchy, mapped_franchises, mapped_players, mapped_teams, mapped_venues):
    logging.info("save_to_database called")
    
    def update_collection(model_cls, mapped_data, collection_name):
        updated_count = 0
        new_count = 0
        if isinstance(mapped_data, dict):
            mapped_data_iterable = mapped_data.items()
        else:
            mapped_data_iterable = ((getattr(entry, 'id', None), entry) for entry in mapped_data) 
        for mapped_entry_id, mapped_entry in mapped_data_iterable:
            if isinstance(mapped_entry, dict) and 'team' in mapped_entry:
                mapped_entry = mapped_entry['team']
            if isinstance(mapped_entry, tuple):
                _, mapped_entry = mapped_entry
            existing_entry = model_cls.objects(id=mapped_entry_id).first()
            logging.info(f"Checking {collection_name} with ID: {mapped_entry_id}")  # Print the ID being checked
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
                    logging.info(f"Updated {collection_name} {mapped_entry_id}: Updated fields: {', '.join(updated_fields)}")
                else:
                    logging.info(f"No updates needed for {collection_name} {mapped_entry_id}")
            else:
                logging.info(f"Type of mapped_entry: {type(mapped_entry)}, Content: {mapped_entry}")
                if model_cls == PlayerDCIinfo:
                    logging.info(f"Player ID from mapped data: {mapped_entry.id}")
                    mapped_entry = mapped_entry.to_mongo().to_dict()
                if isinstance(mapped_entry, dict):
                    new_entry = model_cls(**mapped_entry)
                    mongo_representation = new_entry.to_mongo()
                else:
                    mongo_representation = mapped_entry.to_mongo()
                if '_id' in mongo_representation and model_cls == FranchiseInfo:
                    mongo_representation['id'] = mongo_representation.pop('_id')
                new_entry = model_cls(**mongo_representation)
                new_entry.save()
                logging.info(f"Added new {collection_name} with id {new_entry.id}")  # Print after saving
                new_count += 1
        logging.info(f"Updated {updated_count} {collection_name}s and added {new_count} new {collection_name}s.")
    
    update_collection(FranchiseInfo, mapped_franchises.values(), "franchise")
    update_collection(PlayerDCIinfo, mapped_players.values(), "player")
    update_collection(TeamInfo, mapped_teams.items(), "teams")
    update_collection(VenueInfo, mapped_venues.items(), "venue")
    
    # Handling the LeagueHierarchy separately, as there's only one document.
    existing_league_hierarchy = LeagueHierarchy.objects.first()
    if existing_league_hierarchy:
        # Update the existing document
        updated_fields = []
        fields_to_skip = ['id', 'league_id']
        for field_name in existing_league_hierarchy._fields.keys():
            if field_name not in fields_to_skip:
                existing_value = getattr(existing_league_hierarchy, field_name)
                mapped_value = mapped_leaguehierarchy.get(field_name)
                if existing_value != mapped_value:
                    setattr(existing_league_hierarchy, field_name, mapped_value)
                    updated_fields.append(field_name)
        # Save the updated LeagueHierarchy document
        existing_league_hierarchy.save()
        if updated_fields:
            logging.info(f"Updated the LeagueHierarchy: Updated fields: {', '.join(updated_fields)}")
        else:
            logging.info(f"No updates needed for LeagueHierarchy")

