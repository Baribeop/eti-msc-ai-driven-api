# # from pymongo import MongoClient
# # from app.config import MONGO_URL


# # class MongoAdapter:

# #     def __init__(self):

# #         self.client = MongoClient(MONGO_URL)

# #     def insert(self, data):

# #         print("Inserted into MongoDB")

# #         return True


# from pymongo import MongoClient

# from app.config import MONGO_URL


# class MongoAdapter:

#     def __init__(self):

#         self.client = MongoClient(MONGO_URL)

#         self.db = self.client["polyglot"]

#     def insert(self, data):

#         print("Mongo insert")

#         return {
#             "status": "inserted"
#         }

#     def bulk_insert(self, data):

#         print("Mongo bulk insert")

#         return {
#             "status": "bulk_inserted",
#             "count": len(data)
#         }

#     def upsert(self, data):

#         print("Mongo upsert")

#         return {
#             "status": "upserted"
#         }


"""
mongo_adapter.py (CORRECTED)
------------------------------
Same security model as postgres_adapter.py: every method accepts a
`connection` dict supplied by the calling client in the SAME request,
builds a MongoClient from it for the duration of that single call, and
closes it immediately after. No credentials are stored, logged, or
persisted by this middleware.

STORAGE MODE NOTE:
Unlike PostgresAdapter, MongoDB does not require a storage_mode choice.
MongoDB documents are natively schema-flexible: every top-level key in
`data` is stored as its own real, independently queryable BSON field by
default (equivalent in spirit to PostgresAdapter's "typed_columns" mode),
with no flattening or JSON-blob wrapping needed. An ORM/ODM such as
Mongoose or MongoEngine, or the native PyMongo driver, can query any
field directly (e.g. {"amount": {"$gt": 100}}) without any special
configuration on the developer's part. connection["storage_mode"] is
accepted but currently has no effect, reserved for potential future use
(e.g. a "wrapped" mode that nests the payload under a single field for
namespace isolation).

Expected `connection` dict shape:
{
    "type": "mongo",
    "uri": "mongodb://user:password@host:27017",   # OR host/port/user/password below
    "host": "localhost",
    "port": 27017,
    "user": "myuser",            # optional
    "password": "mypassword",    # optional
    "database": "mydb",
    "collection": "my_collection"   # optional, defaults to "polyglot_data"
}
"""

from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)


class MongoAdapter:

    def _build_client(self, connection: dict):
        """Builds a short-lived MongoClient from caller-supplied
        connection details. Supports either a full URI or discrete
        host/port/user/password fields."""
        if connection.get("uri"):
            client = MongoClient(connection["uri"], serverSelectionTimeoutMS=5000)
        else:
            required = ["host", "database"]
            missing = [f for f in required if not connection.get(f)]
            if missing:
                raise ValueError(f"Missing required connection fields: {missing}")

            host = connection["host"]
            port = connection.get("port", 27017)
            user = connection.get("user")
            password = connection.get("password")

            if user and password:
                uri = f"mongodb://{user}:{password}@{host}:{port}/"
            else:
                uri = f"mongodb://{host}:{port}/"
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)

        # Force a connection check now, so failures surface immediately
        # rather than on the first actual operation
        client.admin.command("ping")
        return client

    def insert(self, data, connection: dict = None):
        if connection is None:
            raise ValueError("MongoAdapter.insert() requires a connection dict")

        client = self._build_client(connection)
        try:
            db_name = connection.get("database", "polyglot")
            collection_name = connection.get("collection", "polyglot_data")
            db = client[db_name]
            collection = db[collection_name]

            result = collection.insert_one(dict(data))

            logger.info(f"Mongo insert successful: db={db_name}, collection={collection_name}, id={result.inserted_id}")
            return {
                "status": "inserted",
                "database": "mongo",
                "collection": collection_name,
                "id": str(result.inserted_id)
            }
        finally:
            client.close()

    def bulk_insert(self, data: list, connection: dict = None):
        if connection is None:
            raise ValueError("MongoAdapter.bulk_insert() requires a connection dict")

        client = self._build_client(connection)
        try:
            db_name = connection.get("database", "polyglot")
            collection_name = connection.get("collection", "polyglot_data")
            db = client[db_name]
            collection = db[collection_name]

            result = collection.insert_many([dict(item) for item in data])

            logger.info(f"Mongo bulk insert successful: db={db_name}, collection={collection_name}, count={len(result.inserted_ids)}")
            return {
                "status": "bulk_inserted",
                "database": "mongo",
                "collection": collection_name,
                "count": len(result.inserted_ids),
                "ids": [str(i) for i in result.inserted_ids]
            }
        finally:
            client.close()

    def upsert(self, data, connection: dict = None, key_field: str = "_id"):
        if connection is None:
            raise ValueError("MongoAdapter.upsert() requires a connection dict")

        client = self._build_client(connection)
        try:
            db_name = connection.get("database", "polyglot")
            collection_name = connection.get("collection", "polyglot_data")
            db = client[db_name]
            collection = db[collection_name]

            data_dict = dict(data)
            key_value = data_dict.get(key_field)

            if key_value is not None:
                result = collection.update_one(
                    {key_field: key_value},
                    {"$set": data_dict},
                    upsert=True
                )
                action = "updated" if result.matched_count > 0 else "inserted"
                return {
                    "status": "upserted",
                    "database": "mongo",
                    "action": action,
                    "id": str(result.upserted_id) if result.upserted_id else key_value
                }
            else:
                result = collection.insert_one(data_dict)
                return {
                    "status": "upserted",
                    "database": "mongo",
                    "action": "inserted",
                    "id": str(result.inserted_id)
                }
        finally:
            client.close()
