# from neo4j import GraphDatabase

# from app.config import (
#     NEO4J_URL,
#     NEO4J_USER,
#     NEO4J_PASSWORD
# )


# class Neo4jAdapter:

#     def __init__(self):

#         self.driver = GraphDatabase.driver(
#             NEO4J_URL,
#             auth=(
#                 NEO4J_USER,
#                 NEO4J_PASSWORD
#             )
#         )

#     def create_node(self, data):

#         print("Neo4j node created")

#         return {
#             "status": "node_created"
#         }

#     def create_edge(self, data):

#         print("Neo4j edge created")

#         return {
#             "status": "edge_created"
#         }
    

"""
neo4j_adapter.py (CORRECTED)
------------------------------
Same security model as the other adapters: every method accepts a
`connection` dict supplied by the calling client in the SAME request,
builds a short-lived Neo4j driver from it, executes the write, and
closes the driver immediately after. No credentials are stored, logged,
or persisted by this middleware.

STORAGE MODEL NOTE:
Neo4j stores labelled nodes with properties, and labelled, directed
relationships (edges) between them. This adapter maps an incoming
payload as follows: create_node() creates a single node, using
connection["label"] (or "PolyglotNode" by default) as the node label,
and all top-level scalar key-value pairs in the payload as node
properties (nested dict/list values are JSON-stringified, since Neo4j
node properties must be primitive types or arrays of primitives).
create_edge() expects the payload to contain "source" and "target" node
identifiers (matched by an "id" property) and creates a relationship of
type connection["relationship_type"] (or "RELATED_TO" by default)
between them, creating the nodes if they do not already exist (MERGE
semantics) to avoid duplicate-node errors on repeated calls.

Expected `connection` dict shape:
{
    "type": "neo4j",
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "mypassword",
    "label": "Person",                    # optional, defaults to "PolyglotNode"
    "relationship_type": "FRIENDS_WITH"   # optional, defaults to "RELATED_TO"
}
"""

from neo4j import GraphDatabase
import json
import logging

logger = logging.getLogger(__name__)


class Neo4jAdapter:

    def _build_driver(self, connection: dict):
        required = ["uri", "user", "password"]
        missing = [f for f in required if not connection.get(f)]
        if missing:
            raise ValueError(f"Missing required connection fields: {missing}")

        driver = GraphDatabase.driver(
            connection["uri"],
            auth=(connection["user"], connection["password"])
        )
        driver.verify_connectivity()  # fail fast if connection details are wrong
        return driver

    def _flatten_properties(self, data: dict) -> dict:
        """Neo4j node/relationship properties must be primitive types
        (or arrays of primitives) - nested dicts/lists are JSON-stringified
        so no payload can fail to be stored, at the cost of losing native
        graph-queryability on those specific nested fields."""
        props = {}
        for key, value in data.items():
            if isinstance(value, (dict,)):
                props[key] = json.dumps(value)
            elif isinstance(value, list) and any(isinstance(v, (dict, list)) for v in value):
                props[key] = json.dumps(value)
            else:
                props[key] = value
        return props

    def insert(self, data, connection: dict = None):
        """Generic entry point matching the other adapters' insert()
        signature, so main.py's /persist handler can call all five
        adapters uniformly. Delegates to create_node()."""
        return self.create_node(data, connection=connection)

    def create_node(self, data, connection: dict = None):
        if connection is None:
            raise ValueError("Neo4jAdapter.create_node() requires a connection dict")

        driver = self._build_driver(connection)
        try:
            label = connection.get("label", "PolyglotNode")
            props = self._flatten_properties(dict(data))

            with driver.session() as session:
                result = session.run(
                    f"CREATE (n:{label} $props) RETURN elementId(n) AS node_id",
                    props=props
                )
                record = result.single()
                node_id = record["node_id"]

            logger.info(f"Neo4j node created: label={label}, id={node_id}")
            return {
                "status": "node_created",
                "database": "neo4j",
                "label": label,
                "id": node_id
            }
        finally:
            driver.close()

    def create_edge(self, data, connection: dict = None):
        """Expects data to contain 'source' and 'target' node identifiers
        (matched against each node's 'id' property). Uses MERGE so
        repeated calls with the same source/target do not create
        duplicate nodes."""
        if connection is None:
            raise ValueError("Neo4jAdapter.create_edge() requires a connection dict")

        data_dict = dict(data)
        if "source" not in data_dict or "target" not in data_dict:
            raise ValueError("create_edge() requires 'source' and 'target' fields in data")

        driver = self._build_driver(connection)
        try:
            label = connection.get("label", "PolyglotNode")
            rel_type = connection.get("relationship_type", "RELATED_TO")
            edge_props = {k: v for k, v in data_dict.items() if k not in ("source", "target")}
            edge_props = self._flatten_properties(edge_props)

            with driver.session() as session:
                result = session.run(
                    f"""
                    MERGE (a:{label} {{id: $source}})
                    MERGE (b:{label} {{id: $target}})
                    CREATE (a)-[r:{rel_type} $props]->(b)
                    RETURN elementId(r) AS edge_id
                    """,
                    source=data_dict["source"],
                    target=data_dict["target"],
                    props=edge_props
                )
                record = result.single()
                edge_id = record["edge_id"]

            logger.info(f"Neo4j edge created: {data_dict['source']}-[{rel_type}]->{data_dict['target']}")
            return {
                "status": "edge_created",
                "database": "neo4j",
                "relationship_type": rel_type,
                "id": edge_id
            }
        finally:
            driver.close()
