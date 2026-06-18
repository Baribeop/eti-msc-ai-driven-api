# rom neo4j import GraphDatabase
# from app.config import (
#     NEO4J_URL,
#     NEO4J_USER,
#     NEO4J_PASSWORD
# )


# class Neo4jAdapter:

#     def __init__(self):

#         self.driver = GraphDatabase.driver(
#             NEO4J_URL,
#             auth=(NEO4J_USER, NEO4J_PASSWORD)
#         )

#     def insert(self, data):

#         print("Stored in Neo4j")

#         return True


from neo4j import GraphDatabase

from app.config import (
    NEO4J_URL,
    NEO4J_USER,
    NEO4J_PASSWORD
)


class Neo4jAdapter:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            NEO4J_URL,
            auth=(
                NEO4J_USER,
                NEO4J_PASSWORD
            )
        )

    def create_node(self, data):

        print("Neo4j node created")

        return {
            "status": "node_created"
        }

    def create_edge(self, data):

        print("Neo4j edge created")

        return {
            "status": "edge_created"
        }