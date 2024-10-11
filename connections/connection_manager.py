"""
Connection Manager Module 

This module provides a factory for creating connection managers based on the specified connection type.
"""

import logging

from .base import IConnectionManager
from .kafka import KafkaProducerManager
from .mongo import MongoConnectionManager
from .redis import RedisConnectionManager

logger = logging.getLogger(__name__)


class ConnectionFactory:
    """
    Connection Factory Class

    This class provides a method to create connection managers based on the specified connection type.

    Methods:
        create_connection(connection_type: str) -> IConnectionManager:
            Creates and returns a connection manager based on the specified connection type.
    """

    _connection_map = {
        "kafka_producer": KafkaProducerManager,
        # "kafka_consumer": KafkaConsumerManager,
        "redis": RedisConnectionManager,
        "mongo": MongoConnectionManager,
    }

    @staticmethod
    def create_connection(connection_type: str) -> IConnectionManager:
        """
        Create and return a connection manager based on the specified connection type.

        Args:
            connection_type (str): The type of connection to create.

        Returns:
            IConnectionManager: An instance of the connection manager.

        Raises:
            ValueError: If the connection_type is invalid.
        """
        try:
            connection_cls = ConnectionFactory._connection_map[connection_type]
            return connection_cls()
        except KeyError:
            raise ValueError(f"Invalid connection type: {connection_type}")

    @staticmethod
    def get_connection(connection_type: str) -> IConnectionManager:
        """
        Get an existing connection manager based on the specified connection type.

        Args:
            connection_type (str): The type of connection to retrieve.

        Returns:
            IConnectionManager: An instance of the connection manager.

        Raises:
            ValueError: If the connection_type is invalid.
        """
        try:
            connection_cls = ConnectionFactory._connection_map[connection_type]
            return connection_cls()
        except KeyError:
            raise ValueError(f"Invalid connection type: {connection_type}")
