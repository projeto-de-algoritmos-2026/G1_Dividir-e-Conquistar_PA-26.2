"""Mede os três algoritmos e gera CSV e gráfico log-log."""

import csv
import math
import random
import statistics
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dados import TAMANHOS, gerar_musicas
from inversoes import contar_inversoes
from mediana import mediana
from par_proximo import musicas_mais_parecidas

PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"
CAMINHO_CSV = PASTA_DADOS / "resultados_benchmark.csv"
CAMINHO_GRAFICO = PASTA_DADOS / "resultados_benchmark.png"
REPETICOES = 5


def _medir(funcao, repeticoes=REPETICOES):
    tempos = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        funcao()
        tempos.append(time.perf_counter() - inicio)
    return statistics.median(tempos)


def medir_tamanho(n, repeticoes=REPETICOES):
    rng = random.Random(42 + n)
    ranking = list(range(n))
    rng.shuffle(ranking)
    musicas = gerar_musicas(n)
    plays = [musica.plays for musica in musicas]

    return {
        "n": n,
        "inversoes_segundos": _medir(lambda: contar_inversoes(ranking), repeticoes),
        "par_proximo_segundos": _medir(lambda: musicas_mais_parecidas(musicas), repeticoes),
        "mediana_segundos": _medir(lambda: mediana(plays), repeticoes),
    }


def salvar_csv(resultados, caminho=CAMINHO_CSV):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=resultados[0].keys())
        escritor.writeheader()
        escritor.writerows(resultados)


def _curva_referencia(tamanhos, tempo_inicial, complexidade):
    base = complexidade(tamanhos[0])
    return [tempo_inicial * complexidade(n) / base for n in tamanhos]


def salvar_grafico(resultados, caminho=CAMINHO_GRAFICO):
    tamanhos = [resultado["n"] for resultado in resultados]
    series = {
        "Inversões medido": [r["inversoes_segundos"] for r in resultados],
        "Par próximo medido": [r["par_proximo_segundos"] for r in resultados],
        "Mediana medida": [r["mediana_segundos"] for r in resultados],
    }

    figura, eixo = plt.subplots(figsize=(8, 5))
    for rotulo, tempos in series.items():
        eixo.loglog(tamanhos, tempos, "o-", label=rotulo)

    n_log_n = lambda n: n * math.log2(n)
    linear = lambda n: n
    eixo.loglog(
        tamanhos,
        _curva_referencia(tamanhos, series["Inversões medido"][0], n_log_n),
        "--",
        label="Referência O(n log n) — inversões",
    )
    eixo.loglog(
        tamanhos,
        _curva_referencia(tamanhos, series["Par próximo medido"][0], n_log_n),
        "--",
        label="Referência O(n log n) — par próximo",
    )
    eixo.loglog(
        tamanhos,
        _curva_referencia(tamanhos, series["Mediana medida"][0], linear),
        "--",
        label="Referência O(n) — mediana",
    )
    eixo.set(title="Crescimento empírico dos algoritmos", xlabel="n", ylabel="Tempo (s)")
    eixo.grid(True, which="both", linestyle=":", alpha=0.5)
    eixo.legend(fontsize=8)
    figura.tight_layout()
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(caminho, dpi=160)
    plt.close(figura)


def executar_benchmark(tamanhos=TAMANHOS, repeticoes=REPETICOES):
    resultados = []
    print("n       inversões (s)   par próximo (s)   mediana (s)")
    for n in tamanhos:
        resultado = medir_tamanho(n, repeticoes)
        resultados.append(resultado)
        print(
            f"{n:<7} {resultado['inversoes_segundos']:<15.6f} "
            f"{resultado['par_proximo_segundos']:<17.6f} "
            f"{resultado['mediana_segundos']:.6f}"
        )
    salvar_csv(resultados)
    salvar_grafico(resultados)
    print(f"\nCSV: {CAMINHO_CSV}")
    print(f"Gráfico: {CAMINHO_GRAFICO}")
    return resultados


if __name__ == "__main__":
    executar_benchmark()
