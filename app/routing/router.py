from app.analysis.payload_analyzer import analyze_payload

from app.routing.decision_engine import decide

from app.strategy.factory import get_strategy

from app.execution.executor import Executor


executor = Executor()


def route_payload(data):

    features = analyze_payload(data)

    decision = decide(features)

    database = decision["database"]

    strategy = get_strategy(
        database,
        features
    )

    execution_result = executor.execute(
        database,
        strategy,
        data
    )

    return {

        "decision": decision,

        "strategy":
            strategy.__class__.__name__,

        "execution":
            execution_result,

        "features": features
    }