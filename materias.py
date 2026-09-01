# -*- coding: utf-8 -*-
"""O grafo das matérias — nós, arestas e o WARRANT de cada seta.

Regra desta base: **nenhuma aresta entra sem dizer de onde veio.** O mapa vai
ser usado para apontar onde um aluno travou; uma seta errada manda o aluno
estudar a coisa errada. Três classes de warrant, e elas aparecem no mapa:

  (a) DEFINIÇÃO — X entra na definição de Y na obra citada. É a seta forte:
      não é ordem de conveniência, é dependência lógica. Ex.: a derivada é
      definida como um limite (Guidorizzi §7.2);
  (b) ORDEM     — X é definido antes de Y na mesma obra, e Y a usa. Evidência
      de precedência curricular consolidada, mais fraca que (a);
  (c) FRONTEIRA — matéria que o acervo do Mouseion NÃO cobre. O nó aparece
      porque o mapa precisa mostrar para onde as estradas vão, mas a seta é
      julgamento declarado, não fonte. Desenhada em traço fraco.
  (d) ORIENTAÇÃO — a seta vem de ORIENTAÇÃO ACADÊMICA registrada, não de
      página conferível. Mais forte que (c), porque há uma pessoa responsável
      e uma data; mais fraca que (b), porque não se abre o livro para conferir.
      REGRA DURA: só entra com data. Sem data é opinião anônima, e vira (c).
      Nota de publicação: o nome de quem orientou fica FORA do artefato
      público enquanto não houver aval da pessoa — o texto do warrant vai
      inteiro para o HTML, e nome de terceiro não se publica sem consentir.

Obras (todas dissecadas, `mouseion/_dissecado/`):
  GUI  Guidorizzi, Um Curso de Cálculo v.1 (5ª ed.) — classe A, TOC 157
  ELO  Elon Lages Lima, Geometria Analítica e Álgebra Linear — classe A
  CAL  Callioli, Domingues & Costa, Álgebra Linear e Aplicações (6ª ed.)
       — classe B (scan sem TOC; a ficha do acervo marca "conferir se é
       parcial"), por isso só sustenta aresta (b), nunca (a)
  BOY  Merzbach & Boyer, A History of Mathematics (3ª ed.) — classe A, TOC 300
"""

# --- nós: id, rótulo, ramo, o que é (uma linha) -----------------------------
NOS = [
    ("aritmetica",   "Aritmética\ne as operações", "base", "contar, somar, multiplicar — a operação antes da letra"),

    # A LINGUAGEM E AS FIGURAS, ANTES DA CONTA (2026-08-25, orientação).
    # A taxonomia da matemática de base tem SEIS áreas, e três não estavam
    # no mapa: a linguagem dos conjuntos (que precede tudo), os problemas de
    # contagem (que não são a aritmética das operações) e a geometria — plana
    # e não plana, com a trigonometria DENTRO dela em vez de solta.
    ("conjuntos",    "Conjuntos",                 "base", "pertencer, conter, unir, cortar — a língua em que o resto é dito"),
    ("conj_num",     "Conjuntos\nnuméricos",      "base", "ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ — cada um existe porque o anterior não bastava: o inteiro dá o oposto, o racional dá o inverso, o real fecha os buracos"),
    ("contagem",     "Problemas\nde contagem",    "base", "quantos são, sem listar um a um — o raciocínio combinatório"),
    ("relacoes",     "Relações\ne o par ordenado","base", "o vínculo entre dois conjuntos; a função é o caso com unicidade"),
    ("geom_plana",   "Geometria\nplana",          "base", "a figura de duas dimensões — comprimento e largura"),
    ("geom_espacial","Geometria\nespacial",       "base", "o sólido de três dimensões — e o volume"),

    # OS PILARES DA ARITMÉTICA (2026-08-24). "Aritmética e as operações" é um
    # CONJUNTO, e o mapa mostrava só o rótulo dele — o que escondia justamente
    # onde as lacunas do ensino básico moram. Cada pilar abaixo aponta para o
    # que ele sustenta lá na frente, e é por aqui que se aponta o buraco.
    # 2026-08-25 (orientação): NÃO são quatro. A subtração não existe como
    # operação própria — é somar o oposto; a divisão é multiplicar pelo
    # inverso. Duas operações e seus inversos, e o mesmo se estende à
    # potenciação. O nó dizia "as quatro operações" e ensinava o contrário.
    ("operacoes",    "Soma e produto\ne seus inversos", "base", "duas operações, não quatro: subtrair é somar o oposto, dividir é multiplicar pelo inverso"),
    ("fracoes",      "Frações\ne proporção",      "base", "a parte do todo, a razão entre duas grandezas, a regra de três"),
    # A potenciação NÃO é comutativa (2³ ≠ 3²), e é por isso que ela tem DUAS
    # inversas, enquanto a soma e o produto — comutativos — têm uma cada: a
    # raiz acha a BASE, o logaritmo acha o EXPOENTE. É essa assimetria que dá
    # ao logaritmo lugar próprio aqui, e não no cálculo.
    ("potencias",    "Potência, raiz\ne logaritmo",  "base", "a operação com DUAS inversas: a raiz acha a base, o logaritmo acha o expoente"),
    ("negativos",    "Negativos\ne a reta",       "base", "o sinal, a ordem e a distância — os números postos em fila"),
    ("fatoracao",    "Divisibilidade\ne fatoração","base", "primos, o que divide o quê, e por que isso simplifica"),
    ("algebra_elem", "Álgebra\nelementar",         "base", "a letra no lugar do número"),
    # 2026-09-01. O nó FALTAVA, e a falta era visível de dentro: o warrant de
    # determinante->autovalores já dizia "o polinômio característico é um
    # determinante", isto é, o mapa CITAVA um objeto que ele não tinha. Nos
    # seminários a dívida tem a mesma forma da que gerou o deck da
    # trigonometria: 9 menções no corpo dos decks, uma folha inteira do G4
    # ("um polinômio É um ponto") com figura própria — e nenhum deck ensina
    # grau, raiz ou fatoração.
    # ⚠️ ESTE nó é a EXPRESSÃO algébrica, não a função polinomial. São dois
    # slots com a mesma palavra: GUI trata a expressão nos exercícios do cap. 1
    # (p.33-34) e só define a FUNÇÃO polinomial em §2.1, p.62, depois de
    # funções. Fichar a expressão é o que põe o nó ANTES dos dois troncos, que
    # é onde ele é consumido — pelo cálculo e pela álgebra linear.
    ("polinomios",   "Polinômios",                 "base", "a soma de potências da letra — grau, raiz e fatoração"),
    ("trigonometria","Trigonometria",              "base", "razão entre lados de um triângulo"),
    ("reais",        "Números reais",              "base", "o corpo ordenado completo onde tudo se passa"),
    ("funcoes",      "Funções",                    "base", "leva número em número"),

    ("limite",       "Limite\ne continuidade",     "calculo", "para onde a função tende, e quando não salta"),
    ("sequencias",   "Sequências",                 "calculo", "limite ao longo dos naturais"),
    ("exp_log",      "Exponencial\ne logaritmo",   "calculo", "a potência de expoente real, e sua inversa"),
    ("derivada",     "Derivada",                   "calculo", "a taxa de variação — definida como um limite"),
    ("regra_cadeia", "Regra da cadeia",            "calculo", "a derivada da composta"),
    ("inversa",      "Funções inversas",           "calculo", "desfazer a função, e derivar o desfazimento"),
    ("variacao",     "Estudo da variação\n(TVM)",  "calculo", "crescimento, concavidade, máximos e mínimos"),
    ("primitiva",    "Primitivas",                 "calculo", "a operação que desfaz a derivada"),
    ("integral",     "Integral\nde Riemann",       "calculo", "a soma que vira área, e o teorema fundamental"),
    ("tecnicas_int", "Técnicas\nde primitivação",  "calculo", "partes, substituição, frações parciais"),
    ("polares",      "Coordenadas polares\ne aplicações", "calculo", "volume, comprimento de curva, área polar"),

    ("coord_plano",  "Coordenadas\nno plano",      "geometria", "o par ordenado que vira ponto"),
    ("reta",         "Equações da reta",           "geometria", "a reta como conjunto de soluções"),
    ("conicas",      "Cônicas",                    "geometria", "circunferência, elipse, hipérbole, parábola"),
    ("coord_espaco", "Coordenadas\nno espaço",     "geometria", "a terceira coordenada"),
    ("vetores",      "Vetores",                    "geometria", "a flecha com soma e escala"),
    ("plano_eq",     "Equação do plano",           "geometria", "a superfície de grau um"),

    ("matrizes",     "Matrizes",                   "algebra", "a tabela que guarda o sistema"),
    ("sistemas",     "Sistemas lineares",          "algebra", "muitas equações, uma solução (ou nenhuma)"),
    ("determinante", "Determinantes",              "algebra", "o número que diz se inverte"),
    ("esp_vetorial", "Espaços vetoriais",          "algebra", "o vetor sem a flecha: só os axiomas"),
    ("base_dim",     "Base e dimensão",            "algebra", "as coordenadas de volta, agora escolhidas"),
    ("transf_lin",   "Transformações\nlineares",   "algebra", "a função que respeita soma e escala"),
    ("prod_interno", "Produto interno",            "algebra", "ângulo e comprimento dentro do espaço"),
    ("autovalores",  "Autovalores\ne autovetores", "algebra", "as direções que a transformação só estica"),
    ("formas_quad",  "Formas quadráticas\ne quádricas", "algebra", "o grau dois em qualquer dimensão"),

    ("varias_var",   "Cálculo de\nvárias variáveis", "fronteira", "derivada parcial, gradiente, a jacobiana"),
    ("edo",          "Equações\ndiferenciais",     "fronteira", "a equação cuja incógnita é uma função"),
    ("analise_real", "Análise real",               "fronteira", "o cálculo refeito com demonstração"),
    ("algebra_abs",  "Álgebra abstrata",           "fronteira", "grupo, anel, corpo"),
    ("topologia",    "Topologia",                  "fronteira", "vizinhança sem distância"),
    ("medida",       "Medida\ne integração",       "fronteira", "a integral que aguenta o patológico"),
    ("geom_dif",     "Geometria\ndiferencial",     "fronteira", "cálculo sobre superfícies curvas"),
    ("analise_func", "Análise funcional",          "fronteira", "espaços vetoriais de dimensão infinita"),
]

# --- arestas: (de, para, warrant, fonte) ------------------------------------
A = "definicao"; O = "ordem"; F = "fronteira"; R = "orientacao"
ARESTAS = [
    # A LINGUAGEM PRIMEIRO (2026-08-25, orientação). O conjunto é a língua em
    # que número, relação e figura são ditos — por isso ele, e não a
    # aritmética, é onde o mapa começa.
    ("conjuntos",    "conj_num",     R, "orientação acadêmica, 2026-08-25 — conjunto numérico é, antes de tudo, um conjunto"),
    ("conjuntos",    "contagem",     R, "orientação acadêmica, 2026-08-25 — contar é contar os elementos de um conjunto"),
    ("conjuntos",    "relacoes",     R, "orientação acadêmica, 2026-08-25 — a relação é um subconjunto do produto cartesiano"),
    ("conj_num",     "aritmetica",   R, "orientação acadêmica, 2026-08-25 — a operação precisa saber sobre QUE números ela opera"),
    # ⚠️ NÃO ENTRAM as arestas conj_num->negativos e conj_num->fracoes. Elas
    # são TRANSITIVAMENTE REDUNDANTES: conj_num->aritmetica->negativos (e
    # ->fracoes) já dizem a mesma coisa, e as duas custavam 15 cruzamentos
    # medidos. O que elas carregavam de informação — o inteiro é o que o
    # natural não dava (o oposto), o racional é o que o inteiro não dava (o
    # inverso) — foi para a NOTA do nó conj_num, onde não atravessa o desenho.
    #
    # Redundância topológica NÃO é motivo suficiente para remover: há 11 outras
    # arestas redundantes no grafo, e quase todas são de DEFINIÇÃO — "a derivada
    # É um limite" (GUI §7.2) é redundante por caminho e é a informação central
    # do cálculo. Só sai a aresta cuja informação o caminho alternativo já diz.

    # a função é um caso de relação, e o par ordenado é a MESMA coisa que a
    # coordenada no plano — é a raiz comum da função e da geometria analítica.
    ("relacoes",     "funcoes",      R, "orientação acadêmica, 2026-08-25 — função é a relação em que cada entrada tem uma saída só"),
    ("relacoes",     "coord_plano",  R, "orientação acadêmica, 2026-08-25 — o par ordenado do produto cartesiano É o ponto do plano"),

    # a figura, plana e não plana. A trigonometria deixa de flutuar: ela é
    # razão entre lados de um TRIÂNGULO, e o triângulo mora aqui.
    ("geom_plana",   "geom_espacial",R, "orientação acadêmica, 2026-08-25 — o sólido acrescenta a terceira dimensão à figura plana"),
    ("geom_plana",   "trigonometria",R, "orientação acadêmica, 2026-08-25 — a razão é entre os lados de um triângulo, que é figura plana"),
    ("geom_espacial","coord_espaco", R, "orientação acadêmica, 2026-08-25 — o espaço de três dimensões antes de receber coordenadas"),

    # a contagem sustenta o determinante: ele é uma soma sobre as n!
    # permutações, e é essa a lacuna que o tabuleiro do seminário ensina.
    ("contagem",     "determinante", O, "seminario-determinantes — o determinante é a soma sobre as permutações"),

    # a cadeia da base — já é a fig-3-base do mapa-genealogia
    # o conjunto abre nos seus pilares
    ("aritmetica",   "operacoes",    O, "norma de notação do autor §1 — o arco do cálculo exige aritmética com FAMILIARIDADE, não com \"já vi\""),
    ("aritmetica",   "fracoes",      O, "norma de notação do autor §1 · seminário de cálculo 0, folha 2"),
    ("aritmetica",   "potencias",    O, "norma de notação do autor §1 · seminário de cálculo 0, folha 2"),
    ("aritmetica",   "negativos",    O, "norma de notação do autor §1 · seminário de cálculo 0, folha 2"),
    ("aritmetica",   "fatoracao",    O, "norma de notação do autor §1 · seminário de cálculo 0, folha 2"),

    # e cada pilar sustenta o que vem depois — é aqui que a lacuna aparece
    ("operacoes",    "algebra_elem", O, "mapa-genealogia, fig-3-base · a letra obedece às MESMAS propriedades: comutativa, associativa, distributiva"),
    ("fatoracao",    "algebra_elem", O, "seminario-calculo-0, folha 9 — fatorar é o que revela ou esconde um buraco no domínio"),
    ("fracoes",      "trigonometria",O, "trigonometria é RAZÃO entre lados: sem fração, o seno não tem sentido"),
    # OS POLINÔMIOS (2026-09-01). Duas entradas e três saídas, e as saídas vão
    # para os DOIS troncos — é o que justifica o domínio vazio do nó.
    ("algebra_elem", "polinomios",   O, "GUI cap. 1, p. 33-34 — o polinômio do 2.º grau, a fórmula de suas raízes e sua fatoração são exercícios do capítulo de NÚMEROS REAIS, antes de qualquer função"),
    ("fatoracao",    "polinomios",   O, "GUI cap. 1, p. 34 — ax²+bx+c = a(x−x₁)(x−x₂): fatorar o polinômio é a fatoração com a letra no lugar do número"),
    ("negativos",    "reais",        O, "GUI cap. 1 — a reta ordenada é o que os reais completam"),
    ("negativos",    "coord_plano",  O, "seminario-geometria, Estação 3 — o eixo tem lado negativo, e o observador fica na origem"),
    # A CISÃO (2026-08-25): a OPERAÇÃO potência/raiz/log é da base — expoente
    # racional, conta fechada. O que fica no cálculo é a FUNÇÃO de expoente
    # REAL, que só o limite define. Esta aresta é a costura entre as duas.
    ("potencias",    "exp_log",      O, "seminario-calculo-0 — a potência de expoente racional antes da de expoente real; o limite é o que atravessa"),
    ("fracoes",      "funcoes",      O, "seminario-calculo-0, folha 9 — a função escrita como quociente, e o domínio que ela perde"),
    ("aritmetica",   "algebra_elem", O, "mapa-genealogia, fig-3-base · BOY caps. 1-3 (contagem antes da equação)"),
    ("algebra_elem", "trigonometria",O, "mapa-genealogia, fig-3-base"),
    ("algebra_elem", "reais",        O, "GUI cap. 1 (racionais §1.1 antes dos reais §1.2)"),
    ("trigonometria","funcoes",      O, "GUI §2.2 define seno e cosseno como funções"),
    ("reais",        "funcoes",      A, "GUI §2.1 — função de uma variável REAL a valores reais"),

    # cálculo — Guidorizzi, ordem de definição
    ("funcoes",      "limite",       A, "GUI §3.3 define limite de uma função"),
    ("polinomios",   "limite",       O, "GUI §2.1 p. 62 define a função polinomial; §3, p. 119, a usa — 'EXEMPLO 12. Toda função polinomial é contínua'"),
    ("reais",        "limite",       A, "GUI §3.3 — o ε e o δ são reais"),
    ("limite",       "sequencias",   O, "GUI §4.3-4.4 (sequência depois do limite; §4.4 liga os dois)"),
    ("limite",       "exp_log",      A, "GUI §6.3 — o limite define a potência de expoente real"),
    ("limite",       "derivada",     A, "GUI §7.2 — a derivada É um limite"),
    ("derivada",     "regra_cadeia", A, "GUI §7.10 — derivada da função composta"),
    ("derivada",     "inversa",      A, "GUI §8.2 — derivada da função inversa"),
    ("exp_log",      "derivada",     O, "GUI §7.4 deriva e^x e ln x"),
    ("derivada",     "variacao",     A, "GUI §9.1 — o TVM é enunciado sobre a derivada"),
    ("derivada",     "primitiva",    A, "GUI §10.2 — primitiva é definida por 'F' = f'"),
    ("limite",       "integral",     A, "GUI §11.3 — a integral é o limite das somas de Riemann"),
    ("primitiva",    "integral",     A, "GUI §11.5 — o 1º teorema fundamental liga as duas"),
    ("primitiva",    "tecnicas_int", O, "GUI cap. 12 vem depois do cap. 10"),
    ("regra_cadeia", "tecnicas_int", A, "GUI §12.4 — a mudança de variável É a regra da cadeia ao contrário"),
    ("integral",     "polares",      O, "GUI cap. 13 — aplicações da integral"),
    ("trigonometria","polares",      A, "GUI §13.7 — a coordenada polar é ângulo e raio"),

    # geometria analítica — Elon
    ("reais",        "coord_plano",  A, "ELO 'Coordenadas no Plano' — o par de reais"),
    ("coord_plano",  "reta",         A, "ELO 'As Equações da Reta'"),
    ("algebra_elem", "reta",         O, "ELO — a equação da reta é álgebra elementar em duas letras"),
    ("reta",         "conicas",      O, "ELO — circunferência e hipérbole depois da reta"),
    ("coord_plano",  "vetores",      O, "ELO 'Vetores' depois de 'Coordenadas'"),
    ("coord_plano",  "coord_espaco", O, "ELO 'Coordenadas no Espaço'"),
    ("coord_espaco", "plano_eq",     A, "ELO 'Equação do Plano' — três coordenadas"),
    ("vetores",      "plano_eq",     A, "ELO — o plano pelo vetor normal"),

    # álgebra linear
    ("sistemas",     "matrizes",     O, "ELO — a matriz aparece com o sistema"),
    ("algebra_elem", "sistemas",     O, "ELO/CAL — sistema é equação com muitas letras"),
    ("matrizes",     "determinante", A, "ELO 'Determinantes' — o determinante é DE uma matriz"),
    # ⚠ REMOVIDA: ("determinante","sistemas") fechava o ciclo
    #   sistemas -> matrizes -> determinante -> sistemas. O determinante DECIDE
    #   um sistema (invertibilidade, Cramer), mas não é pré-requisito para
    #   DEFINIR sistema — é consequência, não precedência. O detector de ciclo
    #   do layout.py pegou; a confusão era entre "usa" e "precede".
    ("vetores",      "esp_vetorial", O, "CAL — o espaço vetorial generaliza o vetor (classe B)"),
    # O polinômio como VETOR — e quem declara a precedência é o próprio livro:
    # "O leitor, QUE JÁ ESTUDOU OS POLINÔMIOS SOBRE ℝ, não terá dificuldades em
    # perceber que…" (CAL, ao apresentar Pₙ(ℝ)). É a folha 10 do seminário de
    # espaços vetoriais: "um polinômio É um ponto, e o espaço dele tem quatro
    # eixos". CAL é classe B, logo sustenta ORDEM, nunca definição.
    ("polinomios",   "esp_vetorial", O, "CAL cap. 2 — 'O leitor, que já estudou os polinômios sobre ℝ, não terá dificuldades…': o livro DECLARA o polinômio como pré-requisito, e Pₙ(ℝ) é o exemplo canônico de espaço sem flecha (classe B)"),
    ("esp_vetorial", "base_dim",     A, "CAL — base é definida dentro do espaço vetorial (classe B)"),
    ("esp_vetorial", "transf_lin",   A, "ELO 'Transformações Lineares' — entre espaços"),
    ("matrizes",     "transf_lin",   A, "ELO — a matriz representa a transformação numa base"),
    ("base_dim",     "transf_lin",   A, "ELO/CAL — a representação exige a base escolhida"),
    ("vetores",      "prod_interno", A, "ELO 'Distância de um Ponto a uma Reta' usa o produto"),
    ("transf_lin",   "autovalores",  A, "CAL — autovalor é da transformação (classe B)"),
    ("determinante", "autovalores",  A, "CAL — o polinômio característico é um determinante (classe B)"),
    # A aresta que FECHA a citação órfã: até hoje o warrant acima citava o
    # polinômio característico sem que o mapa tivesse o nó. ELO é classe A e
    # define: o polinômio característico é o polinômio de grau n em λ cujas
    # RAÍZES são os autovalores — logo é o polinômio, não só o determinante,
    # que entra na definição. Custo declarado: salta da camada 5 à 11, e
    # sozinha responde por 5 dos 9 nós virtuais novos.
    ("polinomios",   "autovalores",  A, "ELO — 'chama-se polinômio característico da matriz m ao polinômio de grau três na variável λ… as RAÍZES deste polinômio são chamadas os autovalores'"),
    ("conicas",      "formas_quad",  O, "ELO 'Formas Quadráticas' depois das cônicas"),
    ("autovalores",  "formas_quad",  A, "ELO 'Completando Quadrados' — diagonalizar a forma"),

    # fronteira — o acervo não cobre; seta é julgamento declarado
    ("derivada",     "varias_var",   F, "sem obra no acervo (Guidorizzi v.1 para em uma variável)"),
    ("vetores",      "varias_var",   F, "sem obra no acervo"),
    ("integral",     "edo",          F, "sem obra no acervo"),
    ("derivada",     "edo",          F, "sem obra no acervo"),
    ("limite",       "analise_real", F, "sem obra no acervo"),
    ("sequencias",   "analise_real", F, "sem obra no acervo"),
    ("esp_vetorial", "algebra_abs",  F, "sem obra no acervo"),
    ("analise_real", "topologia",    F, "sem obra no acervo"),
    ("analise_real", "medida",       F, "sem obra no acervo"),
    ("varias_var",   "geom_dif",     F, "sem obra no acervo"),
    ("transf_lin",   "geom_dif",     F, "sem obra no acervo"),
    ("topologia",    "analise_func", F, "sem obra no acervo"),
    ("medida",       "analise_func", F, "sem obra no acervo"),
    ("esp_vetorial", "analise_func", F, "sem obra no acervo"),
]


# --- domínio: a que tronco a matéria pertence -------------------------------
# 2026-08-25 — O TRONCO AZUL COLAPSOU. Eram três (Cálculo, Álgebra Linear e
# Geometria Analítica, em RGB aditivo, declaração de 2026-08-18). A orientação
# desta data desfez o terceiro:
#
#   "Geometria Analítica é uma forma de enxergar a Álgebra Linear."
#
# A GA não é irmã da AL: está CONTIDA nela. E a contenção tem nome exato — é a
# parte da Álgebra Linear onde existe PRODUTO INTERNO, que é o que dá distância
# e ângulo, que é o que permite desenhar a figura. Em QUALQUER dimensão: prender
# a GA a três dimensões confunde o limite da ILUSTRAÇÃO, que precisa caber no
# papel, com o limite da ESTRUTURA, que não tem nenhum.
#
# O argumento que fecha: o próprio número real já é um espaço vetorial de
# dimensão 1, e um real qualquer se representa pelo segmento orientado que vai
# da origem até ele. Se o objeto mais elementar da reta já é vetorial, não há
# onde cortar uma da outra.
#
# ⚠️ CONTENÇÃO NÃO É PRECEDÊNCIA. Nenhuma aresta mudou por causa disto — e não
# pode mudar. "GA está contida em AL" diz onde a matéria MORA; a seta diz de
# quem ela DEPENDE. Desenhar a contenção como seta mandaria o aluno estudar
# espaço vetorial antes de coordenadas no plano. É o mesmo erro que já derrubou
# o ciclo determinante→sistemas: ali era "usa" × "precede", aqui é "contém".
#
# Restam DOIS troncos, que é o que o mapa-genealogia sempre disse — "os dois
# pilares". O desenho e o documento pararam de se desmentir.
#
#     Cálculo = vermelho   ·   Álgebra Linear = verde
#
# Conjunto VAZIO é a base, anterior aos dois. REGIAO_GEO marca, DENTRO da
# álgebra linear, o que é geometria analítica: desenhada por contorno duplo —
# um contorno dentro do outro, que é o desenho da própria contenção.
C, AL = "calculo", "algebra"

# A região da Álgebra Linear onde há produto interno — logo, distância, ângulo
# e figura. É a Geometria Analítica, em qualquer dimensão.
REGIAO_GEO = {
    "coord_plano", "reta", "conicas", "coord_espaco", "plano_eq",
    "vetores", "prod_interno", "formas_quad", "geom_dif",
}

DOMINIOS = {
    # a base — anterior aos dois troncos
    "conjuntos": ((), "anterior a tudo: é a língua em que o resto é dito"),
    "conj_num": ((), "anterior aos dois — que números existem, antes de operar com eles"),
    "contagem": ((), "anterior aos dois — o raciocínio combinatório, que o determinante cobra"),
    "relacoes": ((), "anterior aos dois — o par ordenado, raiz comum da função e do plano"),
    "geom_plana": ((), "anterior aos dois — a figura antes da coordenada"),
    "geom_espacial": ((), "anterior aos dois — o sólido antes da terceira coordenada"),
    "aritmetica": ((), "anterior aos dois — nenhum curso a ensina, todos a exigem"),
    "operacoes": ((), "pilar da aritmética — as propriedades que a letra vai herdar"),
    "fracoes": ((), "pilar da aritmética — razão e proporção, que a trigonometria cobra"),
    "potencias": ((), "pilar da aritmética — a operação de duas inversas; o log nasce aqui"),
    "negativos": ((), "pilar da aritmética — a reta ordenada, que os reais completam"),
    "fatoracao": ((), "pilar da aritmética — o que permite simplificar sem mudar o valor"),
    "algebra_elem": ((), "anterior aos dois"),
    "polinomios": ((), "anterior aos dois — o único objeto da base que os DOIS troncos "
                       "consomem de frente: o cálculo pela continuidade, a álgebra "
                       "linear por Pₙ(ℝ) e pelo polinômio característico"),
    "trigonometria": ((), "anterior aos dois; mora na geometria plana, GUI §2.2 a retoma como função"),
    "reais": ((), "anterior aos dois; GUI cap. 1 a formaliza antes de tudo"),
    "funcoes": ((), "anterior aos dois; é o objeto que os dois manipulam"),

    # cálculo — Guidorizzi v.1 é a ementa de Cálculo I
    "limite": ((C,), "GUI cap. 3"), "sequencias": ((C,), "GUI §4.3"),
    "exp_log": ((C,), "GUI cap. 6 — a FUNÇÃO de expoente real; a operação ficou na base"),
    "derivada": ((C,), "GUI cap. 7"),
    "regra_cadeia": ((C,), "GUI §7.10"), "inversa": ((C,), "GUI cap. 8"),
    "variacao": ((C,), "GUI cap. 9"), "primitiva": ((C,), "GUI cap. 10"),
    "integral": ((C,), "GUI cap. 11"), "tecnicas_int": ((C,), "GUI cap. 12"),
    "polares": ((C,), "GUI cap. 13"),

    # álgebra linear — a região com produto interno é a geometria analítica
    "coord_plano": ((AL,), "ELO 'Coordenadas no Plano' — o par ordenado num espaço de dimensão 2"),
    "reta": ((AL,), "ELO 'As Equações da Reta' — o subespaço de dimensão 1, transladado"),
    "conicas": ((AL,), "ELO — o grau dois no plano; a diagonalização as classifica"),
    "coord_espaco": ((AL,), "ELO 'Coordenadas no Espaço' — a mesma coisa em dimensão 3"),
    "plano_eq": ((AL,), "ELO 'Equação do Plano' — definido pelo vetor normal, que é produto interno"),
    "matrizes": ((AL,), "ELO/CAL"), "sistemas": ((AL,), "ELO/CAL"),
    "determinante": ((AL,), "ELO 'Determinantes'"),
    "esp_vetorial": ((AL,), "CAL — o vetor sem a flecha: fora da região geométrica, "
                            "porque sem produto interno não há distância nem ângulo"),
    "base_dim": ((AL,), "CAL — base e dimensão"),
    "transf_lin": ((AL,), "ELO 'Transformações Lineares'"),
    "autovalores": ((AL,), "CAL — autovalores e autovetores"),
    "algebra_abs": ((AL,), "generaliza a estrutura da álgebra linear"),
    "vetores": ((AL,), "ELO trata o vetor dentro da geometria e CAL o axiomatiza — "
                       "o título do Elon carrega os dois nomes porque é uma coisa só"),
    "prod_interno": ((AL,), "É O OPERADOR QUE FABRICA A GEOMETRIA DENTRO DA ÁLGEBRA: "
                            "dele saem distância e ângulo, em qualquer dimensão"),
    "formas_quad": ((AL,), "ELO trata quádricas e as diagonaliza por autovalores"),

    # os que moram nos dois troncos
    "geom_dif": ((C, AL), "cálculo sobre superfície curva — e a superfície tem métrica"),
    "analise_func": ((C, AL), "espaço vetorial de dimensão infinita, com análise por cima"),
    "topologia": ((C, AL), "a vizinhança SEM distância — é o que sobra da geometria "
                           "quando se tira o produto interno, e por isso fica FORA da região"),

    # fronteira que fica num tronco só
    "varias_var": ((C,), "Cálculo II/III — pertence ao cálculo mesmo dependendo de vetores"),
    "edo": ((C,), "Cálculo/EDO"), "analise_real": ((C,), "o cálculo refeito com demonstração"),
    "medida": ((C,), "a integral de Lebesgue, dentro da análise"),
}
