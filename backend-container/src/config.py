import os
from pickle import TRUE
import logging
from dotenv import load_dotenv
# Consider a custom exception class


class ConfigurationError(Exception):
    pass


# Only load the environment variables once, ideally in a separate script
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)
if not hasattr(os, 'add_dll_directory'):
    def add_dll_directory(path):
        pass
# Base Configuration


class Config:
    DEBUG = False
    TESTING = False
    connection_string = os.getenv('MONGODB_URL')
    if not connection_string:
        raise ConfigurationError(
            "MONGODB_URL must be set in .env or environment variables")
    MONGODB_SETTINGS = {
        'db': 'Current_Season',
        'host': connection_string,
        'maxPoolSize': 50,
        'minPoolSize': 5
    }
    LOGGING_LEVEL = logging.ERROR


class DevelopmentConfig(Config):
    DEBUG = TRUE
    TESTING = TRUE
    LOGGING_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    LOGGING_LEVEL = logging.WARNING
