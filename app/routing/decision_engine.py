from app.ai.predictor import predict
from app.routing.rules import hard_rules


def decide(features):

    rule = hard_rules(features)

    if rule:

        db = rule["database"]
        confidence = 1.0

    else:

        prediction = predict(features)

        db = prediction["database"]
        confidence = prediction["confidence"]

    mapping = {
        "postgres": "relational",
        "mongo": "document",
        "redis": "cache",
        "influxdb": "time-series",
        "neo4j": "graph"
    }

    return {
        "database": db,
        "category": mapping.get(db),
        "confidence": confidence
    }