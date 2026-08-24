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

    # OS PILARES DA ARITMÉTICA (2026-08-24). "Aritmética e as operações" é um
    # CONJUNTO, e o mapa mostrava só o rótulo dele — o que escondia justamente
    # onde as lacunas do ensino básico moram. Cada pilar abaixo aponta para o
    # que ele sustenta lá na frente, e é por aqui que se aponta o buraco.
    ("op_quatro",    "As quatro\noperações",      "base", "somar, subtrair, multiplicar, dividir — e em que ordem se aplicam"),
    ("fracoes",      "Frações\ne proporção",      "base", "a parte do todo, a razão entre duas grandezas, a regra de três"),
    ("potencias",    "Potência\ne raiz",          "base", "o expoente, e a operação que o desfaz"),
    ("negativos",    "Negativos\ne a reta",       "base", "o sinal, a ordem e a distância — os números postos em fila"),
    ("fatoracao",    "Divisibilidade\ne fatoração","base", "primos, o que divide o quê, e por que isso simplifica"),
    ("algebra_elem", "Álgebra\nelementar",         "base", "a letra no lugar do número"),
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
A = "definicao"; O = "ordem"; F = "fronteira"
ARESTAS = [
    # a cadeia da base — já é a fig-3-base do mapa-genealogia
    # o conjunto abre nos seus pilares
    ("aritmetica",   "op_quatro",    O, "hipatia/norma-de-notacao.md §1 — o arco do cálculo exige aritmética com FAMILIARIDADE, não com \"já vi\""),
    ("aritmetica",   "fracoes",      O, "hipatia/norma-de-notacao.md §1 · seminario-calculo-0, folha 2"),
    ("aritmetica",   "potencias",    O, "hipatia/norma-de-notacao.md §1 · seminario-calculo-0, folha 2"),
    ("aritmetica",   "negativos",    O, "hipatia/norma-de-notacao.md §1 · seminario-calculo-0, folha 2"),
    ("aritmetica",   "fatoracao",    O, "hipatia/norma-de-notacao.md §1 · seminario-calculo-0, folha 2"),

    # e cada pilar sustenta o que vem depois — é aqui que a lacuna aparece
    ("op_quatro",    "algebra_elem", O, "mapa-genealogia, fig-3-base · a letra obedece às MESMAS propriedades: comutativa, associativa, distributiva"),
    ("fatoracao",    "algebra_elem", O, "seminario-calculo-0, folha 9 — fatorar é o que revela ou esconde um buraco no domínio"),
    ("fracoes",      "trigonometria",O, "trigonometria é RAZÃO entre lados: sem fração, o seno não tem sentido"),
    ("negativos",    "reais",        O, "GUI cap. 1 — a reta ordenada é o que os reais completam"),
    ("negativos",    "coord_plano",  O, "seminario-geometria, Estação 3 — o eixo tem lado negativo, e o observador fica na origem"),
    ("potencias",    "exp_log",      O, "seminario-calculo-0 — a potência de expoente natural antes da de expoente real"),
    ("fracoes",      "funcoes",      O, "seminario-calculo-0, folha 9 — a função escrita como quociente, e o domínio que ela perde"),
    ("aritmetica",   "algebra_elem", O, "mapa-genealogia, fig-3-base · BOY caps. 1-3 (contagem antes da equação)"),
    ("algebra_elem", "trigonometria",O, "mapa-genealogia, fig-3-base"),
    ("algebra_elem", "reais",        O, "GUI cap. 1 (racionais §1.1 antes dos reais §1.2)"),
    ("trigonometria","funcoes",      O, "GUI §2.2 define seno e cosseno como funções"),
    ("reais",        "funcoes",      A, "GUI §2.1 — função de uma variável REAL a valores reais"),

    # cálculo — Guidorizzi, ordem de definição
    ("funcoes",      "limite",       A, "GUI §3.3 define limite de uma função"),
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
    ("esp_vetorial", "base_dim",     A, "CAL — base é definida dentro do espaço vetorial (classe B)"),
    ("esp_vetorial", "transf_lin",   A, "ELO 'Transformações Lineares' — entre espaços"),
    ("matrizes",     "transf_lin",   A, "ELO — a matriz representa a transformação numa base"),
    ("base_dim",     "transf_lin",   A, "ELO/CAL — a representação exige a base escolhida"),
    ("vetores",      "prod_interno", A, "ELO 'Distância de um Ponto a uma Reta' usa o produto"),
    ("transf_lin",   "autovalores",  A, "CAL — autovalor é da transformação (classe B)"),
    ("determinante", "autovalores",  A, "CAL — o polinômio característico é um determinante (classe B)"),
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


# --- domínio: a qual dos três troncos a matéria pertence --------------------
# O operador declarou (2026-08-18) que a matemática do ciclo básico se organiza
# em três troncos — Cálculo (I, II, III), Álgebra Linear e Geometria Analítica —
# e que o mapa deve mostrar isso por FORMA e por COR, em RGB aditivo:
#
#     Cálculo = R (vermelho)  ·  Álgebra Linear = G (verde)  ·  Geom. Analítica = B (azul)
#
# Uma matéria pode estar em mais de um tronco: a cor soma como luz soma
# (R+G = amarelo, R+B = magenta, G+B = ciano, os três = branco). Conjunto VAZIO
# é o tronco anterior aos três — a base, que nenhum deles pode dispensar.
#
# ATENÇÃO: pertencer a um tronco NÃO é o mesmo que depender dele. "Cálculo de
# várias variáveis" DEPENDE de vetores (geometria), mas PERTENCE ao Cálculo. A
# aresta diz de quem se depende; o domínio diz onde a matéria é ensinada.
C, AL, GA = "calculo", "algebra", "geometria"
DOMINIOS = {
    # a base — anterior aos três troncos
    "aritmetica": ((), "anterior aos três — nenhum curso a ensina, todos a exigem"),
    "op_quatro": ((), "pilar da aritmética — as propriedades que a letra vai herdar"),
    "fracoes": ((), "pilar da aritmética — razão e proporção, que a trigonometria cobra"),
    "potencias": ((), "pilar da aritmética — o expoente natural, que a exponencial estende"),
    "negativos": ((), "pilar da aritmética — a reta ordenada, que os reais completam"),
    "fatoracao": ((), "pilar da aritmética — o que permite simplificar sem mudar o valor"),
    "algebra_elem": ((), "anterior aos três"),
    "trigonometria": ((), "anterior aos três; GUI §2.2 a retoma como função"),
    "reais": ((), "anterior aos três; GUI cap. 1 a formaliza antes de tudo"),
    "funcoes": ((), "anterior aos três; é o objeto que os três manipulam"),

    # cálculo — Guidorizzi v.1 é a ementa de Cálculo I
    "limite": ((C,), "GUI cap. 3"), "sequencias": ((C,), "GUI §4.3"),
    "exp_log": ((C,), "GUI cap. 6"), "derivada": ((C,), "GUI cap. 7"),
    "regra_cadeia": ((C,), "GUI §7.10"), "inversa": ((C,), "GUI cap. 8"),
    "variacao": ((C,), "GUI cap. 9"), "primitiva": ((C,), "GUI cap. 10"),
    "integral": ((C,), "GUI cap. 11"), "tecnicas_int": ((C,), "GUI cap. 12"),
    "polares": ((C,), "GUI cap. 13"),

    # geometria analítica — Elon, primeira metade do título
    "coord_plano": ((GA,), "ELO 'Coordenadas no Plano'"),
    "reta": ((GA,), "ELO 'As Equações da Reta'"),
    "conicas": ((GA,), "ELO 'Equação da Circunferência' e 'da Hipérbole'"),
    "coord_espaco": ((GA,), "ELO 'Coordenadas no Espaço'"),
    "plano_eq": ((GA,), "ELO 'Equação do Plano'"),

    # álgebra linear — Callioli, e a segunda metade do título do Elon
    "matrizes": ((AL,), "ELO/CAL"), "sistemas": ((AL,), "ELO/CAL"),
    "determinante": ((AL,), "ELO 'Determinantes'"),
    "esp_vetorial": ((AL,), "CAL — espaços vetoriais"),
    "base_dim": ((AL,), "CAL — base e dimensão"),
    "transf_lin": ((AL,), "ELO 'Transformações Lineares'"),
    "autovalores": ((AL,), "CAL — autovalores e autovetores"),
    "algebra_abs": ((AL,), "generaliza a estrutura da álgebra linear"),

    # os que moram em dois troncos — a cor soma
    "vetores": ((AL, GA), "o objeto comum: ELO trata vetor dentro da geometria, "
                          "CAL o axiomatiza — o título do Elon carrega os dois nomes"),
    "prod_interno": ((AL, GA), "ELO usa o produto para distância e ângulo (geometria); "
                               "CAL o define sobre o espaço vetorial"),
    "formas_quad": ((AL, GA), "ELO trata quádricas na geometria e as diagonaliza "
                              "por autovalores — a ponte entre os dois"),
    "geom_dif": ((C, GA), "cálculo sobre superfície curva"),
    "analise_func": ((C, AL), "espaço vetorial de dimensão infinita, com análise por cima"),
    "topologia": ((C, GA), "a vizinhança sem distância — nasce da análise e da geometria"),

    # fronteira que fica num tronco só
    "varias_var": ((C,), "Cálculo II/III — pertence ao cálculo mesmo dependendo de vetores"),
    "edo": ((C,), "Cálculo/EDO"), "analise_real": ((C,), "o cálculo refeito com demonstração"),
    "medida": ((C,), "a integral de Lebesgue, dentro da análise"),
}
