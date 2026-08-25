# O mapa das matérias — a ordem lógica do ciclo básico

Um mapa interativo de **pré-requisitos** da matemática do ciclo básico: 50
matérias, 78 dependências, cada seta declarando de onde ela saiu. Clicar
numa matéria acende toda a cadeia que a sustenta, até a linguagem dos conjuntos.

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
matéria acende **toda a cadeia que a sustenta**, até a linguagem dos conjuntos — e mostra, no
painel, de onde veio cada seta.

```bash
python3 gerar_mapa.py     # regenera o HTML (autossuficiente, abre sem servidor)
```

Abrir já apontando: `mapa-materias.html#integral` — o link fica pronto antes da
aula. Os identificadores estão em `materias.py`.

## O que o mapa mede

| | |
|---|---|
| matérias | **50** em **13 camadas** |
| dependências | **78** |
| cruzamentos de aresta | **102 → 41** |

## Nenhuma seta entra sem dizer de onde veio

O mapa vai apontar onde um aluno travou: **uma seta errada manda o aluno estudar
a coisa errada.** Por isso cada dependência carrega sua classe de warrant, e ela
aparece no desenho e no painel:

- **definição** (26) — X entra na *definição* de Y na obra citada. É a seta
  forte: dependência lógica, não conveniência de currículo. *A derivada é
  definida como um limite* (Guidorizzi §7.2);
- **ordem do livro** (29) — X é definido antes de Y na mesma obra, e Y o usa.
  Precedência consolidada, evidência mais fraca;
- **orientação acadêmica** (9) — a seta vem de **orientação registrada**, não
  de página conferível. Mais forte que a fronteira, porque há uma pessoa
  responsável e uma data; mais fraca que a ordem, porque não se abre o livro
  para conferir. **Só entra com data** — sem data é opinião anônima. Desenhada
  pontilhada. O nome de quem orientou fica fora desta publicação enquanto não
  houver aval da pessoa: o texto do warrant vai inteiro para a página, e nome
  de terceiro não se publica sem consentimento;
- **fronteira** (14) — matéria que **o acervo não cobre**. O nó aparece porque o
  mapa precisa mostrar para onde as estradas vão; a seta é julgamento declarado,
  desenhada em traço fraco. É honestidade, não decoração.

Obras (todas em `mouseion/_dissecado/`): **Guidorizzi** v.1 (classe A, TOC de
157) · **Elon Lages Lima** (classe A) · **Callioli** (classe B — scan sem TOC, e
a ficha do acervo pede conferir se é parcial; por isso só sustenta aresta de
*ordem*, nunca de *definição*) · **Merzbach & Boyer** (classe A, TOC de 300).

## Dois troncos, e um deles contém o outro

Eram **três** até 2026-08-25 — Cálculo, Álgebra Linear e Geometria Analítica,
desenhados em RGB aditivo, com a cor somando como luz soma. Uma orientação
acadêmica desfez o terceiro:

> *"Geometria Analítica é uma forma de enxergar a Álgebra Linear."*

A Geometria Analítica não é irmã da Álgebra Linear: está **contida** nela. E a
contenção tem nome exato — é a região da Álgebra Linear onde existe **produto
interno**, que é o que dá distância e ângulo, e portanto figura. Em **qualquer**
dimensão: prender a Geometria Analítica a três dimensões confunde o limite da
*ilustração*, que precisa caber no papel, com o limite da *estrutura*, que não
tem nenhum.

O argumento que fecha: o próprio **número real já é um espaço vetorial** de
dimensão 1, e um real qualquer se representa pelo segmento orientado que vai da
origem até ele. Se o objeto mais elementar da reta já é vetorial, não há onde
cortar uma coisa da outra.

| tronco | forma | cor |
|---|---|---|
| **Cálculo** (I, II, III) | laterais arredondadas | vermelho |
| **Álgebra Linear** | hexágono (o nó de tempo do Nuke) | verde |
| **Geometria Analítica** | **contorno duplo** dentro do hexágono | traço azul |
| **dois troncos** | cantos chanfrados | a soma das duas luzes |
| **a base** | canto suave | ouro — anterior aos dois |

A contenção é **desenhada**, não declarada em legenda: contorno dentro de
contorno. A mistura de cor dizia *"estes dois se cruzam"*; o contorno interno diz
*"este está dentro daquele"*, que é o que a matemática afirma. O RGB saiu junto
com o terceiro tronco — não havia mais três luzes para somar.

⚠️ **Contenção não é precedência, e por isso nenhuma seta mudou.** "A Geometria
Analítica está contida na Álgebra Linear" diz onde a matéria **mora**; a seta diz
de quem ela **depende**. Desenhar a contenção como seta mandaria o aluno estudar
espaço vetorial antes de coordenadas no plano. É o mesmo erro que já derrubou um
ciclo neste mapa: lá era *"usa"* contra *"precede"*, aqui é *"contém"*.

**Pertencer a um tronco não é depender dele.** *Cálculo de várias variáveis*
depende de vetores mas pertence ao Cálculo. A aresta diz de quem se depende; a
forma diz onde a matéria é ensinada.

## A base tem seis áreas, e a conta não é a primeira

A camada anterior aos dois troncos tem **16 nós**, organizados nas seis áreas da
matemática elementar (taxonomia de orientação, 2026-08-25):

1. **conjuntos e conjuntos numéricos** — a língua em que o resto é dito, e por
   isso é onde o mapa começa. ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ: cada um existe porque o anterior
   não bastava — o inteiro dá o oposto, o racional dá o inverso, o real fecha os
   buracos;
2. **aritmética e problemas de contagem** — o raciocínio combinatório, que não é
   a mesma área da aritmética das operações. Ela sustenta o **determinante**,
   que é uma soma sobre as *n*! permutações;
3. **geometria plana e não plana** — a figura de duas dimensões e o sólido de
   três. É aqui que a **trigonometria** mora: ela é razão entre lados de um
   *triângulo*, e antes disso ficava pendurada na álgebra elementar sem chão;
4. **álgebra elementar** — a letra no lugar do número;
5. **aritmética e as operações** — que abre em cinco pilares, e onde as lacunas
   do ensino básico aparecem;
6. **relações e funções** — a função é a relação em que cada entrada tem uma
   saída só. E o **par ordenado** do produto cartesiano é o mesmo objeto que a
   coordenada no plano: é a raiz comum da função e da geometria analítica.

**Não existem quatro operações.** A subtração não é operação própria — é somar o
oposto; a divisão é multiplicar pelo inverso. São **duas** operações e seus
inversos, e o mesmo vale para a potenciação.

E é daí que sai o lugar do **logaritmo**: soma e produto são *comutativos*, então
cada um tem **uma** inversa. A potenciação **não é comutativa** (2³ ≠ 3²), e por
isso tem **duas** — a raiz acha a *base*, o logaritmo acha o *expoente*. O log
não é um intruso na aritmética: é a segunda inversa que a assimetria obriga a
existir. O que fica no cálculo é a *função* de expoente real, que só o limite
define.

## A coluna de propriedades, e os verbetes

Clicar num nó abre o painel **dele** numa coluna própria — o raciocínio do
Properties Bin do Nuke, aplicado a um mapa. A coluna fica **sempre aberta**,
mesmo vazia: coluna que aparece e some faz o mapa saltar de largura a cada
clique, e o leitor perde de vista o nó que estava olhando. **Um nó por vez.**

Cada matéria tem quatro campos, escritos fora da página e embutidos aqui (a
página é estática — não há modelo rodando ao vivo):

| campo | o que responde |
|---|---|
| **o que é** | a definição, em uma frase |
| **por que existe** | que problema apareceu ANTES e obrigou isto a existir |
| **onde aparece no mundo** | onde isto vive hoje, em serviços que qualquer pessoa reconhece |
| **onde se trava** | o erro comum de quem está aprendendo |

**Os verbetes são escritos por um modelo de linguagem, e a página diz isso.**
Cada um carrega sua procedência — qual modelo, onde rodou, em que data, e se já
passou por leitura humana. Num mapa cujo valor inteiro é declarar de onde vem
cada seta, um texto entrando calado seria a única afirmação sem warrant aqui.

O gerador não é só um prompt. Três coisas fazem a regra valer:

- **um validador** que recusa campo vazio, transbordo, fórmula em LaTeX (a
  página não desenha LaTeX) e exemplo tirado de efeitos visuais, computação
  gráfica ou processamento de imagem — que é o assunto de outro material, não
  deste mapa;
- **um verificador adversarial** sobre o campo do exemplo, que é onde um modelo
  inventa. Ele é **portão, não etiqueta**: reprovou, o nó volta para a fila com
  o motivo e o modelo troca de exemplo. Como simples marcador ele reprovava 3
  em 4, e uma lista com 35 suspeitos em 50 não separa nada;
- **um teto por domínio de exemplo.** Numa rodada, 13 dos 50 verbetes ancoraram
  em GPS e navegação. Cada um era verdadeiro — o verificador não tinha o que
  marcar — mas juntos faziam o mapa dizer que a matemática toda serve para achar
  caminho. Com o teto, a maior concentração caiu para 6 de 50.

## As linhas não têm diagonal

Só horizontal, vertical e L, por decisão de desenho. Cada trecho vira um **Z**
(desce, anda, desce), com o degrau afastado dentro do vão entre camadas para que
duas arestas não se deitem uma sobre a outra. Medido no SVG gerado: **0
segmentos diagonais em 78 arestas**.

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
- **§2 — a gramática.** O ouro é o fluxo. As **quatro** classes de warrant se
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

4. **O layout partia da ordem alfabética.** O baricentro é local: melhora o
   arranjo que recebe, e recebia os nós de cada camada ordenados **por nome** —
   que não tem relação nenhuma com o grafo. Trocado por descida em profundidade
   a partir das raízes, que põe irmãos lado a lado, e acrescentado o passo de
   **transposição** (testar cada par adjacente, trocar, e só manter se a
   contagem cair). Medido nas quatro combinações, para separar o que é do
   algoritmo do que é do conteúdo novo:

   | | layout antigo | layout novo |
   |---|---|---|
   | grafo de 44 nós/68 arestas | 34 | **28** |
   | grafo de 50 nós/78 arestas | 51 | **41** |

   O algoritmo novo vale **−10** cruzamentos; as seis matérias e dez
   dependências novas custam **+13**. O saldo é declarado, não escondido: o mapa
   cresceu 14% e ficou com 7 cruzamentos a mais do que tinha.

5. **Duas arestas minhas saíram por serem redundantes — e onze ficaram.**
   `conj_num → negativos` e `conj_num → fracoes` custavam 15 cruzamentos
   medidos, e o caminho `conj_num → aritmética → negativos` já dizia a mesma
   coisa; a informação que carregavam foi para a nota do nó. Mas redundância
   topológica **não é** motivo suficiente: há 11 outras arestas redundantes no
   grafo, e quase todas são de *definição* — *"a derivada é um limite"* é
   redundante por caminho e é a informação central do cálculo. Só sai a aresta
   cuja informação o caminho alternativo já diz.

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
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), com o texto
  legal integral em [`LICENSE-CONTENT`](LICENSE-CONTENT): use, adapte e
  redistribua, inclusive comercialmente, **citando a fonte** e mantendo
  qualquer derivado **sob a mesma licença**. O *share-alike* não proíbe uso
  comercial — proíbe fechar o que se derivou daqui.

O copyright do conteúdo é de Mateus Alkimim. A licença acima vale para
terceiros; o titular mantém o direito de licenciar a própria obra sob outros
termos. O nome do projeto e sua identidade visual não são licenciados aqui.

> **Emenda de 2026-08-20.** O conteúdo saiu de CC BY 4.0 para CC BY-SA 4.0. A
> CC BY 4.0 concedida na publicação de 2026-08-19 é irrevogável: quem obteve o
> conteúdo sob ela naquele intervalo segue coberto por ela.

As obras citadas como warrant são referências bibliográficas; nenhum texto delas
é reproduzido aqui.
