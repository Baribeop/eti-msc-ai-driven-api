from app.strategy.base import WriteStrategy


class DocumentInsert(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.insert(data)