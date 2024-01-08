import requests
from src.sportsradar.simulation.available_recordings import AvailableRecordings
from src.sportsradar.simulation.session import create_session
from src.sportsradar.simulation.config import Config

GAME_FEEDS_TYPE = "replay"


class GameFeeds:
    """
    This class is used to interact with game feeds.

    Attributes:
        base_url (str): The base URL for the game feeds.
        game_feeds (str): The type of game feeds.

    Methods:
        get_available_recordings: Retrieve the available recordings.
        get_session: Get the session for a given recording ID.
    """

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.game_feeds = "replay"

    def get_available_recordings(self):
        av_rec = AvailableRecordings(base_url=f"{self.base_url}/graphql")
        query = av_rec.construct_query()
        recording_id = av_rec.post_json_data(query)
        return recording_id.json()["data"]["recordings"][0]["id"]

    def get_session(self, recording_id):
        session = create_session(
            url=f"{self.base_url}/graphql", recording_id=recording_id
        )
        return session.json()["data"]["createSession"]


def get_game_boxscore(recording_id, session_id):
    """
    :param recording_id: The unique identifier for the recording of the game.
    :param session_id: The unique identifier for the session of the game.
    :return: The JSON response containing the game boxscore data.

    This method retrieves the game boxscore data for a given recording and session of a game. It constructs a URL using the base URL, game feeds type, league, recording id, content type
    *, and session id. The constructed URL is then used to make a GET request to the specified endpoint. If the response status code is not 200, an exception is raised with the corresponding
    * status code. The JSON response is returned as the result of the method.
    """
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=boxscore&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


def get_game_info(recording_id, session_id):
    """

    :param recording_id: The ID of the recording.
    :param session_id: The ID of the session.
    :return: The game information in JSON format.

    """
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=game&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


def get_pbp_info(recording_id, session_id):
    """
    Get play-by-play information for a recording.

    :param recording_id: The ID of the recording.
    :param session_id: The session ID.
    :return: The play-by-play information in JSON format.
    """
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=pbp&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


def get_game_roster(recording_id, session_id):
    """
    :param recording_id: Recording ID of the game.
    :param session_id: Session ID of the game.
    :return: JSON object containing the game roster.

    This method retrieves the game roster for a specific game identified by the recording ID and session ID. It makes a GET request to the specified URL, which includes the recording ID
    *, session ID, and other necessary parameters. If the request is successful (status code 200), the response is returned as a JSON object. If the request fails, an exception is raised
    * with the corresponding status code.
    """
    url = f"{Config.BASE_URL}/{GAME_FEEDS_TYPE}/{Config.LEAGUE}/{recording_id}?feed=rosters&contentType={Config.CONTENT_TYPE}&sessionId={session_id}"
    response = requests.get(url=url)
    print(response)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return response.json()


# Usage
# game_feeds = GameFeeds()
# rec_id = game_feeds.get_available_recordings()
# session_id = game_feeds.get_session(recording_id=rec_id)
# game_feeds_data = {'rec_id': rec_id, 'session_id': session_id}
# game_boxscore = get_game_boxscore(recording_id=game_feeds_data['rec_id'], session_id=game_feeds_data['session_id'])
# game_info = get_game_info(recording_id=game_feeds_data['rec_id'], session_id=game_feeds_data['session_id'])
# game_rosters = get_game_roster(recording_id=game_feeds_data['rec_id'], session_id=game_feeds_data['session_id'])
