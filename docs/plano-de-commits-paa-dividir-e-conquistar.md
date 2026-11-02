# Plano de Commits: PAA 3 (Streaming de música)

**Equipe:** Maria e Ana
**Entrega:** 02/11 (segunda)
**Algoritmos (só a versão Dividir e Conquistar):** Contagem de inversões, Mediana das medianas, Par de pontos mais próximo

**Regras:**
- **4 commits no total:** Maria faz os 2 primeiros, Ana faz os 2 últimos.
- Os commits seguem a ordem abaixo, porque cada um depende do anterior (estrutura → algoritmos → integração → entrega).
- Sem versão ingênua nem alternativas: cada algoritmo tem uma única implementação, a de dividir e conquistar.
- Cada pessoa escreve no README a seção do algoritmo que implementou, no mesmo commit (estratégia, recorrência, complexidade).
- Código novo só entra até o commit 4. Depois dele, só revisão, vídeo e submissão.

---

## Visão geral

| # | Responsável | Commit | Entrega |
|---|---|---|---|
| 1 | Maria | `feat: estrutura inicial e contagem de inversões` | Repo + dados + Inversões |
| 2 | Maria | `feat: mediana das medianas` | MoM + testes + README (seções 1 a 5) |
| 3 | Ana | `feat: par de pontos mais próximo` | Par próximo + testes |
| 4 | Ana | `feat: integração, benchmark e entrega final` | `main.py` + experimentos + README completo + vídeo + submissão |

**Fluxo do sistema:**

```
Usuários → INVERSÕES → usuários mais parecidos
Músicas  → PAR MAIS PRÓXIMO → músicas mais parecidas
Músicas  → MEDIANA DAS MEDIANAS → duração e plays típicos
```

**Cenário:** o serviço de streaming quer recomendar usuários e músicas parecidos e entender o comportamento típico de escuta.

| Algoritmo | Aplicação | Complexidade |
|---|---|---|
| Inversões | Similaridade entre usuários (Kendall tau): nº de inversões entre dois rankings de músicas | T(n) = 2T(n/2) + O(n) = O(n log n) |
| Par mais próximo | Músicas mais parecidas em 2 features (energia × dançabilidade) | T(n) = 2T(n/2) + O(n) = O(n log n) |
| Mediana das medianas | Duração e plays típicos, robusto a outliers | T(n) = T(n/5) + T(7n/10) + O(n) = O(n) |

---

## Commit 1: Maria

### `feat: estrutura inicial e contagem de inversões`

**Estrutura (faça primeiro e dê push cedo, é o que destrava a Ana):**
- Criar o repositório no GitHub e adicionar a Ana como colaboradora
- Criar a estrutura de pastas:

```
streaming-paa/
├── src/
│   ├── inversoes.py
│   ├── par_proximo.py
│   ├── mediana.py
│   ├── dados.py
│   ├── main.py
│   └── benchmark.py
├── data/
├── tests/
└── README.md
```

- Criar `requirements.txt` (numpy, matplotlib, pytest) e `.gitignore`
- Definir o formato dos dados:
  - **Música:** id, nome, energia (0 a 1), dançabilidade (0 a 1), duração (s), plays
  - **Usuário:** id, ranking de n músicas (permutação)
- Implementar `dados.py` com gerador aleatório com semente fixa (n = 10, 100, 1.000 e 10.000)
- Escrever `assinaturas.md` com entrada e saída das funções:
  - `contar_inversoes(lista) -> int`
  - `par_mais_proximo(pontos) -> (p1, p2, distancia)`
  - `selecionar(valores, k) -> valor` e `mediana(valores) -> valor`

**Inversões:**
- Sort-and-Count O(n log n): o merge ordena e conta ao mesmo tempo. Não usar a versão do slide 20, que reordena a cada nível e vira O(n log² n)
- Função `similaridade(ranking_a, ranking_b)` normalizada por n(n-1)/2 (0 = idênticos, 1 = invertidos)
- Testes (com resultado conhecido, sem precisar de outra implementação):
  - lista ordenada = 0
  - lista invertida = n(n-1)/2
  - exemplo do slide `1 5 4 8 10 2 6 9 12 11 3 7` = 22
  - lista vazia e lista com 1 elemento = 0
- README: seção "Inversões" (estratégia dividir, conquistar, combinar; recorrência; espaço O(n))

**Saída esperada:** `pip install -r requirements.txt` roda, `pytest` passa, o gerador cria os 4 tamanhos de dados.

---

## Commit 2: Maria

### `feat: mediana das medianas`
- Select com grupos de 5: dividir em grupos, mediana de cada grupo, mediana das medianas (recursivo) como pivô, particionar em L e R, descer no lado certo
- Funções `selecionar(valores, k)`, `mediana(valores)` e `percentil(valores, p)`, aplicadas a duração e plays
- Testes (usar `sorted(x)[k]` só como conferência dentro do teste):
  - resultado igual a `sorted(x)[k]` em entradas aleatórias
  - tamanho par e ímpar
  - valores repetidos
  - lista com 1 elemento
  - lista com um outlier extremo: mediana quase não muda, média dispara
- README: seção "Mediana das medianas" (estratégia, por que o pivô garante entre 3n/10 e 7n/10, recorrência, por que grupos de 3 não dão linear)
- README: completar as seções que não dependem do `main.py`: 1 Introdução, 2 Problema, 3 Objetivo, 4 Entrada, 5 Saída

**Saída esperada:** `pytest` passa, README com as seções 1 a 5 e as seções de Inversões e Mediana das medianas.

---

## Commit 3: Ana

### `feat: par de pontos mais próximo`
- Ordenar por x uma vez no começo
- Recursão devolve o menor δ e a lista de pontos ordenada por y (merge), mantendo O(n log n)
- Faixa de 2δ em volta da linha de divisão, checando cada ponto com os próximos 7 vizinhos na ordem por y (5 já bastam na prática)
- Função `musicas_mais_parecidas(musicas)` que devolve o par e a distância (usar energia e dançabilidade)
- Testes (resultados conhecidos):
  - 2 e 3 pontos
  - pontos em linha reta
  - pontos duplicados (distância 0)
  - par mais próximo cruzando a linha de divisão (caso que a faixa existe para resolver)
  - exemplo pequeno resolvido à mão
- README: seção "Par mais próximo" (estratégia, por que 7 vizinhos bastam, recorrência, espaço O(n))

**Saída esperada:** `pytest` passa, a função roda em 10.000 pontos em poucos segundos.

---

## Commit 4: Ana

### `feat: integração, benchmark e entrega final`

**Integração e testes:**
- `main.py` com o fluxo completo e saída no terminal:
  - Usuários mais parecidos → músicas mais parecidas → duração e plays típicos
- Revisar a cobertura de testes dos três módulos e corrigir bugs (se mexer em algoritmo da Maria, avisar)
- Ler o código da Maria com olhar de revisão e remover código morto

**Benchmark:**
- `benchmark.py`: medir o tempo dos três algoritmos com n = 10, 100, 1.000 e 10.000, salvar em `data/resultados_benchmark.csv`
- Gráfico log-log do tempo vs n, com as retas de referência n log n (inversões e par) e n (mediana), para mostrar que o crescimento medido bate com a teoria

**README final:**
- Seção "Resultados experimentais" com a tabela e o gráfico, comentando se a inclinação medida bate com a teoria
- Seções 10 Conclusão e 11 Exemplo de execução
- Ler o README inteiro como alguém que nunca viu o projeto

**Vídeo (as duas juntas, é a única atividade que exige as duas):**
- Ensaiar uma vez, gravar a tela com o programa rodando de verdade (5 a 7 min)

| Tempo | Conteúdo | Quem |
|---|---|---|
| 00:00 - 00:40 | Problema e cenário | Maria |
| 00:40 - 01:30 | Estrutura do sistema e fluxo | Maria |
| 01:30 - 02:40 | Inversões | Maria |
| 02:40 - 04:00 | Par mais próximo | Ana |
| 04:00 - 05:00 | Mediana das medianas | Maria |
| 05:00 - 05:40 | Demonstração rodando | Ana |
| 05:40 - 06:40 | Resultados experimentais e conclusão | As duas |

**Entrega:**
- Subir o vídeo e colocar o link no README
- Conferir que o repositório é **público**, que o link do vídeo abre em aba anônima e que o histórico de commits mostra o trabalho das duas
- Clone novo + `pip install -r requirements.txt` + `pytest` + `main.py` + `benchmark.py`
- Submeter na planilha ou plataforma da disciplina

**Saída esperada:** `python src/main.py` e `python src/benchmark.py` rodam do zero, `pytest` passa, README completo, vídeo no ar, entrega submetida.

> **Se atrasar:** cortar o n = 10.000 do benchmark e depois o gráfico (manter só o CSV). Nunca cortar testes. Se o vídeo tiver problema (áudio, tela, tempo), regravar antes de submeter e não começar nada novo.

---

## Checklist final de entrega

- [ ] Repositório público, com as duas como autoras dos commits (Maria: commits 1 e 2; Ana: commits 3 e 4)
- [ ] `pip install -r requirements.txt` e `pytest` funcionam num clone novo
- [ ] `main.py` e `benchmark.py` rodam do zero
- [ ] README com as 11 seções, tabela de resultados e gráfico
- [ ] Para cada algoritmo: estratégia, recorrência, complexidade de tempo e espaço
- [ ] Vídeo gravado, link funcionando e referenciado no README
- [ ] Entrega submetida
