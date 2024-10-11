# connections/kafka.py

"""
Kafka Connection Manager Module

This module provides connection managers for Kafka, implementing the IConnectionManager interface.
It handles the creation and management of Kafka consumer and producer connections.

Classes:
    KafkaConsumerManager: Manages Kafka consumer connections.
    KafkaProducerManager: Manages Kafka producer connections.

Usage:
    from connections.kafka import KafkaConsumerManager, KafkaProducerManager

    # Example usage of KafkaConsumerManager
    consumer_manager = KafkaConsumerManager()
    consumer = consumer_manager.get_connection()
    consumer.subscribe(["topic1", "topic2"])
    for message in consumer:
        print(message)

    # Example usage of KafkaProducerManager
    producer_manager = KafkaProducerManager()
    producer = producer_manager.get_connection()
    producer.send("topic1", value="Hello, Kafka!")

Note:
    This module depends on the kafka-python library for Kafka interactions.
    Ensure that the library is installed and the Kafka server is accessible.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08

Updated:
    2024-10-09
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from json import dumps, loads
from typing import Dict, Optional

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError

from config import config

from .base import IConnectionManager, SingletonMeta

# Set up logging
logger = logging.getLogger(__name__)


class KafkaConsumerManager(IConnectionManager, metaclass=SingletonMeta):
    """
    Kafka Consumer Connection Manager

    This class manages the lifecycle of a Kafka consumer connection.
    It implements the IConnectionManager interface, providing connect and disconnect methods.
    """

    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize the KafkaConsumerManager with the given configuration.

        Args:
            config (Optional[Dict[str, str]]): Configuration for the Kafka consumer.
                If None, the configuration is loaded from the application's config.
        """
        self.config = config or config.kafka
        self.client: Optional[KafkaConsumer] = None

    def connect(self) -> KafkaConsumer:
        """
        Establish a connection to Kafka as a consumer.

        Required configuration fields:
            - bootstrap_servers
            - sasl_mechanism
            - sasl_plain_username
            - sasl_plain_password

        Returns:
            KafkaConsumer: A Kafka consumer connection.

        Raises:
            ValueError: If required configuration fields are missing.
            KafkaError: If the connection to Kafka fails.
        """
        try:
            logger.debug("Connecting to Kafka as a consumer.")

            consumer = KafkaConsumer(
                self.config.kafka.topic_name,
                bootstrap_servers=self.config.kafka.bootstrap_servers,
                sasl_plain_username=self.config.kafka.sasl_plain_username,
                sasl_plain_password=self.config.kafka.sasl_plain_password,
                value_deserializer=lambda x: loads(x.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id=self.config.kafka.group_id,
            )
            logger.info("Successfully connected to Kafka as a consumer.")
            return consumer
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka as a consumer: {e}")
            raise

    def get_connection(self) -> KafkaConsumer:
        """
        Get the Kafka consumer connection.

        Returns:
            KafkaConsumer: The Kafka consumer instance.
        """
        if self.client is None:
            logger.info("Creating a new KafkaConsumer instance.")
            self.client = self.connect()
            logger.info("KafkaConsumer connection established successfully.")
        return self.client

    def close_connection(self) -> None:
        """
        Close the Kafka consumer connection.
        """
        if self.client is not None:
            logger.info("Closing KafkaConsumer connection.")
            self.client.close()
            self.client = None
            logger.info("KafkaConsumer connection closed successfully.")


class KafkaProducerManager(IConnectionManager, metaclass=SingletonMeta):
    """
    Kafka Producer Connection Manager

    This class manages the lifecycle of a Kafka producer connection.
    It implements the IConnectionManager interface, providing connect and disconnect methods.

    Attributes:
        thread_pool (ThreadPoolExecutor): Thread pool executor for asynchronous message sending.
    """

    _thread_pool: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=5)

    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize the KafkaProducerManager with the given configuration.

        Args:
            config (Optional[Dict[str, str]]): Configuration for the Kafka producer.
                If None, the configuration is loaded from the application's config.
        """
        self.config = config or config.kafka
        self.client: Optional[KafkaProducer] = None

    def connect(self) -> KafkaProducer:
        """
        Establish a connection to Kafka as a producer.

        Required configuration fields:
            - bootstrap_servers
            - sasl_mechanism
            - sasl_plain_username
            - sasl_plain_password

        Returns:
            KafkaProducer: A Kafka producer connection.

        Raises:
            ValueError: If required configuration fields are missing.
            KafkaError: If the connection to Kafka fails.
        """
        try:
            logger.debug("Connecting to Kafka as a producer.")
            producer = KafkaProducer(
                bootstrap_servers=self.config.kafka.bootstrap_servers,
                sasl_mechanism=self.config.kafka.sasl_mechanism,
                sasl_plain_username=self.config.kafka.sasl_plain_username,
                sasl_plain_password=self.config.kafka.sasl_plain_password,
                value_serializer=lambda x: dumps(x).encode("utf-8"),
            )
            logger.info("Successfully connected to Kafka as a producer.")
            return producer
        except KafkaError as e:
            logger.error(f"Failed to connect to Kafka as a producer: {e}")
            raise

    def get_connection(self) -> KafkaProducer:
        """
        Get the Kafka producer connection.

        Returns:
            KafkaProducer: The Kafka producer instance.
        """
        if self.client is None:
            logger.info("Creating a new KafkaProducer instance.")
            self.client = self.connect()
            logger.info("KafkaProducer connection established successfully.")
        return self.client

    def close_connection(self) -> None:
        """
        Close the Kafka producer connection.
        """
        if self.client is not None:
            logger.info("Closing KafkaProducer connection.")
            self.client.close()
            self.client = None
            logger.info("KafkaProducer connection closed successfully.")
