from app.adapters.postgres_adapter import PostgresAdapter
from app.adapters.mongo_adapter import MongoAdapter
from app.adapters.redis_adapter import RedisAdapter
from app.adapters.influx_adapter import InfluxAdapter
from app.adapters.neo4j_adapter import Neo4jAdapter


class Executor:

    def get_adapter(self, database):

        if database == "postgres":
            return PostgresAdapter()

        if database == "mongo":
            return MongoAdapter()

        if database == "redis":
            return RedisAdapter()

        if database == "influxdb":
            return InfluxAdapter()

        if database == "neo4j":
            return Neo4jAdapter()

    def execute(
        self,
        database,
        strategy,
        data
    ):

        adapter = self.get_adapter(database)

        return strategy.execute(
            adapter,
            data
        )