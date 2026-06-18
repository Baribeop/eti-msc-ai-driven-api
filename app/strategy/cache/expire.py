from app.strategy.base import WriteStrategy


class CacheExpire(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.set_with_expiry(
            data,
            ttl=300
        )