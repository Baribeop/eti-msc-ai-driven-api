# from app.analysis.scs import calculate_scs
# from  app.analysis.workload import transactional_score
# from  app.analysis.cache_detector import cache_score
# from  app.analysis.relationships import relationship_score
# from  app.analysis.time_series import time_series_score


# def extract_keys(data, keys=None):

#     if keys is None:
#         keys = []

#     if isinstance(data, dict):

#         for k, v in data.items():
#             keys.append(k.lower())
#             extract_keys(v, keys)

#     elif isinstance(data, list):

#         for item in data:
#             extract_keys(item, keys)

#     return keys


# def max_depth(data, depth=1):

#     if isinstance(data, dict):

#         if not data:
#             return depth

#         return max(
#             max_depth(v, depth + 1)
#             for v in data.values()
#         )

#     elif isinstance(data, list):

#         if not data:
#             return depth

#         return max(
#             max_depth(i, depth + 1)
#             for i in data
#         )

#     return depth


# def schema_flexibility(data):

#     score = 0

#     if isinstance(data, dict):

#         for value in data.values():

#             if isinstance(value, (dict, list)):
#                 score += 2

#     elif isinstance(data, list):
#         score += 3

#     return min(score, 10)


# def analyze_payload(data):

#     keys = extract_keys(data)

#     return {
#         "scs": calculate_scs(data),
#         "max_depth": max_depth(data),
#         "transactional_score": transactional_score(keys),
#         "cache_score": cache_score(keys),
#         "relationship_score": relationship_score(keys),
#         "time_series_score": time_series_score(keys),
#         "schema_flexibility": schema_flexibility(data),
#         "is_bulk": isinstance(data, list),
#         "has_identifier": (
#             isinstance(data, dict)
#             and (
#                 "id" in data
#                 or "_id" in data
#             )
#         )
#     }



# from app.analysis.scs import calculate_scs
# from app.analysis.workload import transactional_score
# from app.analysis.cache_detector import cache_score
# from app.analysis.relationships import relationship_score
# from app.analysis.time_series import time_series_score

# def extract_keys(data, keys=None):
#     if keys is None:
#         keys = []
#     if isinstance(data, dict):
#         for k, v in data.items():
#             keys.append(str(k).lower())
#             extract_keys(v, keys)
#     elif isinstance(data, list):
#         for item in data:
#             extract_keys(item, keys)
#     return keys

# def max_depth(data, depth=1):
#     if isinstance(data, dict):
#         if not data:
#             return depth
#         return max(max_depth(v, depth + 1) for v in data.values())
#     elif isinstance(data, list):
#         if not data:
#             return depth
#         return max(max_depth(i, depth + 1) for i in data)
#     return depth

# def schema_flexibility(data):
#     score = 0
#     if isinstance(data, dict):
#         for value in data.values():
#             if isinstance(value, (dict, list)):
#                 score += 2
#     elif isinstance(data, list):
#         score += 3
#     return min(score, 10)

# def analyze_payload(data):
#     keys = extract_keys(data)
#     return {
#         "scs": calculate_scs(data),
#         "max_depth": max_depth(data),
#         "transactional_score": transactional_score(keys),
#         "cache_score": cache_score(keys),
#         "relationship_score": relationship_score(keys),
#         "time_series_score": time_series_score(keys),
#         "schema_flexibility": schema_flexibility(data),
#         "is_bulk": isinstance(data, list),
#         "has_identifier": isinstance(data, dict) and ("id" in data or "_id" in data),
#         "num_keys": len(set(keys)),
#         "has_nested": any(isinstance(v, (dict, list)) for v in (data.values() if isinstance(data, dict) else []))
#     }



from typing import Any, Dict
import logging
import json
from app.analysis.scs import calculate_scs
from app.analysis.workload import transactional_score
from app.analysis.cache_detector import cache_score
from app.analysis.relationships import relationship_score
from app.analysis.time_series import time_series_score

logger = logging.getLogger(__name__)

# ====================== LOCAL HELPER FUNCTIONS (your original) ======================

def extract_keys(data, keys=None):
    if keys is None:
        keys = []
    if isinstance(data, dict):
        for k, v in data.items():
            keys.append(str(k).lower())
            extract_keys(v, keys)
    elif isinstance(data, list):
        for item in data:
            extract_keys(item, keys)
    return keys


def max_depth(data, depth=1):
    if isinstance(data, dict):
        if not data:
            return depth
        return max(max_depth(v, depth + 1) for v in data.values())
    elif isinstance(data, list):
        if not data:
            return depth
        return max(max_depth(i, depth + 1) for i in data)
    return depth


def schema_flexibility(data):
    score = 0
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, (dict, list)):
                score += 2
    elif isinstance(data, list):
        score += 3
    return min(score, 10)


# ====================== MAIN ANALYSIS FUNCTION ======================

def analyze_payload(data: Any) -> Dict:
    """Analyze payload and return all 11 features required by the model."""
    if data is None:
        data = {}
    
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            data = {"raw_content": data}

    # Extract keys (your original helper)
    keys = extract_keys(data)

    # === Core features from your original modular design ===
    features = {
        "scs": calculate_scs(data),                    # from app.analysis.scs
        "max_depth": max_depth(data),                  # your local function
        "transactional_score": transactional_score(keys),   # from workload
        "cache_score": cache_score(keys),              # from cache_detector
        "relationship_score": relationship_score(keys),    # from relationships
        "time_series_score": time_series_score(keys),      # from time_series
        "schema_flexibility": schema_flexibility(data),    # your local function
    }

    # === Ensure all 4 structural features are always present (critical fix) ===
    structural = {
        "is_bulk": isinstance(data, list) or (isinstance(data, dict) and len(data) > 8),
        "has_identifier": isinstance(data, dict) and ("id" in data or "_id" in data or "uuid" in data),
        "num_keys": len(set(keys)),
        "has_nested": any(isinstance(v, (dict, list)) for v in (data.values() if isinstance(data, dict) else []))
    }

    # Merge and return complete feature set
    features.update(structural)

    logger.debug(f"Payload analyzed - Features: {list(features.keys())}")
    return features


# ====================== Optional: Direct Test ======================
if __name__ == "__main__":
    test_payload = {
        "user_id": 12345,
        "order_id": "ORD-9876",
        "items": [{"name": "Laptop", "price": 1299}],
        "timestamp": "2025-06-15T10:00:00",
        "total": 1299.0
    }
    
    result = analyze_payload(test_payload)
    print("✅ Analysis successful!")
    print(json.dumps(result, indent=2))