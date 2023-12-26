import pytest
import pymongo
import os
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure

# Assuming the db.py file has been structured into a function for easier testing
# The function to be tested is named `establish_connection`

# Test ID: #1
# Test Description: Happy path test with default environment values
@pytest.mark.parametrize("env_vars, expected_attempts, expected_delay", [
    ({'MONGODB_SERVICE_NAME': 'localhost', 'MONGODB_URL': 'mongodb://localhost:27017/current_season'}, 1, 0),
], ids=["happy_path_defaults"])
def test_happy_path_defaults(env_vars, expected_attempts, expected_delay):
    # Arrange
    with patch.dict(os.environ, env_vars), \
         patch('time.sleep', return_value=None) as mock_sleep, \
         patch('src.Database.db.MongoClient') as mock_client:
        mock_client.return_value.admin.command.return_value = True

    # Act
    establish_connection()

    # Assert
    assert mock_client.call_count == expected_attempts
    mock_sleep.assert_called_with(expected_delay)

# Test ID: #2
# Test Description: Happy path test with custom environment values
@pytest.mark.parametrize("env_vars, expected_attempts, expected_delay", [
    ({'MONGODB_SERVICE_NAME': 'custom_host', 'MONGODB_URL': 'mongodb://custom_host:27017/custom_db'}, 1, 0),
], ids=["happy_path_custom_env"])
def test_happy_path_custom_env(env_vars, expected_attempts, expected_delay):
    # Arrange
    with patch.dict(os.environ, env_vars), \
         patch('time.sleep', return_value=None) as mock_sleep, \
         patch('src.Database.db.MongoClient') as mock_client:
        mock_client.return_value.admin.command.return_value = True

    # Act
    establish_connection()

    # Assert
    assert mock_client.call_count == expected_attempts
    mock_sleep.assert_called_with(expected_delay)

# Test ID: #3
# Test Description: Edge case with maximum retries reached
@pytest.mark.parametrize("env_vars, max_retries, retry_delay, expected_attempts, expected_sleep_calls", [
    ({'MONGODB_SERVICE_NAME': 'localhost', 'MONGODB_URL': 'mongodb://localhost:27017/current_season'}, 5, 5, 5, 4),
], ids=["edge_case_max_retries"])
def test_edge_case_max_retries(env_vars, max_retries, retry_delay, expected_attempts, expected_sleep_calls):
    # Arrange
    with patch.dict(os.environ, env_vars), \
         patch('time.sleep', return_value=None) as mock_sleep, \
         patch('src.Database.db.MongoClient') as mock_client, \
         patch('src.Database.db.logging') as mock_logging:
        mock_client.return_value.admin.command.side_effect = ConnectionFailure

    # Act
    with pytest.raises(ConnectionFailure):
        establish_connection()

    # Assert
    assert mock_client.call_count == expected_attempts
    assert mock_sleep.call_count == expected_sleep_calls
    mock_logging.error.assert_called_once_with("MongoDB server not available after maximum retries.")

# Test ID: #4
# Test Description: Error case with intermittent connection failures
@pytest.mark.parametrize("env_vars, max_retries, retry_delay, fail_attempts, expected_attempts, expected_sleep_calls", [
    ({'MONGODB_SERVICE_NAME': 'localhost', 'MONGODB_URL': 'mongodb://localhost:27017/current_season'}, 5, 5, 2, 3, 2),
], ids=["error_case_intermittent_failures"])
def test_error_case_intermittent_failures(env_vars, max_retries, retry_delay, fail_attempts, expected_attempts, expected_sleep_calls):
    # Arrange
    with patch.dict(os.environ, env_vars), \
         patch('time.sleep', return_value=None) as mock_sleep, \
         patch('src.Database.db.MongoClient') as mock_client, \
         patch('src.Database.db.logging') as mock_logging:
        side_effects = [ConnectionFailure] * fail_attempts + [True]
        mock_client.return_value.admin.command.side_effect = side_effects

    # Act
    establish_connection()

    # Assert
    assert mock_client.call_count == expected_attempts
    assert mock_sleep.call_count == expected_sleep_calls
    mock_logging.warning.assert_called()
    mock_logging.error.assert_not_called()
