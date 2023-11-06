from typing import Optional

# =========================================|
# Custom object definitions for parsing    |
# raw data directly from SportsRadar APIs. |
# =========================================|
# General team & player parsing |
# definitions:                  |
# ==============================|
class Player:
	id: str
	name: str
	position: str
	depth: Optional[int]

class Color:
	type: str
	hex_color: str

class Team:
	id: str
	name: str
	market: str
	alias: str
	team_colors: Optional[list[Color]] # 3.9!
	players: Optional[list[Player]] # 3.9!

class Division:
	id: str
	name: str
	teams: list[Team]

class Conference:
	id: str
	name: str
	divisions: list[Division]

class League:
	id: str
	name: str
	alias: str

class Response:
	league: League
	conferences: list[Conference]

# ==================================|
# Depth-chart-specific definitions: |
# ==================================|
class Week:
	id: str
	sequence: int
	title: str

class Season:
	id: str
	year: int
	type: str
	name: str

class PositionCategory:
	name: str
	players: list[Player]

class DepthCategory:
	position: PositionCategory

class TeamChart:
	id: str
	name: str
	market: str
	alias: str
	offense: list[DepthCategory]
	defense: list[DepthCategory]
	special_teams: list[DepthCategory]

class DepthChart:
	season: Season
	week: Week
	teams: list[TeamChart]
