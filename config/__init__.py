# config/__init__.py

"""
Configuration Package

This package provides access to the application's configuration settings.
It exports the global config object, which can be used throughout the application
to access configuration values.

Usage:
    from config import config

    # Access configuration values
    kafka_servers = config.kafka.bootstrap_servers

Note:
    The actual configuration is loaded based on the ENV environment variable.
    If ENV is not set, it defaults to 'qa'.

Author:
    Your Name <your.email@example.com>

Created:
    2023-05-26
"""

from .base_config import Config

# Create a global instance of the Config class
config = Config()

# Export the config object
__all__ = ["config"]
