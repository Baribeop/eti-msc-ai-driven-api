from app.strategy.base import WriteStrategy


class CachePipeline(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.pipeline(data)