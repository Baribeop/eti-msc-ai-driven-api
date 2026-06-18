from app.strategy.base import WriteStrategy


class DocumentUpsert(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.upsert(data)