from  app.constants import TIME_SERIES_KEYS


def time_series_score(keys):

    score = 0

    for key in keys:

        if key in TIME_SERIES_KEYS:
            score += 2

    return min(score, 10)