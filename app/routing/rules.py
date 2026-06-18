def hard_rules(features):

    if features["cache_score"] >= 8:

        return {
            "database": "redis",
            "reason": "cache workload detected"
        }

    if features["transactional_score"] >= 8:

        return {
            "database": "postgres",
            "reason": "high transactional workload"
        }

    if features["relationship_score"] >= 8:

        return {
            "database": "neo4j",
            "reason": "relationship-heavy workload"
        }

    if features["time_series_score"] >= 8:

        return {
            "database": "influxdb",
            "reason": "time-series workload"
        }

    return None