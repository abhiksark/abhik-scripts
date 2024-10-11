# config/base_config.py

"""
Pythonic Base Configuration Module

This module provides a flexible and readable configuration system that loads
constant settings from YAML files and environment-specific information from
environment variables or .env files.

Classes:
    Config: A Pythonic configuration class that manages application settings.

Usage:
    from config import config

    # Access configuration values
    kafka_bootstrap_servers = config.kafka.bootstrap_servers

Note:
    This module requires pyyaml, pydantic, and python-dotenv.

Author:
    Your Name <your.email@example.com>

Created:
    2023-05-26
"""

import os
from typing import Any, Dict

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Import your Pydantic models here
from .models import (AppConfig, KafkaConfig, MongoConfig, NotificationConfig,
                     ProcessConfig, RedisConfig, StorageConfig)


class Config:
    """
    A Pythonic configuration class that manages application settings.

    This class provides an intuitive way to access configuration settings,
    combining data from YAML files and environment variables.
    """

    def __init__(self):
        self._config = self._load_config()

    def _load_config(self) -> AppConfig:
        """Load and combine configuration from YAML and environment variables."""
        yaml_config = self._load_yaml_config()
        env_config = self._load_env_config()
        combined_config = self._combine_configs(yaml_config, env_config)
        return AppConfig(**combined_config)

    def _load_yaml_config(self) -> Dict[str, Any]:
        """Load configuration from the appropriate YAML file."""
        env = os.getenv("ENV", "qa").lower()
        config_path = os.path.join(os.path.dirname(__file__), f"{env}.yaml")
        with open(config_path, "r") as config_file:
            return yaml.safe_load(config_file)

    def _load_env_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        env_config = {
            "kafka": self._load_kafka_env(),
            "redis": self._load_redis_env(),
            "mongo": self._load_mongo_env(),
            "storage": self._load_storage_env(),
            "notification": self._load_notification_env(),
            "process": self._load_process_env(),
        }
        return {k: v for k, v in env_config.items() if v}  # Remove empty dicts

    def _load_kafka_env(self) -> Dict[str, Any]:
        return {
            "bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "").split(","),
            "group_id": os.getenv("KAFKA_GROUP_ID"),
            "topic_name": os.getenv("KAFKA_TOPIC_NAME", ""),
            "sasl_plain_username": os.getenv("KAFKA_USER_NAME", ""),
            "sasl_plain_password": os.getenv("KAFKA_PASSWORD", ""),
            # "max_poll_interval_ms": 150_000,
            # "max_poll_records": 5,
            # "session_timeout_ms": 75_000,
            # "scram_sha_512": "SCRAM-SHA-512",
            "sasl_plaintext": "SASL_PLAINTEXT",
        }

    def _load_redis_env(self) -> Dict[str, Any]:
        return {
            "host": os.getenv("REDIS_HOST"),
            "port": os.getenv("REDIS_PORT"),
            "password": os.getenv("REDIS_PASSWORD"),
        }

    def _load_mongo_env(self) -> Dict[str, Any]:
        return {
            "uri": os.getenv("MONGO_URI"),
            "db_name": os.getenv("MONGO_DB_NAME"),
        }

    def _load_storage_env(self) -> Dict[str, Any]:
        return {"bucket_name": os.getenv("STORAGE_BUCKET_NAME")}

    def _load_notification_env(self) -> Dict[str, Any]:
        return {"endpoint": os.getenv("NOTIFICATION_ENDPOINT")}

    def _load_process_env(self) -> Dict[str, Any]:
        return {
            "data_identifier": os.getenv("PROCESS_DATA_IDENTIFIER"),
            "name": os.getenv("PROCESS_NAME"),
        }

    @staticmethod
    def _combine_configs(
        yaml_config: Dict[str, Any], env_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine YAML and environment configurations, with environment taking precedence."""
        combined = yaml_config.copy()
        for key, value in env_config.items():
            if key in combined:
                combined[key].update({k: v for k, v in value.items() if v is not None})
            else:
                combined[key] = value
        return combined

    def __getattr__(self, key: str) -> Any:
        """Provide attribute-style access to configuration values."""
        return getattr(self._config, key)


# Create a global instance of the Config class
config = Config()
print(config.dict())
