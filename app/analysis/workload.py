from  app.constants import TRANSACTIONAL_KEYS


def transactional_score(keys):

    score = 0

    for key in keys:

        if any(word in key for word in TRANSACTIONAL_KEYS):
            score += 2

    return min(score, 10)