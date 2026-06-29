

# import redis

# from app.config import REDIS_URL


# class RedisAdapter:

#     def __init__(self):

#         self.client = redis.Redis.from_url(
#             REDIS_URL
#         )

#     def set(self, data):

#         print("Redis set")

#         return {
#             "status": "stored"
#         }

#     def set_with_expiry(
#         self,
#         data,
#         ttl=300
#     ):

#         print("Redis expiry set")

#         return {
#             "status": "stored_with_expiry",
#             "ttl": ttl
#         }

#     def pipeline(self, data):

#         print("Redis pipeline")

#         return {
#             "status": "pipeline_complete",
#             "count": len(data)
#         }





"""
redis_adapter.py (CORRECTED)
------------------------------
Same security model as postgres_adapter.py / mongo_adapter.py: every
method accepts a `connection` dict supplied by the calling client in the
SAME request, builds a short-lived Redis client from it, executes the
operation, and closes the connection immediately after. No credentials
are stored, logged, or persisted by this middleware.

STORAGE MODEL NOTE:
Redis is a key-value store, so "persisting a payload" means storing the
JSON-serialised payload under a key. By default this adapter generates
a key automatically (polyglot:<uuid>) unless the caller specifies one
via connection["key"] or a top-level "key"/"id" field in the payload
itself. This is analogous to PostgresAdapter's json_blob mode - there is
no meaningful "typed_columns" equivalent for Redis, since Redis has no
column/schema concept at all.

Expected `connection` dict shape:
{
    "type": "redis",
    "host": "localhost",
    "port": 6379,
    "password": "mypassword",   # optional, omit if no auth configured
    "db": 0,                    # optional, defaults to 0
    "key": "my_custom_key",     # optional, auto-generated if omitted
    "ttl": 3600                 # optional, seconds; no expiry if omitted
}
"""

import redis
import json
import uuid
import logging

logger = logging.getLogger(__name__)


class RedisAdapter:

    def _build_client(self, connection: dict):
        """Builds a short-lived Redis client from caller-supplied
        connection details."""
        if not connection.get("host"):
            raise ValueError("Missing required connection field: host")

        client = redis.Redis(
            host=connection["host"],
            port=connection.get("port", 6379),
            password=connection.get("password"),
            db=connection.get("db", 0),
            decode_responses=True,
            socket_connect_timeout=5,
        )
        client.ping()  # fail fast if connection details are wrong
        return client

    def _resolve_key(self, data, connection: dict) -> str:
        if connection.get("key"):
            return connection["key"]
        if isinstance(data, dict):
            for id_field in ("id", "_id", "key", "session_id"):
                if id_field in data:
                    return f"polyglot:{data[id_field]}"
        return f"polyglot:{uuid.uuid4()}"

    def insert(self, data, connection: dict = None):
        """Generic entry point matching the insert() signature used by
        the other adapters, so main.py's /persist handler can call all
        five adapters uniformly. Internally delegates to set()."""
        return self.set(data, connection=connection)

    def set(self, data, connection: dict = None):
        if connection is None:
            raise ValueError("RedisAdapter.set() requires a connection dict")

        client = self._build_client(connection)
        try:
            key = self._resolve_key(data, connection)
            value = json.dumps(data)
            ttl = connection.get("ttl")

            if ttl:
                client.setex(key, ttl, value)
            else:
                client.set(key, value)

            logger.info(f"Redis set successful: key={key}, ttl={ttl}")
            return {
                "status": "stored",
                "database": "redis",
                "key": key,
                "ttl": ttl
            }
        finally:
            client.close()

    def set_with_expiry(self, data, connection: dict = None, ttl: int = 300):
        if connection is None:
            raise ValueError("RedisAdapter.set_with_expiry() requires a connection dict")
        # Reuse set(), injecting ttl into the connection dict if not already present
        conn_with_ttl = {**connection, "ttl": connection.get("ttl", ttl)}
        result = self.set(data, connection=conn_with_ttl)
        result["status"] = "stored_with_expiry"
        return result

    def pipeline(self, data: list, connection: dict = None):
        """Stores multiple items in a single Redis pipeline (batched
        round-trip) for efficiency."""
        if connection is None:
            raise ValueError("RedisAdapter.pipeline() requires a connection dict")

        client = self._build_client(connection)
        try:
            pipe = client.pipeline()
            keys = []
            ttl = connection.get("ttl")

            for item in data:
                key = self._resolve_key(item, connection) if connection.get("key") is None else f"{connection['key']}:{len(keys)}"
                keys.append(key)
                value = json.dumps(item)
                if ttl:
                    pipe.setex(key, ttl, value)
                else:
                    pipe.set(key, value)

            pipe.execute()

            logger.info(f"Redis pipeline successful: count={len(keys)}")
            return {
                "status": "pipeline_complete",
                "database": "redis",
                "count": len(keys),
                "keys": keys
            }
        finally:
            client.close()