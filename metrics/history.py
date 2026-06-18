import sqlite3
from pathlib import Path
from datetime import datetime

DB_FILE = Path("data/prediction_history.db")

def initialize_history_db():

    DB_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        database_name TEXT,
        confidence REAL,
        model_used TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_prediction(
        database_name,
        confidence,
        model_used
):

    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
    INSERT INTO prediction_history(
        timestamp,
        database_name,
        confidence,
        model_used
    )
    VALUES (?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        database_name,
        confidence,
        model_used
    ))

    conn.commit()
    conn.close()