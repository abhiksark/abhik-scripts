"""
Test Kafka Connection Manager Module

This module contains unit tests for the KafkaConnectionManager class.

Usage:
    pytest test_kafka_manager.py

Note:
    These tests use pytest fixtures and mocking to simulate Kafka interactions.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

from unittest.mock import MagicMock, patch

import pytest
from kafka.errors import KafkaError

from config import Config
from connections.kafka import KafkaConnectionManager


@pytest.fixture
def mock_config():
    config = MagicMock(spec=Config)
    config.kafka = MagicMock()
    config.kafka.bootstrap_servers = ["localhost:9092"]
    config.kafka.group_id = "test_group"
    config.kafka.auto_offset_reset = "earliest"
    return config


@pytest.fixture
def kafka_manager(mock_config):
    return KafkaConnectionManager(mock_config)


@patch("connections.kafka.KafkaConsumer")
def test_connect_success(mock_kafka_consumer, kafka_manager):
    connection = kafka_manager.connect()

    mock_kafka_consumer.assert_called_once_with(
        bootstrap_servers=["localhost:9092"],
        group_id="test_group",
        auto_offset_reset="earliest",
    )
    assert connection == mock_kafka_consumer.return_value


@patch("connections.kafka.KafkaConsumer", side_effect=KafkaError("Connection failed"))
def test_connect_failure(mock_kafka_consumer, kafka_manager):
    with pytest.raises(ConnectionError):
        kafka_manager.connect()


@patch("connections.kafka.KafkaConsumer")
def test_disconnect(mock_kafka_consumer, kafka_manager):
    connection = kafka_manager.connect()
    kafka_manager.disconnect()

    connection.close.assert_called_once()
    assert kafka_manager.consumer is None


def test_context_manager(kafka_manager):
    with patch.object(kafka_manager, "connect") as mock_connect:
        with patch.object(kafka_manager, "disconnect") as mock_disconnect:
            with kafka_manager as consumer:
                assert consumer == mock_connect.return_value
            mock_connect.assert_called_once()
            mock_disconnect.assert_called_once()
