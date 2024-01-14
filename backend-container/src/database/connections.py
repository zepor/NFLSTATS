import os
import redis
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv 
from src.utils.log import be_logger
load_dotenv()
def get_mongodb_connection():
    """Establishes a connection to MongoDB.

    Returns:
        A MongoClient object representing the connection to MongoDB, or None if the connection could not be established.

    Raises:
        ConnectionFailure: If the connection to MongoDB fails after the maximum number of retries.

    """
    try:
        mongodb_url = os.environ.get('MONGODB_URL')
        if not mongodb_url:
            raise ValueError("MONGODB_URL environment variable not set.")
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000, connect=False,
                             maxPoolSize=10, connectTimeoutMS=30000, retryWrites=True,
                             w='majority', retryReads=True)
        client.admin.command('ping')  # Test the connection
        be_logger.debug("Successfully connected to MongoDB.")
        return client
    except Exception as e:
        be_logger.error(f"Failed to connect to MongoDB: {e}")
        return None

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
