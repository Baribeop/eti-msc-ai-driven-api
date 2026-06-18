from app.strategy.base import WriteStrategy


class CacheSet(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.set(data)