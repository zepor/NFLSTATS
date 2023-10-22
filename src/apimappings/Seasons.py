import sys
sys.path.append('..')
import requests, pandas, json
from flask import Blueprint, jsonify, Flask
import os, time
from pymongo import MongoClient
from datetime import datetime
from uuid import UUID
from models.seasons import(SeasonInfo)
from mongoengine import connect, DoesNotExist, DecimalField, EmbeddedDocumentField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
from bson import ObjectId
import logging
bp = Blueprint('Seasons', __name__)
@bp.route('/Seasons', methods=['GET'])
def fetch_and_save_seasons():
    logging.basicConfig(filename='fetch_and_save_seasons.log', level=logging.INFO)
    logger = logging.getLogger('fetch_and_save_seasons')
    logger.info("fetch_and_save_seasons called")
    print("fetch_and_save_seasons called")
    url = os.getenv('SEASONS_API')
    print(datetime.now(), "Requesting URL:", url)
    response = requests.get(url)
    print("Response status code:", response.status_code)
    if response.status_code != 200:
        return f"Call Hierarchy Successfully"+ str(response.status_code)
    data = response.json()
    season_indo_dict = extract_season_info(data)
    mapped_seasons = map_seaoson_info(season_indo_dict)
    save_to_database(mapped_seasons)
    print("Seasons data fetched and saved successfully.")
    return "Seasons data fetched and saved successfully."

def extract_season_info(data):
    # List to hold the SeasonInfo objects
    seasons_info_dict = {}    
    # Extract each season's data and map it to the SeasonInfo model
    for season in data['seasons']:   # Iterating through list of seasons
        season_info = {
            'id': season['id'],
            'year': season['year'],
            'startdate': season['start_date'],
            'enddate': season['end_date'],
            'status': season['status'],
            'type': season['type']['code']
        }
        seasons_info_dict[season_info['id']] = season_info
    print(f"Number of Seasons extracted: {len(seasons_info_dict)}")
    return seasons_info_dict

def map_seaoson_info(season_info_dict):
    mapped_seasons = {}
    for season_id, season_data in season_info_dict.items():
        # Debug: Print the type and content of season_details
        print("Type of season details:", type(season_data))
        print("Content of season details:", season_data)
        season_embedded = SeasonInfo(
            id=season_data['id'],
            year=season_data['year'],
            startdate=season_data['startdate'],
            enddate=season_data['enddate'],
            status=season_data['status'],
            type=season_data['type']
        )
        mapped_seasons[season_id] = season_embedded

    # Debug: Print the number of mapped seasons and their content
    print(f"Number of mapped seasons: {len(mapped_seasons)}")
    print("Mapped_:", mapped_seasons)
    return mapped_seasons
    
def save_to_database(mapped_seasons):
    print("save_to_database called")

    def update_collection(model_cls, mapped_data, collection_name):
        updated_count = 0
        new_count = 0
        
        for mapped_entry_id, mapped_entry in mapped_data.items():
            if isinstance(mapped_entry, dict):
                new_entry_data = mapped_entry
            else:
                new_entry_data = mapped_entry.to_mongo().to_dict()
            new_entry = model_cls(id=mapped_entry_id, **new_entry_data)  
            existing_entry = model_cls.objects(_id=mapped_entry_id).first()
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
                if isinstance(mapped_entry, dict):
                    new_entry = model_cls(**mapped_entry)
                else:
                    mongo_representation = mapped_entry.to_mongo()
                    if '_id' in mongo_representation and model_cls == SeasonInfo:
                        mongo_representation['id'] = mongo_representation.pop('_id')
                    new_entry = model_cls(**new_entry_data)
                new_entry.save()
                print(f"Added new {collection_name} with id {new_entry.id}")  # Print after saving
                new_count += 1
        
        print(f"Updated {updated_count} {collection_name}s and added {new_count} new {collection_name}s.")
    
    # Call the update function for the season collection
    update_collection(SeasonInfo, mapped_seasons, "SeasonInfo")
