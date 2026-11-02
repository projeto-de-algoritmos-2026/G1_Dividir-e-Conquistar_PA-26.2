import random

import pytest

from inversoes import contar_inversoes, similaridade


def test_lista_vazia_e_um_elemento():
    assert contar_inversoes([]) == 0
    assert contar_inversoes([7]) == 0


def test_lista_ordenada_tem_zero_inversoes():
    assert contar_inversoes(list(range(100))) == 0


@pytest.mark.parametrize("n", [2, 3, 10, 101])
def test_lista_invertida_tem_n_n_menos_1_sobre_2(n):
    assert contar_inversoes(list(range(n, 0, -1))) == n * (n - 1) // 2


def test_exemplo_do_slide():
    assert contar_inversoes([1, 5, 4, 8, 10, 2, 6, 9, 12, 11, 3, 7]) == 22


def test_valores_repetidos_nao_contam_como_inversao():
    assert contar_inversoes([2, 2, 2]) == 0
    assert contar_inversoes([3, 1, 1]) == 2


def test_nao_altera_a_lista_de_entrada():
    lista = [3, 1, 2]
    contar_inversoes(lista)
    assert lista == [3, 1, 2]


def test_similaridade_rankings_identicos_e_invertidos():
    ranking = [4, 2, 9, 1, 7]
    assert similaridade(ranking, ranking) == 0.0
    assert similaridade(ranking, ranking[::-1]) == 1.0


def test_similaridade_uma_troca_adjacente():
    # um único par discordante entre 4 músicas: 1 / (4*3/2)
    assert similaridade([1, 2, 3, 4], [1, 3, 2, 4]) == pytest.approx(1 / 6)


def test_similaridade_e_simetrica():
    rng = random.Random(0)
    a = list(range(50))
    b = list(range(50))
    rng.shuffle(a)
    rng.shuffle(b)
    assert similaridade(a, b) == pytest.approx(similaridade(b, a))


def test_similaridade_trivial_para_menos_de_dois_elementos():
    assert similaridade([], []) == 0.0
    assert similaridade([5], [5]) == 0.0


def test_similaridade_rejeita_rankings_diferentes():
    with pytest.raises(ValueError):
        similaridade([1, 2, 3], [1, 2, 4])
    with pytest.raises(ValueError):
        similaridade([1, 2, 3], [1, 2])
