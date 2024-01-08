from dotenv import load_dotenv
from src.sportsradar import logging_helpers
from src.sportsradar.workspace.datastore import DataStore, SportsRadarFetcher

load_dotenv(".../../.env")

logger = logging_helpers.get_logger(__name__)


class PrimaryFeeds:
    """This class is responsible for extracting game feeds from SportRader"""

    def __init__(self, base_url):
        """
        Initialize an instance of the class
        :param base_url: The base URL for the API
        :type base_url: str
        """

        self.base_url = base_url

    def get_current_season_schedule(
        self, access_level, version, language_code, file_format, api_key
    ):
        """
        Get the current season schedule
        :param access_level:
        :param version:
        :param language_code:
        :param format:
        :param api_key:
        """

        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variiables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/current_season/schedule.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully")
        return result

    def get_current_week_schedule(
        self, access_level, version, language_code, file_format, api_key
    ):
        """
        Get the current week schedule

        :param access_level:
        :param version:
        :param language_code:
        :param format:
        :param api_key:

        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/current_week/schedule.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully")
        return result

    def get_seasons_schedule(
        self,
        access_level,
        version,
        year,
        season_type,
        language_code,
        file_format,
        api_key,
    ):
        """
        Get the seasons schedule
        :param access_level:
        :param version:
        :param year:
        :param season_type:
        :param language_code:
        :param format:
        :param api_key:

        """
        if not api_key:
            logger.error("API key not found in environment variable.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/{year}/{season_type}/schedule.{file_format}?api_key={api_key}"
        )
        return result

    def get_weekly_schedule(
        self,
        access_level,
        version,
        season_year,
        season_type,
        week_number,
        language_code,
        file_format,
        api_key,
    ):
        """
        Get Weekly Schedule

        :param access_level:
        :param version:
        :param season_year:
        :param season_type:
        :param week_number:
        :param language_code:
        :param format:
        :param api_key:

        """

        if not api_key:
            logger.error("API key not found in enviroment variable.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/games/{season_year}/{season_type}/{week_number}/schedule.{file_format}?api_key={api_key}"
        )

        return result
