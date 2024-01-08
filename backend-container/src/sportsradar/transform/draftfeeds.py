from src.sportsradar import logging_helpers

logger = logging_helpers.get_logger(__name__)


class DraftFeedsTransformer:
    """
    DraftFeedsTransformer class is used to transform draft feeds data.

    Attributes:
        UNWANTED_KEYS (list): List of unwanted keys to be removed from the data dictionary.

    Args:
        data (dict): A dictionary containing draft feeds data.

    Methods:
        transform_draft_summary(): Transforms the draft summary.
        transform_prospects: Transforms the prospects' data.
        transform_team_draft_summary(): Transforms the team draft summary data.
        transform_top_prospects(): Transforms the top prospects' data.
        transform_trades(): Transforms the trades' data.

    Returns:
        dict: The transformed data into dictionary.
    """

    UNWANTED_KEYS = ["_comment"]

    def __init__(self, data: dict):
        self.data = data

    def _remove_unwanted_feeds(self):
        for key in self.UNWANTED_KEYS:
            if key in self.data:
                self.data.pop(key)

    def transform_draft_summary(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_prospects(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_team_draft_summary(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_top_prospects(self):
        self._remove_unwanted_feeds()
        return self.data

    def transform_trades(self):
        self._remove_unwanted_feeds()
        return self.data
