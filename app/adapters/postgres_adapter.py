# # from sqlalchemy import create_engine
# # from app.config import POSTGRES_URL


# # class PostgresAdapter:

# #     def __init__(self):

# #         self.engine = create_engine(POSTGRES_URL)

# #     def insert(self, data):

# #         print("Inserted into PostgreSQL")

# #         return True

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from app.config import POSTGRES_URL


# class PostgresAdapter:

#     def __init__(self):

#         self.engine = create_engine(POSTGRES_URL)

#         self.Session = sessionmaker(bind=self.engine)

#     def insert(self, data):

#         print("PostgreSQL insert")

#         return {
#             "status": "inserted",
#             "database": "postgres"
#         }

#     def bulk_insert(self, data):

#         print("PostgreSQL bulk insert")

#         return {
#             "status": "bulk_inserted",
#             "count": len(data)
#         }

#     def upsert(self, data):

#         print("PostgreSQL upsert")

#         return {
#             "status": "upserted"
#         }

#     def transaction(self, operations):

#         print("PostgreSQL transaction")

#         return {
#             "status": "transaction_complete"
#         }


"""
postgres_adapter.py (CORRECTED, WITH STORAGE MODE SUPPORT)
--------------------------------------------------------------
SECURITY MODEL: this adapter does NOT use a hardcoded server-side database
connection (the original POSTGRES_URL from app/config.py). Instead, every
method accepts a `connection` dict supplied by the calling client in the
SAME request, builds a connection from it for the duration of that single
call, executes the operation, and immediately disposes of the connection.
No credentials are stored, logged, or persisted by this middleware at any
point - they exist only in request-scoped memory for the lifetime of one
HTTP call, consistent with a "bring your own database" security model.

STORAGE MODES:
This adapter supports two storage modes, selected via connection["storage_mode"]:

  "json_blob" (default) - stores the entire payload as a single JSONB
  column. Works for ANY arbitrary payload shape with zero schema setup.
  Best for heterogeneous, varied payloads where no fixed schema is known
  in advance. Querying nested fields requires Postgres JSON operators
  (e.g. payload->>'order_id') or an ORM's JSON-column query support.

  "typed_columns" - inspects the top-level keys of the FIRST payload
  written to a given table and creates a table with one real, typed
  column per key (inferring INTEGER/NUMERIC/TEXT/BOOLEAN/JSONB as
  appropriate). Subsequent inserts to the same table reuse this schema,
  adding new columns automatically if a later payload introduces keys
  not seen before. This gives ORMs (SQLAlchemy, Django, etc.) a natural,
  one-to-one column-to-attribute mapping, at the cost of requiring
  reasonably consistent payload shapes within a single table.

Expected `connection` dict shape (matches PersistRequest.connection in
main.py):
{
    "type": "postgres",
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "user": "myuser",
    "password": "mypassword",
    "table": "my_table",          # optional, defaults to "polyglot_data"
    "storage_mode": "json_blob"   # optional, "json_blob" (default) or "typed_columns"
}
"""

from sqlalchemy import create_engine, text, inspect
import json
import logging

logger = logging.getLogger(__name__)


def _infer_pg_type(value):
    """Maps a Python value to a reasonable PostgreSQL column type, for
    typed_columns mode. Falls back to JSONB for anything structured or
    ambiguous, so no value type can ever fail to be stored."""
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, int):
        return "BIGINT"
    if isinstance(value, float):
        return "DOUBLE PRECISION"
    if isinstance(value, (dict, list)):
        return "JSONB"
    return "TEXT"  # strings, None, and anything else default to TEXT


def _sanitize_column_name(key: str) -> str:
    """Ensures a payload key is safe to use as a SQL column identifier.
    Strips anything that isn't alphanumeric/underscore, and ensures the
    result doesn't start with a digit."""
    safe = "".join(c if (c.isalnum() or c == "_") else "_" for c in str(key))
    if safe and safe[0].isdigit():
        safe = f"col_{safe}"
    return safe.lower() or "unnamed_field"


class PostgresAdapter:

    def _build_engine(self, connection: dict):
        """Builds a short-lived SQLAlchemy engine from caller-supplied
        connection details. Raises a clear error if required fields are
        missing, rather than silently falling back to any server-side
        default connection."""
        required = ["host", "database", "user", "password"]
        missing = [f for f in required if not connection.get(f)]
        if missing:
            raise ValueError(f"Missing required connection fields: {missing}")

        port = connection.get("port", 5432)
        url = (
            f"postgresql+psycopg2://{connection['user']}:{connection['password']}"
            f"@{connection['host']}:{port}/{connection['database']}"
        )
        engine = create_engine(url, pool_pre_ping=True)
        return engine

    def _ensure_table(self, engine, table_name: str):
        """Creates a simple JSON-storage table if it doesn't already
        exist (json_blob mode). Each row stores the original payload as
        JSON, plus an auto-incrementing id."""
        with engine.connect() as conn:
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    payload JSONB NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """))
            conn.commit()

    def _ensure_typed_table(self, engine, table_name: str, sample_data: dict):
        """For typed_columns mode: creates the table with one real column
        per key in sample_data if the table doesn't exist yet, or adds
        any missing columns (inferred from sample_data) if it already
        exists. This allows the schema to grow naturally as new payload
        shapes are written to the same table, without ever dropping or
        altering existing columns."""
        inspector = inspect(engine)
        table_exists = inspector.has_table(table_name)

        if not table_exists:
            columns_sql = ["id SERIAL PRIMARY KEY"]
            for key, value in sample_data.items():
                col_name = _sanitize_column_name(key)
                col_type = _infer_pg_type(value)
                columns_sql.append(f'"{col_name}" {col_type}')
            columns_sql.append("created_at TIMESTAMP DEFAULT NOW()")

            with engine.connect() as conn:
                conn.execute(text(f"CREATE TABLE {table_name} ({', '.join(columns_sql)})"))
                conn.commit()
            logger.info(f"Created typed table '{table_name}' with columns: {list(sample_data.keys())}")
        else:
            # Table exists - add any columns present in sample_data but
            # missing from the existing table, so the schema can grow
            existing_columns = {c["name"] for c in inspector.get_columns(table_name)}
            with engine.connect() as conn:
                for key, value in sample_data.items():
                    col_name = _sanitize_column_name(key)
                    if col_name not in existing_columns:
                        col_type = _infer_pg_type(value)
                        conn.execute(text(f'ALTER TABLE {table_name} ADD COLUMN "{col_name}" {col_type}'))
                        logger.info(f"Added new column '{col_name}' ({col_type}) to table '{table_name}'")
                conn.commit()

    def insert(self, data, connection: dict = None):
        if connection is None:
            raise ValueError("PostgresAdapter.insert() requires a connection dict")

        engine = self._build_engine(connection)
        table_name = connection.get("table", "polyglot_data")
        storage_mode = connection.get("storage_mode", "json_blob")

        try:
            if storage_mode == "typed_columns":
                return self._insert_typed(engine, table_name, data)
            else:
                return self._insert_json_blob(engine, table_name, data)
        finally:
            engine.dispose()

    def _insert_json_blob(self, engine, table_name, data):
        self._ensure_table(engine, table_name)
        with engine.connect() as conn:
            result = conn.execute(
                text(f"INSERT INTO {table_name} (payload) VALUES (:payload) RETURNING id"),
                {"payload": json.dumps(data)}
            )
            new_id = result.fetchone()[0]
            conn.commit()

        logger.info(f"PostgreSQL insert (json_blob) successful: table={table_name}, id={new_id}")
        return {
            "status": "inserted",
            "database": "postgres",
            "storage_mode": "json_blob",
            "table": table_name,
            "id": new_id
        }

    def _insert_typed(self, engine, table_name, data):
        data_dict = dict(data)
        self._ensure_typed_table(engine, table_name, data_dict)

        columns = [_sanitize_column_name(k) for k in data_dict.keys()]
        placeholders = [f":{c}" for c in columns]
        values = {}
        for k, v in data_dict.items():
            col = _sanitize_column_name(k)
            # JSON-serialise structured values (dict/list) since they
            # land in a JSONB column; everything else passes through.
            values[col] = json.dumps(v) if isinstance(v, (dict, list)) else v

        with engine.connect() as conn:
            result = conn.execute(
                text(
                    f"INSERT INTO {table_name} ({', '.join(f'\"{c}\"' for c in columns)}) "
                    f"VALUES ({', '.join(placeholders)}) RETURNING id"
                ),
                values
            )
            new_id = result.fetchone()[0]
            conn.commit()

        logger.info(f"PostgreSQL insert (typed_columns) successful: table={table_name}, id={new_id}")
        return {
            "status": "inserted",
            "database": "postgres",
            "storage_mode": "typed_columns",
            "table": table_name,
            "id": new_id
        }

    def bulk_insert(self, data: list, connection: dict = None):
        if connection is None:
            raise ValueError("PostgresAdapter.bulk_insert() requires a connection dict")

        engine = self._build_engine(connection)
        table_name = connection.get("table", "polyglot_data")

        try:
            self._ensure_table(engine, table_name)
            inserted_ids = []
            with engine.connect() as conn:
                for item in data:
                    result = conn.execute(
                        text(f"INSERT INTO {table_name} (payload) VALUES (:payload) RETURNING id"),
                        {"payload": json.dumps(item)}
                    )
                    inserted_ids.append(result.fetchone()[0])
                conn.commit()

            logger.info(f"PostgreSQL bulk insert successful: table={table_name}, count={len(inserted_ids)}")
            return {
                "status": "bulk_inserted",
                "database": "postgres",
                "table": table_name,
                "count": len(inserted_ids),
                "ids": inserted_ids
            }
        finally:
            engine.dispose()

    def upsert(self, data, connection: dict = None, key_field: str = "id"):
        if connection is None:
            raise ValueError("PostgresAdapter.upsert() requires a connection dict")

        engine = self._build_engine(connection)
        table_name = connection.get("table", "polyglot_data")
        record_key = data.get(key_field)

        try:
            self._ensure_table(engine, table_name)
            with engine.connect() as conn:
                if record_key is not None:
                    existing = conn.execute(
                        text(f"SELECT id FROM {table_name} WHERE payload->>'{key_field}' = :key"),
                        {"key": str(record_key)}
                    ).fetchone()
                    if existing:
                        conn.execute(
                            text(f"UPDATE {table_name} SET payload = :payload WHERE id = :id"),
                            {"payload": json.dumps(data), "id": existing[0]}
                        )
                        conn.commit()
                        return {"status": "upserted", "action": "updated", "id": existing[0]}

                result = conn.execute(
                    text(f"INSERT INTO {table_name} (payload) VALUES (:payload) RETURNING id"),
                    {"payload": json.dumps(data)}
                )
                new_id = result.fetchone()[0]
                conn.commit()
                return {"status": "upserted", "action": "inserted", "id": new_id}
        finally:
            engine.dispose()

    def transaction(self, operations: list, connection: dict = None):
        """Executes multiple insert operations atomically - all succeed
        or all roll back together."""
        if connection is None:
            raise ValueError("PostgresAdapter.transaction() requires a connection dict")

        engine = self._build_engine(connection)
        table_name = connection.get("table", "polyglot_data")

        try:
            self._ensure_table(engine, table_name)
            inserted_ids = []
            with engine.begin() as conn:  # begin() auto-commits on success, auto-rollback on exception
                for op in operations:
                    result = conn.execute(
                        text(f"INSERT INTO {table_name} (payload) VALUES (:payload) RETURNING id"),
                        {"payload": json.dumps(op)}
                    )
                    inserted_ids.append(result.fetchone()[0])

            return {
                "status": "transaction_complete",
                "database": "postgres",
                "count": len(inserted_ids),
                "ids": inserted_ids
            }
        finally:
            engine.dispose()
