from src.sportsradar import logging_helpers

logger = logging_helpers.get_logger(__name__)


class AdditionalFeedsTransformer:
    """
    AdditionalFeedsTransformer class is used to transform additional feeds data.

    Args:
        data (dict): A dictionary containing additional feeds data.

    Methods:
        transform_weekly_depth_charts: Transforms the weekly depth charts data by removing unwanted feeds.
        transform_daily_change_log: Transforms the daily change log data by removing unwanted feeds.
        transform_daily_transactions: Transforms the daily transactions data by removing unwanted feeds
        transform_league_hierarchy: Transforms the league hierarchy data by removing unwanted feeds
        transform_seasons: Transforms the seasons data by removing unwanted feeds
        transform_weekly_injuries: Transforms the weekly_injuries data by removing unwanted feeds


    Returns:
        dict: The transformed team weekly depth charts data.
        dict: The transformed daily change logs data
        dict: The transformed daily transactoins data
        dict: The transformed league hierarchy data
        dict: The transformed seasons data
        dict: The Transformed weekly injuries data
    """

    UNWANTED_KEYS = ["_comment"]

    def __init__(self, data: dict):
        self.data = data

    def _remove_unwanted_feeds(self):
        for key in self.UNWANTED_KEYS:
            if key in self.data:
                self.data.pop(key)

    def transform_weekly_depth_charts(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_daily_change_log(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_daily_transactions(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_league_hierarchy(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_postgame_standings(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_seasons(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_weekly_injuries(self):
        self._remove_unwanted_feeds()
        return self.data
