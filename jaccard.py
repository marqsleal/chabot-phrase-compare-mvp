def jaccard_index(token1: str, token2: str) -> int:

    # Criação de set() cortando em espaços vazios:
    words_token1_norm = set(token1.split())
    words_token2_norm = set(token2.split())

    # Intersection:
    intersection = words_token1_norm.intersection(words_token2_norm)

    # Union:
    union = words_token1_norm.union(words_token2_norm)

    # Index
    index = int(len(intersection)) / len(union)

    return index