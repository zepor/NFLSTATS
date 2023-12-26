import sys
import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from src.utils.logandcatchexceptions import log_and_catch_exceptions
from src.utils.log import be_logger

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)  
sys.path.append(os.path.join(project_root, 'src'))

@log_and_catch_exceptions
def fetch_allseasonsteamstatdetails():
    be_logger.info("Starting fetch for fetch_allseasonsteamstatdetails...")
    return [
        {
            '$lookup': {
                'from': 'TeamInfo',
                'localField': 'teamid',
                'foreignField': '_id',
                'as': 'teamInfo'
            }
        }, {
            '$unwind': '$teamInfo'
        }, {
            '$lookup': {
                'from': 'FranchiseInfo',
                'localField': 'teamid',
                'foreignField': 'teamid',
                'as': 'franchiseInfo'
            }
        }, {
            '$unwind': '$franchiseInfo'
        }, {
            '$lookup': {
                'from': 'SeasonInfo',
                'localField': 'seasonid',
                'foreignField': '_id',
                'as': 'seasonInfo'
            }
        }, {
            '$unwind': '$seasonInfo'
        }, {
            '$lookup': {
                'from': 'SeasonStatOppo',
                'let': {
                    'team_id': '$teamid',
                    'season_id': '$seasonid'
                },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    {
                                        '$eq': [
                                            '$teamid', '$$team_id'
                                        ]
                                    }, {
                                        '$eq': [
                                            '$seasonid', '$$season_id'
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ],
                'as': 'seasonStatOppo'
            }
        }, {
            '$unwind': '$seasonStatOppo'
        }, {
            '$lookup': {
                'from': 'SeasonStatTeam',
                'let': {
                    'team_id': '$teamid',
                    'season_id': '$seasonid'
                },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    {
                                        '$eq': [
                                            '$teamid', '$$team_id'
                                        ]
                                    }, {
                                        '$eq': [
                                            '$seasonid', '$$season_id'
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ],
                'as': 'seasonStatTeam'
            }
        }, {
            '$unwind': '$seasonStatTeam'
        }, {
            '$group': {
                '_id': {
                    'year': '$seasonInfo.year',
                    'season_type': '$seasonInfo.type',
                    'team': '$teamInfo.team.name'
                },
                'teamInfo': {
                    '$first': '$teamInfo'
                },
                'franchiseInfo': {
                    '$first': '$franchiseInfo'
                },
                'seasonStatOppo': {
                    '$first': '$seasonStatOppo'
                },
                'seasonStatTeam': {
                    '$first': '$seasonStatTeam'
                }
            }
        }, {
            '$sort': {
                '_id.year': -1,
                '_id.season_type': 1
            }
        }
    ]