import random
import statistics

import numpy as np
import pytest

from mediana import mediana, percentil, selecionar


def test_selecionar_igual_ao_sorted_em_entradas_aleatorias():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 120)
        valores = [rng.randint(-50, 50) for _ in range(n)]
        esperado = sorted(valores)
        for k in rng.sample(range(n), min(n, 5)):
            assert selecionar(valores, k) == esperado[k]


def test_selecionar_todas_as_posicoes_de_lista_grande():
    rng = random.Random(2)
    valores = [rng.random() for _ in range(500)]
    esperado = sorted(valores)
    assert [selecionar(valores, k) for k in range(500)] == esperado


@pytest.mark.parametrize("n", [5, 6, 7, 10, 11, 100, 101])
def test_mediana_tamanho_par_e_impar(n):
    valores = list(range(n, 0, -1))
    assert mediana(valores) == statistics.median(valores)


def test_mediana_par_e_media_dos_dois_do_meio():
    assert mediana([1, 2, 3, 4]) == 2.5
    assert mediana([10, 20]) == 15


def test_valores_repetidos():
    assert mediana([7] * 50) == 7
    assert selecionar([3, 1, 3, 3, 2, 3, 3, 1, 3], 4) == 3
    valores = [1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 1, 1] * 5
    esperado = sorted(valores)
    for k in range(len(valores)):
        assert selecionar(valores, k) == esperado[k]


def test_lista_com_um_elemento():
    assert selecionar([42], 0) == 42
    assert mediana([42]) == 42
    assert percentil([42], 90) == 42


def test_entrada_ja_ordenada_e_invertida():
    crescente = list(range(1000))
    assert selecionar(crescente, 250) == 250
    assert selecionar(crescente[::-1], 250) == 250


def test_nao_altera_a_lista_de_entrada():
    valores = [5, 3, 9, 1, 7, 2, 8, 4, 6, 0, 11, 10]
    copia = list(valores)
    selecionar(valores, 3)
    mediana(valores)
    assert valores == copia


def test_outlier_extremo_mediana_quase_nao_muda_media_dispara():
    base = [100, 120, 130, 140, 150, 160, 170, 180, 190]
    com_outlier = base + [10_000_000]

    assert mediana(com_outlier) - mediana(base) < 20
    assert statistics.mean(com_outlier) > 100 * statistics.mean(base)


def test_k_fora_do_intervalo_e_lista_vazia():
    with pytest.raises(IndexError):
        selecionar([1, 2, 3], 3)
    with pytest.raises(IndexError):
        selecionar([1, 2, 3], -1)
    with pytest.raises(IndexError):
        selecionar([], 0)
    with pytest.raises(ValueError):
        mediana([])
    with pytest.raises(ValueError):
        percentil([], 50)


@pytest.mark.parametrize("p", [0, 10, 25, 50, 75, 90, 99, 100])
def test_percentil_bate_com_numpy(p):
    rng = random.Random(3)
    valores = [rng.randint(0, 1000) for _ in range(101)]
    assert percentil(valores, p) == pytest.approx(np.percentile(valores, p))
    valores_par = valores[:100]
    assert percentil(valores_par, p) == pytest.approx(np.percentile(valores_par, p))


def test_percentil_50_e_a_mediana_e_p_invalido():
    valores = [4, 8, 15, 16, 23, 42]
    assert percentil(valores, 50) == mediana(valores)
    with pytest.raises(ValueError):
        percentil(valores, 101)
    with pytest.raises(ValueError):
        percentil(valores, -1)
