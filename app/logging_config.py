import logging
import sys
from pathlib import Path

def setup_logging():
    log_dir = Path("app/ai")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log", encoding='utf-8'),   # Force UTF-8
            logging.StreamHandler(sys.stdout)  # Safe console output
        ]
    )

    # Suppress noisy loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)

    return logging.getLogger(__name__)