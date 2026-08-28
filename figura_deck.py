# -*- coding: utf-8 -*-
"""O "você está aqui" — o mapa vira figura dentro de um deck da série.

Cada seminário abre dizendo ONDE ESTAMOS e fecha dizendo PARA ONDE VAMOS, e as
duas perguntas pedem desenhos diferentes:

  abertura   o mapa INTEIRO. As matérias do episódio e seus vizinhos diretos
             com rótulo legível; as outras ~40 como blocos apagados SEM rótulo.
             Não se lê caixa por caixa — lê-se a mancha: quanto do campo já foi
             andado, e onde este episódio cai.
  fecho      o RECORTE da vizinhança, todo rotulado, com as setas que saem dele.
             Aqui os nomes importam, porque a próxima dependência é o assunto.

Sob a §1.5 da norma de diagramas — **apagar em vez de sumir**: o contexto
continua visível, o foco não. É o mesmo gesto que o mapa interativo faz ao
acender uma cadeia; aqui ele vira artefato parado.

⚠️ TEMA CLARO, não o do site. Os decks do autor têm fundo `#f3f5f9`; o mapa
vive em navy. Herdar as cores do site poria texto claro sobre papel claro. As
matizes dos troncos são as mesmas — muda a mistura, que no claro é média e não
soma (`cor_do_no`), e a tinta do texto.

SVG e não PNG por uma razão de portão: o `auditar_rotulos_pdf` lê o TEXTO
VETORIAL do PDF. Rótulo em bitmap é rótulo que o auditor não vê.

Uso:
    python3 figura_deck.py --ids matrizes,sistemas,determinante \\
        --modo abertura --titulo "G2 · Determinantes" --saida onde-estamos.svg
"""
import argparse, html, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from materias import NOS, ARESTAS, DOMINIOS, REGIAO_GEO
from gerar_mapa import (CAIXA_L, CAIXA_A, TRONCOS, COR_REGIAO, _hx,
                        forma, contorno_regiao, ortogonal, montar_svg)

# A paleta do DECK, não a do site. Ver o cabeçalho.
PAPEL   = "#f3f5f9"
TINTA   = "#16233f"
APAGADO = "#c3ccdb"
OURO_D  = "#a9713f"     # o bronze do deck, no lugar do ouro do site


def cor_clara(doms):
    """Média das matizes — no claro a SOMA estoura para o branco."""
    if not doms:
        return OURO_D
    cs = [TRONCOS[d][0] for d in doms]
    return _hx(tuple(round(sum(c[i] for c in cs) / len(cs)) for i in range(3)))


def vizinhanca(ids):
    """Os do episódio, mais quem entra e quem sai deles — nada além."""
    dentro = set(ids)
    volta = {a for a, b, *_ in ARESTAS if b in dentro}
    sai = {b for a, b, *_ in ARESTAS if a in dentro}
    return dentro, volta - dentro, sai - dentro


def comprimir(pos, nivel, presentes, gap=120):
    """No recorte, as camadas SEM nó relevante colapsam.

    A vizinhança do determinante vai da camada 1 (contagem) à 9 (autovalores):
    no layout inteiro isso são 1.624px de altura por 714 de largura, que numa
    folha 16:9 vira um fio ilegível. Aqui as camadas presentes viram
    consecutivas — a ORDEM vertical se mantém (quem precede continua acima), e
    só o vão morto some. O x não se toca: a geografia horizontal é a mesma que
    o leitor viu na abertura.
    """
    camadas = sorted({nivel[i] for i in presentes})
    novo_y = {c: k * gap for k, c in enumerate(camadas)}
    return {i: (pos[i][0], novo_y[nivel[i]]) for i in presentes}, len(camadas)


def desenhar(ids, modo, titulo=None, margem=40):
    r, pos, W, H, _ = montar_svg()
    dentro, pais, filhos = vizinhanca(ids)
    rotulado = dentro | pais | filhos
    rot = {n[0]: n[1] for n in NOS}

    # ---- o quadro ----
    if modo == "recorte":
        pos, _n_cam = comprimir(pos, r["nivel"], dentro | pais | filhos)
        # ⚠️ O RECORTE É POR viewBox, com o layout INTACTO. Recalcular posições
        # só para os nós da vizinhança daria um desenho mais compacto e mentiria
        # sobre a geografia: o leitor acabou de ver o mapa inteiro na abertura,
        # e as caixas têm de estar onde estavam.
        xs = [pos[i][0] for i in rotulado]; ys = [pos[i][1] for i in rotulado]
        x0, y0 = min(xs) - margem, min(ys) - margem - (26 if titulo else 0)
        x1, y1 = max(xs) + CAIXA_L + margem, max(ys) + CAIXA_A + margem
    else:
        x0, y0 = -margem, -margem - (26 if titulo else 0)
        x1, y1 = W + margem, H + margem
    LW, LH = x1 - x0, y1 - y0

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} '
           f'{LW:.0f} {LH:.0f}" width="{LW:.0f}" height="{LH:.0f}" '
           f'role="img" aria-label="{html.escape(titulo or "mapa do episódio")}">',
           f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{LW:.0f}" height="{LH:.0f}" fill="{PAPEL}"/>']

    # ---- as arestas ----
    for idx, (a, b, w, f) in enumerate(ARESTAS):
        if modo == "recorte" and not (a in rotulado and b in rotulado):
            continue
        forte = (a in dentro or b in dentro)
        if modo == "recorte" and (a not in pos or b not in pos):
            continue
        p0 = (pos[a][0] + CAIXA_L / 2, pos[a][1] + CAIXA_A)
        p1 = (pos[b][0] + CAIXA_L / 2, pos[b][1])
        pts = ortogonal([p0, p1], ((idx % 7) - 3) * 5)
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        cor = OURO_D if forte else APAGADO
        larg = 1.6 if forte else 1.0
        tracejo = ' stroke-dasharray="5 4"' if w == "fronteira" else (
                  ' stroke-dasharray="2 3"' if w == "orientacao" else "")
        svg.append(f'<polyline points="{d}" fill="none" stroke="{cor}" '
                   f'stroke-width="{larg}"{tracejo} opacity="{0.85 if forte else 0.35}"/>')

    # ---- os nós ----
    for nid, rotulo, ramo, _nota in NOS:
        if modo == "recorte" and nid not in rotulado:
            continue
        x, y = pos[nid]
        doms = tuple(sorted(DOMINIOS[nid][0]))
        eh_foco = nid in dentro
        eh_vizinho = nid in rotulado and not eh_foco
        traco = cor_clara(doms) if (eh_foco or eh_vizinho) else APAGADO
        larg = 2.6 if eh_foco else (1.6 if eh_vizinho else 1.0)
        preenche = "#ffffff" if eh_foco else PAPEL
        svg.append(f'<g transform="translate({x:.1f},{y:.1f})" '
                   f'fill="{preenche}" stroke="{traco}" stroke-width="{larg}">')
        svg.append(forma(doms, CAIXA_L, CAIXA_A, raiz=(r["nivel"][nid] == 0)))
        if nid in REGIAO_GEO and (eh_foco or eh_vizinho):
            svg.append(contorno_regiao(doms, CAIXA_L, CAIXA_A,
                                       raiz=(r["nivel"][nid] == 0))
                       .replace('class="regiao-geo"',
                                f'fill="none" stroke="{_hx(COR_REGIAO)}" stroke-width="1.2"'))
        svg.append("</g>")
        # O RÓTULO SÓ NOS RELACIONADOS — decisão do autor. Cinquenta nomes
        # numa folha de 1920 não se leem; o que importa é ler os que importam.
        if nid in rotulado:
            linhas = rotulo.split("\n")
            for i, linha in enumerate(linhas):
                yy = y + CAIXA_A / 2 + (i - (len(linhas) - 1) / 2) * 14 + 4.5
                peso = 600 if eh_foco else 500
                svg.append(f'<text x="{x + CAIXA_L/2:.1f}" y="{yy:.1f}" '
                           f'text-anchor="middle" font-family="Inter,sans-serif" '
                           f'font-size="12" font-weight="{peso}" fill="{TINTA}">'
                           f'{html.escape(linha)}</text>')

    if titulo:
        svg.append(f'<text x="{x0 + 6:.0f}" y="{y0 + 18:.0f}" '
                   f'font-family="Inter,sans-serif" font-size="15" font-weight="600" '
                   f'fill="{TINTA}">{html.escape(titulo)}</text>')
    svg.append("</svg>")
    return "\n".join(svg), len(dentro), len(pais), len(filhos)


def main():
    ap = argparse.ArgumentParser(description="O mapa como figura de um deck.")
    ap.add_argument("--ids", required=True, help="ids das matérias do episódio, por vírgula")
    ap.add_argument("--modo", choices=["abertura", "recorte"], default="abertura")
    ap.add_argument("--titulo", default=None)
    ap.add_argument("--saida", required=True)
    a = ap.parse_args()

    ids = [i.strip() for i in a.ids.split(",") if i.strip()]
    conhecidos = {n[0] for n in NOS}
    fora = [i for i in ids if i not in conhecidos]
    if fora:
        # Falhar ALTO: id errado desenharia um mapa sem o episódio dentro, e
        # ninguém notaria olhando a figura.
        sys.exit(f"id(s) que não existem no mapa: {', '.join(fora)}")

    svg, n_d, n_p, n_f = desenhar(ids, a.modo, a.titulo)
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(svg)
    import re
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1).split()
    L, A = float(vb[2]), float(vb[3])
    print(f"{a.saida}")
    print(f"  modo {a.modo} · {n_d} do episódio · {n_p} de quem ele exige · "
          f"{n_f} de quem o exige")
    # A PROPORÇÃO É DADO DE COMPOSIÇÃO, não curiosidade: a folha é 1,78 e a
    # norma trabalha com figura de 1,48. Sai impressa para quem monta a folha
    # não descobrir na hora da diagramação.
    print(f"  {L:.0f}×{A:.0f} · proporção {L/A:.2f} (folha 1,78 · figura da norma 1,48)")


if __name__ == "__main__":
    main()
