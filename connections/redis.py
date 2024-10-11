"""
Redis Connection Manager Module

This module provides a connection manager for Redis, implementing the IConnectionManager interface.
It handles the creation and management of Redis client connections.

Classes:
    RedisConnectionManager: Manages Redis client connections.

Usage:
    from connections.redis import RedisConnectionManager

    redis_manager = RedisConnectionManager()
    redis_client = redis_manager.get_connection()
    redis_client.set('key', 'value')
    value = redis_client.get('key')

Note:
    This module depends on the redis-py library for Redis interactions.
    Ensure that the library is installed and the Redis server is accessible.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

import logging
from typing import Optional

import redis
from redis.exceptions import RedisError

from config import config
from config.models import RedisConfig

from .base import IConnectionManager, SingletonMeta

# Set up logging
logger = logging.getLogger(__name__)


class RedisConnectionManager(IConnectionManager, metaclass=SingletonMeta):
    """
    Redis Connection Manager

    This class manages the lifecycle of a Redis client connection.
    It implements the IConnectionManager interface, providing connect and close_connection methods.

    Attributes:
        client (Optional[redis.Redis]): The Redis client instance.

    Methods:
        connect: Establishes a connection to Redis and returns a Redis client.
        get_connection: Retrieves the Redis client connection.
        close_connection: Closes the Redis client connection.
    """

    def __init__(self, config: Optional[RedisConfig] = None):
        """
        Initialize the RedisConnectionManager.

        Args:
            config (Optional[RedisConfig]): Configuration for Redis connection.
                If None, configuration is loaded from the application's config.
        """
        self.config = config or config.redis
        self.client: Optional[redis.Redis] = None

    def connect(self) -> redis.Redis:
        """
        Establish a connection to Redis.

        Returns:
            redis.Redis: A connected Redis client instance.

        Raises:
            ConnectionError: If unable to connect to Redis.
        """
        if self.client is None:
            try:
                self.client = redis.Redis(
                    host=self.config.host,
                    port=self.config.port,
                    db=self.config.db,
                    password=self.config.password,
                )
                # Ping the server to ensure the connection is established
                self.client.ping()
                logger.info(
                    f"Connected to Redis: {self.config.host}:{self.config.port}"
                )
            except RedisError as e:
                logger.error(f"Failed to connect to Redis: {str(e)}")
                raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
        return self.client

    def get_connection(self) -> redis.Redis:
        """
        Get the Redis client connection.

        Returns:
            redis.Redis: The Redis client instance.
        """
        if self.client is None:
            logger.info("Creating a new Redis client instance.")
            self.client = self.connect()
            logger.info("Redis connection established successfully.")
        return self.client

    def close_connection(self) -> None:
        """
        Close the Redis client connection.

        Closes the Redis client instance if it exists and sets it to None.

        Logs any exceptions that occur during disconnection.
        """
        if self.client:
            try:
                self.client.close()
                logger.info("Closed Redis connection.")
            except RedisError as e:
                logger.error(f"Error while closing Redis connection: {str(e)}")
            finally:
                self.client = None
