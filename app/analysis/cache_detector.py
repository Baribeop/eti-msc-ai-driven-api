from app.constants import CACHE_KEYS


def cache_score(keys):

    score = 0

    for key in keys:

        if key in CACHE_KEYS:
            score += 2

    return min(score, 10)