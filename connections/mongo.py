"""
MongoDB Connection Manager Module

This module provides a connection manager for MongoDB, implementing the IConnectionManager interface.
It handles the creation and management of MongoDB client connections.

Classes:
    MongoConnectionManager: Manages MongoDB client connections.

Usage:
    from connections.mongo import MongoConnectionManager

    with MongoConnectionManager() as mongo_client:
        db = mongo_client.get_database()
        collection = mongo_client.get_collection()
        collection.insert_one({'key': 'value'})

Note:
    This module depends on the pymongo library for MongoDB interactions.
    Ensure that the library is installed and the MongoDB server is accessible.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

import logging
from typing import Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from config import config

from .base import IConnectionManager, SingletonMeta

# Set up logging
logger = logging.getLogger(__name__)


class MongoConnectionManager(IConnectionManager, metaclass=SingletonMeta):
    """
    MongoDB Connection Manager

    This class manages the lifecycle of a MongoDB connection.
    It implements the IConnectionManager interface, providing methods to connect and disconnect.
    """

    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize the MongoConnectionManager with the given configuration.

        Args:
            config (Optional[Dict[str, str]]): Configuration for the MongoDB connection.
                If None, the configuration is loaded from the application's config.
        """
        self.config = config or config.mongo
        self.client: Optional[MongoClient] = None

    def connect(self) -> MongoClient:
        """
        Establish a connection to MongoDB.

        Required configuration fields:
            - uri
            - host
            - port
            - username
            - password

        Returns:
            MongoClient: A MongoDB client connection.

        Raises:
            ValueError: If neither MongoDB URI nor host/port is provided.
            ConnectionFailure: If the connection to MongoDB fails.
        """
        try:
            if self.config.mongo.uri:
                logger.debug("Connecting to MongoDB using URI.")
                client = MongoClient(self.config.mongo.uri)
            elif self.config.host and self.config.port:
                logger.debug("Connecting to MongoDB using host and port.")
                client = MongoClient(
                    host=self.config.host,
                    port=self.config.port,
                    username=self.config.username,
                    password=self.config.password,
                )
            else:
                logger.error("MongoDB URI or host and port must be provided.")
                raise ValueError("MongoDB URI or host and port must be provided.")
            # Attempt a connection to verify
            client.admin.command("ping")
            logger.info("Successfully connected to MongoDB.")
            return client
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_connection(self) -> MongoClient:
        """
        Get the MongoDB client connection.

        Returns:
            MongoClient: The MongoDB client instance.
        """
        if self.client is None:
            logger.info("Creating a new MongoClient instance.")
            self.client = self.connect()
            logger.info("MongoClient connection established successfully.")
        return self.client

    def close_connection(self) -> None:
        """
        Close the MongoDB client connection.
        """
        if self.client is not None:
            logger.info("Closing MongoClient connection.")
            self.client.close()
            self.client = None
            logger.info("MongoClient connection closed successfully.")

    def get_database(self) -> Database:
        """
        Retrieve the specified MongoDB database.

        Required configuration fields:
            - db_name

        Returns:
            Database: The MongoDB database instance.
        """
        db = self.get_connection()[self.config.db_name]
        logger.debug(f"Accessed database: {self.config.db_name}")
        return db

    def get_collection(self) -> Collection:
        """
        Retrieve the specified MongoDB collection.

        Required configuration fields:
            - db_name
            - collection_name

        Returns:
            Collection: The MongoDB collection instance.
        """
        collection = self.get_database()[self.config.collection_name]
        logger.debug(f"Accessed collection: {self.config.collection_name}")
        return collection
