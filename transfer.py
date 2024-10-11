import logging
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import UpdateOne, DeleteOne
from pymongo.errors import BulkWriteError
from config import config
from connections.mongo import MongoConnectionManager

def process_batch(batch, dest_collection, source_collection):
    try:
        # Write to destination collection
        result = dest_collection.bulk_write(batch['dest'], ordered=False)
        transferred = result.upserted_count + result.modified_count

        # If transfer successful, delete from source collection
        if transferred > 0:
            source_collection.bulk_write(batch['source'], ordered=False)

        return transferred
    except BulkWriteError as bwe:
        logging.error(f"Bulk write error: {bwe.details}")
        return 0
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return 0

def transfer_documents(source_collection, dest_collection, batch_size=10):
    total_documents = 0
    start_time = datetime.now()

    try:
        cursor = source_collection.find({})
        batch = {'dest': [], 'source': []}

        while True:
            try:
                for _ in range(batch_size):
                    doc = next(cursor)
                    batch['dest'].append(UpdateOne({'_id': doc['_id']}, {'$set': doc}, upsert=True))
                    batch['source'].append(DeleteOne({'_id': doc['_id']}))
            except StopIteration:
                pass  # No more documents to process

            if batch['dest']:
                total_documents += process_batch(batch, dest_collection, source_collection)
                logging.info(f"Transferred and deleted {total_documents} documents so far...")
                batch = {'dest': [], 'source': []}  # Clear the batch for the next iteration
            else:
                break  # No more documents to process

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logging.info(f"Total documents transferred and deleted: {total_documents}")
    logging.info(f"Time taken: {duration:.2f} seconds")

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set up MongoDB connection
    mongo_connection = MongoConnectionManager(config)
    mongo_client = mongo_connection.get_connection()
    logging.info("MongoDB connection established.")

    try:
        # Specify database and collections
        db_name = "prod_annotator"
        collection_source_name = "prod_face_clean_old"
        collection_dest_name = "prod_face_clean"

        # Get database and collections
        db = mongo_client[db_name]
        source_collection = db[collection_source_name]
        dest_collection = db[collection_dest_name]

        # Transfer documents and delete from source
        transfer_documents(source_collection, dest_collection)

    finally:
        # Close MongoDB connection
        mongo_client.close()
        logging.info("MongoDB connection closed.")

if __name__ == "__main__":
    main()