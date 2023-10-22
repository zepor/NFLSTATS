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
from src.models.season_stat_player_info import(SeasonStatPlayer, int_returns, player,
 passing, receiving, defense, field_goals, punts, rushing, extra_points, 
 kick_returns, punt_returns, conversions, kickoffs, fumbles, penalties, statistics)  
from src.models.venue_info import(venue1, location, VenueInfo)
from src.models.league_info import(league, team, conference, division, typeleague, season, changelog, leagueweek, LeagueInfo)
from src.models.game_info import(gamegame, awayteam, hometeam, broadcast, weather, wind, GameInfo)
from mongoengine import DecimalField, EmbeddedDocumentField, Document, StringField, UUIDField, IntField, BooleanField, DateTimeField, EmbeddedDocument, EmbeddedDocumentListField
from bson import ObjectId
bp = Blueprint('Player_Profile', __name__)
@bp.route('/PlayerProfile', methods=['GET'])
def fetch_and_save_all_seasons_schedule():
    print("PlayerProfile")
    url = os.getenv('PLAYER_PROFILE_API_URL')
    API_KEY = os.getenv('APIKEY')
    URL = "http://api.sportradar.us/nfl/official/trial/v7/en/teams/{TeamID}/profile.json?api_key={API_KEY}"
    team_ids = []