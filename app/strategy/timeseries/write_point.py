from app.strategy.base import WriteStrategy


class TimeSeriesWrite(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.write_point(data)