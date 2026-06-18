# from sqlalchemy import create_engine
# from app.config import POSTGRES_URL


# class PostgresAdapter:

#     def __init__(self):

#         self.engine = create_engine(POSTGRES_URL)

#     def insert(self, data):

#         print("Inserted into PostgreSQL")

#         return True

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import POSTGRES_URL


class PostgresAdapter:

    def __init__(self):

        self.engine = create_engine(POSTGRES_URL)

        self.Session = sessionmaker(bind=self.engine)

    def insert(self, data):

        print("PostgreSQL insert")

        return {
            "status": "inserted",
            "database": "postgres"
        }

    def bulk_insert(self, data):

        print("PostgreSQL bulk insert")

        return {
            "status": "bulk_inserted",
            "count": len(data)
        }

    def upsert(self, data):

        print("PostgreSQL upsert")

        return {
            "status": "upserted"
        }

    def transaction(self, operations):

        print("PostgreSQL transaction")

        return {
            "status": "transaction_complete"
        }