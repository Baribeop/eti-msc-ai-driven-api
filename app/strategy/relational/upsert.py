from app.strategy.base import WriteStrategy


class RelationalUpsert(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.upsert(data)