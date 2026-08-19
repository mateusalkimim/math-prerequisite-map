# -*- coding: utf-8 -*-
"""Layout em camadas com minimização de cruzamentos — §1.1 da norma de diagramas.

Purchase (1997) mediu cinco estéticas de desenho de grafo contra compreensão
humana e achou que **reduzir cruzamento de arestas é, de longe, a mais
importante**. A norma da Hipátia adota o achado e vai além: em conflito com
qualquer outra regra, o cruzamento perde.

Por isso o layout não é escrito à mão. É Sugiyama enxuto:

  1. CAMADA por caminho mais longo — um nó fica abaixo de todos os seus
     pré-requisitos, sempre;
  2. NÓS VIRTUAIS nas arestas que pulam camadas, para que uma seta longa
     ocupe lugar em cada camada por onde passa em vez de atravessar o desenho;
  3. BARICENTRO iterado (descida e subida alternadas), guardando a melhor
     ordenação encontrada;
  4. CONTAGEM de cruzamentos antes e depois — o número entra no relatório,
     porque regra sem medida é preferência.
"""
from materias import NOS, ARESTAS


def camadas(ids, arestas):
    """Camada = 1 + a maior camada entre os pré-requisitos. Acusa ciclo."""
    pais = {i: [] for i in ids}
    for a, b, _, _ in arestas:
        pais[b].append(a)
    nivel, pend, voltas = {}, set(ids), 0
    while pend:
        voltas += 1
        if voltas > len(ids) + 2:
            raise ValueError(f"ciclo no grafo — não resolvem: {sorted(pend)}")
        for i in list(pend):
            ps = pais[i]
            if all(p in nivel for p in ps):
                nivel[i] = 1 + max([nivel[p] for p in ps], default=-1)
                pend.discard(i)
    return nivel


def com_virtuais(nivel, arestas):
    """Aresta que pula camada vira corrente de nós virtuais, um por camada."""
    novas, virtuais = [], []
    for a, b, w, f in arestas:
        salto = nivel[b] - nivel[a]
        if salto <= 1:
            novas.append((a, b, w, f, False))
            continue
        ant = a
        for k in range(1, salto):
            v = f"~{a}>{b}#{k}"
            virtuais.append((v, nivel[a] + k))
            novas.append((ant, v, w, f, True))
            ant = v
        novas.append((ant, b, w, f, True))
    return novas, virtuais


def cruzamentos(ordem, arestas, nivel):
    """Inversões entre pares de arestas que ligam as mesmas duas camadas."""
    total = 0
    por_camada = {}
    for a, b, *_ in arestas:
        por_camada.setdefault(nivel[a], []).append((ordem[a], ordem[b]))
    for pares in por_camada.values():
        for i in range(len(pares)):
            for j in range(i + 1, len(pares)):
                (a1, b1), (a2, b2) = pares[i], pares[j]
                if (a1 - a2) * (b1 - b2) < 0:
                    total += 1
    return total


def ordenar(nivel, arestas, passadas=24):
    niveis = {}
    for i, n in nivel.items():
        niveis.setdefault(n, []).append(i)
    for n in niveis:
        niveis[n].sort()
    ordem = {i: k for n in niveis for k, i in enumerate(niveis[n])}

    filhos, pais = {}, {}
    for a, b, *_ in arestas:
        filhos.setdefault(a, []).append(b)
        pais.setdefault(b, []).append(a)

    inicial = cruzamentos(ordem, arestas, nivel)
    melhor, melhor_ordem = inicial, dict(ordem)
    for p in range(passadas):
        descendo = p % 2 == 0
        camadas_ord = sorted(niveis) if descendo else sorted(niveis, reverse=True)
        for n in camadas_ord:
            viz = pais if descendo else filhos
            def bar(i):
                vs = [ordem[v] for v in viz.get(i, []) if v in ordem]
                return sum(vs) / len(vs) if vs else ordem[i]
            niveis[n].sort(key=bar)
            for k, i in enumerate(niveis[n]):
                ordem[i] = k
        c = cruzamentos(ordem, arestas, nivel)
        if c < melhor:
            melhor, melhor_ordem = c, dict(ordem)
    return melhor_ordem, inicial, melhor


def alinhar(pos_ordem, nivel, arestas, larg, gap, voltas=8):
    """Endireita as arestas SEM trocar a ordem — só encosta cada nó no x que
    seus vizinhos pedem, respeitando quem está ao lado.

    Sem isto, o baricentro acerta a ORDEM (que é o que corta cruzamento) e erra
    a POSIÇÃO: os nós virtuais ficam longe da reta entre origem e destino, e com
    roteamento ortogonal isso vira moldura correndo pela borda do desenho — o
    defeito que o olho pegou na 2ª geração. Cruzamento e desvio não são a mesma
    coisa, e a medida de um não vê o outro.
    """
    camadas_ = {}
    for i, n in nivel.items():
        camadas_.setdefault(n, []).append(i)
    for n in camadas_:
        camadas_[n].sort(key=lambda i: pos_ordem[i])

    viz = {}
    for a, b, *_ in arestas:
        viz.setdefault(a, []).append(b)
        viz.setdefault(b, []).append(a)

    x = {}
    for n, ids in camadas_.items():
        c = 0.0
        for i in ids:
            x[i] = c
            c += larg(i) + gap

    for _ in range(voltas):
        for n in sorted(camadas_) + sorted(camadas_, reverse=True):
            ids = camadas_[n]
            alvo = {}
            for i in ids:
                vs = [x[v] + larg(v) / 2 for v in viz.get(i, []) if v in x]
                alvo[i] = (sum(vs) / len(vs) - larg(i) / 2) if vs else x[i]
            # empurra para a direita respeitando a ordem, depois para a esquerda
            for k, i in enumerate(ids):
                x[i] = alvo[i]
                if k:
                    ant = ids[k - 1]
                    x[i] = max(x[i], x[ant] + larg(ant) + gap)
            for k in range(len(ids) - 2, -1, -1):
                i, prox = ids[k], ids[k + 1]
                x[i] = min(x[i], x[prox] - larg(i) - gap)
    return x


def montar():
    ids = [n[0] for n in NOS]
    nivel = camadas(ids, ARESTAS)
    arestas_v, virtuais = com_virtuais(nivel, ARESTAS)
    for v, n in virtuais:
        nivel[v] = n
    ordem, antes, depois = ordenar(nivel, arestas_v)
    return {"nivel": nivel, "ordem": ordem, "arestas_v": arestas_v,
            "alinhar": lambda larg, gap: alinhar(ordem, nivel, arestas_v, larg, gap),
            "virtuais": [v for v, _ in virtuais],
            "cruz_antes": antes, "cruz_depois": depois}
