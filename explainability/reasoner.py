def generate_reason(features):

    reasons = []

    if features["transactional_score"] >= 7:
        reasons.append("transactional workload detected")

    if features["cache_score"] >= 7:
        reasons.append("cache workload detected")

    if features["relationship_score"] >= 7:
        reasons.append("relationship workload detected")

    if features["time_series_score"] >= 7:
        reasons.append("time-series workload detected")

    if features["schema_flexibility"] >= 7:
        reasons.append("high schema flexibility detected")

    return reasons