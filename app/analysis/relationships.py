from  app.constants import RELATIONSHIP_KEYS


# def relationship_score(keys):

#     score = 0

#     for key in keys:

#        if any(word in key for word in RELATIONSHIP_KEYS):
#             score += 2

#     return min(score, 10)



def relationship_score(keys):
    score = 0

    for key in keys:
        if any(word in key for word in RELATIONSHIP_KEYS):
            score += 2

    return min(score, 10)