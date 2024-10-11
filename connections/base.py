"""
Base Connection Management Module
=================================

This module defines the base classes and interfaces used in the construction of
connection managers for various services (like Kafka, Redis, etc.).

It provides a foundation for implementing connection management in a standardized
and consistent manner across different types of connections.

Classes:
    IConnectionManager: An abstract base class (ABC) for all connection managers.
    SingletonMeta: A metaclass for implementing the Singleton design pattern.

The IConnectionManager class defines a standard interface for connection managers,
ensuring that all derived classes implement the required methods.

The SingletonMeta metaclass ensures that only one instance of a connection manager
is created, following the Singleton design pattern. This is useful for managing
resources like database connections or API clients where a single instance is sufficient.

Usage:
    This module is intended to be used as a base for creating specific connection
    manager classes in the ml_api_process package. It is not intended to be used
    directly in application code.

Example:
    class KafkaConnectionManager(IConnectionManager, metaclass=SingletonMeta):
        # Implementation of a Kafka connection manager

Dependencies:
    - abc: Python's built-in module for creating abstract base classes.


Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08

Copyright 2024 Cloudastructure Inc. All rights reserved.

"""

import logging
import threading
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict, List, Type

logger = logging.getLogger(__name__)


class IConnectionManager(ABC, metaclass=ABCMeta):
    @abstractmethod
    def get_connection(self) -> Any:
        """
        Abstract method to be implemented by concrete connection managers. This method
        should return a connection object.

        Returns:
            Any: The connection object provided by the concrete implementation.
        """
        pass

    def _raise_key_not_exists(self, list_keys: List[str]) -> None:
        """
        Checks if a given list of keys is present in
        config.json file.

        Raises an Exception if not .

        Args:
            list_keys (List[str]): List of keys to check.

        Exceptions:
            Exception: If any of the keys is not present in config.json file.

        """

        for key in list_keys:
            if key not in self._config_data:
                raise KeyError(f"{key} is not there in config.json file.")


class SingletonMeta(ABCMeta):
    _instances: Dict[Type, "SingletonMeta"] = {}
    _lock: threading.Lock = threading.Lock()  # Lock for thread safety

    def __call__(cls, *args, **kwargs) -> "SingletonMeta":
        """
        Call method that ensures only one instance of the class is created, following
        the Singleton design pattern.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            SingletonMeta: A single instance of the class.
        """
        if cls not in cls._instances:
            with cls._lock:
                if (
                    cls not in cls._instances
                ):  # Check again to avoid race condition, Why?
                    logger.info(f"Creating new instance of {cls.__name__}")
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]
