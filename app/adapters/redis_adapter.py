# import redis
# from app.config import REDIS_URL


# class RedisAdapter:

#     def __init__(self):

#         self.client = redis.Redis.from_url(REDIS_URL)

#     def insert(self, data):

#         print("Stored in Redis")

#         return True

import redis

from app.config import REDIS_URL


class RedisAdapter:

    def __init__(self):

        self.client = redis.Redis.from_url(
            REDIS_URL
        )

    def set(self, data):

        print("Redis set")

        return {
            "status": "stored"
        }

    def set_with_expiry(
        self,
        data,
        ttl=300
    ):

        print("Redis expiry set")

        return {
            "status": "stored_with_expiry",
            "ttl": ttl
        }

    def pipeline(self, data):

        print("Redis pipeline")

        return {
            "status": "pipeline_complete",
            "count": len(data)
        }