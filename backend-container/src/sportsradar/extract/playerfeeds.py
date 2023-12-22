from dotenv import load_dotenv
from src.sportsradar import logging_helpers
from src.sportsradar.workspace.datastore import DataStore, SportsRadarFetcher

load_dotenv("../../../.env")

logger = logging_helpers.get_logger(__name__)


class PlayerFeeds:
    """This class is responsible for extracting players feed from SportRadar."""

    def __init__(self, base_url):
        """
        Initialize an instance of the class.
        :param base_url: The base URL for the API.
        :type base_url: str
        """
        self.base_url = base_url

    def get_player_profile(
        self, access_level, version, language_code, player_id, file_format, api_key
    ):
        """
        Get the game boxscore for a given game_id
        :param access_level:
        :param version:
        :param language_code:
        :param player_id:
        :param file_format:
        :param api_key:
        :return: The game boxscore for the given game_id
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/players/{player_id}/profile.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result
