"""Mediana das medianas: seleção do k-ésimo menor valor em tempo linear.

Aplicação: duração e plays típicos das músicas, robustos a outliers
(uma música com plays absurdos mexe na média, mas quase não mexe na mediana).
"""

import math

TAMANHO_GRUPO = 5


def _selecionar(valores, k):
    """k-ésimo menor (0-indexado) de uma lista não vazia, com 0 <= k < len."""
    if len(valores) <= TAMANHO_GRUPO:
        return sorted(valores)[k]

    # Dividir em grupos de 5 e tirar a mediana de cada um (custo constante
    # por grupo, O(n) no total).
    grupos = [valores[i:i + TAMANHO_GRUPO] for i in range(0, len(valores), TAMANHO_GRUPO)]
    medianas = [sorted(g)[(len(g) - 1) // 2] for g in grupos]

    # Pivô: a mediana das medianas, achada recursivamente em ~n/5 elementos.
    pivo = _selecionar(medianas, (len(medianas) - 1) // 2)

    # Particionar em L (< pivô), iguais ao pivô e R (> pivô). Tratar os iguais
    # à parte garante progresso mesmo com muitos valores repetidos.
    menores = [x for x in valores if x < pivo]
    maiores = [x for x in valores if x > pivo]
    n_iguais = len(valores) - len(menores) - len(maiores)

    # Descer só no lado que contém a posição k.
    if k < len(menores):
        return _selecionar(menores, k)
    if k < len(menores) + n_iguais:
        return pivo
    return _selecionar(maiores, k - len(menores) - n_iguais)


def selecionar(valores, k):
    """k-ésimo menor valor (k começa em 0) em O(n) no pior caso."""
    if not 0 <= k < len(valores):
        raise IndexError(f"k = {k} fora do intervalo [0, {len(valores)})")
    return _selecionar(list(valores), k)


def mediana(valores):
    """Mediana: valor do meio (n ímpar) ou média dos dois do meio (n par)."""
    n = len(valores)
    if n == 0:
        raise ValueError("a lista não pode ser vazia")
    if n % 2 == 1:
        return selecionar(valores, n // 2)
    return (selecionar(valores, n // 2 - 1) + selecionar(valores, n // 2)) / 2


def percentil(valores, p):
    """Percentil p (0 a 100) com interpolação linear entre os vizinhos.

    Usa a mesma definição de numpy.percentile, então percentil(v, 50) == mediana(v).
    """
    n = len(valores)
    if n == 0:
        raise ValueError("a lista não pode ser vazia")
    if not 0 <= p <= 100:
        raise ValueError("p deve estar entre 0 e 100")

    posicao = p / 100 * (n - 1)
    baixo = math.floor(posicao)
    alto = math.ceil(posicao)
    v_baixo = selecionar(valores, baixo)
    if alto == baixo:
        return v_baixo
    v_alto = selecionar(valores, alto)
    return v_baixo + (v_alto - v_baixo) * (posicao - baixo)
