"""
Main Application Script

This script serves as the entry point for the application. It demonstrates the usage
of the configuration system and various connection managers to process data from Kafka,
interact with Redis and MongoDB, and simulate other operations.

Usage:
    python main.py

Note:
    Ensure that all required environment variables are set or the appropriate YAML
    configuration file is in place before running this script.

Author:
    Abhik Sarkar <abhik@cloudastructure.com>

Created:
    2024-10-08
"""

import logging
import time
from typing import Dict, Any
import json
from config import config
from connections.kafka import KafkaConsumerManager  
from connections.redis import RedisConnectionManager
from connections.mongo import MongoConnectionManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_message(message: Dict[str, Any]) -> None:
    """
    Process a message received from Kafka.

    This function demonstrates a sample workflow of processing a Kafka message,
    interacting with Redis and MongoDB, and simulating other operations.

    Args:
        message (Dict[str, Any]): The message received from Kafka.
    """
    logger.info(f"Processing message for data identifier: {config.process.data_identifier}")

    # Simulate some processing
    processed_data = {
        "id": message.get("id"),
        "processed_content": f"Processed: {message.get('content', '')}",
        "timestamp": message.get("timestamp")
    }

    # Interact with Redis
    with RedisConnectionManager() as redis_client:
        redis_key = f"{config.process.data_identifier}:{processed_data['id']}"
        redis_client.set(redis_key, json.dumps(processed_data))
        logger.info(f"Stored processed data in Redis with key: {redis_key}")

    # Interact with MongoDB
    with MongoConnectionManager() as mongo_client:
        db = mongo_client[config.mongo.db_name]
        collection = db[config.mongo.collection_name]
        result = collection.insert_one(processed_data)
        logger.info(f"Stored processed data in MongoDB with ID: {result.inserted_id}")

    # Simulate storage operation
    logger.info(f"Would store data in bucket: {config.storage.bucket_name}, folder: {config.storage.folder_name}")

    # Simulate notification
    logger.info(f"Would send notification to endpoint: {config.notification.endpoint}")

def process_kafka_message(message: Any, redis_client: redis.Redis, mongo_client: pymongo.MongoClient) -> None:
    """
    Process a Kafka message, handling errors gracefully.

    Args:
        message (Any): The Kafka message.
    """
    try:
        message_data = json.loads(message.value.decode('utf-8'))
        process_message(message_data)
    except json.JSONDecodeError:
        logger.error(f"Failed to decode message: {message.value}")
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

def main() -> None:
    """
    Main function to run the application.

    This function sets up a Kafka consumer and processes incoming messages.
    It demonstrates the usage of the KafkaConnectionManager as a context manager
    and the application of configuration values.
    """
    logger.info(f"Starting the {config.process.name} application")
    
    kafka_consumer = KafkaConsumerManager(config)

    while True:
        try:
            kafka_consumer         
        except KeyboardInterrupt:
            logger.info("Application stopped by user")
            break
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            logger.info("Retrying connection in 5 seconds...")
            time.sleep(5)  # Wait before retrying to connect to Kafka

    logger.info("Application shutdown complete")

if __name__ == "__main__":
    main()
