# from pymongo import MongoClient
# from app.config import MONGO_URL


# class MongoAdapter:

#     def __init__(self):

#         self.client = MongoClient(MONGO_URL)

#     def insert(self, data):

#         print("Inserted into MongoDB")

#         return True


from pymongo import MongoClient

from app.config import MONGO_URL


class MongoAdapter:

    def __init__(self):

        self.client = MongoClient(MONGO_URL)

        self.db = self.client["polyglot"]

    def insert(self, data):

        print("Mongo insert")

        return {
            "status": "inserted"
        }

    def bulk_insert(self, data):

        print("Mongo bulk insert")

        return {
            "status": "bulk_inserted",
            "count": len(data)
        }

    def upsert(self, data):

        print("Mongo upsert")

        return {
            "status": "upserted"
        }