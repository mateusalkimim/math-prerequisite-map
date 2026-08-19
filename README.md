# O mapa das matérias — a ordem lógica do ciclo básico

Um mapa interativo de **pré-requisitos** da matemática do ciclo básico: 39
matérias, 56 dependências, cada seta declarando de qual obra ela saiu. Clicar
numa matéria acende toda a cadeia que a sustenta, até a aritmética.

**→ [Abrir o mapa](https://mateusalkimim.github.io/math-prerequisite-map/)**

> **Estado: PROPOSTA.** O grafo é uma afirmação sobre o que precede o quê, e
> ainda não foi ratificado — é rascunho com fonte, não material de aula. Está
> publicado assim de propósito: uma seta errada manda o aluno estudar a coisa
> errada, e é melhor que ela seja contestada do que aceita em silêncio.
> Discordâncias são bem-vindas nas issues.

Um mapa da **ordem lógica** das matérias — não a histórica, não a curricular. As
três ordens já estavam distinguidas na `fig-tres-ordens` do
um mapa da genealogia histórica (documento irmão, não publicado); este documento leva **a terceira**
até o fim, e a torna instrumento.

**Para que serve**: projetar na tela e apontar onde um aluno travou. Clicar numa
matéria acende **toda a cadeia que a sustenta**, até a aritmética — e mostra, no
painel, de onde veio cada seta.

```bash
python3 gerar_mapa.py     # regenera o HTML (autossuficiente, abre sem servidor)
```

Abrir já apontando: `mapa-materias.html#integral` — o link fica pronto antes da
aula. Os identificadores estão em `materias.py`.

## O que o mapa mede

| | |
|---|---|
| matérias | **39** em **10 camadas** |
| dependências | **56** |
| cruzamentos de aresta | **131 → 11** |

## Nenhuma seta entra sem dizer de onde veio

O mapa vai apontar onde um aluno travou: **uma seta errada manda o aluno estudar
a coisa errada.** Por isso cada dependência carrega sua classe de warrant, e ela
aparece no desenho e no painel:

- **definição** (26) — X entra na *definição* de Y na obra citada. É a seta
  forte: dependência lógica, não conveniência de currículo. *A derivada é
  definida como um limite* (Guidorizzi §7.2);
- **ordem do livro** (17) — X é definido antes de Y na mesma obra, e Y o usa.
  Precedência consolidada, evidência mais fraca;
- **fronteira** (14) — matéria que **o acervo do Mouseion não cobre**. O nó
  aparece porque o mapa precisa mostrar para onde as estradas vão; a seta é
  julgamento declarado, desenhada em traço fraco. É honestidade, não decoração.

Obras (todas em `mouseion/_dissecado/`): **Guidorizzi** v.1 (classe A, TOC de
157) · **Elon Lages Lima** (classe A) · **Callioli** (classe B — scan sem TOC, e
a ficha do acervo pede conferir se é parcial; por isso só sustenta aresta de
*ordem*, nunca de *definição*) · **Merzbach & Boyer** (classe A, TOC de 300).

## Os três troncos, em RGB

A matemática do ciclo básico se organiza, aqui, em três troncos, e o mapa os
mostra por **forma** e por **cor**:

| tronco | forma | cor |
|---|---|---|
| **Cálculo** (I, II, III) | laterais arredondadas | **R** — vermelho |
| **Álgebra Linear** | hexágono (o nó de tempo do Nuke) | **G** — verde |
| **Geometria Analítica** | cantos vivos | **B** — azul |
| **dois troncos** | cantos chanfrados | a **soma** das duas luzes |
| **a base** | canto suave | ouro — anterior aos três |

A cor **soma como luz soma**: cálculo + álgebra = amarelo, cálculo + geometria =
magenta, álgebra + geometria = ciano. O **mapa RGB** fica na lateral da página,
sempre visível — sem ele a mistura seria enfeite, e a norma passou a exigi-lo.

**Pertencer a um tronco não é depender dele.** *Cálculo de várias variáveis*
depende de vetores (geometria) mas pertence ao Cálculo. A aresta diz de quem se
depende; a forma diz onde a matéria é ensinada. As duas informações são
diferentes e o mapa mostra as duas ao mesmo tempo.

## As linhas não têm diagonal

Só horizontal, vertical e L, por decisão de desenho. Cada trecho vira um **Z**
(desce, anda, desce), com o degrau afastado dentro do vão entre camadas para que
duas arestas não se deitem uma sobre a outra. Medido no SVG gerado: **0
segmentos diagonais em 56 arestas**.

## A norma, citada onde foi aplicada

Sob uma norma de diagramas própria (documento irmão, não publicado):

- **§1.1 — cruzamento é o defeito nº 1** (Purchase 1997) e vence qualquer outra
  regra em conflito. Por isso o layout **não é desenhado, é medido**: camadas por
  caminho mais longo, nós virtuais nas arestas que pulam camada, baricentro
  iterado, e a contagem no rodapé da própria página. Regra sem medida é
  preferência;
- **§1.2 — a direção se declara uma vez e não se mistura.** Aqui é **de cima
  para baixo**, dito no cabeçalho da página: o pré-requisito fica sempre acima de
  quem o exige;
- **§1.3 — kit de três formas.** Retângulo arredondado para matéria, oval para a
  raiz (terminador de início). **Losango não aparece porque não há decisão** no
  mapa. Nenhuma forma inventada;
- **§1.4 — o nó é caixa, nunca ponto**, com o rótulo dentro. *"Ponto obriga a ler
  legenda; caixa se lê de uma vez"*;
- **§1.5 — modularidade por ocultação.** Escolhida uma matéria, o resto **apaga
  em vez de sumir**: o contexto continua visível, o foco não;
- **§2 — a gramática.** O ouro é o fluxo. As três classes de warrant se
  distinguem por peso e traço, declaradas na legenda do rodapé;
- **§4 — a armadilha do SVG.** A página foi medida em **1366×768 e 1920×1080**.

## Dois defeitos que o próprio instrumento pegou

1. **Um ciclo no meu modelo.** `sistemas → matrizes → determinante → sistemas`. O
   determinante *decide* um sistema (invertibilidade, Cramer), mas não é
   pré-requisito para **definir** sistema. Era confusão entre **"usa"** e
   **"precede"** — e um grafo de pré-requisitos que tem ciclo está errado por
   construção. A aresta saiu, com o motivo escrito em `materias.py`;
2. **O alinhamento que eu quis fazer, e a medida derrubou.** Com as arestas
   ortogonais, as linhas longas passaram a correr pelas bordas formando
   *molduras* em volta do desenho. Escrevi um alinhamento de coordenada (puxar
   cada nó para o baricentro dos vizinhos) e medi antes de adotar: o comprimento
   das arestas caiu **1,4%** e a largura subiu **64%** (1.572 → 2.581 px). Ideia
   descartada, código mantido em `layout.py` com o número escrito. **O que
   rendeu de verdade foi banal**: dar um vão menor entre dois nós virtuais
   vizinhos (7 px em vez de 20);
3. **Nó virtual não é caixa.** Na 1ª geração ele ocupava a largura de uma caixa
   inteira, o que inflava o desenho para 2484 px e fazia as arestas longas
   desviarem até a borda — bicos que a medida de cruzamento **não pegava**,
   porque cruzamento não é a mesma coisa que desvio. O olho pegou. Corrigido, a
   largura caiu para **1668 px**.

## O que este mapa NÃO faz

- **não é ordem de currículo** — a §1.2 vale para o desenho, não para a
  secretaria. Que a álgebra linear elementar (sistemas, matrizes, determinantes)
  não dependa de limite é um fato do grafo, não uma sugestão de grade horária;
- **não cobre a fronteira com fonte** — análise funcional, topologia, medida,
  geometria diferencial e álgebra abstrata estão no mapa **sem obra por baixo**.
  Fechar isso pede livro no acervo, não mais desenho;
- **não mede aprendizagem.** Apontar onde o aluno travou é hipótese do professor
  na hora; o mapa organiza a conversa, não a diagnostica.

## Licença

- **Código** (`gerar_mapa.py`, `layout.py`, `materias.py`) — [MIT](LICENSE).
  O arquivo `LICENSE` traz o texto MIT puro, para que o GitHub o reconheça;
  a divisão de escopo entre código e conteúdo é esta seção.
- **Conteúdo** (o grafo, seus warrants e este README) —
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use, adapte e
  redistribua, inclusive comercialmente, citando a fonte.

As obras citadas como warrant são referências bibliográficas; nenhum texto delas
é reproduzido aqui.
