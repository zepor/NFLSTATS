from dotenv import load_dotenv
from src.sportsradar import logging_helpers
from src.sportsradar.workspace.datastore import DataStore, SportsRadarFetcher

load_dotenv("../../../.env")

logger = logging_helpers.get_logger(__name__)


class TeamFeeds:
    """This class is responsible for extracting team feeds from SportRadar."""

    def __init__(self, base_url):
        """
        Initialize an instance of the class.
        :param base_url: The base URL for the API.
        :type base_url: str
        """
        self.base_url = base_url

    def get_team_roster(
        self, access_level, version, language_code, team_id, file_format, api_key
    ):
        """
        Get the team roster for a given team_id
        :param access_level:
        :param version:
        :param language_code:
        :param team_id:
        :param file_format:
        :param api_key:
        :return: The team roster for the given team_id
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/teams/{team_id}/full_roster.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result

    def get_seasonal_statistics(
        self,
        access_level,
        version,
        language_code,
        year,
        nfl_season,
        team_id,
        file_format,
        api_key,
    ):
        """
        Get the team roster for a given year, nfl_season, and team_id
        :param access_level:
        :param version:
        :param language_code:
        :param year:
        :param nfl_season:
        :param team_id:
        :param file_format:
        :param api_key:
        :return: The seasonsal statistics feed of the given team_id, nfl_season, and year
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/seasons/{year}/{nfl_season}/teams/{team_id}/statistics.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result
