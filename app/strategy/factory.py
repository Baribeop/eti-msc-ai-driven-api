from app.strategy.relational.insert import RelationalInsert
from app.strategy.relational.bulk_insert import RelationalBulkInsert
from app.strategy.relational.upsert import RelationalUpsert
from app.strategy.relational.transaction import RelationalTransaction

from app.strategy.document.insert import DocumentInsert
from app.strategy.document.bulk_insert import DocumentBulkInsert
from app.strategy.document.upsert import DocumentUpsert

from app.strategy.cache.set import CacheSet
from app.strategy.cache.expire import CacheExpire

# check thsi again , use of pipeline seams to conflict with the na
from app.strategy.cache.pipe import CachePipeline

from app.strategy.timeseries.write_point import TimeSeriesWrite
from app.strategy.timeseries.batch_write import TimeSeriesBatchWrite

from app.strategy.graph.create_node import GraphCreateNode
from app.strategy.graph.create_edge import GraphCreateEdge


def get_strategy(database, features):

    # BULK OPERATIONS
    if features["is_bulk"]:

        if database == "postgres":
            return RelationalBulkInsert()

        if database == "mongo":
            return DocumentBulkInsert()

        if database == "redis":
            return CachePipeline()

        if database == "influxdb":
            return TimeSeriesBatchWrite()

    # UPSERT OPERATIONS
    if features["has_identifier"]:

        if database == "postgres":
            return RelationalUpsert()

        if database == "mongo":
            return DocumentUpsert()

    # TRANSACTIONAL
    if (
        database == "postgres"
        and features["transactional_score"] >= 8
    ):
        return RelationalTransaction()

    # CACHE
    if database == "redis":

        if "expires" in features.get("keys", []):
            return CacheExpire()

        return CacheSet()

    # GRAPH
    if database == "neo4j":

        if features["relationship_score"] >= 7:
            return GraphCreateEdge()

        return GraphCreateNode()

    # TIMESERIES
    if database == "influxdb":
        return TimeSeriesWrite()

    # DEFAULTS
    if database == "postgres":
        return RelationalInsert()

    if database == "mongo":
        return DocumentInsert()
    


    