import datetime
from abc import ABC, abstractmethod
from typing import Any, NamedTuple, Optional, cast
from dotenv import load_dotenv, find_dotenv
import redis
import json

from src.sportsradar.logging_helpers import get_logger

logger = get_logger(__name__)
load_dotenv(find_dotenv())


class NFLStatsResourceKey(NamedTuple):
    """
    Represents a resource key for NFL statistics.

    Attributes:
        None

    Methods:
        __str__(): Returns the string representation of the resource key.

    Usage:
        resource_key = NFLStatsResourceKey()
        key_str = str(resource_key)
    """

    def __str__(self) -> str:
        return "NFLStats_" + datetime.date.today().strftime("%Y-%m-%d")


class AbstractCache(ABC):
    """
    AbstractCache

    This class is an abstract base class for cache implementations. It defines the common interface that all cache implementations should adhere to.

    Attributes:
        _read_only (bool): Indicates whether the cache is read-only or not.

    Methods:
        __init__(self, read_only: bool = False):
            Initializes the AbstractCache object.

            Args:
                read_only (bool, optional): Indicates whether the cache is read-only. Defaults to False.

        is_read_only(self) -> bool:
            Returns the read-only status of the cache.

            Returns:
                bool: True if the cache is read-only, False otherwise.

        get(self, resource: NFLStatsResourceKey) -> Any:
            Retrieves the content associated with the given resource key from the cache.

            Args:
                resource (NFLStatsResourceKey): The resource key to retrieve the content for.

            Returns:
                Any: The content associated with the given resource key.

        add(self, resource: NFLStatsResourceKey, content: Any) -> None:
            Adds the content to the cache under the given resource key.

            Args:
                resource (NFLStatsResourceKey): The resource key to add the content under.
                content (Any): The content to be added to the cache.

            Returns:
                None

        delete(self, resource: NFLStatsResourceKey) -> None:
            Deletes the content associated with the given resource key from the cache.

            Args:
                resource (NFLStatsResourceKey): The resource key to delete the content for.

            Returns:
                None

        contains(self, resource: NFLStatsResourceKey) -> bool:
            Checks whether the cache contains the content associated with the given resource key.

            Args:
                resource (NFLStatsResourceKey): The resource key to check for.

            Returns:
                bool: True if the cache contains the content for the given resource key, False otherwise.
    """

    def __init__(self, read_only: bool = False):
        self._read_only = read_only

    def is_read_only(self) -> bool:
        return self._read_only

    @abstractmethod
    def get(self, resource: NFLStatsResourceKey) -> Any:
        pass

    @abstractmethod
    def add(self, resource: NFLStatsResourceKey, content: Any) -> None:
        pass

    @abstractmethod
    def delete(self, resource: NFLStatsResourceKey) -> None:
        pass

    @abstractmethod
    def contains(self, resource: NFLStatsResourceKey) -> bool:
        pass


class RedisCache(AbstractCache):
    """
    RedisCache

    A class that represents a cache using Redis as the underlying storage.

    Methods:
        - get(resource: NFLStatsResourceKey) -> Any:
            Retrieves the value associated with the given resource key from the cache.
            If the key does not exist in the cache, a KeyError is raised.

        - add(resource: NFLStatsResourceKey, value: Any):
            Adds the given resource key-value pair to the cache.
            If the cache is read-only, the operation is ignored.

        - delete(resource: NFLStatsResourceKey):
            Deletes the value associated with the given resource key from the cache.
            If the cache is read-only, the operation is ignored.

        - contains(resource: NFLStatsResourceKey) -> bool:
            Checks whether the cache contains the given resource key.

    Parameters:
        - host: Optional[str] = None
            The host address of the Redis server. If not provided, the default value is None.

        - port: Optional[str] = None
            The port number of the Redis server. If not provided, the default value is None.

        - password: Optional[str] = None
            The password to authenticate with the Redis server. If not provided, the default value is None.

        - **kwargs: Any
            Additional keyword arguments to customize the cache.

    Attributes:
        - _db: redis.StrictRedis
            The Redis client used for interacting with the Redis server.

    Note:
        This class is designed to be used as a subclass of AbstractCache.
        It assumes the existence of the Redis package in the Python environment.
        The Redis server must be accessible for the cache operations to work.

    Example usage:
        cache = RedisCache(host='localhost', port='6379', password='password')
        cache.add('resource_key', {'data': 'value'})
        value = cache.get('resource_key')
        cache.contains('resource_key')

    Caution:
        Be cautious when using this cache implementation with sensitive data as Redis is an in-memory database.
        Ensure proper security measures are in place to protect the data stored in Redis.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self._db = redis.StrictRedis(
            host=cast(str, host), port=cast(str, port), password=cast(str, password)
        )

    def get(self, resource: NFLStatsResourceKey) -> Any:
        value = self._db.get(str(resource))
        if value is None:
            raise KeyError(f"Resource - {resource} not found in the Redis cache")
        return json.loads(value)

    def add(self, resource: NFLStatsResourceKey, value: Any):
        if self.is_read_only():
            logger.debug(f"Read-only cache: ignoring set({resource})")
            return
        self._db.set(str(resource), json.dumps(value))

    def delete(self, resource: NFLStatsResourceKey):
        if self.is_read_only():
            logger.debug(f"Read-only cache: ignoring delete({resource})")
            return
        self._db.delete(str(resource))

    def contains(self, resource: NFLStatsResourceKey) -> bool:
        return bool(self._db.exists(str(resource)))


# example usage
# document_to_store = {
#     "name": "John",
#     "documents": [
#         {"title": "Doc 1", "content": "Content 1"},
#         {"title": "Doc 2", "content": "Content 2"},
#     ],
# }
#
# redis_host = os.getenv("REDIS_HOST_GG")
# redis_port = os.getenv("REDIS_PORT_GG")
# redis_pass = os.getenv("REDIS_PASS_GG")
#
# nfl_stats_resource_key = NFLStatsResourceKey()
#
# redis_cache = RedisCache(host=redis_host, port=redis_port, password=redis_pass)
#
# redis_cache.add(resource=nfl_stats_resource_key, value=document_to_store)
#
# try:
#     retrieved_content = redis_cache.get(resource=nfl_stats_resource_key)
#     print(retrieved_content)
#
# except KeyError:
#     print("Resource not found in the Redis cache")
