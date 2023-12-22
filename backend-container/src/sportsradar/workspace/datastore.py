from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib3.util.retry import Retry
from pydantic import HttpUrl
from requests.adapters import HTTPAdapter
import requests
from src.sportsradar import logging_helpers
import os

logger = logging_helpers.get_logger(__name__)

# load_dotenv("../../../../../.env")


def create_mongo_client():
    mongo_url = os.getenv("MONGODB_URL")
    if mongo_url is None:
        raise ValueError("MongoDB environment variable for URL not set.")
    return MongoClient(host=mongo_url, server_api=ServerApi("1"), port=27017)


def setup_http_session():
    retries = Retry(
        total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def save_data(response, db_uri, database, collection):
    mongo_client = MongoClient(host=db_uri, server_api=ServerApi("1"), port=27017)
    if database is None:
        raise ValueError("MongoDB environment variable not set.")
    print(database)
    db = mongo_client[database]
    db[collection].insert_one(response.json())


class SportsRadarFetcher:
    def __init__(self, timeout: float = 30):
        self.timeout = timeout
        self.http = setup_http_session()
        self.mongo_client = create_mongo_client()
        self.mongo_db = os.getenv("MONGODB_DATABASE")
        if self.mongo_db is None:
            raise ValueError("MongoDB environment variable for Database not set.")

    # def save_data(self, collection, data):
    #     db = self.mongo_client[self.mongo_db]
    #     db[collection].insert_one(data)

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
    def __init__(self, fetcher: SportsRadarFetcher):
        self.fetcher = fetcher
        self.data = {}

    # other methods remain same
    def fetch_data(self, url):
        try:
            response = self.fetcher.fetch_data(url)
            if response.status_code == requests.codes.ok:
                self.data.update({url: response.json()})
                return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise
