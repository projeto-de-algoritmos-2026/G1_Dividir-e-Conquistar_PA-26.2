"""Par de pontos mais próximo por dividir e conquistar."""

from math import hypot


def _distancia(a, b):
    return hypot(a[0] - b[0], a[1] - b[1])


def _melhor(resultado_a, resultado_b):
    """Escolhe a menor distância e desempata pela ordem de entrada."""
    chave_a = (resultado_a[2], resultado_a[0][2], resultado_a[1][2])
    chave_b = (resultado_b[2], resultado_b[0][2], resultado_b[1][2])
    return resultado_a if chave_a <= chave_b else resultado_b


def _forca_bruta(registros):
    melhor = None
    for i, a in enumerate(registros):
        for b in registros[i + 1:]:
            par = (a, b, _distancia(a, b))
            melhor = par if melhor is None else _melhor(melhor, par)
    return melhor


def _mesclar_por_y(esquerda, direita):
    mesclados = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if (esquerda[i][1], esquerda[i][0]) <= (direita[j][1], direita[j][0]):
            mesclados.append(esquerda[i])
            i += 1
        else:
            mesclados.append(direita[j])
            j += 1
    mesclados.extend(esquerda[i:])
    mesclados.extend(direita[j:])
    return mesclados


def _resolver_recursivo(ordenados_x):
    n = len(ordenados_x)
    if n <= 3:
        return _forca_bruta(ordenados_x), sorted(
            ordenados_x, key=lambda ponto: (ponto[1], ponto[0], ponto[2])
        )

    meio = n // 2
    esquerda_x = ordenados_x[:meio]
    direita_x = ordenados_x[meio:]
    melhor_esquerda, esquerda_y = _resolver_recursivo(esquerda_x)
    melhor_direita, direita_y = _resolver_recursivo(direita_x)
    melhor = _melhor(
        melhor_esquerda,
        melhor_direita,
    )
    ordenados_y = _mesclar_por_y(esquerda_y, direita_y)
    delta = melhor[2]
    x_divisao = ordenados_x[meio][0]
    faixa = [ponto for ponto in ordenados_y if abs(ponto[0] - x_divisao) < delta]

    for i, a in enumerate(faixa):
        for b in faixa[i + 1:i + 8]:
            if b[1] - a[1] >= delta:
                break
            melhor = _melhor(melhor, (a, b, _distancia(a, b)))
            delta = melhor[2]

    return melhor, ordenados_y


def _par_mais_proximo(itens, coordenadas):
    if len(itens) < 2:
        raise ValueError("são necessários pelo menos dois pontos")

    registros = [(*coordenadas(item), indice, item) for indice, item in enumerate(itens)]
    ordenados_x = sorted(registros, key=lambda ponto: (ponto[0], ponto[1], ponto[2]))
    (a, b, distancia), _ = _resolver_recursivo(ordenados_x)
    return a[3], b[3], distancia


def par_mais_proximo(pontos):
    """Devolve os dois pontos mais próximos e a distância euclidiana."""
    return _par_mais_proximo(list(pontos), lambda ponto: (ponto[0], ponto[1]))


def musicas_mais_parecidas(musicas):
    """Compara músicas pelas coordenadas energia e dançabilidade."""
    return _par_mais_proximo(
        list(musicas),
        lambda musica: (musica.energia, musica.dancabilidade),
    )
