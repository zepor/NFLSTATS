import sys
sys.path.append('..')
import requests, pandas, json
from flask import Blueprint, jsonify, Flask
import os, time
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
from datetime import datetime
from uuid import UUID
from models.franchise_info import(FranchiseInfo) 
from models.venue_info import(venue1, location, VenueInfo)
from models.leaguehierarchy import( teams, division, conference, league,typeleague, LeagueHierarchy)
from models.team_info import(coach, rgb_color, team_color, team, TeamInfo)
from models.changelog import ChangelogEntry  # Import the ChangelogEntry model
from mongoengine import DoesNotExist, DecimalField, EmbeddedDocumentField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
from bson import ObjectId
bp = Blueprint('LeagueHierarchy', __name__)
@bp.route('/LeagueHierarchy', methods=['GET'])
def fetchandsaveLeagueHierarchy():
    #print("LeagueHierarchy")
    url = os.getenv('LEAGUE_HIERARCHY_API_URL')
    print(datetime.now(), "Requesting URL:", url)
    response = requests.get(url)
    print("Response status code:", response.status_code)
    if response.status_code != 200:
        return f"Call Seasons Successfully{response.status_code}"
    data = response.json()
    venue_info_dict = extract_venue_info(data)
    league_hierarchy_dict = extract_league_hierarchy(data)
    franchise_info_dict = extract_franchise_info(data)
    team_info_dict = extract_team_info(data)
    mapped_venues = map_venue_info(venue_info_dict)
    mapped_leaguehierarchy = map_league_hierarchy(league_hierarchy_dict)
    mapped_franchises = map_franchise_info(franchise_info_dict)
    mapped_teams = map_team_info(team_info_dict)
    save_to_database(mapped_venues, mapped_leaguehierarchy, mapped_franchises, mapped_teams)
    print("League Hierarchy data fetched and saved successfully.")
    return "League Hierarchy data fetched and saved successfully."
def extract_venue_info(data):
    venue_info_dict = {}
    for conference_data in data['conferences']:
        for division_data in conference_data['divisions']:
            for team_data in division_data['teams']:
                venue_info = {
                    'id': team_data['venue']['id'],
                    'name': team_data['venue']['name'],
                    'city': team_data['venue']['city'],
                    'state': team_data['venue'].get('state'),
                }
                venue_info['country'] = team_data['venue'].get('country')
                venue_info['zip'] = team_data['venue'].get('zip')
                venue_info['address'] = team_data['venue']['address']
                venue_info['capacity'] = team_data['venue']['capacity']
                venue_info['surface'] = team_data['venue']['surface']
                venue_info['roof_type'] = team_data['venue']['roof_type']
                venue_info['sr_id'] = team_data['venue']['sr_id']
                venue_info['lat'] = team_data.get('venue', {}).get('location', {}).get('lat', None)
                venue_info['lng'] = team_data.get('venue', {}).get('location', {}).get('lng', None)
                venue_info_dict[team_data['venue']['id']] = venue_info
                            #print("venue_info_dict:", venue_info_dict)
    return venue_info_dict
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
    #print(len(mapped_venues))   
    #print("Mapped_Venues", mapped_venues)
    return mapped_venues
def extract_franchise_info(data):
    franchise_info_dict = {}
    for conference_data in data['conferences']:
        for division_data in conference_data['divisions']:
            for team_data in division_data['teams']:
                franchise_data = team_data['franchise']
                franchise_info = {
                    'teamid': team_data['id'],  # Corrected field name
                    'alias': franchise_data['alias'],
                    'id': franchise_data['id'],
                    'name': franchise_data['name']
                }
                franchise_info_dict[franchise_info['id']] = franchise_info
    return franchise_info_dict
def map_franchise_info(franchise_info_dict):
    mapped_franchises = {}
    for franchise_id, franchise_data in franchise_info_dict.items():
        franchise_embedded = FranchiseInfo(
            teamid=franchise_data['teamid'],
            id=franchise_data['id'],
            alias=franchise_data['alias'],
            name=franchise_data['name']
        )
        mapped_franchises[franchise_id] = franchise_embedded
    return mapped_franchises
def extract_team_info(data):
    team_info_dict = {}
    for conference_data in data['conferences']:
        for division_data in conference_data['divisions']:
            for team_data in division_data['teams']:
                team_info = {
                    'alias': team_data['alias'],
                    'id': team_data['id'],
                    'market': team_data['market'],
                    'name': team_data['name'],
                    'sr_id': team_data['sr_id'],
                    'conference_id': conference_data['id'],  # Add conference_id
                    'division_id': division_data['id']  # Add division_id
                }
                team_colors_data = team_data.get('team_colors', [])
                team_colors = []
                for color_data in team_colors_data:
                    color_info = {
                        'type': color_data['type'],
                        'alpha': color_data['alpha'],
                        'hex_color': color_data['hex_color'],
                        'rgb_color': {
                            'red': color_data['rgb_color']['red'],
                            'green': color_data['rgb_color']['green'],
                            'blue': color_data['rgb_color']['blue']
                        }
                    }
                    team_colors.append(color_info)
                team_info['team_colors'] = team_colors
                team_info_dict[team_info['id']] = team_info
    return team_info_dict
def map_team_info(team_info_dict):
    mapped_teams = {}
    for team_id, team_data in team_info_dict.items():
        mapped_team = team(
            alias=team_data['alias'],
            id=team_data['id'],
            market=team_data['market'],
            name=team_data['name'],
            sr_id=team_data['sr_id']
        )
        mapped_team_colors = []
        for color_data in team_data['team_colors']:
            team_color_embedded = team_color(
                alpha=color_data['alpha'],
                hex_color=color_data['hex_color'],
                type=color_data['type']
            )
            mapped_team_colors.append(team_color_embedded)

        mapped_teams[team_id] = TeamInfo(
            team=mapped_team,  # Removed the list wrapping here
            coachs=None,
            rgb_colors=None,
            team_colors=mapped_team_colors,
            conference_id=team_data['conference_id'],
            division_id=team_data['division_id']
)

    return mapped_teams
def extract_league_hierarchy(data):
    league_hierarchy_dict = {
        'league': {
            'id': data['league']['id'],
            'name': data['league']['name'],
            'alias': data['league']['alias']
        },
        'conferences': []
    }
    #print("league_hierarchy_dict:", league_hierarchy_dict)
    for conference_data in data['conferences']:
        conference_info = {
            'id': conference_data['id'],
            'alias': conference_data['alias'],
            'name': conference_data['name'],
            'divisions': []
        }
        for division_data in conference_data['divisions']:
            division_info = {
                'id': division_data['id'],
                'alias': division_data['alias'],
                'name': division_data['name'],
                'teams': []
            }
            for team_data in division_data['teams']:
                team_info = {
                    'id': team_data['id'],
                    'name': team_data['name'],
                    'market': team_data['market'],
                    'alias': team_data['alias'],
                    'sr_id': team_data['sr_id'],

                }                   # Add other team-related information here
                division_info['teams'].append(team_info)
            conference_info['divisions'].append(division_info)
        league_hierarchy_dict['conferences'].append(conference_info)
    #print("Extracted League Hierarchy Data:")
    print("league_hierarchy_dict", league_hierarchy_dict)  # Print the extracted data
    return league_hierarchy_dict
def map_league_hierarchy(league_hierarchy_dict):
    print("Type of league_hierarchy_dict:", type(league_hierarchy_dict))
    print("Content of league_hierarchy_dict:", league_hierarchy_dict)

    league_id = league_hierarchy_dict['league']['id']
    current_mapped_league = league(
        id=league_id,
        alias=league_hierarchy_dict['league']['alias'],
        name=league_hierarchy_dict['league']['name'],
        conferences=[]
    )

    for conference_data in league_hierarchy_dict['conferences']:
        mapped_conference = conference(
            cid=conference_data['id'],
            calias=conference_data['alias'],
            cname=conference_data['name'],
            divisions=[]
        )

        mapped_divisions = []  # Initialize a list to hold division objects

        for division_data in conference_data['divisions']:
            mapped_teams = []  # Initialize a list to hold team objects

            for team_data in division_data['teams']:
                mapped_team = teams(
                    teamid=team_data['id'],
                    teamname=team_data['name']
                )
                mapped_teams.append(mapped_team)

            mapped_division = division(
                did=division_data['id'],
                dalias=division_data['alias'],
                dname=division_data['name'],
                teams=mapped_teams
            )

            mapped_divisions.append(mapped_division)

        mapped_conference.divisions = mapped_divisions
        current_mapped_league.conferences.append(mapped_conference)

    return {
        league_id: LeagueHierarchy(
            league=current_mapped_league, typeleague=None
        )
    }
def save_to_database(mapped_venues, mapped_leaguehierarchy, mapped_franchises, mapped_teams):
    print("save_to_database called")
    
    def update_collection(model_cls, mapped_data, collection_name):
        updated_count = 0
        new_count = 0
        for mapped_entry_info in mapped_data:
            mapped_entry = mapped_entry_info
            
            # Update ID before converting to mongo representation
            if isinstance(mapped_entry, VenueInfo):
                mapped_entry.id = mapped_entry.venue1.id
            
            mapped_entry_id = mapped_entry.id  # Extract the ID from the mapped entry
            existing_entry = model_cls.objects(id=mapped_entry_id).first()
            
            print(f"Checking {collection_name} with ID: {mapped_entry_id}")  # Print the ID being checked
            
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
                    print(f"Updated {collection_name} {mapped_entry_id}: Updated fields: {', '.join(updated_fields)}")
                else:
                    print(f"No updates needed for {collection_name} {mapped_entry_id}")
            else:
                mongo_representation = mapped_entry.to_mongo()
                if '_id' in mongo_representation and model_cls == FranchiseInfo:
                    mongo_representation['id'] = mongo_representation.pop('_id')
                new_entry = model_cls(**mongo_representation)
                new_entry.save()
                print(f"Added new {collection_name} with id {new_entry.id}")  # Print after saving
                new_count += 1
            
        print(f"Updated {updated_count} {collection_name}s and added {new_count} new {collection_name}s.")

    update_collection(VenueInfo, mapped_venues.values(), "venue")
    update_collection(LeagueHierarchy, mapped_leaguehierarchy.values(), "season")
    update_collection(FranchiseInfo, mapped_franchises.values(), "franchise")
    update_collection(TeamInfo, mapped_teams.values(), "teams")
