"""
Test Configuration Module

This module contains unit tests for the configuration system, including
the Config class and the Pydantic models used for configuration.

Usage:
    pytest test_config.py

Note:
    These tests use pytest fixtures and mocking to simulate different
    environments and configurations.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

import os
from unittest.mock import mock_open, patch

import pytest

from config import Config
from config.models import (AppConfig, KafkaConfig, MongoConfig,
                           NotificationConfig, ProcessConfig, RedisConfig,
                           StorageConfig)


@pytest.fixture
def mock_yaml_config():
    return """
    kafka:
      auto_offset_reset: earliest
    redis:
      db: 0
    mongo:
      collection_name: test_collection
      collection_name_other: other_collection
    storage:
      folder_name: test_folder
    process:
      data_identifier: test
      name: test_process
    """


@pytest.fixture
def mock_env_vars():
    return {
        "KAFKA_BOOTSTRAP_SERVERS": "server1:9092,server2:9092",
        "KAFKA_GROUP_ID": "test_group",
        "KAFKA_TOPIC_NAME": "test_topic1,test_topic2",
        "REDIS_HOST": "redis.test.com",
        "REDIS_PORT": "6380",
        "REDIS_PASSWORD": "test_password",
        "MONGO_URI": "mongodb://test:27017",
        "MONGO_DB_NAME": "test_db",
        "STORAGE_BUCKET_NAME": "test_bucket",
        "NOTIFICATION_ENDPOINT": "https://test.com/notify",
    }


@pytest.fixture
def config_instance(mock_yaml_config, mock_env_vars):
    with patch("builtins.open", mock_open(read_data=mock_yaml_config)):
        with patch.dict(os.environ, mock_env_vars):
            return Config()


def test_config_loading(config_instance):
    assert isinstance(config_instance._config, AppConfig)
    assert isinstance(config_instance.kafka, KafkaConfig)
    assert isinstance(config_instance.redis, RedisConfig)
    assert isinstance(config_instance.mongo, MongoConfig)
    assert isinstance(config_instance.storage, StorageConfig)
    assert isinstance(config_instance.notification, NotificationConfig)
    assert isinstance(config_instance.process, ProcessConfig)


def test_kafka_config(config_instance):
    assert config_instance.kafka.bootstrap_servers == ["server1:9092", "server2:9092"]
    assert config_instance.kafka.group_id == "test_group"
    assert config_instance.kafka.auto_offset_reset == "earliest"
    assert config_instance.kafka.topic_name == ["test_topic1", "test_topic2"]


def test_redis_config(config_instance):
    assert config_instance.redis.host == "redis.test.com"
    assert config_instance.redis.port == 6380
    assert config_instance.redis.db == 0
    assert config_instance.redis.password == "test_password"


def test_mongo_config(config_instance):
    assert config_instance.mongo.uri == "mongodb://test:27017"
    assert config_instance.mongo.db_name == "test_db"
    assert config_instance.mongo.collection_name == "test_collection"
    assert config_instance.mongo.collection_name_other == "other_collection"


def test_storage_config(config_instance):
    assert config_instance.storage.bucket_name == "test_bucket"
    assert config_instance.storage.folder_name == "test_folder"


def test_notification_config(config_instance):
    assert config_instance.notification.endpoint == "https://test.com/notify"


def test_process_config(config_instance):
    assert config_instance.process.data_identifier == "test"
    assert config_instance.process.name == "test_process"


def test_config_precedence(mock_yaml_config):
    env_vars = {"KAFKA_AUTO_OFFSET_RESET": "latest", "PROCESS_NAME": "env_process"}
    with patch("builtins.open", mock_open(read_data=mock_yaml_config)):
        with patch.dict(os.environ, env_vars):
            config = Config()
            assert config.kafka.auto_offset_reset == "latest"
            assert config.process.name == "env_process"
