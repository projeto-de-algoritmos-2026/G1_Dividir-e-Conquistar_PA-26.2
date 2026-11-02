import pytest

from dados import TAMANHOS, gerar_musicas, gerar_usuarios, salvar_csv


def test_tamanhos_do_enunciado():
    assert TAMANHOS == (10, 100, 1000, 10000)


@pytest.mark.parametrize("n", TAMANHOS)
def test_gerador_cria_os_quatro_tamanhos(n):
    musicas = gerar_musicas(n)
    assert len(musicas) == n
    assert [m.id for m in musicas] == list(range(n))
    for m in musicas:
        assert 0 <= m.energia <= 1
        assert 0 <= m.dancabilidade <= 1
        assert m.duracao > 0
        assert m.plays >= 0


@pytest.mark.parametrize("n", TAMANHOS)
def test_ranking_de_usuario_e_permutacao(n):
    for u in gerar_usuarios(3, n):
        assert sorted(u.ranking) == list(range(n))


def test_semente_fixa_e_reprodutivel():
    assert gerar_musicas(100) == gerar_musicas(100)
    assert gerar_usuarios(3, 100) == gerar_usuarios(3, 100)
    assert gerar_musicas(100, semente=1) != gerar_musicas(100, semente=2)


def test_salvar_csv(tmp_path):
    musicas, usuarios = salvar_csv(10, pasta=tmp_path)
    assert len(musicas.read_text(encoding="utf-8").splitlines()) == 11
    assert len(usuarios.read_text(encoding="utf-8").splitlines()) > 1
