import numpy as np

def normalizacao_levenshtein(levenshtein: float, token1: str, token2: str) -> float:
    return 1 - (levenshtein / max(len(token1), len(token2)))

def levenshtein_distance(token1: str, token2: str) -> float:

    token1len = len(token1) + 1
    token2len = len(token2) + 1

    distances = np.zeros(
        (token1len,
         token2len)
    )
    for t1 in range(token1len):
        distances[t1][0] = t1

    for t2 in range(token2len):
        distances[0][t2] = t2

    for t1 in range(1, token1len):
        for t2 in range(1, token2len):

            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]

            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    levenshtein = float(distances[len(token1)][len(token2)])

    return levenshtein