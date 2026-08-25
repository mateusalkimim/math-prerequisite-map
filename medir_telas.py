# -*- coding: utf-8 -*-
"""O portão das telas — o mapa medido onde ele quase não foi usado.

A norma de diagramas §4 mandava medir em 1366x768 e 1920x1080, e era isso que
se media. O celular ficou de fora, e o defeito que apareceu em 2026-08-25 era
exatamente dele: as colunas de texto e de figuras EXISTIAM no DOM e eram
INALCANÇÁVEIS — o palco cobria o meio da tela com `touch-action: none`, então o
dedo não rolava a página, e clicar num nó preenchia um painel fora da vista.

Medido antes do conserto (celular 390x844): painel no topo 710 de 844, coluna
de figuras em 860 — fora da tela — e o clique num nó rolava 0px.

Duas medidas, porque são dois defeitos diferentes:

  telas()  o painel fica VISÍVEL depois de clicar num nó?
  gesto()  um dedo pertence à página e dois ao mapa?

A segunda existe porque o CSS certo não basta: o handler ainda podia chamar
preventDefault e matar a rolagem com o touch-action correto ao lado.

Uso:  ~/venvs/kaggle/bin/python medir_telas.py
"""

import sys
from playwright.sync_api import sync_playwright

ALVO = "file:///home/matte/repos/math-prerequisite-map/index.html"
TELAS = [("celular retrato", 390, 844), ("celular pequeno", 360, 640),
         ("celular deitado", 844, 390), ("tablet", 820, 1180)]

with sync_playwright() as pw:
    # o build que o playwright novo quer não está no cache; usa-se o que há,
    # em vez de baixar 180 MB para medir três larguras de tela.
    nav = pw.chromium.launch(executable_path="/home/matte/.cache/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-linux64/chrome-headless-shell")
    for nome, L, A in TELAS:
        pg = nav.new_page(viewport={"width": L, "height": A},
                          has_touch=True, is_mobile=True)
        pg.goto(ALVO); pg.wait_for_timeout(700)
        m = pg.evaluate("""() => {
          const q = s => document.querySelector(s);
          const cx = e => { const r = e.getBoundingClientRect();
             return {top: Math.round(r.top), h: Math.round(r.height),
                     vis: r.height > 0 && r.width > 0,
                     dentro: r.top < innerHeight && r.bottom > 0}; };
          const palco = q('#palco'), props = q('#propriedades'), aside = q('aside');
          return {
            vh: innerHeight, docH: Math.round(document.body.scrollHeight),
            rolavel: document.body.scrollHeight > innerHeight + 4,
            palco: cx(palco), props: cx(props), aside: cx(aside),
            touchPalco: getComputedStyle(palco).touchAction,
            touchBody: getComputedStyle(document.body).touchAction,
          };
        }""")
        print(f"\n━━ {nome} ({L}×{A})")
        print(f"   altura da página {m['docH']}px · viewport {m['vh']}px · rolável: {m['rolavel']}")
        print(f"   palco: topo {m['palco']['top']} alt {m['palco']['h']} · touch-action: {m['touchPalco']}")
        for k in ("props", "aside"):
            e = m[k]
            print(f"   {k:6s}: topo {e['top']:5d} alt {e['h']:4d} · "
                  f"visível no DOM: {e['vis']} · dentro da tela: {e['dentro']}")
        # o teste que importa: clicar num nó leva o leitor ao painel?
        pg.evaluate("window.scrollTo(0,0)")
        pg.wait_for_timeout(150)
        pg.evaluate("document.querySelector('.no[data-id=\"limite\"]').dispatchEvent(new MouseEvent('click',{bubbles:true}))")
        pg.wait_for_timeout(900)
        d = pg.evaluate("""() => {
          const r = document.querySelector('#propriedades').getBoundingClientRect();
          const p = document.querySelector('#painel');
          return {topo: Math.round(r.top), scrollY: Math.round(scrollY),
                  dentro: r.top < innerHeight && r.bottom > 0,
                  preenchido: !p.querySelector('.vazio')};
        }""")
        print(f"   → clicando num nó: painel preenchido={d['preenchido']} · "
              f"rolou para {d['scrollY']}px · painel no topo {d['topo']} · "
              f"VISÍVEL: {d['dentro']}")
        pg.close()
    nav.close()


# ======================================================================
# O GESTO
# ======================================================================

from playwright.sync_api import sync_playwright
BIN = ("/home/matte/.cache/ms-playwright/chromium_headless_shell-1228/"
       "chrome-headless-shell-linux64/chrome-headless-shell")
ALVO = "file:///home/matte/repos/math-prerequisite-map/index.html"

JS = """(nDedos) => {
  const palco = document.getElementById('palco');
  const r = palco.getBoundingClientRect();
  const toque = (x, y, id) => new Touch({identifier:id, target:palco,
      clientX:x, clientY:y, pageX:x, pageY:y});
  const pts = [];
  for(let i=0;i<nDedos;i++) pts.push(toque(r.left+80+i*60, r.top+80, i));
  const ev = (tipo, lista, cancelavel) => {
    const e = new TouchEvent(tipo, {touches:lista, targetTouches:lista,
      changedTouches:lista, bubbles:true, cancelable:cancelavel});
    palco.dispatchEvent(e); return e;
  };
  const antes = {tx: palco.querySelector('svg').style.transform};
  ev('touchstart', pts, true);
  const mov = [];
  for(let i=0;i<nDedos;i++) mov.push(toque(r.left+80+i*60, r.top+180, i));
  const e2 = ev('touchmove', mov, true);
  ev('touchend', [], true);
  return {impediuRolagem: e2.defaultPrevented,
          mapaMoveu: palco.querySelector('svg').style.transform !== antes.tx};
}"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=BIN)
    for nome, L, A, espera_impede in [("celular 390", 390, 844, False),
                                      ("celular 360", 360, 640, False),
                                      ("desktop 1440", 1440, 900, True)]:
        pg = nav.new_page(viewport={"width": L, "height": A},
                          has_touch=True, is_mobile=(L < 900))
        pg.goto(ALVO); pg.wait_for_timeout(600)
        um = pg.evaluate(JS, 1)
        dois = pg.evaluate(JS, 2)
        ta = pg.evaluate("getComputedStyle(document.getElementById('palco')).touchAction")
        ok1 = (um["impediuRolagem"] == espera_impede)
        ok2 = dois["mapaMoveu"]
        print(f"\n━━ {nome} · touch-action: {ta}")
        print(f"   {'✓' if ok1 else '✗'} UM dedo: impede a rolagem da página? "
              f"{um['impediuRolagem']} (esperado {espera_impede}) · mapa moveu: {um['mapaMoveu']}")
        print(f"   {'✓' if ok2 else '✗'} DOIS dedos: mapa moveu? {dois['mapaMoveu']}")
        pg.close()
    nav.close()
