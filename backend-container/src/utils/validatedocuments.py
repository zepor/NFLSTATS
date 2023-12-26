from src.utils.log import be_logger
from src.utils.logandcatchexceptions import log_and_catch_exceptions

@log_and_catch_exceptions
def validate_document(doc):
    try:
        assert '_id' in doc, "Missing field: _id"
        assert 'awayteam' in doc and 'id' in doc['awayteam'], "Missing field: awayteam.id"
        if 'broadcast' not in doc or '_id' not in doc['broadcast']:
            doc['broadcast'] = {
                'internet': ["Not Available"],
                'network': ["Not Available"]
            }
        if 'weather' not in doc:
            doc['weather'] = {
                'condition': "Unavailable",
                'humidity': "Unavailable",
                'temp': "Unavailable"
            }
        else:
            if 'condition' not in doc['weather']:
                doc['weather']['condition'] = "Unavailable"
            if 'humidity' not in doc['weather']:
                doc['weather']['humidity'] = "Unavailable"
            if 'temp' not in doc['weather']:
                doc['weather']['temp'] = "Unavailable"
        if 'wind' not in doc:
            doc['wind'] = {
                'direction': "Unavailable",
                'speed': "Unavailable"
            }
        else:
            if 'direction' not in doc['wind']:
                doc['wind']['direction'] = "Unavailable"
            if 'speed' not in doc['wind']:
                doc['wind']['speed'] = "Unavailable"
        if 'boxscore_info' not in doc or '_id' not in doc['boxscore_info']:
            doc['boxscore_info'] = {
                '_id': "Game not yet started"
            }
        assert 'gamegame' in doc and all(key in doc['gamegame'] for key in [
                                         '_id', 'seasonid', 'leagueweek']), "Missing field in gamegame"
        assert 'hometeam' in doc and 'id' in doc['hometeam'], "Missing field: hometeam.id"
        assert 'boxscore_info' in doc and '_id' in doc['boxscore_info'], "Missing field: boxscore_info._id"
        home_team_id = doc['hometeam']['id']
        away_team_id = doc['awayteam']['id']
        home_team_found = False
        away_team_found = False
        for team_obj in doc['team_info']:
            if team_obj['_id'] == home_team_id:
                home_team_found = True
            if team_obj['_id'] == away_team_id:
                away_team_found = True
        assert home_team_found, f"Missing home team information for team ID {home_team_id}"
        assert away_team_found, f"Missing away team information for team ID {away_team_id}"
        return True
    except AssertionError as e:
        be_logger.warning(
            f"Invalid document reason for ID {doc.get('_id', 'unknown')}: {str(e)}")
        return False
