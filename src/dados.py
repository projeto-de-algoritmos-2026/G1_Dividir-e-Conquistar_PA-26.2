"""Formato dos dados e gerador aleatório com semente fixa.

Música:  id, nome, energia (0 a 1), dançabilidade (0 a 1), duração (s), plays
Usuário: id, ranking de n músicas (permutação dos ids das músicas)

Uso: python src/dados.py  -> grava os CSVs de n = 10, 100, 1000 e 10000 em data/
"""

import csv
import random
from dataclasses import dataclass
from pathlib import Path

TAMANHOS = (10, 100, 1000, 10000)
SEMENTE = 42
USUARIOS_POR_TAMANHO = 5
PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"


@dataclass(frozen=True)
class Musica:
    id: int
    nome: str
    energia: float
    dancabilidade: float
    duracao: int
    plays: int


@dataclass(frozen=True)
class Usuario:
    id: int
    ranking: tuple  # ids das músicas, da preferida para a menos preferida


def gerar_musicas(n, semente=SEMENTE):
    """Gera n músicas aleatórias, sempre as mesmas para a mesma semente."""
    rng = random.Random(semente)
    return [
        Musica(
            id=i,
            nome=f"Musica {i}",
            energia=rng.random(),
            dancabilidade=rng.random(),
            duracao=rng.randint(60, 600),
            plays=int(rng.lognormvariate(8, 2)),
        )
        for i in range(n)
    ]


def gerar_usuarios(n_usuarios, n_musicas, semente=SEMENTE):
    """Gera n_usuarios rankings, cada um uma permutação dos ids 0..n_musicas-1."""
    rng = random.Random(semente)
    usuarios = []
    for i in range(n_usuarios):
        ranking = list(range(n_musicas))
        rng.shuffle(ranking)
        usuarios.append(Usuario(id=i, ranking=tuple(ranking)))
    return usuarios


def salvar_csv(n, pasta=PASTA_DADOS, semente=SEMENTE):
    """Grava musicas_n{n}.csv e usuarios_n{n}.csv e devolve os dois caminhos."""
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    caminho_musicas = pasta / f"musicas_n{n}.csv"
    with open(caminho_musicas, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "nome", "energia", "dancabilidade", "duracao", "plays"])
        for m in gerar_musicas(n, semente):
            w.writerow([m.id, m.nome, f"{m.energia:.6f}", f"{m.dancabilidade:.6f}", m.duracao, m.plays])

    caminho_usuarios = pasta / f"usuarios_n{n}.csv"
    with open(caminho_usuarios, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "ranking"])
        for u in gerar_usuarios(USUARIOS_POR_TAMANHO, n, semente):
            w.writerow([u.id, " ".join(map(str, u.ranking))])

    return caminho_musicas, caminho_usuarios


if __name__ == "__main__":
    for n in TAMANHOS:
        musicas, usuarios = salvar_csv(n)
        print(f"n = {n:>6}: {musicas.name}, {usuarios.name}")
