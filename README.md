<!-- idioma: linha gerada por i18n.py -->
> [!NOTE]
> ### 🇧🇷 **[Leia esta página em português →](README.pt-BR.md)**

# The map of subjects — the logical order of the basic cycle

An interactive map of **prerequisites** for mathematics in the basic cycle: 50  
subjects, 78 dependencies, each arrow declaring where it came from. Clicking  
on a subject lights up the entire chain that supports it, up to the language of sets.

**→ [Open the map](https://mateusalkimim.github.io/math-prerequisite-map/)**

> **Status: PROPOSAL.** The graph is a statement about what precedes what, and it has not yet been ratified — it is a draft with a source, not teaching material. It is published this way on purpose: a wrong arrow sends the student to study the wrong thing, and it is better that it be contested than accepted in silence.  
> Disagreements are welcome in the issues.

A map of the **logical order** of the subjects — not the historical, not the curricular. The three orders were already distinguished in the `fig-tres-ordens` of a map of the historical genealogy (sibling document, unpublished); this document takes **the third** to its conclusion and makes it an instrument.

**Purpose**: Design on the screen and point where a student got stuck. Clicking on a topic lights up **the entire chain that supports it**, up to the language of sets — and shows, in the panel, where each arrow came from.

```bash
python3 gerar_mapa.py     # regenera o HTML (autossuficiente, abre sem servidor)
```

Open already pointing: `mapa-materias.html#integral` — the link is ready before the  
lesson. The identifiers are in `materias.py`.

## What the map measures

| | |
|---|---|
| subjects | **50** in **13 layers** |
| dependencies | **78** |
| edge crossings | **102 → 41** |

## No arrow enters without saying where it came from

The map will point out where a student got stuck: **a wrong arrow leads the student to study the wrong thing.** That's why each dependency carries its class of warrant, and it appears in the drawing and the panel:

- **definition** (26) — X enters the *definition* of Y in the cited work. It is the strong arrow: logical dependency, not curriculum convenience. *The derivative is defined as a limit* (Guidorizzi §7.2);  
- **order of the book** (29) — X is defined before Y in the same work, and Y uses it.  
  Established precedence, weaker evidence;  
- **academic orientation** (9) — the arrow comes from **registered orientation**, not  
  a verifiable page. Stronger than the border, because there is a responsible person  
  and a date; weaker than the order, because the book is not opened to check.  
  **Only enters with a date** — without a date, it's anonymous opinion. Dotted line.  
  The name of the person who oriented is not included in this publication until  
  there is approval from the person: the text of the warrant goes entirely to the  
  page, and a third party's name is not published without consent;  
- **border** (14) — a subject that **the archive does not cover**. The node appears  
  because the map needs to show where the roads go; the arrow is a declared judgment,  
  drawn with a weak line. It's honesty, not decoration.

Works (all in `mouseion/_dissecado/`): **Guidorizzi** v.1 (class A, TOC of  
157) · **Elon Lages Lima** (class A) · **Callioli** (class B — scan without TOC, and  
the archive card asks to check if it's partial; for this reason it only supports edge of  
*order*, never of *definition*) · **Merzbach & Boyer** (class A, TOC of 300).

## Two trunks, and one contains the other

There were **three** until 2026-08-25 — Calculus, Linear Algebra, and Analytic Geometry,  
designed in additive RGB, with color adding like light adds. An academic orientation  
dissolved the third:

> *"Analytic Geometry is a way of seeing Linear Algebra."*

Analytic Geometry is not a sister of Linear Algebra: it is **contained** within it. And containment has an exact name — it is the region of Linear Algebra where there exists **inner product**, which gives distance and angle, and therefore figure. In **any** dimension: tying Analytic Geometry to three dimensions confuses the limit of *illustration*, which needs to fit on paper, with the limit of *structure*, which has none.

The argument that concludes: the **real number itself is already a vector space** of dimension 1, and any real number is represented by the oriented segment that goes from the origin to it. If the most elementary object of the line is already vectorial, there is no way to separate one from the other.

| trunk | shape | color |
|---|---|---|
| **Calculus** (I, II, III) | rounded sides | red |
| **Linear Algebra** | hexagon (the time node of Nuke) | green |
| **Analytic Geometry** | **double outline** inside the hexagon | blue stroke |
| **two trunks** | beveled corners | the sum of the two lights |
| **the base** | soft corner | gold — prior to the two |

Containment is **drawn**, not declared in a legend: contour within a contour.  
The color mix said *"these two intersect"*; the inner contour said *"this is  
within that"*, which is what mathematics asserts. RGB went away with the third  
trunk — there were no more three lights to add.

⚠️ **Containment is not precedence, and therefore no arrow changed.** "Analytic Geometry is contained in Linear Algebra" says where the subject **resides**; the arrow says of what it **depends**. Drawing containment as an arrow would lead the student to study vector space before coordinates in the plane. It's the same mistake that already derailed a cycle in this map: there it was *"use"* against *"precedes"*, here it is *"contains"*.

**Belonging to a trunk is not depending on it.** *Calculus of several variables* depends on vectors but belongs to Calculus. The edge says who you depend on; the shape says where the subject is taught.

## The base has six areas, and the count is not the first

The layer prior to the two trunks has **16 nodes**, organized into the six areas  
of elementary mathematics (taxonomy of orientation, 2026-08-25):

1. **sets and numeric sets** — the language in which the remainder is spoken, and thus where the map begins. ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ: each exists because the previous was not enough — the integer provides the opposite, the rational provides the inverse, the real closes the gaps;  
2. **arithmetic and counting problems** — combinatorial reasoning, which is not the same area as the arithmetic of operations. It supports the **determinant**, which is a sum over the *n*! permutations;  
3. **plane and non-plane geometry** — the two-dimensional figure and the three-dimensional solid. This is where **trigonometry** resides: it is the ratio between the sides of a *triangle*, and before that it hung on elementary algebra without a base;  
4. **elementary algebra** — the letter in place of the number;  
5. **arithmetic and the operations** — which opens into five pillars, and where the gaps in basic education appear;  
6. **relations and functions** — a function is a relation in which each input has only one output. And the **ordered pair** of the Cartesian product is the same object as the coordinate in the plane: it is the common root of the function and analytic geometry.

**There are not four operations.** Subtraction is not an operation in its own  
right — it is adding the opposite; division is multiplying by the inverse. There  
are **two** operations and their inverses, and the same holds for exponentiation.

And that's where the place of the **logarithm** comes from: addition and multiplication are *commutative*, so each has **one** inverse. Exponentiation **is not commutative** (2³ ≠ 3²), and for that reason it has **two** — the root finds the *base*, the logarithm finds the *exponent*. The log is not an intruder in arithmetic: it is the second inverse that asymmetry obliges to exist. What remains in the calculation is the *function* of real exponent, which only the limit defines.

## The primordial logic, declared

The map named the trunks — "Calculus", "Linear Algebra" — and **nowhere did it say what they are**. The color encoded the trunk; no one decoded the reason for it. Now it is stated in four places:

> **Linear algebra speaks of what is LINEAR** — sum and scale preserved.  
> **Calculus speaks of what is CONSTANT**, and what changes near a point.  
> They are two subjects, and neither relies on the other.

It is this distinction that makes the series a **tree** and not a queue, and for that reason it needed to be in the map, not just in the standard.

**The corner mark.** Each subject carries in the corner a disk with a letter — **C** for constant, **L** for linear — in the gesture of the Nuke nodes, where a disk in the corner indicates that the node has animation, expression, or clone. The label does not change; the information comes from outside. A subject that lives in both trunks carries both marks.

**The base is left unmarked, on purpose**: it is neither one nor the other, it is prior to both. Marking everything would imply that everything classifies.

## Shortcuts

| key | what it does |
|---|---|
| **F** | reframes the entire map on the screen — the same as "fit to screen" |

The **F** is ignored while typing in the search: without this, searching for "function" would reframe the map with each `f` pressed.

## The column of properties, and the entries

Clicking on a node opens its **panel** in its own column — the Properties Bin of Nuke, applied to a map. The text is **snugged up to the map**, and the key of colors and shapes goes to the end: the person who clicks looks to the side and reads, while the legend is an occasional reference. The column stays **always open**, even if empty: a column that appears and disappears makes the map jump in width with each click, and the reader loses sight of the node they were looking at. **One node at a time.**

Each subject has four fields, written outside the page and embedded here (the page is static — there is no live model running):

| field | what it answers |
|---|---|
| **what it is** | the definition, in a sentence |
| **why it exists** | what problem appeared BEFORE and necessitated this to exist |
| **where it appears in the world** | where this exists today, in services that anyone recognizes |
| **where it gets stuck** | the common error of someone who is learning |

**The entries are written by a language model, and the page says so.** Each one carries its provenance — which model, where it ran, on what date, and if it has already been reviewed by a human. In a map whose entire value is to declare the origin of each arrow, a text entering silently would be the only assertion without warrant here.

The generator is not just a prompt. Three things make the rule valid:

- **a validator** that rejects empty field, overflow, formula in LaTeX (the
  page does not draw LaTeX) and example taken from visual effects, computer
  graphics, or image processing — which is the subject of another material, not
  this map;
- **an adversarial checker** on the example field, which is where a model
  invents. It is **gate, not label**: if it fails, the node goes back to the
  queue with the reason and the model changes the example. As a simple marker
  it failed 3 in 4, and a list with 35 suspects in 50 does not separate anything;
- **a ceiling per example domain.** In one round, 13 of the 50 entries anchored
  in GPS and navigation. Each one was true — the checker had nothing to mark —
  but together they made the map say that all of mathematics is for finding
  a path. With the ceiling, the highest concentration fell to 6 of 50.

## On a cell phone, one finger is for the page and two are for the map

The map was measured at 1366×768 and 1920×1080, and on the phone there was a defect that  
none of these measurements catch: the columns of text and figures **existed and were unreachable**.  
The stage covered the middle of the screen with `touch-action: none`, so the finger over the map  
did not scroll the page, and clicking on a node filled a panel out of view.

Measured at 390×844 before the fix: top panel **710** of 844 of viewport,  
column of figures at **860** — off-screen — and the click on a node scrolled **0px**.

Three changes, and all three are measured by [`medir_telas.py`](medir_telas.py):

- **One finger scrolls the page, two fingers move and zoom the map** — the embedded map pattern. As the drag of one finger ended, the drag of two began to move beyond zooming; without this, the phone would only be able to zoom, never navigate;
- **Clicking on a node takes the reader to the panel**, with smooth scrolling. Only on click, never on search: scrolling with each key pressed, with the phone's keyboard open, would be worse than the original defect;
- **A "return to map" button**, which only appears when the columns are stacked — side by side the map is never out of sight, and the button would be noise.

The gate checks the two things separately because they are different defects: the panel becomes visible after the click, and the one-finger gesture is not captured. The second measure exists because the correct CSS is not enough — the handler could still call `preventDefault` and kill the scroll with the correct `touch-action` alongside.

## The map as a figure within a lesson

[`figura_deck.py`](figura_deck.py) exports the map in SVG with a focused episode, for the lecture deck to open saying **where we are** and close saying **where we are going**:

```bash
python3 figura_deck.py --ids matrizes,sistemas,determinante \
    --modo abertura --titulo "G2 · Determinantes" --saida onde-estamos.svg
python3 figura_deck.py --ids matrizes,sistemas,determinante \
    --modo recorte  --titulo "where we are going"    --saida proximo.svg
```

| mode | what it draws | for what |
|---|---|---|
| `abertura` | the **entire** map; label only on the subjects of the episode and their direct neighbors | reads the blot: how much of the field has been traversed |
| `recorte` | only the neighborhood, fully labeled, with empty layers collapsed | reads the name: what is the next dependency |

Three decisions that the drawing carries:

- **label only on related items.** Fifty names on a sheet of 1920 do not read. The other subjects remain drawn and erased — §1.5 of the standard: *erase instead of disappear*, the context stays, the focus does not;  
- **the crop is by `viewBox`, with the layout intact.** Recalculating positions only for the neighborhood would give a more compact drawing and **lie about the geography**: the reader just saw the entire map in the opening, and the boxes need to be where they were. What is compressed are the **empty layers** — the neighborhood of the determinant goes from layer 1 to 9, which in real height would be 1,624 px against 714 of width, an illegible thread on a 16:9 sheet. Collapsed, the ratio comes out between 0.83 and 1.10 in the episodes measured;  
- **SVG and not PNG**, because of a gate: the auditor of labels reads the **vector text** of the PDF. A label in bitmap is a label that the auditor does not see.

The palette is that of the **deck** (paper `#f3f5f9`), not that of the site: the tints of  
the trunks are the same, but in the light the color **mixes by average** and not by sum —  
adding light over light paper blows out to white.

## The lines have no diagonal

Only horizontal, vertical, and L, by design decision. Each segment becomes a **Z** (descends, moves, descends), with the step offset within the gap between layers so that two edges do not lie one on top of the other. Measured in the generated SVG: **0 diagonal segments in 78 edges**.

## The norm, cited where it was applied

Under a diagram norm of its own (sibling document, not published):

- **§1.1 — crossing is the #1 defect** (Purchase 1997) and overrides any other conflicting rule. Therefore, the layout **is not designed, it is measured**: layers by longest path, virtual nodes on edges that skip layers, iterated centroid, and the count in the footer of the page itself. Rule without measure is preference;
- **§1.2 — direction is declared once and not mixed.** Here it is **top to bottom**, stated in the page header: the prerequisite always stays above what requires it;
- **§1.3 — kit of three shapes.** Rounded rectangle for content, oval for the root (terminator of start). **Rhombus does not appear because there is no decision** in the map. No invented shapes;
- **§1.4 — the node is a box, never a point**, with the label inside. *"Point forces reading the legend; box is read at once"*;
- **§1.5 — modularity by occlusion.** Once a topic is chosen, the rest **turns off instead of disappearing**: the context remains visible, the focus does not;
- **§2 — the grammar.** The gold is the flow. The **four** classes of warrant are distinguished by weight and stroke, declared in the footer legend;
- **§4 — the SVG trap.** The page was measured in **1366×768 and 1920×1080**.

## Two Flaws That the Instrument Itself Has

1. **A cycle in my model.** `sistemas → matrizes → determinante → sistemas`. The determinant *decides* a system (invertibility, Cramer), but it is not a prerequisite to **define** a system. There was confusion between **"uses"** and **"precedes"** — and a graph of prerequisites that has a cycle is wrong by construction. The edge was removed, with the reason written in `materias.py`;  
2. **The alignment I wanted to make, and the measurement knocked it down.** With orthogonal edges, the long lines started running along the edges forming *frames* around the drawing. I wrote a coordinate alignment (pulling each node to the centroid of its neighbors) and measured before adopting: the length of the edges fell **1.4%** and the width rose **64%** (1,572 → 2,581 px). Idea discarded, code kept in `layout.py` with the number written. **What really paid off was banal**: giving a smaller gap between two adjacent virtual nodes (7 px instead of 20);  
3. **A virtual node is not a box.** In the 1st generation it occupied the width of an entire box, which inflated the drawing to 2,484 px and made the long edges deviate to the edge — spikes that the crossing **measure did not catch**, because crossing is not the same as deviation. The eye caught it. Corrected, the width fell to **1,668 px**.

4. **The layout started with alphabetical order.** The centroid is local: it improves the  
   arrangement that receives, and received the nodes of each layer ordered **by name** —  
   which has no relation at all with the graph. Replaced by descent in depth  
   from the roots, which puts siblings side by side, and added the step of  
   **transposition** (test each adjacent pair, swap, and only keep if the  
   count falls). Measured in the four combinations, to separate what is from the  
   algorithm and what is from the new content:

| | old layout | new layout |
   |---|---|---|
   | graph of 44 nodes/68 edges | 34 | **28** |
   | graph of 50 nodes/78 edges | 51 | **41** |

The new algorithm is worth **−10** crossings; the six new subjects and ten
   new dependencies cost **+13**. The balance is declared, not hidden: the map
   grew 14% and ended up with 7 crossings more than it had.

5. **Two of my edges came out as redundant — and eleven stayed.**  
   `conj_num → negativos` and `conj_num → fracoes` cost 15 measured crossings,  
   and the path `conj_num → aritmética → negativos` already said the same thing;  
   the information they carried went to the node's note. But topological  
   redundancy **is not** a sufficient reason: there are 11 other redundant edges  
   in the graph, and almost all are of *definition* — *"the derivative is a limit"*  
   is redundant by path and is the central information of calculus. Only the edge  
   whose information the alternative path already says is removed.

## What this map DOES NOT do

- **not curriculum order** — the §1.2 applies to the drawing, not to the
  administration. That elementary linear algebra (systems, matrices, determinants)
  does not depend on limits is a fact of the graph, not a suggestion of the
  schedule;
- **does not cover the border with source** — functional analysis, topology,
  measure theory, differential geometry, and abstract algebra are on the map
  **without groundwork**. Closing this requires a book in the collection, not
  more drawing;
- **does not measure learning.** Pointing where the student got stuck is the
  professor's hypothesis at the moment; the map organizes the conversation, not
  the diagnosis.

## License

- **Code** (`gerar_mapa.py`, `layout.py`, `materias.py`) — [MIT](LICENSE).  
  The `LICENSE` file contains the pure MIT text so that GitHub can recognize it;  
  the scope division between code and content is this section.  
- **Content** (the graph, its warrants, and this README) —  
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), with the full  
  legal text in [`LICENSE-CONTENT`](LICENSE-CONTENT): use, adapt, and  
  redistribute, even commercially, **citing the source** and keeping any  
  derivative **under the same license**. The *share-alike* does not prohibit  
  commercial use — it prohibits closing what was derived from here.

The copyright of the content is by Mateus Alkimim. The license above applies to third parties; the holder retains the right to license their own work under other terms. The project name and its visual identity are not licensed here.

> **Amendment of 2026-08-20.** The content moved from CC BY 4.0 to CC BY-SA 4.0.  
> The CC BY 4.0 granted in the publication of 2026-08-19 is irrevocable: anyone who  
> obtained the content under it during that interval remains covered by it.

The works cited as warrant are bibliographic references; no text from them is reproduced here.