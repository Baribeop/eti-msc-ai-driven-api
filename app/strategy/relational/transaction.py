from app.strategy.base import WriteStrategy


class RelationalTransaction(WriteStrategy):

    def execute(self, adapter, operations):

        return adapter.transaction(operations)