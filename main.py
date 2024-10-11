# main.py
"""
Main Application Script
"""
import logging
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId
from config import config
from connections.mongo import MongoConnectionManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def delete_old_documents(mongo_client, db_name, collection_name):
    # Set the cutoff to 30 days ago in milliseconds
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)
    cutoff_millis = int(cutoff_date.timestamp() * 1000)
    logging.info("Cutoff date for deletion: %s (millis: %d)", cutoff_date, cutoff_millis)

    # Access the database and collection
    db = mongo_client[db_name]
    collection = db[collection_name]
    logging.info("Accessing collection: %s in database: %s", collection_name, db_name)

    # Find the approximate starting point for deletion using binary search on start_time_millis
    approximate_id = find_approximate_id_by_millis(collection, cutoff_millis)

    logging.info("Using approximate ObjectId for deletion: %s", approximate_id)

    # Access the database and collection
    db = mongo_client[db_name]
    collection = db[collection_name]
    logging.info("Accessing collection: %s in database: %s", collection_name, db_name)

    # Delete documents in batches for efficiency
    batch_size = 1000
    delete_filter = {"_id": {"$lt": approximate_id}}
    logging.info("Starting deletion process with batch size: %d", batch_size)

    total_deleted = 0
    while True:
        # Find the documents to delete
        docs_to_delete = list(collection.find(delete_filter).sort("_id", 1).limit(batch_size))
        logging.info("Found %d documents to delete in this batch.", len(docs_to_delete))
        
        if not docs_to_delete:
            logging.info("No more documents to delete. Deletion process completed.")
            break

        # Extract the IDs of the documents to delete
        ids_to_delete = [doc["_id"] for doc in docs_to_delete]

        # Delete the batch of documents
        result = collection.delete_many({"_id": {"$in": ids_to_delete}})
        deleted_count = result.deleted_count
        total_deleted += deleted_count
        logging.info("Deleted %d documents in this batch.", deleted_count)

        # if deleted_count < batch_size:
        #     logging.info("Deletion process completed. Total documents deleted: %d", total_deleted)
        #     break

    logging.info("Final total documents deleted: %d", total_deleted)

def find_approximate_id_by_millis(collection, target_millis):
    # Find closest *id for a target start_time_millis using binary search
    lower_bound = collection.find_one(sort=[("_id", 1)])["_id"]
    # Use approximate upper bound for the search
    upper_bound = collection.find_one(sort=[("_id", -1)])["_id"]
    
    logging.info("Finding approximate *id for target millis: %d", target_millis)
    logging.info("Initial lower bound: %s, upper bound: %s", lower_bound, upper_bound)
    logging.info("Performing binary search...")

    i = 0
    while lower_bound < upper_bound and i < 30:
        i += 1
        mid = ObjectId.from_datetime(
            datetime.fromtimestamp((lower_bound.generation_time.timestamp() + upper_bound.generation_time.timestamp()) / 2, tz=timezone.utc)
        )
        logging.info("Mid: %s", mid)
        mid_doc = collection.find_one({"_id": {"$gte": mid}}, sort=[("_id", 1)])
        logging.info("Mid doc id: %s", mid_doc["_id"])
        if not mid_doc:
            upper_bound = mid
            continue
        
        mid_millis = mid_doc.get("start_time_millis")
        
        if mid_millis is None:
            logging.warning("Document %s is missing start_time_millis", mid_doc["_id"])
            lower_bound = mid_doc["_id"]
            continue
        
        if mid_millis < target_millis:
            lower_bound = mid_doc["_id"]
        else:
            upper_bound = mid_doc["_id"]
        
        logging.debug("Current bounds - lower: %s, upper: %s", lower_bound, upper_bound)
    
    logging.info("Binary search completed. Closest *id found: %s", lower_bound)
    return lower_bound

def main():
    # kafka_consumer = KafkaConsumerManager(config)
    # consumer = kafka_consumer.get_connection()

    # Set up MongoDB connection
    mongo_connection = MongoConnectionManager(config)
    mongo_client = mongo_connection.get_connection()
    logging.info("MongoDB connection established.")

    # Delete old documents from the specified database and collection
    db_name = "prod_annotator"
    collection_name = "prod_vehicle"
    delete_old_documents(mongo_client, db_name, collection_name)

if __name__ == "__main__":
    main()