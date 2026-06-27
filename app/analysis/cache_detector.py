from app.constants import CACHE_KEYS


def cache_score(keys):

    score = 0

    for key in keys:

        if any(word in key for word in CACHE_KEYS):
            score += 2

    return min(score, 10)