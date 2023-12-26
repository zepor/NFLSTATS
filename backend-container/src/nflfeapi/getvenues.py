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
bp_venues = Blueprint('venues', __name__)
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger
@log_and_catch_exceptions
@bp_venues.route('/venues')
def venues():
    be_logger.debug("Accessing /venues")
    # Fetch all venues from the database
    venue_infos = VenueInfo.objects.all()
    # Extract the venue1 dictionaries from each document and add lat and lng
    venues = []
    for venue_info in venue_infos:
        # Use the instance 'venue_info.venue1', not the class definition
        venue = venue_info.venue1.to_mongo().to_dict()
        # Use the instance 'venue_info.location', not the class definition
        location_dict = venue_info.location.to_mongo().to_dict()
        if location_dict.get('lat') and location_dict.get('lng'):
            venue.update(location_dict)
            venues.append(venue)
    return render_template('venues.html', venues=venues)
