from app.strategy.base import WriteStrategy


class GraphCreateNode(WriteStrategy):

    def execute(self, adapter, data):

        return adapter.create_node(data)