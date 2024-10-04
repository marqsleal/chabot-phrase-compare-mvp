# Comparador de frases de um Chatbot
_Projeto para fins acadêmicos criando um sistema básico de chatbot que reconheça perguntas semelhantes feitas por diferentes usuários e gere respostas utilizando normalização com expressões regulares, índice de Jaccard e distância de Levenshtein._

## Dependências 

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```

## Instalação 

1. Clone o repositório:

```bash
git clone https://github.com/marqsleal/chabot-phrase-compare-mvp.git
```

2. Execute o arquivo `main.py`:

```bash
python3 main.py
```

## `stopwords.txt`
Arquivo `.txt` contendo algumas stopwords na lingua portuguesa. Stopwords são palavras comuns em qualquer lingua que não possuem conteúdo significativo e são frequentemente filtradas em processamento de linguagem natural.  
Alguns tipos de stopwords são: preposições, artigos, conjunções, e pronomes. A filtragem dessas palavras faz com que se reduza o ruído do algorítimo, melhore a eficiência da analise e foca apenas no conteúdo relevante da mensagem.  

## `regex.py`
Expressões regulares, também conhecido como regex, é uma sequência de caracteres que forma um padrão de busca. Essas expressões são utilizadas para encontrar, manipular ou validar textos de acordo com padrões.

### Imports:
```python
import re
```
Biblioteca `re`: Biblioteca padrão para a manipulação de regex na linguagem python.

### Funções:

`normalizar_texto`: Recebe uma `str` e devolve a mesma `str` normalizada. Convertendo para letras minúsculas, removendo pontuação, trocando digitos por palavras, removendo acentos das letras removendo stopwords e removendo espaços extras.  
Esta função faz uso de outras funções, como `digito_para_palavra`, `acento_para_letra` e `is_stopword`.
```python
def normalizar_texto(texto: str) -> str:
    texto_norm = texto.lower()
    texto_norm = re.sub(r'[^\w\s]', '', texto_norm)
    texto_norm = re.sub(r'\d', digito_para_palavra, texto_norm)
    texto_norm = re.sub(r'[áàãâéêíóôõúüç]', acento_para_letra, texto_norm)
    texto_norm = re.sub(r'\bw+\b', is_stopword, texto_norm)
    texto_norm = re.sub(r'\s+', ' ', texto_norm).strip()

    return texto_norm
```

`digito_para_palavra`: Faz uma comparação entre os dígitos para devolver uma palavra correspondente.
```python
def digito_para_palavra(match):
    digito_palavra = {'0': 'zero', '1': 'um', '2': 'dois', '3': 'três',
        '4': 'quatro', '5': 'cinco', '6': 'seis', '7': 'sete',
        '8': 'oito', '9': 'nove'}
    return digito_palavra[match.group(0)]
```

`acento_para_letra`: Faz uma comparação entre caracteres acentuados para devolver o caractere sem acento correspondente.
```python
def acento_para_letra(match):
    map_acento = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u',
        'ç': 'c'}
    return map_acento[match.group(0)]
```

`is_stopword`: Recebe um `set` de stopwords carregados pela função `load_stopwords`. Busca no texto por stopwords correspondentes e devolve um espaço simples.
```python
def is_stopword(stopwords_set=load_stopwords):
    def check_stopword(match):
        word = match.group(0)
        return '' if word in stopwords_set else word
```

`load_stopwords`: Recebe um _path_ para o arquivo `stopwords.txt`. Devolve um `set` com as stopwords carregadas.
```python
def load_stopwords(path='stopwords.txt'):
    with open(path, 'r', encoding='utf8') as f:
        stopwords = f.read().splitlines()
    return set(stopwords)
```

## `jaccard.py`
O Índice de Jaccard, também conhecido como coeficiente de Jaccard, é uma métrica utilizada para calcular a similaridade entre dois conjuntos. Ele é definido como o tamanho da interseção dos conjuntos dividido pelo tamanho da união dos conjuntos.  
Essa métrica varia de 0 a 1, onde 0 indica que os conjuntos são completamente diferentes, e 1 indica que são idênticos. O Índice de Jaccard é amplamente utilizado em tarefas de comparação de textos e detecção de similaridade.  

### Funções:
`jaccard_index`: Recebe duas `str` e realiza as operações para retornar o index como `float`.
```python
def jaccard_index(token1: str, token2: str) -> float:
    words_token1_norm = set(token1.split())
    words_token2_norm = set(token2.split())
    intersection = words_token1_norm.intersection(words_token2_norm)
    union = words_token1_norm.union(words_token2_norm)

    if len(union) == 0:
        return 0.0
    
    index = float(len(intersection)) / len(union)

    return index
```

## `levenshtein.py`

A Distância de Levenshtein é uma métrica que mede a diferença entre duas sequências de caracteres. Ela calcula o número mínimo de operações de edição necessárias para transformar uma string na outra. As operações permitidas são:
- Inserção de um caractere;
- Exclusão de um caractere;
- Substituição de um caractere;

### Imports:
```python
import numpy as np
```
Biblioteca `numpy`: Biblioteca usada para realizar manipulações matemáticas, além de criação e gerenciamento de arrays.

### Funções:

`levenshtein_distance`: Recebe duas `str` e realiza as operações para retornar a distância como `float`..
```python
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
```

`normalizacao_levenshtein`: Função que realiza uma normalização da distância para realizar comparações.
```python
def normalizacao_levenshtein(levenshtein: float, token1: str, token2: str) -> float:
    return 1 - (levenshtein / max(len(token1), len(token2)))
```

## `respostas.py`
Arquivo contendo as funções que realizam a comparação entre o input (`str`) do usuário e as perguntas na base de dados (`dict`: `str`).

### Imports:
```python
from jaccard import jaccard_index
from levenshtein import levenshtein_distance, normalizacao_levenshtein
from regex import normalizar_texto
```
Imports das funções desenvolvidas para este projeto.

### Funções:

`escolhe_resposta`: Função que recebe o input do usuário (`str`), base de perguntas e respostas (`dict`: `str`) e retorna a pergunta que melhor combina com o input ou uma mensagem de desculpas.  
Aleḿ disso, pode se fazer configuração de `debug` e ajustar o `threshold_jaccard` e `threshold_levenshtein` para melhor refinamento do projeto.
Os thresholds estão em `0.15` e `10.0` respectivamente pois foi um _soft spot_ encontrado durante o desenvolvimento. Se o usuário digitar apenas uma palavra-chave, o programa vai devolver uma resposta que combina com a palavra-chave. Pode ser alterado conforme escalonamento da base de dados e testes.
```python
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
```

`comparador_sim`: Funçaõ responsável por fazer comparação entre o índice de Jaccard, a distância de Levenshtein e a melhor similaridade.
```python
def comparador_sim(indice_jaccard: float, distancia_levenshtein: float, melhor_similaridade: float,
                   pergunta_usuario_norm: str, pergunta_norm: str, threshold_jaccard: float, threshold_levenshtein: float) -> float:
    if indice_jaccard > melhor_similaridade and indice_jaccard >= threshold_jaccard:
        return indice_jaccard
    elif distancia_levenshtein <= threshold_levenshtein:
        return normalizacao_levenshtein(distancia_levenshtein, pergunta_usuario_norm, pergunta_norm)
    return melhor_similaridade
```

## `main.py`
Principal arquivo de execução do projeto.

### Imports:
```python
from resposta import escolhe_resposta
```
Imports das funções desenvolvidas para este projeto.

### Método Main:

Dicionário de perguntas e respostas:
```python
perguntas_respostas = {
        'Qual é o horário de funcionamento?': 'Estamos abertos de segunda a sexta, das 9h às 18h. Aos sábados, das 9h às 14h. Fechamos aos domingos e feriados.',
        'Onde vocês estão localizados?': 'Estamos localizados na Avenida Principal, 123, no centro da cidade.',
        'Quais formas de pagamento vocês aceitam?': 'Aceitamos cartão de crédito, débito, Pix e transferência bancária.',
        'Quais serviços vocês oferecem?': 'Oferecemos uma variedade de serviços, incluindo consultoria, desenvolvimento de software e suporte técnico. Posso ajudar com mais informações sobre algum desses?',
        'Como funciona a política de devoluções?': 'Você pode devolver qualquer produto em até 30 dias após a compra, desde que esteja nas mesmas condições em que foi entregue. Para iniciar uma devolução, entre em contato com nosso suporte.',
        'Estou com problemas no meu pedido. O que devo fazer?': 'Peço desculpas pelo inconveniente! Por favor, envie o número do pedido e uma breve descrição do problema. Nossa equipe de suporte entrará em contato em breve.',
        'Quanto tempo demora a entrega?': 'O prazo de entrega varia de acordo com sua localização. Em média, leva de 3 a 7 dias úteis para entregas dentro do Brasil.',
        'Como faço para me cadastrar?': 'Você pode se cadastrar diretamente no nosso site, clicando no botão "Registrar-se." Basta preencher o formulário com seus dados e criar uma senha segura.',
        'Vocês têm alguma promoção no momento?': 'Sim! Estamos com descontos especiais em nossos principais serviços. Confira nossa página de promoções para mais detalhes.',
        'Como posso deixar um feedback?': 'Agradecemos por querer nos dar um feedback! Você pode preencher nosso formulário de satisfação no site ou enviar um e-mail diretamente para feedback@empresa.com.'
    }
```
Loop do programa:
```python
pergunta_usuario = ''
while pergunta_usuario.lower() != 'sair':
    pergunta_usuario = input("Você: ")
    print(pergunta_usuario)
    resposta = escolhe_resposta(pergunta_usuario, perguntas_respostas, debug=True) # Para ver a lógica
    print(f"Chatbot: {resposta}")
```

## Conclusão
Apesar da simplicidade do projeto, foi possível notar como as tecnologias de processamento de texto podem ser desenvolidas, testatas e melhoradas. Exemplo disso foi a questão do processamento, foi observado que quando se digitava apenas uma palavra, mesmo que a compatiblidade fosse existente (cerca de `0.1666667`), o threshold não permitia que a frase fosse identificada, devolvendo assim uma mensagem de desculpas para o usuário.

## Próximos Passos
- Aumentar o número de perguntas e respostas do bot, possivelmente utilizando um arquivo `.txt` que carrega um `dict`; 
- Testes Unitários;
- Teste A&B utilizando diferentes `threshold` do índice de jaccard e da distância de levenshtein;
