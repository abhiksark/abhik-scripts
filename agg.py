import logging
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId
from config import config
from connections.mongo import MongoConnectionManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to MongoDB
mongo_connection = MongoConnectionManager(config)
mongo_client = mongo_connection.get_connection()
logging.info("MongoDB connection established.")
db = mongo_client['prod_archive']
source_collection = db['prod_tagger_archive_jul_w3_new']
result_collection = db['aggregation_results']

pipeline = [
    # Step 1: Add time interval
    {
        "$addFields": {
            "interval": {
                "$floor": {
                    "$divide": [{"$hour": "$timestamp"}, 3]
                }
            }
        }
    },

    # Step 2: Match for the specific date (example: July 16, 2024)
    {
        "$match": {
            "day": 16,
            "month": 7,
            "year": 2024
        }
    },

    # Step 3: Unwind results and values
    {"$unwind": "$results"},
    {"$unwind": "$results.values"},

    # Step 4: Group by unique identifiers and calculate statistics
    {
        "$group": {
            "_id": {
                "day": "$day",
                "month": "$month",
                "year": "$year",
                "camera_id": "$camera_id",
                "account_id": "$account_id",
                "interval": "$interval",
                "class_name": "$results.values.class_name"
            },
            "confidences": {"$push": "$results.values.confidence"},
            "detection_count": {"$sum": 1},
            "frame_ids": {"$addToSet": "$frame_id"},
            "avg_confidence": {"$avg": "$results.values.confidence"},
            "min_confidence": {"$min": "$results.values.confidence"},
            "max_confidence": {"$max": "$results.values.confidence"}
        }
    },

    # Step 5: Group results by interval
    {
        "$group": {
            "_id": {
                "day": "$_id.day",
                "month": "$_id.month",
                "year": "$_id.year",
                "camera_id": "$_id.camera_id",
                "account_id": "$_id.account_id",
                "interval": "$_id.interval"
            },
            "total_interval_detections": {"$sum": "$detection_count"},
            "total_interval_frames": {"$sum": {"$size": "$frame_ids"}},
            "results": {
                "$push": {
                    "class_name": "$_id.class_name",
                    "average_confidence": "$avg_confidence",
                    "min_confidence": "$min_confidence",
                    "max_confidence": "$max_confidence",
                    "detection_count": "$detection_count"
                }
            }
        }
    },

    # Step 6: Group by date and calculate overall statistics
    {
        "$group": {
            "_id": {
                "day": "$_id.day",
                "month": "$_id.month",
                "year": "$_id.year",
                "camera_id": "$_id.camera_id",
                "account_id": "$_id.account_id"
            },
            "total_detections": {"$sum": "$total_interval_detections"},
            "total_frames": {"$sum": "$total_interval_frames"},
            "intervals": {
                "$push": {
                    "start_hour": {"$multiply": ["$_id.interval", 3]},
                    "end_hour": {"$multiply": [{"$add": ["$_id.interval", 1]}, 3]},
                    "total_interval_detections": "$total_interval_detections",
                    "total_interval_frames": "$total_interval_frames",
                    "results": "$results"
                }
            }
        }
    },

    # Step 7: Calculate overall class statistics
    {
        "$addFields": {
            "overall_results": {
                "$reduce": {
                    "input": "$intervals",
                    "initialValue": [],
                    "in": {"$concatArrays": ["$$value", "$$this.results"]}
                }
            }
        }
    },
    {
        "$addFields": {
            "overall_results": {
                "$map": {
                    "input": {
                        "$setUnion": {
                            "$map": {
                                "input": "$overall_results",
                                "as": "result",
                                "in": "$$result.class_name"
                            }
                        }
                    },
                    "as": "class_name",
                    "in": {
                        "$let": {
                            "vars": {
                                "class_data": {
                                    "$filter": {
                                        "input": "$overall_results",
                                        "as": "result",
                                        "cond": {"$eq": ["$$result.class_name", "$$class_name"]}
                                    }
                                }
                            },
                            "in": {
                                "class_name": "$$class_name",
                                "average_confidence": {"$avg": "$$class_data.average_confidence"},
                                "min_confidence": {"$min": "$$class_data.min_confidence"},
                                "max_confidence": {"$max": "$$class_data.max_confidence"},
                                "total_detections": {"$sum": "$$class_data.detection_count"}
                            }
                        }
                    }
                }
            }
        }
    },

    # Step 8: Format final output
    {
        "$project": {
            "_id": 0,
            "day": "$_id.day",
            "month": "$_id.month",
            "year": "$_id.year",
            "camera_id": "$_id.camera_id",
            "account_id": "$_id.account_id",
            "total_detections": 1,
            "total_frames": 1,
            "overall_results": 1,
            "intervals": 1
        }
    },

    # Step 9: Sort the results
    {
        "$sort": {
            "year": 1,
            "month": 1,
            "day": 1,
            "camera_id": 1,
            "account_id": 1
        }
    }
]

# Execute the aggregation pipeline
results = source_collection.aggregate(pipeline, allowDiskUse=True)

# Save results to a new collection
for result in results:
    result_collection.insert_one(result)

print("Aggregation completed and results saved to the 'aggregation_results' collection.")