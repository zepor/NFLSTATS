from src.sportsradar import logging_helpers

logger = logging_helpers.get_logger(__name__)


class PlayerFeedsTransformer:
    """
    PlayerFeedsTransformer class is used to transform player profile data.

    Args:
        data (dict): A dictionary containing player profile data.

    Methods:
        transform_player_profile(): Transforms the player profile data by removing unwanted feeds.

    Returns:
        dict: The transformed player profile data.
    """

    UNWANTED_KEYS = ["_comment"]

    def __init__(self, data: dict):
        self.data = data

    def _remove_unwanted_feeds(self):
        for key in self.UNWANTED_KEYS:
            if key in self.data:
                self.data.pop(key)

    def transform_player_profile(self):
        self._remove_unwanted_feeds()
        return self.data
