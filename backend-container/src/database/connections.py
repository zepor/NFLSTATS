import os
from src.utils.log import be_logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import redis
from dotenv import load_dotenv 
load_dotenv()
def get_mongodb_connection():
    """Establishes a connection to MongoDB.

    Returns:
        A MongoClient object representing the connection to MongoDB, or None if the connection could not be established.

    Raises:
        ConnectionFailure: If the connection to MongoDB fails after the maximum number of retries.

    """
    mongodb_service_name = os.getenv('MONGODB_SERVICE_NAME', 'localhost')
    mongodb_url = os.getenv(
        'MONGODB_URL', f"mongodb://{mongodb_service_name}:27017/current_season"
    )
    MAX_RETRIES = 5  # Maximum number of retries
    RETRY_DELAY = 5

    client = MongoClient(mongodb_url, connectTimeoutMS=30000, socketTimeoutMS=None)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client.admin.command('ismaster')
            return client  # Return the client object if the connection is successful
        except ConnectionFailure:
            if attempt < MAX_RETRIES:
                logging.warning(f"MongoDB server not available. "
                                f"Attempt {attempt} of {MAX_RETRIES}. "
                                f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)  # Wait for a while before retrying
            else:
                logging.error("MongoDB server not available after maximum retries.")
                # Handle the maximum retries reached scenario
                return None  # Return None to indicate a failure

def connect_to_redis(primary_host, fallback_host, port=6379):
    """Establishes a connection to Redis.

    Args:
        primary_host: The primary Redis host.
        port: The Redis port (default is 6379).

    Returns:
        A Redis connection object.

    Raises:
        redis.exceptions.ConnectionError: If the Redis host is unavailable.

    """
    try:
        # Try connecting to the primary Redis host
        r = redis.StrictRedis(host=primary_host, port=port,
                              decode_responses=False)
        r.ping()
        return r
    except redis.exceptions.ConnectionError:
        # If the primary host is unavailable, try the fallback host
        try:
            r = redis.StrictRedis(host=fallback_host,
                                  port=port, decode_responses=False)
            r.ping()
            return r
        except redis.exceptions.ConnectionError as ex:
            # If both connections fail, handle the exception appropriately
            be_logger.info("Could not connect to Redis: %s", str(ex))
            # You may want to raise an exception or handle it in some other way here
            raise


redis_primary_host = 'redis'  # The host used in the development environment
# The host used in the Kubernetes environment
redis_fallback_host = 'redis-service'
redis_port = 6379  # Default Redis port
r = connect_to_redis(redis_primary_host, redis_fallback_host, redis_port)
