from app.strategy.base import WriteStrategy


class RelationalInsert(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.insert(data)