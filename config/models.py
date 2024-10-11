# config/models.py

"""
Configuration Models Module

This module defines Pydantic models for various configuration types used in the application.
These models provide type checking, data validation, and default values for configuration settings.

Classes:
    KafkaConfig: Configuration settings for Kafka.
    RedisConfig: Configuration settings for Redis.
    MongoConfig: Configuration settings for MongoDB.
    StorageConfig: Configuration settings for storage.
    NotificationConfig: Configuration settings for notifications.
    ProcessConfig: Configuration settings for the process.
    AppConfig: Overall application configuration, composing all other configs.

Usage:
    from config.models import AppConfig

    # Create a config instance
    config = AppConfig(kafka=KafkaConfig(...), redis=RedisConfig(...), ...)

Note:
    This module requires pydantic to be installed.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class KafkaConfig(BaseModel):
    """Configuration settings for Kafka."""

    bootstrap_servers: List[str] = Field(
        default_factory=list, description="List of Kafka bootstrap servers"
    )
    group_id: str = Field(default="", description="Kafka consumer group ID")
    auto_offset_reset: str = Field(
        default="earliest", description="Auto offset reset strategy"
    )
    topic_name: str = Field(
        default_factory=str, description="List of Kafka topic names"
    )
    session_timeout_ms: int = Field(
        default=75_000, description="Kafka session timeout in milliseconds"
    )
    scram_sha_512: str = Field(
        default="SCRAM-SHA-512", description="Kafka SASL mechanism"
    )
    sasl_plaintext: str = Field(
        default="SASL_PLAINTEXT", description="Kafka SASL plaintext"
    )
    security_protocol: str = Field(
        default="SASL_PLAINTEXT", description="Kafka security protocol"
    )
    max_poll_interval_ms: int = Field(
        default=150_000, description="Kafka max poll interval in milliseconds"
    )
    max_poll_records: int = Field(default=5, description="Kafka max poll records")

    sasl_plain_username: str = Field(
        default="", description="Kafka SASL plain username"
    )
    sasl_plain_password: str = Field(
        default="", description="Kafka SASL plain password"
    )


class RedisConfig(BaseModel):
    """Configuration settings for Redis."""

    host: str = Field(default="localhost", description="Redis server host")
    port: int = Field(default=6379, description="Redis server port")
    db: int = Field(default=0, description="Redis database number")
    password: Optional[str] = Field(default=None, description="Redis password")


class MongoConfig(BaseModel):
    """Configuration settings for MongoDB."""

    uri: str = Field(..., description="MongoDB connection URI")
    db_name: str = Field(..., description="MongoDB database name")
    collection_name: str = Field(..., description="MongoDB collection name")
    collection_name_other: Optional[str] = Field(
        None, description="Secondary MongoDB collection name"
    )


class StorageConfig(BaseModel):
    """Configuration settings for storage."""

    bucket_name: str = Field(..., description="Storage bucket name")
    folder_name: str = Field(..., description="Storage folder name")


class NotificationConfig(BaseModel):
    """Configuration settings for notifications."""

    endpoint: str = Field(..., description="Notification service endpoint URL")


class ProcessConfig(BaseModel):
    """Configuration settings for the process."""

    data_identifier: str = Field(..., description="Data identifier for the process")
    name: str = Field(..., description="Name of the process")


class AppConfig(BaseModel):
    """Overall application configuration, composing all other configs."""

    kafka: KafkaConfig = Field(default_factory=KafkaConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    mongo: MongoConfig = Field(default_factory=MongoConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    notification: NotificationConfig = Field(default_factory=NotificationConfig)
    process: ProcessConfig = Field(default_factory=ProcessConfig)

    class Config:
        """Pydantic config for AppConfig."""

        populate_by_name = True
        arbitrary_types_allowed = True
