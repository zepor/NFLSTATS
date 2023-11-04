# ==========|
# config.py |
# ===============================|
# Global configuration settings: |
# ===============================|
api_key = 'tz4rfve8mpvzsxsjunjmm8su'
application_version = "1.0.2"

base_uri = 'https://api.sportradar.us/nfl/official/trial/v7/en'
league_endpoint = '/league/hierarchy.json?api_key={api_key}'
team_roster_endpoint = '/teams/{id}/profile.json?api_key={api_key}'
depth_chart_endpoint = '/seasons/{year}/{nfl_season_type}/{nfl_season_week}/depth_charts.json?api_key={api_key}'

depth_year = "2022"
depth_nfl_season_type = "REG" # PRE, REG, or PST (post)
depth_nfl_season_week = "18"

# TODO: Condense this into a proper class instead of
# aligned arrays?
allowed_positions = [ 'WR', 'RB', 'TE', 'QB', 'K' ]
max_depth_by_position = [ 2, 2, 1, 1, 1 ]

# =====================|
# Question templating: |
# =====================|
team_conference_question = 'What conference are the {team} in?'
team_division_question = 'What division are the {team} in?'
player_team_question = 'What team does {player} belong to?'
division_team_question = 'Which team is in the {division}?' # AFC North, etc.
player_position_question = 'Which of the following is a {position}?' # WR, TE, etc.

# ===================================|
# Global league data storage object: |
# ===================================|
league = None