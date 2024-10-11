"""
Test Redis Connection Manager Module

This module contains unit tests for the RedisConnectionManager class.

Usage:
    pytest test_redis_connection_manager.py

Note:
    These tests use pytest fixtures and mocking to simulate Redis interactions.
    Ensure that pytest and pytest-mock are installed in your development environment.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-09
"""

import logging
from unittest.mock import MagicMock, patch

import pytest
from redis.exceptions import RedisError

from config import config  # Assuming this is how you import your config
from connections.redis import RedisConnectionManager


@pytest.fixture
def mock_redis_config():
    """Fixture to provide a mock Redis configuration."""
    config.redis = MagicMock()
    config.redis.host = "localhost"
    config.redis.port = 6379
    config.redis.db = 0
    return config


@pytest.fixture
def redis_manager(mock_redis_config):
    """Fixture to create a RedisConnectionManager instance."""
    return RedisConnectionManager()


def test_init(redis_manager):
    """Test the initialization of RedisConnectionManager."""
    assert redis_manager.client is None


@patch("redis.Redis")
def test_connect_success(mock_redis, redis_manager, mock_redis_config):
    """Test successful connection to Redis."""
    mock_client = MagicMock()
    mock_redis.return_value = mock_client

    client = redis_manager.connect()

    mock_redis.assert_called_once_with(
        host=mock_redis_config.redis.host,
        port=mock_redis_config.redis.port,
        db=mock_redis_config.redis.db,
    )
    mock_client.ping.assert_called_once()
    assert client == mock_client
    assert redis_manager.client == mock_client


@patch("redis.Redis")
def test_connect_failure(mock_redis, redis_manager):
    """Test connection failure to Redis."""
    mock_redis.side_effect = RedisError("Connection failed")

    with pytest.raises(ConnectionError) as exc_info:
        redis_manager.connect()

    assert "Failed to connect to Redis" in str(exc_info.value)
    assert redis_manager.client is None


@patch("redis.Redis")
def test_disconnect(mock_redis, redis_manager):
    """Test disconnection from Redis."""
    mock_client = MagicMock()
    mock_redis.return_value = mock_client

    redis_manager.connect()
    redis_manager.disconnect()

    mock_client.close.assert_called_once()
    assert redis_manager.client is None


@patch("redis.Redis")
def test_disconnect_with_error(mock_redis, redis_manager):
    """Test disconnection from Redis when an error occurs."""
    mock_client = MagicMock()
    mock_redis.return_value = mock_client
    mock_client.close.side_effect = RedisError("Disconnection failed")

    redis_manager.connect()
    redis_manager.disconnect()

    mock_client.close.assert_called_once()
    assert redis_manager.client is None


@patch("redis.Redis")
def test_context_manager(mock_redis, redis_manager):
    """Test the RedisConnectionManager as a context manager."""
    mock_client = MagicMock()
    mock_redis.return_value = mock_client

    with redis_manager as client:
        assert client == mock_client
        assert redis_manager.client == mock_client

    mock_client.close.assert_called_once()
    assert redis_manager.client is None


@patch("redis.Redis")
def test_multiple_connections(mock_redis, redis_manager):
    """Test that multiple calls to connect() reuse the same client."""
    mock_client = MagicMock()
    mock_redis.return_value = mock_client

    client1 = redis_manager.connect()
    client2 = redis_manager.connect()

    assert mock_redis.call_count == 1
    assert client1 == client2


@patch("redis.Redis")
def test_logging(mock_redis, redis_manager, caplog):
    """Test that proper logging occurs during connection and disconnection."""
    mock_client = MagicMock()
    mock_redis.return_value = mock_client

    with caplog.at_level(logging.INFO):
        redis_manager.connect()
        assert "Connected to Redis" in caplog.text

        redis_manager.disconnect()
        assert "Closed Redis connection" in caplog.text


@patch("redis.Redis")
def test_error_logging(mock_redis, redis_manager, caplog):
    """Test that errors are properly logged."""
    mock_redis.side_effect = RedisError("Test error")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ConnectionError):
            redis_manager.connect()
        assert "Failed to connect to Redis: Test error" in caplog.text
