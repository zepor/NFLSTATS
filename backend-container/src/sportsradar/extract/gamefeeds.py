from dotenv import load_dotenv
from src.sportsradar import logging_helpers
from src.sportsradar.workspace.datastore import DataStore, SportsRadarFetcher

load_dotenv("../../../.env")

logger = logging_helpers.get_logger(__name__)


class GameFeeds:
    """This class is responsible for extracting game feeds from SportsRadar"""

    def __init__(self, base_url):
        """
        Initialize an instance of the class.
        :param base_url: The base URL for the API.
        :type base_url: str
        """
        self.base_url = base_url

    def get_game_boxscore(
        self, access_level, version, language_code, game_id, file_format, api_key
    ):
        """
        Get the game boxscore for a given game_id
        :param access_level:
        :param version:
        :param language_code:
        :param game_id:
        :param file_format:
        :param api_key:
        :return: The game boxscore for the given game_id
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/{game_id}/boxscore.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result

    def get_game_roster(
        self, access_level, version, language_code, game_id, file_format, api_key
    ):
        """
        Get the game roster for a given game_id
        :param access_level:
        :param version:
        :param language_code:
        :param game_id:
        :param file_format:
        :param api_key:
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/{game_id}/roster.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result

    def get_game_statistics(
        self, access_level, version, language_code, game_id, file_format, api_key
    ):
        """
        Get the game statistics for a given game_id
        :param access_level:
        :param version:
        :param language_code:
        :param game_id:
        :param file_format:
        :param api_key:
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/{game_id}/statistics.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result

    def get_game_pbp(
        self, access_level, version, language_code, game_id, file_format, api_key
    ):
        """
        Get the game - play by play for a given game_id
        :param access_level:
        :param version:
        :param language_code:
        :param game_id:
        :param file_format:
        :param api_key:
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/{game_id}/pbp.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result
