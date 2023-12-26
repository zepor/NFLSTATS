import sys
import os
import pickle
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from src.models.game_info import GameInfo
from src.database.connections import r
from src.utils.validatedocuments import validate_document
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))  

@log_and_catch_exceptions
def fetch_live_games_data():
    global live_games_query_running
    live_games_cache_key = "livegames_cache"
    cached_live_games = r.get(live_games_cache_key)
    if live_games_query_running:
        be_logger.warning("Live games query is already running.")
        return None
    elif cached_live_games is not None:
        be_logger.info("Using cached live games data.")
        return pickle.loads(cached_live_games)
    else:
        be_logger.info("No cached live games data found.")
    live_games_query_running = True
    try:
        now_utc = datetime.now(timezone.utc)
        in_three_days_utc = now_utc + timedelta(days=3)
        be_logger.debug("Querying games between %s and %s",
                        now_utc, in_three_days_utc)
        thisweeksgames = [
            {
                '$match': {
                    'gamegame.scheduled': {
                        '$gte': now_utc,
                        '$lt': in_three_days_utc
                    }
                }
            }, {
                '$group': {
                    '_id': '$gamegame.leagueweek'
                }
            }, {
                '$project': {
                    '_id': 0,
                    'leagueweek': '$_id'
                }
            }, {
                '$lookup': {
                    'from': 'GameInfo',
                    'localField': 'leagueweek',
                    'foreignField': 'gamegame.leagueweek',
                    'as': 'games'
                }
            }, {
                '$unwind': '$games'
            }, {
                '$lookup': {
                    'from': 'BoxscoreInfo',
                    'localField': 'games._id',
                    'foreignField': '_id',
                    'as': 'games.boxscore_info'
                }
            }, {
                '$lookup': {
                    'from': 'LeagueInfo',
                    'localField': 'games.gamegame.leagueweek',
                    'foreignField': '_id',
                    'as': 'games.league_info'
                }
            }, {
                '$lookup': {
                    'from': 'SeasonStatPlayer',
                    'let': {
                        'teamIds': [
                            '$games.hometeam.id', '$games.awayteam.id'
                        ]
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$in': [
                                        '$teamid', '$$teamIds'
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'games.season_stat_player'
                }
            }, {
                '$lookup': {
                    'from': 'SeasonStatPlayer',
                    'let': {
                        'teamIds': [
                            '$games.hometeam.id', '$games.awayteam.id'
                        ],
                        'gameSeasonId': '$games.gamegame.seasonid'
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {
                                            '$in': [
                                                '$teamid', '$$teamIds'
                                            ]
                                        }, {
                                            '$eq': [
                                                '$seasonid', '$$gameSeasonId'
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'games.season_stat_player'
                }
            }, {
                '$lookup': {
                    'from': 'SeasonStatOppo',
                    'let': {
                        'teamIds': [
                            '$games.hometeam.id', '$games.awayteam.id'
                        ],
                        'gameSeasonId': '$games.gamegame.seasonid'
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {
                                            '$in': [
                                                '$teamid', '$$teamIds'
                                            ]
                                        }, {
                                            '$eq': [
                                                '$seasonid', '$$gameSeasonId'
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'games.season_stat_oppo'
                }
            }, {
                '$lookup': {
                    'from': 'SeasonStatTeam',
                    'let': {
                        'teamIds': [
                            '$games.hometeam.id', '$games.awayteam.id'
                        ],
                        'gameSeasonId': '$games.gamegame.seasonid'
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {
                                            '$in': [
                                                '$teamid', '$$teamIds'
                                            ]
                                        }, {
                                            '$eq': [
                                                '$seasonid', '$$gameSeasonId'
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'games.season_stat_team'
                }
            }, {
                '$lookup': {
                    'from': 'TeamInfo',
                    'let': {
                        'homeTeamId': '$games.hometeam.id',
                        'awayTeamId': '$games.awayteam.id'
                    },
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$or': [
                                        {
                                            '$eq': [
                                                '$_id', '$$homeTeamId'
                                            ]
                                        }, {
                                            '$eq': [
                                                '$_id', '$$awayTeamId'
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'games.team_info'
                }
            }, {
                '$replaceRoot': {
                    'newRoot': '$games'}}]
        games = list(GameInfo.objects.aggregate(*thisweeksgames))
        for game in games:
            if not validate_document(game):
                be_logger.warning(
                    f"Game document with ID {game['_id']} is invalid.")
        if not games:
            be_logger.warning(
                "No live games found for this week in the database after aggregation.")
            r.delete(live_games_cache_key)
            be_logger.info("Deleted cache key: %s", live_games_cache_key)
            return None
        else:
            if 'gamegame' in games[0] and 'hometeam' in games[0]:
                be_logger.debug(
                    "Retrieved %d games for this week.", len(games))
                r.set(live_games_cache_key, pickle.dumps(
                    {"upcominggames": games}))
                return {"upcominggames": games}
            else:
                be_logger.warning(
                    "fetch_live_games_data did not return expected data format.")
                return None
    except Exception as e:
        be_logger.error(
            f"Error occurred while fetching live games data: {str(e)}")
        return None
    finally:
        live_games_query_running = False