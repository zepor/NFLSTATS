from dotenv import load_dotenv
from src.sportsradar import logging_helpers
from src.sportsradar.workspace.datastore import DataStore, SportsRadarFetcher

load_dotenv("../../../.env")

logger = logging_helpers.get_logger(__name__)


class AdditionalFeeds:
    """This class is responsible for extracting additional feeds from SportRadar."""

    def __init__(self, base_url):
        """
        Initialize an instance of the class.
        :param base_url: The base URL for the API.
        :type base_url: str
        """
        self.base_url = base_url

    def get_weekly_depth_charts(
        self,
        access_level,
        version,
        language_code,
        year,
        nfl_season,
        nfl_season_week,
        file_format,
        api_key,
    ):
        """
        Get the depth_charts for a given team_id
        :param access_level:
        :param version:
        :param language_code:
        :param year: Year in 4 digit format (YYYY).
        :param nfl_season:	Preseason (PRE), Regular Season (REG), or Post-Season (PST).
        :param nfl_season_week:	The number of weeks into the season in 2 digit format (WW).
        :param file_format:
        :param api_key:
        :return: The weeekly depth charts for the given year, nfl_season, nfl_season_week
        """
        if not api_key:
            logger.error("API key not found in environment variables.")
            raise ValueError("API key not found in environment variables")
        datastore = DataStore(SportsRadarFetcher())
        result = datastore.fetch_data(
            url=f"{self.base_url}/{access_level}/{version}/{language_code}/seasons/{year}/{nfl_season}/{nfl_season_week}/depth_charts.{file_format}?api_key={api_key}"
        )
        logger.info("Data retrieved successfully.")
        return result
