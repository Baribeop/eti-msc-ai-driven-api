# import os
# from dotenv import load_dotenv

# load_dotenv()

# POSTGRES_URL = os.getenv("POSTGRES_URL")
# MONGO_URL = os.getenv("MONGO_URL")
# REDIS_URL = os.getenv("REDIS_URL")
# INFLUX_URL = os.getenv("INFLUX_URL")
# NEO4J_URL = os.getenv("NEO4J_URL")
# NEO4J_USER = os.getenv("NEO4J_USER")
# NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
# API_KEY = os.getenv("API_KEY")


# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     POSTGRES_URL = os.getenv("POSTGRES_URL")
#     MONGO_URL = os.getenv("MONGO_URL")
#     REDIS_URL = os.getenv("REDIS_URL")
#     INFLUX_URL = os.getenv("INFLUX_URL")
#     INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
#     INFLUX_ORG = os.getenv("INFLUX_ORG")
#     INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
#     NEO4J_URL = os.getenv("NEO4J_URL")
#     NEO4J_USER = os.getenv("NEO4J_USER")
#     NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
#     API_KEY = os.getenv("API_KEY", "developer_key")



# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

class Config:
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    MONGO_URL = os.getenv("MONGO_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    INFLUX_URL = os.getenv("INFLUX_URL")
    INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
    INFLUX_ORG = os.getenv("INFLUX_ORG")
    INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
    NEO4J_URL = os.getenv("NEO4J_URL")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    
    # API Key for authentication
    API_KEY = os.getenv("API_KEY", "developer_key")   # Default fallback


    MAX_FILE_SIZE = int(
    os.getenv(
        "MAX_FILE_SIZE",
        10485760
    )
)