import copy
import random

from enum import Enum, auto

import config

class QuestionType(Enum):
	TEAM_CONFERENCE = auto()
	TEAM_DIVISION = auto()
	PLAYER_TEAM = auto()
	DIVISION_TEAM = auto()
	PLAYER_POSITION = auto()

	@classmethod
	def value_of(cls, val):
		for k, v in cls.__members__.items():
			if k == val:
				return v
		raise ValueError(f'{cls.__name__} enum not found for {val}.')

# ============================================|
# Question-related dictionary initialization: |
# ============================================|
questions = {}

# Configure '@question' decorator tag:
question = lambda q: questions.setdefault(q.__name__, q)

# =============================================|
# Question definitions based on configuration: |
# =============================================|
# TODO: Set max question options to provide    |
# (using range(?)) dynamically via config.     |
# =============================================|
@question
def get_team_conference_question(league):
	conferences = []
	conference_names = []

	for conference in league.conferences:
		conferences.append(conference)
		conference_names.append(conference.name)

	chosen_conference = random.sample(conferences, 1)[0]
	chosen_division = random.sample(chosen_conference.divisions, 1)[0]
	chosen_team = random.sample(chosen_division.teams, 1)[0]

	response = {
		'question': f'{config.team_conference_question}'.replace(
			"{team}", f'{chosen_team.market} {chosen_team.name}'),
		'type': QuestionType.TEAM_CONFERENCE.name,
		'market': chosen_team.market,
		'team': chosen_team.name,
		'options': conference_names
	}

	return response

@question
def get_team_division_question(league):
	chosen_conferences = []
	chosen_divisions = []
	chosen_division_names = []

	for i in range(4):
		chosen_conferences.append(random.choice(league.conferences))

	for conference in chosen_conferences:
		division = random.choice(conference.divisions)
		chosen_divisions.append(division)
		conference.divisions.remove(division)

	for division in chosen_divisions:
		chosen_division_names.append(division.name)

	chosen_division = random.choice(chosen_divisions)
	chosen_team = random.choice(chosen_division.teams)

	response = {
		'question': f'{config.team_division_question}'.replace(
			"{team}", f'{chosen_team.market} {chosen_team.name}'),
		'type': QuestionType.TEAM_DIVISION.name,
		'market': chosen_team.market,
		'team': chosen_team.name,
		'options': chosen_division_names
	}

	return response

@question
def get_player_team_question(league):
	chosen_conferences = []
	chosen_divisions = []
	chosen_teams = []
	chosen_team_names = []
	choen_players = []

	for i in range(4):
		chosen_conferences.append(random.choice(league.conferences))

	for conference in chosen_conferences:
		division = random.choice(conference.divisions)
		chosen_divisions.append(division)
		conference.divisions.remove(division)

	for division in chosen_divisions:
		team = random.choice(division.teams)
		chosen_teams.append(team)
		division.teams.remove(team)

	for team in chosen_teams:
		chosen_team_names.append(team.name)

	chosen_team = random.choice(chosen_teams)

	while True:
		chosen_player = random.choice(chosen_team.players)

		if chosen_player.position in config.allowed_positions:
			break

	response = {
		'question': f'{config.player_team_question}'.replace(
			"{player}", f'{chosen_player.name}'),
		'type': QuestionType.PLAYER_TEAM.name,
		'player': chosen_player.name,
		'options': chosen_team_names
	}

	return response

@question
def get_division_team_question(league):
	chosen_conferences = []
	chosen_divisions = []
	chosen_teams = []
	chosen_team_names = []

	for i in range(4):
		chosen_conferences.append(random.choice(league.conferences))

	for conference in chosen_conferences:
		division = random.choice(conference.divisions)
		chosen_divisions.append(division)
		conference.divisions.remove(division)

	for division in chosen_divisions:
		team = random.choice(division.teams)
		chosen_teams.append(team)
		division.teams.remove(team)

	for team in chosen_teams:
		chosen_team_names.append(team.name)

	chosen_division = random.choice(chosen_divisions)

	response = {
		'question': f'{config.division_team_question}'.replace(
			"{division}", f'{chosen_division.name}'),
		'type': QuestionType.DIVISION_TEAM.name,
		'division': chosen_division.name,
		'options': chosen_team_names
	}

	return response

@question
def get_player_position_question(league):
	chosen_conferences = []
	chosen_divisions = []
	chosen_teams = []
	chosen_players = []
	chosen_player_names = []

	for i in range(4):
		chosen_conferences.append(random.choice(league.conferences))

	for conference in chosen_conferences:
		division = random.choice(conference.divisions)
		chosen_divisions.append(division)
		conference.divisions.remove(division)

	for division in chosen_divisions:
		team = random.choice(division.teams)
		chosen_teams.append(team)
		division.teams.remove(team)

	# Pick initial player & position:
	while True:
		chosen_player = random.choice(chosen_teams[0].players)

		if chosen_player.position in config.allowed_positions:
			chosen_players.append(chosen_player)
			chosen_position = chosen_player.position
			chosen_teams.remove(chosen_teams[0])
			break

	for team in chosen_teams:
		while True:
			player = random.choice(team.players)

			if not player.position == chosen_position:
				if player.position in config.allowed_positions:
					chosen_players.append(player)
					break

	for player in chosen_players:
		chosen_player_names.append(player.name)

	response = {
		'question': f'{config.player_position_question}'.replace(
			"{position}", f'{chosen_position}'),
		'type': QuestionType.PLAYER_POSITION.name,
		'position': chosen_position,
		'options': chosen_player_names
	}

	return response
