import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend-container.src.utils.log import be_logger

from datetime import datetime
from Database.rediscache import FootballData, clear_cache

from nflfetchqueries.fetchallseasonsplayerstatdetails import fetch_AllSeasonsPlayerStatDetails
from unittest.mock import patch

# The following tests are designed to achieve 100% line and branch coverage for the fetch_AllSeasonsPlayerStatDetails function.
# Since the function is a static method and does not take any parameters, the tests will focus on the behavior of the decorator and the output.

# Happy path tests with various realistic test values
@pytest.mark.parametrize("test_id, expected_output", [
    ("HP-1", [{'$lookup': ...}, {'$unwind': ...}, ...]),  # The ellipsis (...) represents the full expected pipeline.
    # Add more test cases with different expected outputs if necessary.
])
def test_fetch_AllSeasonsPlayerStatDetails_happy_path(test_id, expected_output):
    # Arrange
    # Mocking the decorator to bypass any logging or exception handling for a clean test of the function's return value.
    with patch('utils.logandcatchexceptions.log_and_catch_exceptions', lambda x: x):
        
        # Act
        result = fetch_AllSeasonsPlayerStatDetails()
        
        # Assert
        assert result == expected_output, f"Test Failed: {test_id}"

# Edge cases
# Since the function does not take any parameters, there are no traditional edge cases to test.
# However, we can test the behavior when the decorator is supposed to handle exceptions.
@pytest.mark.parametrize("test_id, side_effect, expected_exception", [
    ("EC-1", Exception("Database connection failed"), Exception),
    # Add more test cases if there are other specific exceptions or side effects to test.
])
def test_fetch_AllSeasonsPlayerStatDetails_edge_cases(test_id, side_effect, expected_exception):
    # Arrange
    with patch('utils.logandcatchexceptions.log_and_catch_exceptions') as mock_decorator:
        mock_decorator.side_effect = side_effect
        
        # Act and Assert
        with pytest.raises(expected_exception):
            fetch_AllSeasonsPlayerStatDetails()
            assert mock_decorator.called, f"Test Failed: {test_id}"

# Error cases
# Since the function does not take any parameters and is not supposed to raise exceptions (handled by the decorator),
# there are no traditional error cases to test.
# However, we can ensure that the decorator is called and that it handles any exceptions that may occur.
@pytest.mark.parametrize("test_id, side_effect", [
    ("ER-1", Exception("Unexpected error")),
    # Add more test cases if there are other specific exceptions or side effects to test.
])
def test_fetch_AllSeasonsPlayerStatDetails_error_cases(test_id, side_effect):
    # Arrange
    with patch('utils.logandcatchexceptions.log_and_catch_exceptions') as mock_decorator:
        mock_decorator.side_effect = side_effect
        
        # Act
        # Call the function, expecting the decorator to handle any exceptions.
        fetch_AllSeasonsPlayerStatDetails()
        
        # Assert
        assert mock_decorator.called, f"Test Failed: {test_id}"
