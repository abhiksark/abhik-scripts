"""
Test MongoDB Connection Manager Module

This module contains unit tests for the MongoConnectionManager class.
It ensures that the connection manager correctly handles connections,
disconnections, and error scenarios when interacting with MongoDB.

Classes:
    TestMongoConnectionManager: Test cases for the MongoConnectionManager class.

Usage:
    pytest tests/test_mongo_manager.py

Note:
    These tests use pytest fixtures and mocking to simulate MongoDB interactions.
    Ensure that pytest and pytest-mock are installed in your development environment.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

from unittest.mock import MagicMock, patch

import pytest
from pymongo.errors import ConnectionFailure

from config import config
from connections.mongo import MongoConnectionManager


@pytest.fixture
def mongo_manager():
    """
    Fixture to create a MongoConnectionManager instance for each test.
    """
    return MongoConnectionManager()


@patch("connections.mongo.MongoClient")
def test_connect_success(mock_mongo_client, mongo_manager):
    """
    Test successful connection to MongoDB.

    This test ensures that the connect method correctly initializes
    a MongoClient with the right configuration and performs a ping.
    """
    connection = mongo_manager.connect()

    mock_mongo_client.assert_called_once_with(config.mongo.uri)
    mock_mongo_client.return_value.admin.command.assert_called_once_with("ping")
    assert connection == mock_mongo_client.return_value
    assert mongo_manager.client == mock_mongo_client.return_value


@patch(
    "connections.mongo.MongoClient", side_effect=ConnectionFailure("Connection failed")
)
def test_connect_failure(mock_mongo_client, mongo_manager):
    """
    Test MongoDB connection failure.

    This test ensures that the connect method raises a ConnectionError
    when MongoClient initialization fails.
    """
    with pytest.raises(ConnectionError) as excinfo:
        mongo_manager.connect()
    assert "Failed to connect to MongoDB" in str(excinfo.value)
    assert mongo_manager.client is None


@patch("connections.mongo.MongoClient")
def test_disconnect_success(mock_mongo_client, mongo_manager):
    """
    Test successful disconnection from MongoDB.

    This test ensures that the disconnect method correctly closes
    the MongoClient and resets the client attribute.
    """
    connection = mongo_manager.connect()
    mongo_manager.disconnect()

    connection.close.assert_called_once()
    assert mongo_manager.client is None


@patch("connections.mongo.MongoClient")
def test_disconnect_with_error(mock_mongo_client, mongo_manager):
    """
    Test disconnection when an error occurs.

    This test ensures that the disconnect method handles errors during
    disconnection gracefully and still resets the client attribute.
    """
    connection = mongo_manager.connect()
    connection.close.side_effect = Exception("Disconnection failed")

    mongo_manager.disconnect()

    connection.close.assert_called_once()
    assert mongo_manager.client is None


def test_context_manager():
    """
    Test MongoConnectionManager as a context manager.

    This test ensures that the MongoConnectionManager can be used
    as a context manager, connecting on enter and disconnecting on exit.
    """
    with patch("connections.mongo.MongoClient") as mock_mongo_client:
        with MongoConnectionManager() as client:
            assert client == mock_mongo_client.return_value
        mock_mongo_client.return_value.close.assert_called_once()


@patch("connections.mongo.MongoClient")
def test_multiple_connections(mock_mongo_client, mongo_manager):
    """
    Test multiple connection attempts.

    This test ensures that multiple calls to connect() reuse the same
    MongoClient instance instead of creating new ones.
    """
    connection1 = mongo_manager.connect()
    connection2 = mongo_manager.connect()

    assert mock_mongo_client.call_count == 1
    assert connection1 == connection2


# Add more specific tests for edge cases or specific MongoDB scenarios as needed
