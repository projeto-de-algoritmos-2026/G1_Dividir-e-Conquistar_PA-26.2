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

## Inversões

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
