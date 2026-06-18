from app.strategy.base import WriteStrategy


class GraphCreateEdge(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.create_edge(data)