# Assinaturas das funções

Contrato de entrada e saída de cada módulo, para a integração no `main.py`.

## Dados (`src/dados.py`)

| Função | Entrada | Saída |
|---|---|---|
| `gerar_musicas(n, semente=42)` | `n`: quantidade de músicas | lista de `Musica(id, nome, energia, dancabilidade, duracao, plays)` |
| `gerar_usuarios(n_usuarios, n_musicas, semente=42)` | quantidade de usuários e de músicas | lista de `Usuario(id, ranking)`, `ranking` é uma permutação dos ids `0..n_musicas-1` |
| `salvar_csv(n, pasta)` | `n` e pasta de destino | caminhos de `musicas_n{n}.csv` e `usuarios_n{n}.csv` |

Campos: `energia` e `dancabilidade` em [0, 1]; `duracao` em segundos; `plays` inteiro.
Tamanhos usados: `TAMANHOS = (10, 100, 1000, 10000)`.

## Inversões (`src/inversoes.py`)

| Função | Entrada | Saída |
|---|---|---|
| `contar_inversoes(lista)` | lista de valores comparáveis | `int`: número de pares `(i, j)`, `i < j`, com `lista[i] > lista[j]` |
| `similaridade(ranking_a, ranking_b)` | dois rankings (listas de ids, mesmo conjunto) | `float` em [0, 1]: inversões / `n(n-1)/2` (0 = idênticos, 1 = invertidos) |

## Par mais próximo (`src/par_proximo.py`)

| Função | Entrada | Saída |
|---|---|---|
| `par_mais_proximo(pontos)` | lista de pontos `(x, y)` | `(p1, p2, distancia)` |
| `musicas_mais_parecidas(musicas)` | lista de `Musica` | `(musica_1, musica_2, distancia)` usando `(energia, dancabilidade)` |

## Mediana das medianas (`src/mediana.py`)

| Função | Entrada | Saída |
|---|---|---|
| `selecionar(valores, k)` | lista de números e `k` (0-indexado) | o k-ésimo menor valor |
| `mediana(valores)` | lista de números | a mediana |
| `percentil(valores, p)` | lista de números e `p` em [0, 100] | valor no percentil `p`, com interpolação linear (igual a `numpy.percentile`) |

`selecionar` levanta `IndexError` se `k` estiver fora de `[0, n)`; `mediana` e `percentil` levantam `ValueError` para lista vazia (e `percentil` também para `p` fora de [0, 100]).
