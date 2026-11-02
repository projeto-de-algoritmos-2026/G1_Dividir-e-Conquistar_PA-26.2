"""Contagem de inversões por dividir e conquistar (Sort-and-Count).

Uma inversão é um par (i, j) com i < j e lista[i] > lista[j]. Aplicação:
a distância de Kendall tau entre dois rankings de músicas é o número de
inversões de um ranking visto na ordem do outro.
"""


def _ordenar_e_contar(lista):
    """Devolve (lista ordenada, número de inversões) em O(n log n)."""
    n = len(lista)
    if n <= 1:
        return list(lista), 0

    meio = n // 2
    esq, inv_esq = _ordenar_e_contar(lista[:meio])
    dir_, inv_dir = _ordenar_e_contar(lista[meio:])

    # Combinar: o merge ordena e conta ao mesmo tempo. Quando um elemento da
    # direita passa na frente, ele forma inversão com todos os que ainda
    # restam na esquerda (que já estão ordenados).
    mesclada = []
    inv_cruzadas = 0
    i = j = 0
    while i < len(esq) and j < len(dir_):
        if esq[i] <= dir_[j]:
            mesclada.append(esq[i])
            i += 1
        else:
            mesclada.append(dir_[j])
            inv_cruzadas += len(esq) - i
            j += 1
    mesclada.extend(esq[i:])
    mesclada.extend(dir_[j:])

    return mesclada, inv_esq + inv_dir + inv_cruzadas


def contar_inversoes(lista):
    """Número de pares (i, j), i < j, com lista[i] > lista[j]."""
    return _ordenar_e_contar(lista)[1]


def similaridade(ranking_a, ranking_b):
    """Distância de Kendall tau normalizada entre dois rankings.

    Os rankings são listas de ids de música (permutações do mesmo conjunto).
    Devolve 0.0 para rankings idênticos e 1.0 para rankings invertidos:
    número de inversões dividido por n(n-1)/2.
    """
    if len(ranking_a) != len(ranking_b) or set(ranking_a) != set(ranking_b):
        raise ValueError("os rankings precisam conter as mesmas músicas")

    n = len(ranking_a)
    if n < 2:
        return 0.0

    # Reescreve A usando a posição de cada música em B; as inversões dessa
    # sequência são exatamente os pares em que A e B discordam.
    posicao_em_b = {musica: pos for pos, musica in enumerate(ranking_b)}
    sequencia = [posicao_em_b[musica] for musica in ranking_a]

    return contar_inversoes(sequencia) / (n * (n - 1) / 2)
