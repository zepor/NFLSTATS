print("Fetching AllSeasonsPlayerStatDetails for the first time...")
self.get_AllSeasonsPlayerStatDetails_cache = FootballData.fetch_AllSeasonsPlayerStatDetails()


@staticmethod
    @log_and_catch_exceptions
    def fetch_AllSeasonsPlayerStatDetails():
        print("Starting fetch for AllSeasonsPlayerStatDetails...")
        data = [
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
                    'from': 'SeasonStatPlayer',
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
                    'as': 'seasonstatplayer'
                }
            }, {
                '$unwind': '$seasonstatplayer'
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
                    'seasonInfo': {
                        '$first': '$seasonInfo'
                    },
                    'seasonstatplayer': {
                        '$first': '$seasonstatplayer'
                    }
                }
            }, {
                '$sort': {
                    '_id.year': -1,
                    '_id.season_type': 1
                }
            }
        ]
        print("Finished fetch for AllSeasonsPlayerStatDetails.")
        return data  