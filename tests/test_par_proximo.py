import math

import pytest

from dados import Musica
from par_proximo import musicas_mais_parecidas, par_mais_proximo


def test_dois_e_tres_pontos():
    assert par_mais_proximo([(0, 0), (3, 4)]) == ((0, 0), (3, 4), 5.0)
    a, b, distancia = par_mais_proximo([(0, 0), (10, 10), (11, 10)])
    assert {a, b} == {(10, 10), (11, 10)}
    assert distancia == 1.0


def test_pontos_em_linha_reta():
    a, b, distancia = par_mais_proximo([(0, 0), (4, 0), (7, 0), (20, 0)])
    assert {a, b} == {(4, 0), (7, 0)}
    assert distancia == 3.0


def test_pontos_duplicados_tem_distancia_zero():
    a, b, distancia = par_mais_proximo([(2, 3), (0, 0), (2, 3), (10, 10)])
    assert a == b == (2, 3)
    assert distancia == 0.0


def test_par_mais_proximo_cruza_a_divisao():
    pontos = [(-10, 0), (-1, 1), (1, 1.1), (10, 0)]
    a, b, distancia = par_mais_proximo(pontos)
    assert {a, b} == {(-1, 1), (1, 1.1)}
    assert distancia == pytest.approx(math.hypot(2, 0.1))


def test_musicas_usam_energia_e_dancabilidade():
    musicas = [
        Musica(1, "A", 0.1, 0.1, 200, 10),
        Musica(2, "B", 0.9, 0.9, 210, 20),
        Musica(3, "C", 0.11, 0.12, 220, 30),
    ]
    a, b, distancia = musicas_mais_parecidas(musicas)
    assert {a.id, b.id} == {1, 3}
    assert distancia == pytest.approx(math.hypot(0.01, 0.02))


def test_exige_pelo_menos_dois_pontos():
    with pytest.raises(ValueError):
        par_mais_proximo([])
    with pytest.raises(ValueError):
        par_mais_proximo([(0, 0)])
