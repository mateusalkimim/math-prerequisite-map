# -*- coding: utf-8 -*-
"""Gera o mapa das matérias — HTML autossuficiente, para projetar em aula.

Sob a `norma-de-diagramas.md` da Hipátia, com a regra citada em cada decisão:

  §1.1  cruzamento é o defeito nº 1 e vence qualquer outra regra em conflito
        (Purchase 1997) — por isso o layout é medido, não desenhado: 131 -> 11;
  §1.2  a direção se declara UMA vez e não se mistura — aqui é T->B (o
        pré-requisito sempre acima de quem o exige), dito no cabeçalho;
  §1.3  kit de três formas: retângulo arredondado (matéria), oval (a raiz, que
        é terminador de início). Losango não aparece porque não há decisão.
        Nada de forma inventada;
  §1.4  o nó é CAIXA, nunca ponto — rótulo dentro, legível de uma vez;
  §1.5  modularidade: o mapa abre em UM ramo por vez quando se escolhe matéria
        (information hiding — o resto apaga em vez de sumir);
  §2    a gramática: o ouro é o fluxo. As três classes de warrant se
        distinguem por peso e traço, declarado na legenda;
  §4    SVG com max-height em vh, e a página medida em mais de uma resolução.

Saída: index.html (abre com duplo clique, sem servidor; e é o que o
GitHub Pages serve na raiz).
"""
import html, json, os
from materias import NOS, ARESTAS, DOMINIOS, REGIAO_GEO
from layout import montar

AQUI = os.path.dirname(os.path.abspath(__file__))
# Bilíngue desde 2026-08-27: `pt/` guarda a página gerada em português, `en/` é
# derivada dela pelas tabelas de `traducao/`, e a raiz é a porta que encaminha
# por idioma. Sem esta linha o gerador sobrescreveria a porta a cada rodada,
# e nada acusaria — uma página válida ficaria no lugar de outra página válida.
SAIDA = os.path.join(AQUI, "pt" if os.path.isdir(os.path.join(AQUI, "pt")) else "",
                     "index.html")

CAIXA_L, CAIXA_A = 152, 58
GAP_X, GAP_Y = 20, 146
GAP_VIRTUAL = 7         # entre duas passagens, o vão pode ser menor
VIRTUAL_L = 16          # o nó virtual é passagem, não caixa (§1.4 vale para nó, não para dobra)
MARGEM = 48

# DOIS troncos (2026-08-25). Eram três até a orientação desta data desfazer o
# terceiro: a Geometria Analítica não é irmã da Álgebra Linear, está CONTIDA
# nela — é a região onde há produto interno, logo distância, ângulo e figura,
# em qualquer dimensão. Ver o cabeçalho de DOMINIOS em materias.py.
#
# A cor deixou de somar como luz porque não há mais três luzes para somar. O
# que ela faz agora é mais simples e mais verdadeiro: dois troncos, duas cores,
# e a contenção desenhada por CONTORNO DUPLO em vez de por mistura. Mistura
# dizia "estes dois se cruzam"; o contorno dentro do contorno diz "este está
# dentro daquele", que é o que a matemática afirma.
TRONCOS = {
    # os matizes de 2026-08-24 ficam INTACTOS: o vermelho e o verde não mudam
    # de cor por causa do colapso — quem some é o azul, e nada herda o lugar.
    "calculo":   ((244, 78, 62),  "Cálculo (I, II, III)", "laterais arredondadas"),
    "algebra":   ((58, 200, 72),  "Álgebra Linear",       "hexágono"),
}

# A LÓGICA PRIMORDIAL, que faltava (2026-08-25). O mapa nomeava os troncos e não
# dizia o que eles SÃO. A cor codificava o tronco; ninguém decodificava a razão.
#
# CORRIGIDA EM 2026-08-26 (emenda ratificada da `norma-de-notacao.md` §1.2c).
# Até aqui isto dizia "o cálculo fala do que é CONSTANTE, a álgebra linear do
# que é LINEAR". O segundo rótulo é a definição do livro e fica. O primeiro
# estava errado por TIPO: "linear" é propriedade verificável de um mapa
# (T(x+y)=T(x)+T(y) e T(ax)=aT(x)); "constante" não nomeia o que o cálculo
# estuda — nomeia o caso degenerado que ele existe para detectar a ausência.
#
# Pior, os dois rótulos não eram irmãos: a derivada É um operador linear, e ser
# derivável É ser localmente linear — f(a+h) = f(a) + L(h) + o(|h|), onde f(a)
# é a CONSTANTE e L é a parte LINEAR. Eram o termo 0 e o termo 1 da mesma
# expansão, não dois reinos. A constante desceu de assunto do arco para ZERO DO
# INSTRUMENTO: ker D, o que a derivada não enxerga (e daí o "+C" da integral).
#
# A independência dos arcos SOBREVIVE, com outro fundamento: é curricular e
# vale em UMA VARIÁVEL. Em várias, a derivada vira matriz e os arcos se fundem
# — ver os três nós que já moram nos dois troncos (geom_dif, analise_func,
# topologia), que são o teto medido desta dicotomia.
NATUREZA = {
    "calculo":  ("C", "o que acontece perto de um ponto",
                 "o que acontece perto de um ponto — e a constante é o zero do "
                 "instrumento: ker D, o que a derivada não vê"),
    "algebra":  ("L", "o que se preserva — soma e escala",
                 "o que se preserva: soma e escala, exatamente, em todo o domínio"),
}
# O azul da geometria vira o traço da REGIÃO, não de um tronco: é o contorno
# interno que marca, dentro do verde, o que é geometria analítica.
COR_REGIAO = (120, 196, 255)
OURO = "#c9a266"

# DEFEITO ACHADO EM 2026-08-24: os chips do cabeçalho usavam cores PRÓPRIAS, e
# elas estavam ROTACIONADAS em relação ao contorno dos nós — o chip "cálculo"
# era azul (o matiz da geometria), o "geometria" era verde (o da álgebra), e o
# "álgebra" era uma terracota que não pertencia a ninguém. Medido: 207°, 102° e
# 103° de diferença de matiz. Com o chip dizendo uma cor e o nó dizendo outra, o
# olho não aprende a associação — que é a razão de o mapa ser colorido.
# Agora o chip É a cor do tronco, derivada da mesma fonte.
def _hx(rgb):
    return "#%02x%02x%02x" % rgb


RAMOS = {
    "base":      ("o tronco — anterior aos dois", "#c9a266"),
    "calculo":   ("cálculo · PERTO DE UM PONTO",  _hx(TRONCOS["calculo"][0])),
    "algebra":   ("álgebra linear · O QUE SE PRESERVA", _hx(TRONCOS["algebra"][0])),
    "geometria": ("geometria analítica — dentro da álgebra linear", _hx(COR_REGIAO)),
    "fronteira": ("fronteira — sem obra no acervo", "#7c88a1"),
}


def cor_do_no(doms, tema):
    """Soma de luz no tema escuro; média no claro (a soma clareia demais lá)."""
    if not doms:
        return OURO
    cs = [TRONCOS[d][0] for d in doms]
    if tema == "escuro":
        c = tuple(min(255, sum(x[i] for x in cs)) for i in range(3))
    else:
        c = tuple(round(sum(x[i] for x in cs) / len(cs)) for i in range(3))
    return "#%02x%02x%02x" % c


def forma(doms, L, A, raiz=False):
    """A forma carrega o tronco — §1.3(a): forma é significado atribuído.

    base (nenhum tronco)  retângulo de canto suave · o tronco anterior aos dois
    cálculo               laterais arredondadas (o stadium)
    álgebra linear        hexágono, como o nó de tempo do Nuke
    dois troncos          octógono — os cantos chanfrados dizem "mistura"

    A GEOMETRIA ANALÍTICA NÃO TEM FORMA PRÓPRIA desde 2026-08-25: ela não é um
    tronco, é uma região DENTRO do hexágono da álgebra linear, e se marca por
    contorno duplo (ver `contorno_regiao`). Dar-lhe forma própria de novo seria
    voltar a afirmar que ela é irmã, e não parte.
    """
    if raiz:
        return f'<rect width="{L}" height="{A}" rx="{A/2}" ry="{A/2}"></rect>'
    if len(doms) >= 2:
        c = 11
        pts = [(c,0),(L-c,0),(L,c),(L,A-c),(L-c,A),(c,A),(0,A-c),(0,c)]
        return '<polygon points="' + " ".join(f"{x},{y}" for x, y in pts) + '"></polygon>'
    if doms == ("calculo",):
        return f'<rect width="{L}" height="{A}" rx="{A/2}" ry="{A/2}"></rect>'
    if doms == ("algebra",):
        c = 15
        pts = [(c,0),(L-c,0),(L,A/2),(L-c,A),(c,A),(0,A/2)]
        return '<polygon points="' + " ".join(f"{x},{y}" for x, y in pts) + '"></polygon>'
    return f'<rect width="{L}" height="{A}" rx="8"></rect>'


def contorno_regiao(doms, L, A, raiz=False):
    """O contorno INTERNO que marca a região geométrica dentro da álgebra.

    Contenção se desenha como contorno dentro de contorno — não como cor
    misturada, que dizia "cruzam-se", nem como forma própria, que dizia
    "são irmãs". A mesma silhueta, um pouco menor, por dentro.
    """
    d = 5
    l, a = L - 2 * d, A - 2 * d
    if raiz:
        corpo = f'<rect width="{l}" height="{a}" rx="{a/2}" ry="{a/2}"></rect>'
    elif len(doms) >= 2:
        c = 8
        pts = [(c,0),(l-c,0),(l,c),(l,a-c),(l-c,a),(c,a),(0,a-c),(0,c)]
        corpo = '<polygon points="' + " ".join(f"{x},{y}" for x, y in pts) + '"></polygon>'
    elif doms == ("calculo",):
        corpo = f'<rect width="{l}" height="{a}" rx="{a/2}" ry="{a/2}"></rect>'
    elif doms == ("algebra",):
        c = 12
        pts = [(c,0),(l-c,0),(l,a/2),(l-c,a),(c,a),(0,a/2)]
        corpo = '<polygon points="' + " ".join(f"{x},{y}" for x, y in pts) + '"></polygon>'
    else:
        corpo = f'<rect width="{l}" height="{a}" rx="6"></rect>'
    return f'<g class="regiao-geo" transform="translate({d},{d})">{corpo}</g>'


def badges(doms, L, A):
    """As marcas de canto — a metodologia dos nós do Nuke, aplicada ao mapa.

    No Nuke um nó carrega no canto um disco com letra dizendo o que ele TEM:
    A de animação, E de expressão, C de clone. O rótulo não muda; a informação
    entra por fora. Aqui a letra diz o TRONCO da matéria — C de cálculo, L de
    álgebra linear.

    ATÉ 2026-08-26 a letra dizia a NATUREZA ("C de constante, L de linear") e
    este docstring afirmava ser o único lugar da página onde a tese aparecia no
    próprio nó. A emenda da `norma-de-notacao.md` §1.2c derrubou aquele par de
    rótulos, e nenhum par de INICIAIS o substitui — "preserva" e "perto de um
    ponto" começam com a mesma letra. A natureza passou inteira para o painel,
    e esta afirmação sai daqui em vez de ficar mentindo.

    A base fica SEM marca de propósito: ela não é nem uma coisa nem outra, é
    anterior às duas. Marcar tudo diria que tudo se classifica.
    """
    if not doms:
        return ""
    r, saida = 8.5, []
    for k, d in enumerate(doms):
        letra, _nome, _ = NATUREZA[d]
        cx, cy = L - r - 2, r + 2 + k * (2 * r + 3)
        saida.append(
            f'<g class="badge badge-{d}">'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"></circle>'
            f'<text x="{cx:.1f}" y="{cy + 3.6:.1f}" text-anchor="middle">{letra}</text>'
            f'</g>')
    return "".join(saida)


def ortogonal(pts, desvio):
    """Sem diagonal: cada trecho vira um Z — desce, anda, desce.

    Pedido do operador (2026-08-18): só horizontal, vertical e L. A diagonal
    some. O `desvio` afasta o degrau horizontal de cada aresta dentro do vão
    entre camadas, para que duas arestas não se deitem uma sobre a outra.
    """
    saida = [pts[0]]
    for k in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[k], pts[k + 1]
        if abs(x1 - x2) < 0.5:
            saida.append((x2, y2))
            continue
        ym = (y1 + y2) / 2 + desvio
        saida += [(x1, ym), (x2, ym), (x2, y2)]
    return saida


def montar_svg():
    r = montar()
    nivel, ordem = r["nivel"], r["ordem"]
    reais = {n[0]: n for n in NOS}

    # x pela ordem dentro da camada, centralizado; y pela camada.
    # O nó virtual NÃO é caixa: ele é só o lugar por onde a seta longa passa.
    # Dar a ele a largura de uma caixa inflava o desenho e fazia a aresta
    # desviar até a borda — o "bico" que o olho pegou na 1ª geração.
    por_camada = {}
    for i, n in nivel.items():
        por_camada.setdefault(n, []).append(i)
    for n in por_camada:
        por_camada[n].sort(key=lambda i: ordem[i])

    def larg(i):
        return VIRTUAL_L if i.startswith("~") else CAIXA_L

    H = MARGEM * 2 + (max(nivel.values()) + 1) * GAP_Y - (GAP_Y - CAIXA_A)

    # ⚠ MEDIDO e DESCARTADO (2026-08-18): tentei alinhar as coordenadas ao
    # baricentro dos vizinhos para endireitar as arestas. A medida derrubou a
    # ideia — comprimento das arestas caiu só 1,4% (29.590 -> 29.170 px) e a
    # largura subiu 64% (1.572 -> 2.581 px). O código do alinhamento fica em
    # layout.py para quem quiser retomar com resolução de colisão melhor.
    # O que rendeu de verdade foi o gap menor entre nós virtuais vizinhos.
    def gap_entre(i, j):
        return GAP_VIRTUAL if (i.startswith("~") and j.startswith("~")) else GAP_X

    def total_da_camada(ids):
        t = sum(larg(i) for i in ids)
        return t + sum(gap_entre(ids[k], ids[k+1]) for k in range(len(ids)-1))

    W = MARGEM * 2 + max(total_da_camada(v) for v in por_camada.values())
    pos = {}
    for n, ids in por_camada.items():
        x = (W - total_da_camada(ids)) / 2
        for k, i in enumerate(ids):
            pos[i] = (x, MARGEM + n * GAP_Y)
            if k < len(ids) - 1:
                x += larg(i) + gap_entre(i, ids[k+1])
    return r, pos, W, H, reais


def caminhos(arestas_v, pos):
    """Uma polilinha por aresta original, passando pelos nós virtuais."""
    partes = {}
    for a, b, w, f, virtual in arestas_v:
        raiz = a if not a.startswith("~") else a.split("#")[0][1:]
        chave = raiz if virtual else f"{a}>{b}"
        partes.setdefault(chave, []).append((a, b, w, f))
    return partes


def gerar():
    r, pos, W, H, reais = montar_svg()
    nivel = r["nivel"]

    # --- arestas: encadeia os trechos virtuais numa polilinha só ------------
    seguinte = {}
    for a, b, w, f, v in r["arestas_v"]:
        seguinte.setdefault(a, []).append((b, w, f, v))

    linhas = []
    for idx, (a, b, w, f) in enumerate(ARESTAS):
        pts, atual = [], a
        pts_ids = [a]
        pts.append(pos[a])
        while atual != b:
            prox = None
            for cand, cw, cf, cv in seguinte.get(atual, []):
                if cand == b or (cand.startswith("~") and cand.startswith(f"~{a}>{b}#")):
                    prox = cand
                    break
            if prox is None:
                break
            pts.append(pos[prox])
            pts_ids.append(prox)
            atual = prox
        d = []
        ids_pts = [a] + [p for p in pts_ids[1:]]
        for k, (x, y) in enumerate(pts):
            nid = ids_pts[k]
            cx = x + (VIRTUAL_L if nid.startswith("~") else CAIXA_L) / 2
            cy = y + (CAIXA_A if k == 0 else 0)
            if k and k < len(pts) - 1:
                cy = y + CAIXA_A / 2
            d.append((cx, cy))
        desvio = ((idx % 7) - 3) * 5          # espalha os degraus dentro do vão
        linhas.append({"de": a, "para": b, "warrant": w, "fonte": f,
                       "pts": ortogonal(d, desvio)})

    # --- SVG ---------------------------------------------------------------
    svg = []

    # O CONJUNTO DA ARITMÉTICA, desenhado (2026-08-24). Os cinco pilares são o
    # CONTEÚDO de "Aritmética e as operações", não cinco irmãos soltos — e é
    # neste bloco que se aponta a lacuna que veio do ensino básico. Uma moldura
    # tracejada dá a ver o conjunto sem inventar um nó que não existe.
    PILARES = ("op_quatro", "fracoes", "potencias", "negativos", "fatoracao")
    if all(k in pos for k in PILARES):
        xs = [pos[k][0] for k in PILARES]
        ys = [pos[k][1] for k in PILARES]
        m = 16
        gx, gy = min(xs) - m, min(ys) - m - 20
        gw = (max(xs) + CAIXA_L + m) - gx
        gh = (max(ys) + CAIXA_A + m) - gy
        svg.append(
            f'<g class="grupo-aritmetica">'
            f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{gw:.1f}" height="{gh:.1f}" '
            f'rx="14" ry="14"></rect>'
            f'<text x="{gx + 14:.1f}" y="{gy + 16:.1f}">'
            f'os pilares da aritmética — onde a lacuna do ensino básico aparece'
            f'</text></g>')

    for L in linhas:
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in L["pts"])
        svg.append(f'<polyline class="aresta w-{L["warrant"]}" points="{p}" '
                   f'data-de="{L["de"]}" data-para="{L["para"]}" '
                   f'marker-end="url(#seta-{L["warrant"]})"></polyline>')
    for nid, rot, ramo, nota in NOS:
        x, y = pos[nid]
        doms = tuple(sorted(DOMINIOS[nid][0]))
        chave = "-".join(doms) if doms else "base"
        raiz = nivel[nid] == 0
        svg.append(
            f'<g class="no ramo-{ramo} dom-{chave}'
            f'{" na-regiao" if nid in REGIAO_GEO else ""}" data-id="{nid}" '
            f'data-dom="{chave}" transform="translate({x:.1f},{y:.1f})">'
            + forma(doms, CAIXA_L, CAIXA_A, raiz)
            + (contorno_regiao(doms, CAIXA_L, CAIXA_A, raiz)
               if nid in REGIAO_GEO else "")
            + badges(doms, CAIXA_L, CAIXA_A)
            + "".join(
                f'<text x="{CAIXA_L/2}" y="{CAIXA_A/2 + (i - (len(rot.split(chr(10)))-1)/2)*15 + 5:.1f}">'
                f'{html.escape(l)}</text>'
                for i, l in enumerate(rot.split("\n")))
            + "</g>")

    # OS VERBETES (2026-08-25). Gerados fora daqui — a página é estática, e
    # quem escreve é o phi-4 local, orquestrado pelo `gerar_textos_mapa.py` da
    # Hipátia. Aqui eles só são EMBUTIDOS. Se o arquivo não existe, o mapa
    # continua funcionando sem eles: o texto é acréscimo, não dependência.
    verbetes = {}
    cam = os.path.join(AQUI, "textos-nos.json")
    if os.path.exists(cam):
        with open(cam, encoding="utf-8") as f:
            verbetes = json.load(f).get("nos", {})
    faltam = [n[0] for n in NOS if n[0] not in verbetes]
    if faltam:
        print(f"  ⚠ {len(faltam)} nó(s) sem verbete: {', '.join(faltam[:6])}"
              + ("…" if len(faltam) > 6 else ""))

    dados = {
        "verbetes": verbetes,
        "nos": {n[0]: {"rotulo": n[1].replace("\n", " "), "ramo": n[2], "nota": n[3],
                       "camada": nivel[n[0]],
                       "dom": list(sorted(DOMINIOS[n[0]][0])),
                       "geo": n[0] in REGIAO_GEO,
                       "dom_fonte": DOMINIOS[n[0]][1]} for n in NOS},
        "arestas": [{"de": a, "para": b, "w": w, "fonte": f} for a, b, w, f in ARESTAS],
        "cruz": {"antes": r["cruz_antes"], "depois": r["cruz_depois"]},
        "ramos": {k: v[0] for k, v in RAMOS.items()},
        "troncos": {k: v[1] for k, v in TRONCOS.items()},
        # a natureza vai ao painel: clicar num nó passa a dizer se ele é do que
        # se PRESERVA ou do que acontece PERTO DE UM PONTO, não só a que tronco
        # pertence. A frase já vem pronta de NATUREZA (2026-08-26) — antes era
        # montada aqui com um "o que é {...}" que a redação nova quebraria.
        "natureza": {k: v[1] for k, v in NATUREZA.items()},
    }

    combos = sorted({tuple(sorted(DOMINIOS[n[0]][0])) for n in NOS})
    css_dom = []
    for doms in combos:
        chave = "-".join(doms) if doms else "base"
        css_dom.append(f'.dom-{chave} > :first-child{{stroke:{cor_do_no(doms,"escuro")}}}')
        css_dom.append(f'html[data-tema="claro"] .dom-{chave} > :first-child'
                       f'{{stroke:{cor_do_no(doms,"claro")}}}')
    css_dom = "\n".join(css_dom)

    legenda_ramos = "".join(
        f'<span class="chip"><i style="background:{c}"></i>{html.escape(t)}</span>'
        for t, c in RAMOS.values())

    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(TEMPLATE
                .replace("{{SVG}}", "\n".join(svg))
                .replace("{{W}}", str(int(W)))
                .replace("{{H}}", str(int(H)))
                .replace("{{DADOS}}", json.dumps(dados, ensure_ascii=False))
                .replace("{{RAMOS}}", legenda_ramos)
                # o Venn e os ícones da legenda saem da MESMA fonte que os nós
                .replace("{{C_CALC}}", _hx(TRONCOS["calculo"][0]))
                .replace("{{C_ALG}}", _hx(TRONCOS["algebra"][0]))
                .replace("{{C_GEO}}", _hx(COR_REGIAO))
                .replace("/*{{CSS_DOM}}*/", css_dom)
                .replace("{{CRUZ_ANTES}}", str(r["cruz_antes"]))
                .replace("{{CRUZ_DEPOIS}}", str(r["cruz_depois"]))
                .replace("{{N_NOS}}", str(len(NOS)))
                .replace("{{N_ARESTAS}}", str(len(ARESTAS)))
                .replace("{{N_CAMADAS}}", str(max(nivel.values()) + 1)))
    return dados, r


TEMPLATE = r"""<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>O mapa das matérias — Hipátia</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0a1424; --sup:#111e34; --sup2:#16233f; --borda:#2a3d5e;
  --ink:#f0e4cc; --ink2:#ded2ba; --muted:#8b98b3;
  --ouro:#c9a266; --ouro-claro:#d4af6a; --terracota:#c56a45;
  --serif:"Cormorant Garamond",Georgia,serif;
  --sans:"Inter",system-ui,sans-serif;
}
html[data-tema="claro"]{
  --bg:#f3f5f9; --sup:#ffffff; --sup2:#eef1f7; --borda:#d9e0ec;
  --ink:#16233f; --ink2:#2b3a58; --muted:#7c88a1;
  --ouro:#a9713f; --ouro-claro:#8f5e33; --terracota:#b35430;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
     font-size:15px;line-height:1.5}
header{padding:18px 26px 12px;border-bottom:1px solid var(--borda)}
h1{font-family:var(--serif);font-weight:600;font-size:30px;margin:0 0 2px;
   letter-spacing:.01em}
.sub{color:var(--muted);font-size:13px;max-width:74ch}
.sub b{color:var(--ink2);font-weight:500}
.barra{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:12px}
input[type=search]{background:var(--sup);border:1px solid var(--borda);
  color:var(--ink);border-radius:8px;padding:7px 11px;font:inherit;font-size:13px;
  min-width:220px}
button{background:var(--sup);border:1px solid var(--borda);color:var(--ink2);
  border-radius:8px;padding:7px 12px;font:inherit;font-size:13px;cursor:pointer}
button:hover{border-color:var(--ouro);color:var(--ink)}
kbd{font:inherit;font-size:11px;border:1px solid var(--borda);border-radius:4px;
    padding:1px 5px;margin-left:5px;color:var(--muted);background:var(--fundo)}
.chips{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted)}
.chip{display:inline-flex;align-items:center;gap:6px}
.chip i{width:11px;height:11px;border-radius:3px;display:inline-block}
main{display:flex;gap:0;align-items:stretch}
#palco{flex:1;overflow:hidden;position:relative;cursor:grab;touch-action:none;
       height:calc(100vh - 210px);min-height:340px}
#palco.arrastando{cursor:grabbing}
svg{display:block;max-height:none}
aside{width:330px;flex:none;border-left:1px solid var(--borda);padding:18px 20px;
      overflow-y:auto;height:calc(100vh - 210px);min-height:340px;background:var(--sup)}
/* A COLUNA DE PROPRIEDADES (2026-08-25). Raciocínio do Nuke aplicado ao mapa:
   seleciona-se um nó e ele abre o painel de propriedades DELE, numa coluna
   própria. Antes isto vivia espremido embaixo do Venn, no fim de uma coluna
   que o leitor já tinha percorrido — e o texto mais longo da página ficava no
   pior lugar dela.
   ORDEM (correção do operador): o TEXTO vem primeiro, encostado no mapa, e as
   figuras ficam na ponta. Quem clica num nó olha para o lado e lê; a chave de
   cores e formas é consulta ocasional, e consulta ocasional mora mais longe.
   Fica SEMPRE aberta, mesmo vazia: coluna que aparece e some faz o mapa saltar
   de largura a cada clique, e o leitor perde o nó que estava olhando.
   UM POR VEZ, por decisão do operador — o Properties Bin do Nuke empilha, este
   não. */
#propriedades{width:390px;flex:none;border-left:1px solid var(--borda);
      padding:18px 22px;overflow-y:auto;height:calc(100vh - 210px);
      min-height:340px;background:var(--fundo)}
#propriedades h2{font-family:var(--serif);font-size:25px;margin:0 0 2px;font-weight:600}
#propriedades .ramo{font-size:12px;color:var(--muted);text-transform:uppercase;
      letter-spacing:.08em;margin-bottom:14px}
#propriedades h3{font-size:11.5px;text-transform:uppercase;letter-spacing:.08em;
      color:var(--muted);margin:18px 0 6px;font-weight:600}
#propriedades .verbete{color:var(--ink2);font-size:14px;line-height:1.55;margin:0 0 2px}
#propriedades .campo{margin-bottom:14px}
#propriedades .campo b{display:block;font-size:11.5px;text-transform:uppercase;
      letter-spacing:.06em;color:var(--ouro-claro);font-weight:600;margin-bottom:3px}
.proc{margin-top:20px;padding-top:10px;border-top:1px solid var(--borda);
      font-size:11px;color:var(--muted);line-height:1.5}
.sem-texto{font-size:12.5px;color:var(--muted);font-style:italic}
/* só aparece quando as colunas estão EMPILHADAS: no lado a lado o mapa nunca
   sai de vista, e um botão para "voltar" ao que está ali seria ruído. */
#ao-mapa{display:none}
@media (max-width: 1199px){
  #ao-mapa{display:inline-flex;align-items:center;gap:6px;margin-bottom:12px;
    background:var(--sup);border:1px solid var(--borda);color:var(--ink2);
    border-radius:8px;padding:8px 12px;font:inherit;font-size:13px;cursor:pointer}
  #ao-mapa:hover{border-color:var(--ouro);color:var(--ink)}
}
aside h2{font-family:var(--serif);font-size:23px;margin:0 0 2px;font-weight:600}
aside .ramo{font-size:12px;color:var(--muted);text-transform:uppercase;
            letter-spacing:.08em;margin-bottom:10px}
aside .nota{color:var(--ink2);font-size:14px;margin-bottom:16px}
aside h3{font-size:12px;text-transform:uppercase;letter-spacing:.08em;
         color:var(--muted);margin:16px 0 7px;font-weight:600}
.pre{border-left:2px solid var(--borda);padding:5px 0 5px 10px;margin-bottom:9px}
.pre b{font-weight:500;font-size:14px}
.pre .fonte{display:block;color:var(--muted);font-size:11.5px;margin-top:2px}
.marca-geo{color:{{C_GEO}};font-weight:600}
.pre.w-definicao{border-left-color:var(--ouro)}
.pre.w-ordem{border-left-color:var(--borda)}
.pre.w-orientacao{border-left-color:var(--ouro);border-left-style:dotted}
.pre.w-fronteira{border-left-color:var(--terracota);border-left-style:dashed}
.vazio{color:var(--muted);font-size:13px}
footer{padding:9px 26px;border-top:1px solid var(--borda);color:var(--muted);
       font-size:11.5px;display:flex;gap:18px;flex-wrap:wrap}
footer a{color:inherit;text-decoration:underline;text-underline-offset:2px}
footer .licenca{margin-left:auto}
/* --- o grafo --- */
.aresta{fill:none;stroke:var(--ouro);stroke-width:1.6;opacity:.75}
.aresta.w-ordem{stroke-width:1.1;opacity:.42}
/* orientação: pontilhada CURTA — mais presente que a fronteira (há uma pessoa
   responsável e uma data), menos que a ordem (não se abre o livro para
   conferir). O tracejado longo continua sendo só da fronteira. */
.aresta.w-orientacao{stroke-width:1.25;stroke-dasharray:2 3;opacity:.6}
.aresta.w-fronteira{stroke:var(--muted);stroke-width:1.1;stroke-dasharray:5 4;opacity:.5}

/* A REGIÃO GEOMÉTRICA — contorno dentro do contorno. Não tem preenchimento:
   se tivesse, competiria com a cor do tronco, e a região não é outro tronco. */
.regiao-geo > *{fill:none;stroke:{{C_GEO}};stroke-width:1.3;opacity:.85}
svg.focado .no:not(.acesa) .regiao-geo > *{opacity:.18}
/* AS MARCAS DE CANTO (2026-08-25) — o gesto dos nós do Nuke: um disco com
   letra dizendo o que a matéria É, sem tocar no rótulo. C de constante,
   L de linear. Ficam discretas até o nó entrar em foco. */
.badge circle{stroke:none;opacity:.85}
.badge text{font-family:var(--sans);font-size:11px;font-weight:700;
            fill:#0a1424;pointer-events:none}
.badge-calculo circle{fill:{{C_CALC}}}
.badge-algebra circle{fill:{{C_ALG}}}
svg.focado .no:not(.acesa) .badge{opacity:.15}
.no:hover .badge circle{opacity:1}
.no > :first-child{fill:var(--sup);stroke:var(--borda);stroke-width:1.7}
.no text{fill:var(--ink);font-family:var(--sans);font-size:12.5px;font-weight:500;
         text-anchor:middle;pointer-events:none}
.no{cursor:pointer}
.no:hover > :first-child{stroke-width:2.6}
.ramo-fronteira > :first-child{stroke-dasharray:5 4}
.ramo-fronteira text{fill:var(--muted)}
/*{{CSS_DOM}}*/
/* =======================================================================
   MOBILE (2026-08-24). Antes disto o mapa era inusável no telefone: o aside
   de 330px fixos comia 85% de uma tela de 390, sobrando ~155px para o grafo,
   e ainda transbordava para fora da janela. O cabeçalho tomava 40% da altura
   antes de mostrar qualquer coisa.

   A escolha: em tela estreita o mapa vira a tela inteira e o painel lateral
   desce para baixo dele, virando leitura em coluna. Não se esconde nada — a
   §1.5 da casa é information hiding, não information deleting.
   ======================================================================= */
/* ENTRE O TELEFONE E A TELA LARGA (2026-08-25). Com a coluna de propriedades
   são 330+390 = 720px de coluna FIXA: numa tela de 900px sobrariam 180px de
   mapa, que não é mapa nenhum. Aqui o mapa fica inteiro em cima e as duas
   colunas descem.
   É bloco PRÓPRIO, e não uma subida do breakpoint de 860: aquele carrega
   ajustes de DEDO (input a 16px para o iOS não dar zoom, alvo de toque de
   40px) que não têm o que fazer numa tela de mouse. */
@media (min-width: 861px) and (max-width: 1199px){
  main{flex-direction:column}
  #palco{flex:none;height:60vh;min-height:320px;width:100%}
  aside,#propriedades{width:100%;flex:none;height:auto;min-height:0;
        border-left:0;border-top:1px solid var(--borda)}
}

@media (max-width: 860px){
  body{font-size:15px}
  header{padding:12px 14px 10px}
  h1{font-size:22px}
  /* a explicação longa vira resumo: o texto inteiro fica no título do
     elemento e no painel, não sumiu */
  .sub{font-size:12.5px;max-width:none;
       display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;
       overflow:hidden}
  .barra{gap:8px;margin-top:10px}
  input[type=search]{min-width:0;flex:1 1 100%;padding:10px 12px;font-size:16px}
  button{padding:10px 13px}          /* alvo de toque: 40px de altura */
  .chips{width:100%;gap:10px 12px;font-size:11.5px}

  main{flex-direction:column}
  /* flex:none é ESSENCIAL: com flex:1 o flex-basis vence o height em coluna,
     e o palco crescia até a altura nativa do SVG (medido: 1614px), empurrando
     o mapa inteiro para fora da tela. */
  /* UM DEDO ROLA A PÁGINA, DOIS MOVEM O MAPA (2026-08-25). Com
     touch-action:none o palco engolia o gesto vertical, e como ele ocupa o
     MEIO da tela (medido: 439px de 844 no celular retrato), não sobrava por
     onde rolar: as colunas de texto e de figuras existiam no DOM e eram
     inalcançáveis. Padrão de mapa embutido em página: o gesto primário do
     celular é rolar. O mapa continua inteiro com dois dedos e com
     "ajustar à tela". */
  #palco{flex:none;height:58vh;min-height:280px;width:100%;touch-action:pan-y}
  aside{width:100%;flex:none;height:auto;min-height:0;max-height:none;
        border-left:0;border-top:1px solid var(--borda);padding:16px 14px}
  #propriedades{width:100%;flex:none;height:auto;min-height:0;
        border-left:0;border-top:1px solid var(--borda);padding:16px 14px}
  .rgb svg{width:100%;height:auto;max-width:252px}
  .formas{font-size:13px}
}

/* telefone estreito de verdade */
@media (max-width: 430px){
  h1{font-size:20px}
  .chips{font-size:11px;gap:8px 10px}
  #palco{flex:none;height:52vh}
}

/* deitado: a tela é baixa, então o mapa toma o que sobra e o painel rola */
@media (max-width: 860px) and (orientation: landscape){
  #palco{flex:none;height:76vh}
  .sub{display:none}
}

/* a moldura do conjunto da aritmética — tracejada porque é agrupamento, não
   dependência: nenhuma seta entra ou sai dela */
.grupo-aritmetica rect{fill:rgba(201,162,102,.05);stroke:var(--ouro);
  stroke-width:1.3;stroke-dasharray:7 5;opacity:.65}
.grupo-aritmetica text{fill:var(--ouro-claro);font-size:13px;font-weight:600;
  letter-spacing:.02em;font-family:Inter,sans-serif;opacity:1}
svg.focado .grupo-aritmetica{opacity:.2}

/* --- os dois troncos, e a região contida num deles --- */
.rgb{background:#0a1424;border:1px solid var(--borda);border-radius:10px;
     padding:12px 10px 8px;margin-bottom:18px}
.rgb svg{display:block;margin:0 auto}
.rgb circle{mix-blend-mode:screen}
.rgb .cap{color:var(--ink2);font-size:11.5px;text-align:center;margin-top:6px;line-height:1.4}
.formas{display:grid;grid-template-columns:auto 1fr;gap:9px 10px;align-items:center;
        font-size:12.5px;color:var(--ink2);margin-bottom:18px}
.formas b{color:var(--ink);font-weight:600}
.formas svg{display:block}
/* apagado, não sumido — §1.5 information hiding */
svg.focado .no{opacity:.16}
svg.focado .aresta{opacity:.07}
svg.focado .no.acesa{opacity:1}
svg.focado .aresta.acesa{opacity:.95;stroke-width:2.2}
svg.focado .no.alvo > :first-child{stroke-width:3.4}
svg.focado .no.alvo text{font-weight:600}
</style></head><body>

<header>
  <h1>O mapa das matérias</h1>
  <div class="sub">A ordem <b>lógica</b> — não a histórica, não a curricular.
    A direção é declarada uma vez e não se mistura: <b>de cima para baixo</b>,
    o pré-requisito sempre acima de quem o exige. Clique numa matéria para
    acender a cadeia inteira que a sustenta, até a linguagem dos conjuntos.<br>
    <b>Dois troncos, e eles não se apoiam um no outro</b>: a álgebra linear fala
    do que é <b>linear</b> — soma e escala preservadas; o cálculo fala do que é
    <b>constante</b>, e do que muda perto de um ponto. Cada matéria carrega no
    canto a marca do seu: <b>L</b> ou <b>C</b>.</div>
  <div class="barra">
    <input type="search" id="busca" placeholder="procurar matéria… (ex.: limite)" autocomplete="off">
    <button id="limpar">limpar</button>
    <button id="ajustar" title="reenquadra o mapa inteiro na tela — atalho: F">ajustar à tela <kbd>F</kbd></button>
    <button id="tema">tema claro</button>
    <span class="chips">{{RAMOS}}</span>
  </div>
</header>

<main>
  <div id="palco">
    <svg id="grafo" viewBox="0 0 {{W}} {{H}}" width="{{W}}" height="{{H}}"
         xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="seta-definicao" viewBox="0 0 8 8" refX="7" refY="4"
                markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--ouro)"></path></marker>
        <marker id="seta-ordem" viewBox="0 0 8 8" refX="7" refY="4"
                markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--ouro)" opacity=".55"></path></marker>
        <marker id="seta-orientacao" viewBox="0 0 8 8" refX="7" refY="4"
                markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--ouro)" opacity=".75"></path></marker>
        <marker id="seta-fronteira" viewBox="0 0 8 8" refX="7" refY="4"
                markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M0,0 L8,4 L0,8 z" fill="var(--muted)"></path></marker>
      </defs>
      {{SVG}}
    </svg>
  </div>
  <section id="propriedades">
    <button id="ao-mapa" type="button">↑ voltar ao mapa</button>
    <div id="painel">
      <div class="vazio">Nenhuma matéria escolhida.<br><br>
        Clique numa caixa do mapa — ou procure pelo nome — para ver o que ela é,
        por que existe, onde aparece no mundo, onde se costuma travar, e
        <b>de onde veio cada seta</b>.</div>
    </div>
  </section>

  <aside>
    <div class="rgb">
      <!-- 2026-08-24: círculos MAIORES (r 42 -> 56) e o rótulo no CENTRO de
           cada um. Os centros ficam na zona PURA — a distância entre dois
           centros (66 e 68) é maior que o raio, então nenhum rótulo cai sobre
           cor misturada, que é o que faria o nome mentir sobre a cor. -->
      <!-- 2026-08-25: eram três círculos que se cruzavam, em soma de luz. A
           orientação desta data desfez o terceiro tronco, e o desenho passou a
           dizer o que a matemática diz: a geometria analítica está DENTRO da
           álgebra linear — é a região dela onde há produto interno. Círculo
           dentro de círculo, não interseção. -->
      <svg width="252" height="186" viewBox="0 0 252 186" aria-label="os dois troncos, e a geometria analítica contida na álgebra linear">
        <circle cx="126" cy="52"  r="46" fill="{{C_CALC}}"></circle>
        <circle cx="126" cy="126" r="56" fill="{{C_ALG}}"></circle>
        <circle cx="126" cy="140" r="34" fill="none" stroke="{{C_GEO}}"
                stroke-width="2.2" stroke-dasharray="3 3"></circle>
        <text x="126" y="46" fill="#fff" font-size="11" font-weight="600"
              text-anchor="middle" dominant-baseline="central"
              font-family="Inter,sans-serif"
              style="paint-order:stroke;stroke:#0a1424;stroke-width:2.5px">CÁLCULO</text>
        <text x="126" y="100" fill="#fff" font-size="11" font-weight="600"
              text-anchor="middle" dominant-baseline="central"
              font-family="Inter,sans-serif"
              style="paint-order:stroke;stroke:#0a1424;stroke-width:2.5px">ÁLGEBRA LINEAR</text>
        <text x="126" y="140" fill="#fff" font-size="10" font-weight="600"
              text-anchor="middle" dominant-baseline="central"
              font-family="Inter,sans-serif"
              style="paint-order:stroke;stroke:#0a1424;stroke-width:2.5px">GEOM. ANALÍTICA</text>
      </svg>
      <div class="cap"><b>A álgebra linear fala do que se preserva</b> — soma e
        escala, exatamente, em todo o domínio; o <b>cálculo</b>, do que acontece
        <b>perto de um ponto</b>. Na ordem de estudo nenhum cobra o outro, e é
        por isso que a série é uma árvore, e não uma fila.<br><br>
        Independentes de <b>ordem</b>, não de natureza: a derivada é ela própria
        um operador linear, e derivar é achar a melhor aproximação linear perto
        do ponto. Em várias variáveis a derivada vira <b>matriz</b> e os dois se
        fundem — e é lá que mora a geometria da imagem.<br><br>
        E a geometria analítica fica <b>dentro</b>
        da álgebra linear — é a região dela onde existe <b>produto interno</b>,
        que é o que dá distância e ângulo, e portanto figura.<br>
        Em <b>qualquer</b> dimensão: o limite de três é da ilustração, que precisa
        caber no papel, nunca da estrutura.</div>
    </div>
    <div class="formas">
      <svg width="46" height="24"><rect x="1" y="1" width="44" height="22" rx="11" ry="11"
        fill="none" stroke="{{C_CALC}}" stroke-width="2.6"></rect></svg>
      <span><b>Cálculo</b> — laterais arredondadas</span>
      <svg width="46" height="24"><polygon points="8,1 38,1 45,12 38,23 8,23 1,12"
        fill="none" stroke="{{C_ALG}}" stroke-width="2.6"></polygon></svg>
      <span><b>Álgebra Linear</b> — hexágono</span>
      <svg width="46" height="24"><polygon points="8,1 38,1 45,12 38,23 8,23 1,12"
        fill="none" stroke="{{C_ALG}}" stroke-width="2.6"></polygon><polygon
        points="12,5 34,5 39,12 34,19 12,19 5,12"
        fill="none" stroke="{{C_GEO}}" stroke-width="1.5"></polygon></svg>
      <span><b>Geometria Analítica</b> — contorno duplo: está <b>dentro</b> da álgebra linear</span>
      <svg width="46" height="24"><polygon points="7,1 39,1 45,6 45,18 39,23 7,23 1,18 1,6"
        fill="none" stroke="#f8d66a" stroke-width="2.6"></polygon></svg>
      <span><b>Dois troncos</b> — cantos chanfrados, cor somada</span>
      <svg width="46" height="24"><rect x="1" y="1" width="44" height="22" rx="6"
        fill="none" stroke="#c9a266" stroke-width="2.6"></rect></svg>
      <span><b>A base</b> — anterior aos dois, e por isso <b>sem marca</b></span>
      <svg width="46" height="24"><circle cx="13" cy="12" r="8.5" fill="{{C_CALC}}"></circle>
        <text x="13" y="15.6" text-anchor="middle" font-size="11" font-weight="700"
          font-family="Inter,sans-serif" fill="#0a1424">C</text>
        <circle cx="33" cy="12" r="8.5" fill="{{C_ALG}}"></circle>
        <text x="33" y="15.6" text-anchor="middle" font-size="11" font-weight="700"
          font-family="Inter,sans-serif" fill="#0a1424">L</text></svg>
      <span><b>A marca de canto</b> — <b>C</b> de constante, <b>L</b> de linear:
        a matéria diz a que tronco pertence sem depender da cor</span>
    </div>
  </aside>
</main>

<footer>
  <span>{{N_NOS}} matérias · {{N_ARESTAS}} dependências · {{N_CAMADAS}} camadas</span>
  <span>cruzamentos de aresta: <b>{{CRUZ_ANTES}} → {{CRUZ_DEPOIS}}</b> (§1.1 da norma de diagramas)</span>
  <span>seta cheia = definição · fraca = ordem do livro · pontilhada = orientação acadêmica · tracejada = sem obra no acervo</span>
  <span class="licenca">© 2026 Mateus Alkimim · conteúdo sob <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a> · código sob MIT</span>
</footer>

<script>
const D = {{DADOS}};
const svg = document.getElementById('grafo');
const palco = document.getElementById('palco');
const painel = document.getElementById('painel');

const pais = {}, filhos = {};
D.arestas.forEach(a => {
  (pais[a.para] = pais[a.para] || []).push(a);
  (filhos[a.de] = filhos[a.de] || []).push(a);
});

function ancestrais(id){
  const vistos = new Set(), fila = [id];
  while(fila.length){
    const c = fila.pop();
    (pais[c]||[]).forEach(a => { if(!vistos.has(a.de)){ vistos.add(a.de); fila.push(a.de); } });
  }
  return vistos;
}

const CAMPOS = [['o_que_e','o que é'], ['por_que_existe','por que existe'],
                ['onde_aparece','onde aparece no mundo'], ['onde_se_trava','onde se trava']];

function verbete(id){
  const v = (D.verbetes||{})[id];
  if(!v) return '<div class="sem-texto">Sem verbete escrito para esta matéria ainda.</div>';
  const corpo = CAMPOS.filter(([k]) => v[k]).map(([k,rot]) =>
    '<div class="campo"><b>' + rot + '</b><p class="verbete">' + esc(v[k]) + '</p></div>').join('');
  const p = v.procedencia || {};
  // A PROCEDÊNCIA aparece porque este mapa declara de onde vem cada seta; um
  // texto de modelo entrando calado seria a única afirmação sem warrant aqui.
  const proc = p.modelo
    ? '<div class="proc">Verbete escrito por <b>' + esc(p.modelo) + '</b> (' +
      esc(p.onde || '') + '), ' + esc(p.data || '') + ' — ' +
      (p.revisado_por_humano ? 'revisado por leitura humana.'
                             : '<b>ainda não revisado por leitura humana.</b>') + '</div>'
    : '';
  return corpo + proc;
}

function esc(t){
  const d = document.createElement('div'); d.textContent = t; return d.innerHTML;
}

// Sem isto, clicar num nó no celular preenchia um painel FORA DA TELA — medido
// em 2026-08-25: painel no topo 710 de um viewport de 844, e 483 de 390 no
// deitado. O leitor tocava, nada acontecia à vista, e concluía que não havia
// nada ali.
function levarAoPainel(){
  if(!empilhado()) return;
  const alvo = document.getElementById('propriedades');
  requestAnimationFrame(() => alvo.scrollIntoView({behavior:'smooth', block:'start'}));
}

function acender(id){
  const anc = ancestrais(id);
  const conjunto = new Set([...anc, id]);
  svg.classList.add('focado');
  svg.querySelectorAll('.no').forEach(g =>
    g.classList.toggle('acesa', conjunto.has(g.dataset.id)));
  svg.querySelectorAll('.no').forEach(g =>
    g.classList.toggle('alvo', g.dataset.id === id));
  svg.querySelectorAll('.aresta').forEach(l =>
    l.classList.toggle('acesa', conjunto.has(l.dataset.de) && conjunto.has(l.dataset.para)));

  const n = D.nos[id];
  const diretos = (pais[id]||[]);
  const usa = (filhos[id]||[]);
  painel.innerHTML =
    '<h2>' + n.rotulo + '</h2>' +
    '<div class="ramo">' + (n.dom.length
        ? n.dom.map(d => D.troncos[d] + ' · ' + (D.natureza[d] || '')).join('  +  ')
        : 'a base — anterior aos dois troncos') + ' · camada ' + n.camada +
        (n.geo ? ' · <b class="marca-geo">geometria analítica</b>' : '') + '</div>' +
    verbete(id) +
    '<div class="nota" style="font-size:11.5px;color:var(--muted);margin-bottom:12px">' +
        n.dom_fonte + '</div>' +
    '<div class="nota">' + n.nota + '</div>' +
    '<h3>depende diretamente de</h3>' +
    (diretos.length ? diretos.map(a =>
      '<div class="pre w-' + a.w + '"><b>' + D.nos[a.de].rotulo + '</b>' +
      '<span class="fonte">' + a.fonte + '</span></div>').join('')
      : '<div class="vazio">Nada. É onde o mapa começa.</div>') +
    '<h3>a cadeia inteira que a sustenta</h3>' +
    '<div class="nota">' + (anc.size ? anc.size + ' matérias acesas no mapa.' :
      'Nenhuma — esta é a raiz.') + '</div>' +
    '<h3>abre caminho para</h3>' +
    (usa.length ? usa.map(a => '<div class="pre w-' + a.w + '"><b>' +
      D.nos[a.para].rotulo + '</b></div>').join('')
      : '<div class="vazio">Ponta do mapa, por enquanto.</div>');
}

function limpar(){
  svg.classList.remove('focado');
  svg.querySelectorAll('.acesa,.alvo').forEach(e => e.classList.remove('acesa','alvo'));
  painel.innerHTML = '<div class="vazio">Nenhuma matéria escolhida.<br><br>' +
    'Clique numa caixa do mapa — ou procure pelo nome — para ver o que ela é, ' +
    'de quais matérias ela depende, e <b>de onde veio cada seta</b>.</div>';
}

// A rolagem vai no CLIQUE, não dentro de acender(): a busca também chama
// acender, e rolar a página a cada tecla digitada — com o teclado do celular
// aberto — seria pior que o defeito que isto conserta.
svg.querySelectorAll('.no').forEach(g =>
  g.addEventListener('click', e => {
    e.stopPropagation(); acender(g.dataset.id); levarAoPainel();
  }));
document.getElementById('ao-mapa').addEventListener('click', () =>
  document.getElementById('palco').scrollIntoView({behavior:'smooth', block:'start'}));
palco.addEventListener('click', limpar);
document.getElementById('limpar').addEventListener('click', limpar);

document.getElementById('busca').addEventListener('input', e => {
  const q = e.target.value.trim().toLowerCase();
  if(!q) return limpar();
  const achado = Object.keys(D.nos).find(k =>
    D.nos[k].rotulo.toLowerCase().includes(q));
  if(achado) acender(achado);
});

document.getElementById('tema').addEventListener('click', e => {
  const claro = document.documentElement.dataset.tema === 'claro';
  document.documentElement.dataset.tema = claro ? '' : 'claro';
  e.target.textContent = claro ? 'tema claro' : 'tema escuro';
});

/* --- zoom e arrasto: o mapa é para apontar na tela --- */
// EMPILHADO: as colunas estão embaixo do mapa, não ao lado — o leitor não vê
// o painel sem rolar. TOQUE-ROLA: tela de dedo, onde um dedo pertence à página
// e não ao mapa. São perguntas diferentes e têm larguras diferentes.
const empilhado = () => matchMedia('(max-width: 1199px)').matches;
const toqueRolaPagina = () => matchMedia('(max-width: 860px)').matches;

let z = 1, tx = 0, ty = 0, arrastando = false, x0 = 0, y0 = 0;
function aplicar(){ svg.style.transform = `translate(${tx}px,${ty}px) scale(${z})`;
                    svg.style.transformOrigin = '0 0'; }
function ajustar(){
  const r = palco.getBoundingClientRect();
  z = Math.min(r.width / {{W}}, r.height / {{H}}) * 0.96;
  tx = (r.width - {{W}} * z) / 2; ty = (r.height - {{H}} * z) / 2;
  aplicar();
}
palco.addEventListener('wheel', e => {
  e.preventDefault();
  const r = palco.getBoundingClientRect();
  const mx = e.clientX - r.left, my = e.clientY - r.top;
  const k = e.deltaY < 0 ? 1.12 : 1/1.12;
  const zn = Math.min(3, Math.max(0.15, z * k));
  tx = mx - (mx - tx) * (zn / z); ty = my - (my - ty) * (zn / z);
  z = zn; aplicar();
}, {passive:false});
palco.addEventListener('mousedown', e => {
  arrastando = true; palco.classList.add('arrastando');
  x0 = e.clientX - tx; y0 = e.clientY - ty;
});
addEventListener('mousemove', e => {
  if(!arrastando) return;
  tx = e.clientX - x0; ty = e.clientY - y0; aplicar();
});
addEventListener('mouseup', () => { arrastando = false; palco.classList.remove('arrastando'); });

/* --- TOQUE (2026-08-24): sem isto o mapa não se move no telefone. Um dedo
   arrasta; dois dedos dão pinça, com o zoom ancorado no PONTO MÉDIO entre os
   dedos — que é o gesto que a mão espera. `touch-action:none` no palco é o que
   impede o navegador de roubar o gesto para rolar a página. --- */
let toqueD = 0, toqueX = 0, toqueY = 0, toqueZ = 1;
const meio = t => ({x:(t[0].clientX + t[1].clientX)/2, y:(t[0].clientY + t[1].clientY)/2});
const dist = t => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
palco.addEventListener('touchstart', e => {
  const t = e.touches;
  // no celular, um dedo é da PÁGINA: quem move o mapa são dois.
  if(t.length === 1 && !toqueRolaPagina()){
    arrastando = true; x0 = t[0].clientX - tx; y0 = t[0].clientY - ty;
  }
  else if(t.length === 2){
    arrastando = false; toqueD = dist(t); toqueZ = z;
    const r = palco.getBoundingClientRect(), m = meio(t);
    toqueX = m.x - r.left; toqueY = m.y - r.top;
  }
}, {passive:true});
palco.addEventListener('touchmove', e => {
  const t = e.touches;
  if(t.length === 1 && arrastando){
    e.preventDefault();
    tx = t[0].clientX - x0; ty = t[0].clientY - y0; aplicar();
  } else if(t.length === 2 && toqueD){
    e.preventDefault();
    const zn = Math.min(3, Math.max(0.15, toqueZ * (dist(t) / toqueD)));
    tx = toqueX - (toqueX - tx) * (zn / z);
    ty = toqueY - (toqueY - ty) * (zn / z);
    z = zn;
    // com um dedo entregue à página, o ARRASTO do mapa passa a ser de dois —
    // sem isto o celular só conseguiria ampliar, nunca deslocar.
    const m = meio(t), r = palco.getBoundingClientRect();
    const mx = m.x - r.left, my = m.y - r.top;
    tx += mx - toqueX; ty += my - toqueY;
    toqueX = mx; toqueY = my;
    aplicar();
  }
}, {passive:false});
palco.addEventListener('touchend', e => {
  if(e.touches.length === 0){ arrastando = false; toqueD = 0; }
}, {passive:true});
document.getElementById('ajustar').addEventListener('click', ajustar);
// F DE FIT, como no Nuke. Ignorado enquanto se digita: procurar por "função"
// reenquadraria o mapa a cada "f" batido na busca.
addEventListener('keydown', e => {
  const t = document.activeElement;
  const digitando = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA');
  if (digitando || e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.key === 'f' || e.key === 'F') { e.preventDefault(); ajustar(); }
});
addEventListener('resize', ajustar);
ajustar();

/* abrir já apontando: index.html#integral — serve para deixar o link
   pronto antes da aula, e é como esta interação se testa sem clicar. */
function doHash(){
  const id = decodeURIComponent(location.hash.replace('#',''));
  if(id && D.nos[id]) acender(id); else limpar();
}
addEventListener('hashchange', doHash);
if(location.hash) doHash();
</script>
</body></html>
"""

if __name__ == "__main__":
    dados, r = gerar()
    print(f"{SAIDA}")
    print(f"  {len(dados['nos'])} matérias · {len(dados['arestas'])} dependências · "
          f"{max(n['camada'] for n in dados['nos'].values())+1} camadas")
    print(f"  cruzamentos: {r['cruz_antes']} -> {r['cruz_depois']}")
