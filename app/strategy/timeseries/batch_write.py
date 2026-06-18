from app.strategy.base import WriteStrategy


class TimeSeriesBatchWrite(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.batch_write(data)