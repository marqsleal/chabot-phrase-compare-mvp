from jaccard import jaccard_index
from levenshtein import levenshtein_distance
from regex import normalizar_texto

def comparador_sim(similaridade_jaccard: float, distancia_levenshtein: float, threshold: float,
                   melhor_similaridade: float) -> float:
    if (similaridade_jaccard > melhor_similaridade
        and similaridade_jaccard > threshold) or (distancia_levenshtein > melhor_similaridade
                                                  and distancia_levenshtein > threshold):
        if similaridade_jaccard > distancia_levenshtein:
            return similaridade_jaccard
        else:
            return distancia_levenshtein
    return melhor_similaridade

def escolhe_resposta(pergunta_usuario: str, perguntas_respostas: dict, threshold=0.5) -> str:
    pergunta_usuario_norm = normalizar_texto(pergunta_usuario)

    melhor_pergunta = None
    melhor_similaridade = float(-1)

    for pergunta, resposta in perguntas_respostas.items():
        pergunta_norm = normalizar_texto(pergunta)

        similaridade_jaccard = jaccard_index(pergunta_usuario_norm, pergunta_norm)
        distancia_levenshtein = levenshtein_distance(pergunta_usuario_norm, pergunta_norm)

        comparador = comparador_sim(similaridade_jaccard, distancia_levenshtein, threshold, melhor_similaridade)

        if comparador > melhor_similaridade and comparador > threshold:
            melhor_similaridade = comparador
            melhor_pergunta = pergunta

    if melhor_pergunta:
        return perguntas_respostas[melhor_pergunta]
    else:
        return 'Desculpe, não entendi sua pergunta!'