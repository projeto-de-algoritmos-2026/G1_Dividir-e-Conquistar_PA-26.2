# G1_Dividir-e-Conquistar_PA-26.2

Trabalho 3 de Projeto e Análise de Algoritmos: um sistema de streaming de música que usa três algoritmos de dividir e conquistar para recomendar usuários e músicas parecidos e entender o comportamento típico de escuta.

| Algoritmo | Aplicação | Complexidade |
|---|---|---|
| Contagem de inversões | Similaridade entre usuários (Kendall tau) | O(n log n) |
| Par de pontos mais próximo | Músicas mais parecidas (energia × dançabilidade) | O(n log n) |
| Mediana das medianas | Duração e plays típicos, robusto a outliers | O(n) |

## Estrutura

```
├── src/
│   ├── inversoes.py
│   ├── par_proximo.py
│   ├── mediana.py
│   ├── dados.py
│   ├── main.py
│   └── benchmark.py
├── data/
├── tests/
├── docs/
└── README.md
```

As assinaturas das funções estão em [docs/assinaturas.md](docs/assinaturas.md).

## Como executar

```bash
pip install -r requirements.txt
pytest
python src/dados.py   # gera os CSVs de n = 10, 100, 1000 e 10000 em data/
```

---

## 1. Introdução

Serviços de streaming guardam muita informação sobre músicas e ouvintes: o que cada usuário prefere, como cada faixa soa e quantas vezes ela foi tocada. Para transformar isso em recomendação é preciso responder, rápido e com milhares de itens, perguntas como "quais usuários têm gosto parecido?", "quais músicas são quase iguais?" e "qual é a duração típica de uma faixa?".

Este trabalho resolve essas três perguntas com algoritmos de dividir e conquistar, que dividem o problema em partes menores, resolvem cada parte e combinam os resultados. Cada pergunta usa um algoritmo clássico, e cada um tem uma única implementação, a de dividir e conquistar.

## 2. Problema

O serviço de streaming quer:

1. **Recomendar usuários parecidos.** Dados os rankings de músicas de dois usuários, medir o quanto eles discordam. Isso é contar os pares de músicas que aparecem em ordem oposta nos dois rankings.
2. **Recomendar músicas parecidas.** Cada música é descrita por duas características (energia e dançabilidade), então vira um ponto no plano. Achar as duas músicas mais próximas entre milhares de pontos, sem comparar todos os pares.
3. **Entender o comportamento típico de escuta.** Achar a duração e o número de plays típicos, sem que algumas músicas com valores absurdos distorçam o resultado.

## 3. Objetivo

- Implementar e testar os três algoritmos de dividir e conquistar: contagem de inversões, par de pontos mais próximo e mediana das medianas.
- Mostrar, para cada um, a estratégia, a recorrência e as complexidades de tempo e espaço.
- Integrar os três num fluxo único sobre dados de streaming gerados com semente fixa.
- Medir os tempos para n = 10, 100, 1.000 e 10.000 e comparar o crescimento medido com a teoria.

## 4. Entrada

Os dados são gerados por [src/dados.py](src/dados.py), com semente fixa (42), então qualquer execução produz os mesmos dados. Os tamanhos são n = 10, 100, 1.000 e 10.000.

| Entidade | Campos |
|---|---|
| **Música** | `id`, `nome`, `energia` (0 a 1), `dancabilidade` (0 a 1), `duracao` (segundos), `plays` |
| **Usuário** | `id`, `ranking`: permutação dos ids das n músicas, da preferida para a menos preferida |

Cada algoritmo recebe:

| Algoritmo | Entrada |
|---|---|
| Inversões | Dois rankings de usuários (listas de ids de músicas) |
| Par mais próximo | Lista de músicas, usando `(energia, dancabilidade)` como ponto |
| Mediana das medianas | Lista de durações ou de plays, mais `k` ou `p` |

`python src/dados.py` grava os dados em `data/musicas_n{n}.csv` e `data/usuarios_n{n}.csv`.

## 5. Saída

O fluxo completo (`python src/main.py`) mostra no terminal:

- os dois usuários mais parecidos e a similaridade entre eles (0 = rankings idênticos, 1 = invertidos);
- o par de músicas mais parecidas e a distância entre elas;
- a mediana e alguns percentis de duração e de plays.

As funções devolvem:

| Função | Saída |
|---|---|
| `contar_inversoes(lista)` | `int`, número de inversões |
| `similaridade(a, b)` | `float` em [0, 1] |
| `par_mais_proximo(pontos)` | `(p1, p2, distancia)` |
| `selecionar(valores, k)` | o k-ésimo menor valor |
| `mediana(valores)` / `percentil(valores, p)` | `float` ou `int` com o valor típico |

## 6. Inversões

**Problema.** Dados dois rankings de músicas feitos por usuários diferentes, medir o quanto eles discordam. Contar os pares de músicas que aparecem em ordem oposta nos dois rankings (distância de Kendall tau). Reescrevendo o ranking A com a posição de cada música no ranking B, isso vira contar as inversões de uma sequência: pares `i < j` com `a[i] > a[j]`.

**Estratégia (Sort-and-Count).**

- **Dividir:** separar a lista em duas metades.
- **Conquistar:** contar recursivamente as inversões de cada metade, que volta ordenada.
- **Combinar:** fazer o merge das duas metades ordenadas. Cada vez que um elemento da direita é escolhido antes de elementos que ainda restam na esquerda, ele forma inversão com todos eles. Basta somar `len(esquerda) - i`.

O merge ordena e conta ao mesmo tempo, então cada nível da recursão custa O(n). A versão que reordena a lista a cada nível custaria O(n log² n), e por isso não foi usada.

**Recorrência.**

T(n) = 2T(n/2) + O(n), que resolve para **O(n log n)** no tempo (Teorema Mestre, caso 2).

**Espaço.** O(n): as listas auxiliares do merge, mais a pilha de recursão de profundidade O(log n).

**Similaridade.** `similaridade(a, b)` divide o número de inversões por n(n-1)/2, o máximo possível. Dá 0 para rankings idênticos e 1 para rankings invertidos.

**Testes.** Lista ordenada (0 inversões), lista invertida (n(n-1)/2), exemplo do slide `1 5 4 8 10 2 6 9 12 11 3 7` (22), lista vazia e com um elemento (0), valores repetidos e propriedades da similaridade.

## 7. Par mais próximo

_Seção a ser preenchida junto com a implementação de `src/par_proximo.py`._

## 8. Mediana das medianas

**Problema.** Achar a duração e o número de plays típicos das músicas. A média não serve: uma única música viral com milhões de plays puxa a média para cima. A mediana (o valor do meio) é robusta a esses outliers. Ordenar tudo para achá-la custa O(n log n), mas o algoritmo de seleção acha o k-ésimo menor valor em **O(n)**.

**Estratégia (select com grupos de 5).** Para achar o k-ésimo menor valor de uma lista:

1. **Dividir** a lista em grupos de 5 elementos.
2. Tirar a **mediana de cada grupo** (custo constante por grupo, O(n) no total).
3. Achar, recursivamente, a **mediana dessas medianas**. Ela é o pivô.
4. **Particionar** a lista em L (menores que o pivô), os iguais ao pivô e R (maiores).
5. **Descer só no lado certo**: se k cai em L, repetir em L; se cai nos iguais, o pivô é a resposta; senão, repetir em R com k ajustado.

Os valores iguais ao pivô são tratados à parte, para a recursão sempre progredir mesmo com muitas repetições.

**Por que o pivô é bom (entre 3n/10 e 7n/10).** Há n/5 grupos, e o pivô é a mediana das medianas, então metade dos grupos (n/10 grupos) tem a mediana menor ou igual ao pivô. Em cada um desses grupos, 3 dos 5 elementos (a mediana e os 2 menores que ela) são menores ou iguais ao pivô. Logo pelo menos 3 · n/10 = 3n/10 elementos são ≤ pivô. Pelo mesmo argumento no sentido contrário, pelo menos 3n/10 são ≥ pivô. Isso significa que L e R têm no máximo 7n/10 elementos cada, então a recursão do passo 5 nunca fica com mais de 7n/10 da lista.

**Recorrência.**

T(n) ≤ T(n/5) + T(7n/10) + O(n)

- T(n/5): achar a mediana das medianas (passo 3).
- T(7n/10): descer no lado maior da partição (passo 5).
- O(n): montar os grupos, as medianas e a partição.

Como n/5 + 7n/10 = 9n/10 < n, a soma dos tamanhos dos subproblemas é uma fração fixa de n. Os custos por nível formam uma série geométrica de razão 9/10, que soma no máximo 10 · cn, então T(n) = **O(n)**.

**Por que grupos de 3 não dão linear.** Com grupos de 3 o argumento de contagem dá apenas n/3 grupos, e cada grupo "bom" contribui com 2 de 3 elementos: pelo menos 2 · n/6 = n/3 elementos de cada lado, ou seja, a partição pode ficar em até 2n/3. A recorrência vira T(n) ≤ T(n/3) + T(2n/3) + O(n). Aqui n/3 + 2n/3 = n: os subproblemas somam o tamanho original e cada nível da recursão ainda custa O(n), com O(log n) níveis. O resultado é O(n log n), igual a ordenar. Com grupos de 5, a soma 9n/10 < n é o que faz a série convergir e dá o tempo linear.

**Espaço.** O(n): as listas L, R e as medianas dos grupos, mais a pilha de recursão de profundidade O(log n).

**Funções.**

- `selecionar(valores, k)`: k-ésimo menor valor (k começa em 0).
- `mediana(valores)`: valor do meio, ou média dos dois do meio se n é par.
- `percentil(valores, p)`: percentil p (0 a 100) com interpolação linear, igual a `numpy.percentile`. Sendo assim, `percentil(v, 50) == mediana(v)`.

Elas são aplicadas à duração e aos plays das músicas.

**Testes.** Resultado igual a `sorted(x)[k]` em entradas aleatórias (a ordenação é usada só como conferência dentro do teste), tamanho par e ímpar, valores repetidos, lista com um elemento, entrada já ordenada, uma lista com outlier extremo (a mediana quase não muda e a média dispara), erros para `k` fora do intervalo e lista vazia, e percentis conferidos contra `numpy.percentile`.
