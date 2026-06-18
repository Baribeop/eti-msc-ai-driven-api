import csv
import os
from datetime import datetime


LOG_FILE = "performance_log.csv"


def log_performance(metrics):
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(metrics)


def create_metrics(**kwargs):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        **kwargs
    }
