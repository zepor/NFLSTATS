import copy
import json
import random

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

import config
import questions as q

frontend_blueprint = Blueprint(name="frontend_blueprint", import_name=__name__)

# ======================|
# Generate Question API |
# ======================|
@frontend_blueprint.route("generate_question")
@cross_origin()
def generate_question():
    index = random.randint(0, len(q.questions) - 1)

    response = q.questions.get(list(q.questions)[index],
        lambda: 'Invalid question position.')(copy.deepcopy(config.league))
    
    return jsonify(response)

# ==============================|
# Generic Answer Validation API |
# ==============================|
@frontend_blueprint.route("validate_answer", methods=['POST'])
@cross_origin()
def validate_answer():
    if (request.content_type == 'application/json'):
        data = json.loads(json.dumps(request.json))
        response = []

        if "type" in data:
            validation = validate_data_by_type(data)

            return jsonify(validation)
    else:
        response = { 'Error': 'Content-Type not supported.' }
        return jsonify(response)

# ===============================================|
# Current Report Generation Config Retrieval API |
# ===============================================|
@frontend_blueprint.route("get_statistic_settings", methods=['GET'])
def get_statistic_settings():
    response = {
        'year': config.depth_year,
        'season_type': config.depth_nfl_season_type,
        'season_week': config.depth_nfl_season_week,
        'version_info': config.application_version
    }

    return jsonify(response)

# ====================================|
# Validate Response by Type (Handler) |
# ====================================|
def validate_data_by_type(data):
    question_type = None
    answers = { "answers": {} }

    if "type" in data:
        question_type = q.QuestionType.value_of(data["type"])
    else:
        raise ValueError('No valid question type provided.')

    if question_type is q.QuestionType.TEAM_CONFERENCE:
        for option in data['options']:
            is_correct = False

            for conference in config.league.conferences:
                if conference.name == option:
                    for division in conference.divisions:
                        for team in division.teams:
                            if team.name == data["team"]:
                                is_correct = True
                                break

            answers["answers"][option] = is_correct
    elif question_type is q.QuestionType.TEAM_DIVISION:
        for option in data['options']:
            is_correct = False

            for conference in config.league.conferences:
                for division in conference.divisions:
                    if division.name == option:
                        for team in division.teams:
                            if team.name == data["team"]:
                                is_correct = True
                                break

            answers["answers"][option] = is_correct
    elif question_type is q.QuestionType.PLAYER_TEAM:
        for option in data['options']:
            is_correct = False

            for conference in config.league.conferences:
                for division in conference.divisions:
                    for team in division.teams:
                        if team.name == option:
                            for player in team.players:
                                if player.name == data["player"]:
                                    is_correct = True
                                    break

            answers["answers"][option] = is_correct
    elif question_type is q.QuestionType.DIVISION_TEAM:
        for option in data['options']:
            is_correct = False

            for conference in config.league.conferences:
                for division in conference.divisions:
                    if division.name == data["division"]:
                        for team in division.teams:
                            if team.name == option:
                                is_correct = True
                                break

            answers["answers"][option] = is_correct
    elif question_type is q.QuestionType.PLAYER_POSITION:
        for option in data['options']:
            is_correct = False

            for conference in config.league.conferences:
                for division in conference.divisions:
                    for team in division.teams:
                        for player in team.players:
                            if player.name == option:
                                if player.position == data["position"]:
                                    is_correct = True
                                    break

            answers["answers"][option] = is_correct
    else:
        raise ValueError(f'{question_type} is not a valid question type.')

    return answers
