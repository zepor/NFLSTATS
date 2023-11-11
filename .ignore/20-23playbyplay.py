    print("Fetching alldetailcurrentseasonplaybyplay for the first time...")
    self.get_alldetailcurrentseasonplaybyplay_cache = FootballData.fetch_alldetailcurrentseasonplaybyplay()
    
    
    
    @staticmethod
    @log_and_catch_exceptions
    def fetch_alldetailcurrentseasonplaybyplay():
        print("Starting fetch for alldetailcurrentseasonplaybyplay...")
        data = [
            {
                '$lookup': {
                    'from': 'BoxscoreInfo',
                    'localField': 'gamegame._id',
                    'foreignField': 'gamebs._id',
                    'as': 'Boxscoreinfo'
                }
            }, {
                '$lookup': {
                    'from': 'SeasonInfo',
                    'localField': 'gamegame.seasonid',
                    'foreignField': '_id',
                    'as': 'season_info'
                }
            }
        ]
        print("Finished fetch for alldetailcurrentseasonplaybyplay.")
        return data
    