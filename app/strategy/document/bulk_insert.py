from app.strategy.base import WriteStrategy


class DocumentBulkInsert(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.bulk_insert(data)