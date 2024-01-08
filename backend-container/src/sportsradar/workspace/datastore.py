import os
from typing import List, Dict
from urllib3.util.retry import Retry
from pydantic import HttpUrl
from requests.adapters import HTTPAdapter
import requests
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from src.sportsradar import logging_helpers

logger = logging_helpers.get_logger(__name__)


# load_dotenv("../../../../../.env")


def create_mongo_client():
    """Create a MongoDB client connection.

    This method retrieves the MongoDB URL from the environment variable MONGODB_URL.
    It then creates a MongoClient instance using the retrieved URL, along with a specified server API version and default port.

    Returns:
        MongoClient: An instance of the MongoDB client.

    Raises:
        ValueError: If the MONGODB_URL environment variable is not set.
    """
    mongo_url = os.getenv("MONGODB_URL")
    if mongo_url is None:
        raise ValueError("MongoDB environment variable for URL not set.")
    return MongoClient(host=mongo_url, server_api=ServerApi("1"), port=27017)


def setup_http_session():
    """

    This function sets up an HTTP session with retries and mounts an adapter for handling HTTP requests.

    Returns:
        session (requests.Session): The initialized HTTP session.

    """
    retries = Retry(
        total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def save_data(response, db_uri, database, collection):
    """
    Save data to MongoDB collection.

    Parameters:
    - response (object): The response object containing the data to be saved.
    - db_uri (str): The MongoDB connection URI.
    - database (str): The name of the database in which to save the data.
    - collection (str): The name of the collection in which to save the data.

    Raises:
    - ValueError: If the database name is None.

    """
    mongo_client = MongoClient(host=db_uri, server_api=ServerApi("1"), port=27017)
    if database is None:
        raise ValueError("MongoDB environment variable not set.")
    else:
        print(database)
        db = mongo_client[database]
        db[collection].insert_one(response.json())


class SportsRadarFetcher:
    """
    Class to fetch data from SportsRadar API.

    Attributes:
    - timeout (float): The timeout value for HTTP requests in seconds.
    - http (Session): The HTTP session object for making requests.
    - mongo_client (MongoClient): The MongoDB client object for connecting to the database.
    - mongo_db (str): The name of the MongoDB database.

    Methods:
    - __init__(timeout: float = 30): Initializes the SportsRadarFetcher instance.
    - _fetch_from_url(url: HttpUrl) -> requests.Response: Fetches data from the given URL.
    - fetch_data(url: HttpUrl) -> requests.Response: Fetches data from the SportsRadar API.

    """

    def __init__(self, timeout: float = 30):
        self.timeout = timeout
        self.http = setup_http_session()
        self.mongo_client = create_mongo_client()
        self.mongo_db = os.getenv("MONGODB_DATABASE")
        if self.mongo_db is None:
            raise ValueError("MongoDB environment variable for Database not set.")

    def _fetch_from_url(self, url: HttpUrl) -> requests.Response:
        logger.info(f"Retrieving {url} from SportsRadar")
        response = self.http.get(url, timeout=self.timeout)
        if response.status_code == requests.codes.ok:
            logger.debug(f"Successfully downloaded from {url}")
            return response
        raise ValueError(f"Could not download from {url}: {response.text}")

    def fetch_data(self, url: HttpUrl) -> requests.Response:
        try:
            return self._fetch_from_url(url)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise


class DataStore:
    """
    Class for storing and retrieving data using a specified fetcher.

    Parameters:
    - fetcher (SportsRadarFetcher): The fetcher object used to retrieve data.

    Attributes:
    - fetcher (SportsRadarFetcher): The fetcher object used to retrieve data.
    - data (dict): A dictionary to store the fetched data.

    Methods:
    - fetch_data(url): Fetches data from the specified URL using the fetcher object. Returns the response if the request is successful.
    - get_data_from_database(collection): Retrieves data from the specified collection in the database. Returns a list of dictionaries.
    """

    def __init__(self, fetcher: SportsRadarFetcher):
        self.fetcher = fetcher
        self.data = {}

    def fetch_data(self, url):
        try:
            response = self.fetcher.fetch_data(url)
            if response.status_code == requests.codes.ok:
                self.data.update({url: response.json()})
                return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise

    def get_data_from_database(self, collection: str) -> List[Dict]:
        try:
            client = self.fetcher.mongo_client
            db = client[self.fetcher.mongo_db]
            data = db[collection].find()
            return list(data)
        except Exception as e:
            logger.error(f"Error getting data from MONGODB_DATABASE: {str(e)}")
            raise
