from src.sportsradar import logging_helpers

logger = logging_helpers.get_logger(__name__)


class GameFeedsTransformer:
    """
    Class to transform game feeds data.

    Attributes:
        UNWANTED_KEYS (list): List of unwanted keys to be removed from the data dictionary.

    Args:
        data (dict): The game feeds data dictionary.

    Methods:
        transform_boxscore: Transforms the boxscore data.
        transform_game_roster: Transforms the game roster data.
        transform_game_statistics: Transforms the game statistics data.
    """

    UNWANTED_KEYS = ["_comment"]

    def __init__(self, data: dict):
        self.data = data

    def _remove_unwanted_feeds(self):
        for key in self.UNWANTED_KEYS:
            if key in self.data:
                self.data.pop(key)

    def transform_boxscore(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_game_roster(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_game_statistics(self):
        self._remove_unwanted_feeds()
        return self.data
