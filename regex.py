import re

def digito_para_palavra(match):
    digito_palavra = {'0': 'zero', '1': 'um', '2': 'dois', '3': 'três',
        '4': 'quatro', '5': 'cinco', '6': 'seis', '7': 'sete',
        '8': 'oito', '9': 'nove'}
    return digito_palavra[match.group(0)]

def load_stopwords(path='stopwords.txt'):
    with open(path, 'r', encoding='utf8') as f:
        stopwords = f.read().splitlines()
    return set(stopwords)

def is_stopword(stopwords_set=load_stopwords):
    def check_stopword(match):
        word = match.group(0)
        return '' if word in stopwords_set else word

    return check_stopword

def normalizar_texto(texto: str) -> str:
    # 1. Converter para minúsculas
    texto_norm = texto.lower()

    # 2. Remover pontuação
    texto_norm = re.sub(r'[^\w\s]', '', texto_norm)

    # 3. Trocar dígitos por palavras
    texto_norm = re.sub(r'\d', digito_para_palavra, texto_norm)

    # 4. Remove Stopwords
    texto_norm = re.sub(r'\bw+\b', is_stopword, texto_norm)

    # 5. Remove Espaços Extras
    texto_norm = re.sub(r'\s+', ' ', texto_norm).strip()

    return texto_norm