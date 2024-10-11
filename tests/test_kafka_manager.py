"""
Test Kafka Connection Manager Module

This module contains unit tests for the KafkaConnectionManager class.
It ensures that the connection manager correctly handles connections,
disconnections, and error scenarios when interacting with Kafka.

Classes:
    TestKafkaConnectionManager: Test cases for the KafkaConnectionManager class.

Usage:
    pytest tests/test_kafka_manager.py

Note:
    These tests use pytest fixtures and mocking to simulate Kafka interactions.
    Ensure that pytest and pytest-mock are installed in your development environment.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

from unittest.mock import MagicMock, patch

import pytest
from kafka.errors import KafkaError

from config import Config, config
from connections.kafka import KafkaConnectionManager


@pytest.fixture
def kafka_manager():
    """
    Fixture to create a KafkaConnectionManager instance for each test.
    """
    return KafkaConnectionManager()


@patch("connections.kafka.KafkaConsumer")
def test_connect_success(mock_kafka_consumer, kafka_manager):
    """
    Test successful connection to Kafka.

    This test ensures that the connect method correctly initializes
    a KafkaConsumer with the right configuration.
    """
    connection = kafka_manager.connect()

    mock_kafka_consumer.assert_called_once_with(
        bootstrap_servers=config.kafka.bootstrap_servers,
        group_id=config.kafka.group_id,
        auto_offset_reset=config.kafka.auto_offset_reset,
    )
    assert connection == mock_kafka_consumer.return_value
    assert kafka_manager.consumer == mock_kafka_consumer.return_value


@patch("connections.kafka.KafkaConsumer", side_effect=KafkaError("Connection failed"))
def test_connect_failure(mock_kafka_consumer, kafka_manager):
    """
    Test Kafka connection failure.

    This test ensures that the connect method raises a ConnectionError
    when KafkaConsumer initialization fails.
    """
    with pytest.raises(ConnectionError) as excinfo:
        kafka_manager.connect()
    assert "Failed to connect to Kafka" in str(excinfo.value)
    assert kafka_manager.consumer is None


@patch("connections.kafka.KafkaConsumer")
def test_disconnect_success(mock_kafka_consumer, kafka_manager):
    """
    Test successful disconnection from Kafka.

    This test ensures that the disconnect method correctly closes
    the KafkaConsumer and resets the consumer attribute.
    """
    connection = kafka_manager.connect()
    kafka_manager.disconnect()

    connection.close.assert_called_once()
    assert kafka_manager.consumer is None


@patch("connections.kafka.KafkaConsumer")
def test_disconnect_with_error(mock_kafka_consumer, kafka_manager):
    """
    Test disconnection when an error occurs.

    This test ensures that the disconnect method handles errors during
    disconnection gracefully and still resets the consumer attribute.
    """
    connection = kafka_manager.connect()
    connection.close.side_effect = KafkaError("Disconnection failed")

    kafka_manager.disconnect()

    connection.close.assert_called_once()
    assert kafka_manager.consumer is None


def test_context_manager():
    """
    Test KafkaConnectionManager as a context manager.

    This test ensures that the KafkaConnectionManager can be used
    as a context manager, connecting on enter and disconnecting on exit.
    """
    with patch("connections.kafka.KafkaConsumer") as mock_kafka_consumer:
        with KafkaConnectionManager() as consumer:
            assert consumer == mock_kafka_consumer.return_value
        mock_kafka_consumer.return_value.close.assert_called_once()


@patch("connections.kafka.KafkaConsumer")
def test_multiple_connections(mock_kafka_consumer, kafka_manager):
    """
    Test multiple connection attempts.

    This test ensures that multiple calls to connect() reuse the same
    KafkaConsumer instance instead of creating new ones.
    """
    connection1 = kafka_manager.connect()
    connection2 = kafka_manager.connect()

    assert mock_kafka_consumer.call_count == 1
    assert connection1 == connection2


# Add more specific tests for edge cases or specific Kafka scenarios as needed
