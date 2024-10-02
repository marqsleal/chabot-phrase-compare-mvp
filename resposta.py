from jaccard import jaccard_index
from levenshtein import levenshtein_distance, normalizacao_levenshtein
from regex import normalizar_texto

def comparador_sim(indice_jaccard: float, distancia_levenshtein: float, melhor_similaridade: float,
                   pergunta_usuario_norm: str, pergunta_norm: str, threshold_jaccard: float, threshold_levenshtein: float) -> float:
    if indice_jaccard > melhor_similaridade and indice_jaccard >= threshold_jaccard:
        return indice_jaccard
    elif distancia_levenshtein <= threshold_levenshtein:
        return normalizacao_levenshtein(distancia_levenshtein, pergunta_usuario_norm, pergunta_norm)
    return melhor_similaridade

def escolhe_resposta(pergunta_usuario: str, perguntas_respostas: dict, threshold_jaccard=0.15, threshold_levenshtein=10.0,
                     debug=False) -> str:
    pergunta_usuario_norm = normalizar_texto(pergunta_usuario)

    melhor_pergunta = None
    melhor_similaridade = float(-1)

    for pergunta, resposta in perguntas_respostas.items():
        pergunta_norm = normalizar_texto(pergunta)

        indice_jaccard = jaccard_index(pergunta_usuario_norm, pergunta_norm)
        distancia_levenshtein = levenshtein_distance(pergunta_usuario_norm, pergunta_norm)

        comparador = comparador_sim(indice_jaccard, distancia_levenshtein, melhor_similaridade, pergunta_usuario_norm,
                                    pergunta_norm, threshold_jaccard, threshold_levenshtein)

        if debug:
            print(f"""Pergunta: '{pergunta}'\nJaccard: {indice_jaccard:.2f}\nLevenshtein: {distancia_levenshtein}\nComparador: {comparador:.2f}\nMelhor Similaridade até agora: {melhor_similaridade:.2f}\n""")

        if comparador > melhor_similaridade:
            melhor_similaridade = comparador
            melhor_pergunta = pergunta

    if melhor_pergunta:
        return perguntas_respostas[melhor_pergunta]
    else:
        return "Desculpe, não entendi sua pergunta."