def jaccard_index(token1: str, token2: str) -> float:

    # Criação de set() cortando em espaços vazios:
    words_token1_norm = set(token1.split())
    words_token2_norm = set(token2.split())

    # Intersection:
    intersection = words_token1_norm.intersection(words_token2_norm)

    # Union:
    union = words_token1_norm.union(words_token2_norm)

    if len(union) == 0:  # Evita divisão por zero
        return 0.0

    # Index
    index = float(len(intersection)) / len(union)

    return index