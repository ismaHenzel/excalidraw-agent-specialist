# Pitfalls Research

**Domain:** Adding UML (sequence/class/use-case/activity) + data-modeling (star/snowflake/data-vault/ER) diagram families and a `diagram-types/` KB layer to the existing constrained Excalidraw authoring subagent
**Researched:** 2026-06-03
**Confidence:** HIGH for the schema-constraint pitfalls (verified against `0.17.3` arrowhead/font facts in STACK.md and the actual `star_schema.excalidraw` source); MEDIUM for the integration/KB-drift pitfalls (design judgement extrapolated from the existing plugin structure)

> **Scope:** These are mistakes specific to drawing THESE families inside THIS system —
> the fixed `arrow|bar|dot|triangle|null` arrowhead set, monospace-only `fontFamily:3`,
> `roughness:0` + sharp boxes, no `label` field, no raw emoji, and an automated
> structural+visual verifier that will FAIL the diagram. Generic "how to draw UML"
> advice lives in FEATURES.md; this file is about how the families break against the
> constraints and the verifier.

> **Load-bearing finding (read first).** The one shipped data-model ground-truth,
> `examples_excalidraw/star_schema.excalidraw`, does NOT follow the rules the new
> families are supposed to enforce. Of its 158 elements: **0 use `boundElements`/`containerId`**
> (all 113 monospace texts are free-floating, manually positioned), **0 use `groupIds`**,
> its arrows have `startBinding:null`/`endBinding:null` (not glued to borders) and
> `roundness:{type:2}` (not `null`), and its outer container uses `roundness:{type:3}`
> (soft, not the sharp `null` STACK.md mandates for formal boxes). So the existing
> "ground truth" silently contradicts STACK.md's recommended recipe. Pitfall 1 and
> Pitfall 9 below are direct consequences — resolve the canonical-recipe question
> before authoring any new example.

## Critical Pitfalls

### Pitfall 1: Faking crow's-foot / aggregation / inheritance notation badly (the arrowhead-set trap)

**What goes wrong:**
The author reaches for crow's-foot (ER "many"), a hollow/open diamond (UML aggregation), a filled diamond (composition), or a hollow triangle (generalization) — none of which exist in the `0.17.3` arrowhead enum (`arrow|bar|dot|triangle|null` only, per STACK.md). One of three failures results: (a) the author writes `endArrowhead:"crowsfoot"` / `"diamond"` and it silently renders as the default/no head — the relationship semantics vanish and the verifier's visual check sees a plain line; (b) the author substitutes a plain `arrow` everywhere, erasing the one/many/aggregation distinction that is the entire point of an ER or class diagram; (c) the author hand-composes a glyph (3-line crow's foot, small diamond) that is mis-sized, mis-rotated, or floats detached from the connector end so it reads as garbage.

**Why it happens:**
Every UML/ER reference (Creately, Lucidchart, the sources in FEATURES.md) shows these decorated endpoints as the canonical notation, so the author assumes Excalidraw supports them. The schema constraint is invisible until something renders wrong.

**How to avoid:**
- KB rule (in each affected `diagram-types/*.md`): embed STACK.md's notation→primitive mapping table verbatim. Generalization/realization = `endArrowhead:"triangle"` (accept FILLED, not hollow — house convention; realization adds `strokeStyle:"dashed"`). Dependency = `arrow` + `dashed`. ER "one" = `bar`; "zero/optional" = `dot` or small `ellipse` glyph; "many" = a grouped 3-`line` crow's-foot glyph OR a textual `1..*` / `0..*` label. Aggregation/composition = a small (~14px) `diamond` element at the owner end (white fill = aggregation, solid fill = composition), grouped with the connector.
- Validator rule (cheap, high value): reject any `startArrowhead`/`endArrowhead` value not in `{arrow,bar,dot,triangle,null}`. This converts the silent-render failure into a loud authoring-time error.
- Pick ONE crow's-foot strategy (glyph vs. textual multiplicity) per the data-modeling KB and use it consistently; mixing them across diagrams looks like a bug.

**Warning signs:**
A connector's intended cardinality/relationship is not visually distinguishable from a plain association at render time; the verifier's visual review reports "all relationships look identical"; an arrowhead value in the JSON that isn't one of the five legal tokens.

**Phase to address:**
The Class + ER phase (the families that introduce relationship-endpoint glyphs). Add the arrowhead-enum validator check here.

---

### Pitfall 2: Multi-line `text` defeats both the compartment layout and the verifier's monospace width-fit check

**What goes wrong:**
To save elements, the author packs a whole class/entity box into one `text` element with `\n`-separated rows (e.g. `"id: int\nname: string\nemail: string"`). Two failures: (1) the box loses per-row alignment and you can't place divider `line`s between compartments — it stops looking like UML/ER; (2) the verifier's structural width-fit check measures container width vs. text width using monospace metrics on a *single* width value, but a multi-line block's width is the widest line — a short class name + one very long attribute row passes the name's column but the long row silently overflows the box at render time, which the cheap structural check can miss and only the vision pass catches (burning tokens, or slipping through).

**Why it happens:**
Fewer elements feels simpler and the `originalText`/`\n` mechanism is right there. The width-fit check is naturally written per-element, so multi-line elements are an edge case it under-handles.

**How to avoid:**
- KB rule: a class/entity box is `rectangle` (sharp) + horizontal `line` dividers + ONE bound/centered `text` for the title + N **separate free-floating left-aligned** `text` rows. Never one multi-line `text` for the row stack (STACK.md "What NOT to Use").
- Verifier rule: the structural width-fit check must (a) split any multi-line `text` on `\n` and check the WIDEST row against the container, and (b) when many free-floating row texts share a container's x-band, check the longest row, not the average. Document the monospace advance width (Cascadia at the diagram's `fontSize`) the check assumes.
- Authoring rule: keep attribute/method row strings short; truncate long type signatures rather than overflow.

**Warning signs:**
A `text` element whose `text` contains `\n` inside a formal box; verifier reports `text_overflow` only on the vision pass and never on the structural pass (means the structural check is blind to multi-line); rows visually spilling past the right border in the PNG.

**Phase to address:**
The Class + ER phase introduces compartmented boxes — harden the verifier's multi-line/multi-row width-fit check there. Flag this phase as needing the verifier touched (STACK.md already flags it).

---

### Pitfall 3: Compartmented entity/class boxes with misaligned dividers and drifting row columns

**What goes wrong:**
The three-compartment class box (name | attributes | methods) or the ER entity box (header | columns) is assembled from a `rectangle`, horizontal `line` dividers, and stacked `text` rows — all positioned by hand. Off-by-a-few-pixels errors accumulate: a divider `line` that doesn't span the full box width or sits at a non-grid Y, rows whose left x doesn't match the header's left x, uneven row vertical spacing, or a divider that lands mid-row. The result reads as sloppy and may trip the grid-alignment convention; in the worst case a divider extends past the box border (visual defect the verifier flags).

**Why it happens:**
There is no native "table" primitive in `0.17.3` (STACK.md confirms). Every compartment is manual geometry, and the existing `star_schema.excalidraw` proves the house style is hand-placed free-floating text with no binding and no grouping — so there's no template enforcing alignment.

**How to avoid:**
- KB rule: define the box as a parametric recipe with fixed offsets — header height H, row pitch R (a multiple of 20), divider `line` from `(x, y)` to `(x+width, y)` exactly at compartment boundaries, all row `text` sharing the same left x = box.x + pad. Give exact numbers in the `diagram-types/*.md` so the agent translates a known-good unit rather than improvising.
- Convention: all coordinates multiples of 20 (existing grid rule); row pitch and divider Y derived from that.
- Verifier rule (structural): for a grouped box unit, assert divider `line` endpoints' x-range == container x-range (±gap) and that row texts share a common left x.

**Warning signs:**
Divider `line` width ≠ box width in the JSON; row `text` x values that don't all match; verifier visual pass notes "dividers don't reach the edges" or "columns ragged."

**Phase to address:**
First phase that ships a compartmented box (Star schema in the DM family / Class in UML). Author the parametric box recipe + the divider-alignment verifier assertion there; later compartmented types reuse it.

---

### Pitfall 4: Sequence-diagram lifelines and activation bars overlap / misalign with messages

**What goes wrong:**
Lifelines (dashed vertical `line`s) and activation bars (thin `rectangle`s) don't line up: a message `arrow` lands beside the lifeline instead of on it; an activation bar is offset from the lifeline x; bars from concurrent calls overlap; the activation bar starts/ends at the wrong message Y so it doesn't bracket the right interactions; self-messages (arrow looping back to the same lifeline) collapse to zero width or overlap the activation bar. Because time flows strictly top-to-bottom, any Y-ordering error makes the scenario read in the wrong sequence.

**Why it happens:**
Sequence diagrams are pure manual geometry on two axes (participant x = fixed per lifeline; message y = strictly increasing). There's no layout engine; the lifeline, its activation bar, and every message that touches it must share an exact center x, and message Ys must monotonically increase — easy to get subtly wrong by hand. STACK.md notes lifeline+activation is a brand-new primitive with no existing analog.

**How to avoid:**
- KB rule: pin each participant to a fixed center x (multiple of 20). The lifeline `line`, the participant-head `rectangle`, and the activation `rectangle` all center on that x. Activation bar x = lifeline_x − halfBarWidth. Message arrow start/end Y is a strictly increasing sequence; document a fixed message pitch.
- KB rule: returns are dashed arrows; every synchronous call should have a matching return (FEATURES.md "good vs beginner"). Cap participants at ~6.
- Verifier rule (structural): assert message-arrow Y values are monotonically non-decreasing top-to-bottom; assert each activation `rectangle`'s center x equals its lifeline's x; assert message endpoints land on a lifeline x (±gap).

**Warning signs:**
Activation `rectangle` x not equal to its lifeline `line` x; message arrow Ys out of order in the JSON; verifier visual pass reports "arrows don't touch the lifeline" or "activation bars float beside the line."

**Phase to address:**
The Sequence phase (introduces the lifeline + activation-bar primitive). Add the monotonic-Y and center-x verifier assertions here.

---

### Pitfall 5: Raw emoji / non-monospace glyphs sneak in via notation shorthand

**What goes wrong:**
The author uses a key emoji 🔑 for a PK, a person 🧍 for an actor, a lock 🔒, or visibility symbols, and under `fontFamily:3` they render as missing-glyph boxes (PROJECT.md emoji policy). Subtler: notation glyphs that *aren't* emoji but may still be risky under Cascadia — guillemets `«»` for stereotypes, multiplicity `1..*`, visibility `+ - #`, underline for PK. STACK.md confirms `«»` render fine under `fontFamily:3`; emoji do not.

**Why it happens:**
UML/ER notation is symbol-dense and emoji are the lazy shorthand for "key," "person," "lock." The author forgets the monospace-only constraint applies to these new symbol-heavy families just as much as to the existing ones.

**How to avoid:**
- KB rule: PK/FK = text prefixes `"PK  id"` / `"FK  customer_id"` (monospace keeps columns aligned, STACK.md); actor = labelled box or composed stick-figure, never 🧍; stereotypes = guillemets `«interface»` (verified safe). No emoji, ever.
- Validator/verifier rule (already mandated in PROJECT.md): structural pre-check rejects raw emoji codepoints in any `text` with `fontFamily:3`. Extend the codepoint deny-list to cover the emoji an author would reach for in these families (🔑🧍🔒📋🗄️ etc.). Visual pass catches survivors as glyph boxes.

**Warning signs:**
Any non-ASCII-emoji codepoint in a `text` element; verifier visual pass reports "tofu boxes" where a key/person symbol was intended.

**Phase to address:**
Cross-cutting — the emoji ban already exists from v1.0. Re-validate the deny-list when authoring the symbol-dense families (Class, ER, Use-case). No new phase; add a checklist item to each family's authoring phase.

---

### Pitfall 6: Canonical example `.excalidraw` files that don't actually render (or render broken)

**What goes wrong:**
PROJECT.md requires one canonical `.excalidraw` + rendered PNG per new type as visual ground truth. If an example is hand-written and only eyeballed (not pushed through `validate_and_render.sh` + the verifier), it can ship with an illegal arrowhead value, an unresolved icon `file_path`, an emoji box, or text overflow. Worse than no example: the agent imitates the broken ground truth and propagates the defect into every diagram of that type.

**Why it happens:**
Authoring 7-8 example pairs (FEATURES.md) is a big chunk of work; the temptation is to write JSON, render once, glance at the PNG, and move on. The CDN-render dependency (CONCERNS.md #2) and fail-open-on-missing-icon behavior (CONCERNS.md #12) mean a "rendered" PNG can still be silently wrong (blank icon slots, stderr warnings the wrapper swallows).

**How to avoid:**
- Process rule: every canonical example must pass the FULL loop — validator → render → `excalidraw_verifier` PASS — before being indexed in the KB. Treat the verifier's pass as the acceptance gate for an example, not human eyeballing.
- Render examples with a `--strict` icon mode (CONCERNS.md #12 mitigation) so a missing/renamed icon fails loudly rather than rendering a blank slot.
- Store both the `.excalidraw` source (in `examples_excalidraw/`) and the PNG; the README already documents this round-trip.

**Warning signs:**
An example indexed in the KB with no corresponding verifier pass on record; stderr `WARNING: Image file not found` during example render; the example PNG shows a blank icon box or a plain line where a relationship glyph was intended.

**Phase to address:**
Every family/type phase owns its own example's render+verify gate. Add "canonical example passes the full verify loop" to each phase's exit criteria, not a separate phase.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Single multi-line `text` for a class/entity box instead of rect + dividers + per-row texts | Far fewer elements, faster to write | No dividers, no column alignment, defeats the verifier width-fit check (Pitfall 2), doesn't look like UML | Never for formal boxes; OK only for a throwaway note block |
| Plain `endArrowhead:"arrow"` everywhere, ignoring cardinality/relationship type | Trivial; no glyph composition | ER/class diagrams lose their entire semantic payload (one vs many, aggregation vs association) | Only for an explicitly conceptual sketch where cardinality isn't the point — and say so in the diagram |
| Skip `groupIds` on box+dividers+rows clusters (as `star_schema.excalidraw` does today) | Less bookkeeping | Can't translate/place a box as a unit; every nudge desyncs dividers from rows; verifier/layout churn | Never for the new families — the existing example got away with it because it's static, but composable diagram-types need grouped units |
| Hand-eyeball canonical examples instead of running the verify loop | Ship examples faster | Broken ground truth the agent then imitates forever (Pitfall 6) | Never |
| Free-floating texts with no `containerId` for titles (copying `star_schema.excalidraw`) | Matches the existing example | Loses Excalidraw's auto-centering; titles drift when the box moves | Acceptable for non-title rows (which must be left-aligned free text anyway); titles should be bound/centered |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| New `diagram-types/` KB layer ↔ existing `kb/` primitive layer | Re-deriving geometry (box offsets, fan-out coords) inside the type file instead of `@`-referencing the primitive file, so the two layers drift and a fix to a primitive doesn't propagate | Each `diagram-types/*.md` references the primitive `kb/*.md` files it composes (FEATURES.md gives the exact mapping) and states only the type-specific recipe + the primitive list. Don't copy geometry. |
| `diagram-types/` index ↔ `kb/README.md` index | Adding a type file but forgetting to index it, or indexing under the wrong family, so the agent never discovers it (mirrors CONCERNS.md #4's two-places-to-update class of bug) | Single documented "adding a diagram type" procedure (like the existing "Adding a new pattern" section): create file, add example pair, add ONE index row under the right family. Verify discovery via `Glob`/`Grep`. |
| Family/type picker ↔ `AskUserQuestion` 4-option cap | Trying to list all 8+ types in one flat picker (exceeds the cap) or mis-routing a sub-pick so UML's type sub-question never fires | Two-tier: Q1 picks family (4 families fit exactly), follow-up sub-pick selects the type only when the family has many (UML→4, DM→4). Test each family path actually reaches its type list and loads the right KB files + example PNG. |
| Family/type selection ↔ which KB files + example PNGs load | Selecting "UML / Class" but the agent loads the generic macro patterns (or no example), because the wiring from selection→assets wasn't updated | The selection must drive a concrete asset set: the type's `diagram-types/*.md`, its composed `kb/*.md` primitives, and its canonical `examples/*.png`. Verify the loaded-asset set per type. |
| Render pipeline (frozen `0.17.3` via `esm.sh` CDN) | Assuming a primitive/property exists because a newer Excalidraw supports it | Everything stays inside `0.17.3` (STACK.md "Version Compatibility"). The CDN pin (CONCERNS.md #2) means you can't even rely on a newer version sneaking in. |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Big diagrams (class diagram with many classes, ER with many entities) blow the verifier's vision budget | Verifier turn truncates or the 3-iteration loop times out; PERFORMANCE constraint (one Docker render + vision tokens per iteration) | Keep canonical examples modest (≤6 participants/classes/entities per FEATURES.md "good" guidance); favour the cheap structural pre-check to catch defects before the vision pass | Diagrams with dozens of compartmented boxes and hundreds of row texts (star_schema already has 113 texts at 16 boxes) |
| Element-count explosion from compartments | A single class box is 8-15 elements (STACK.md); ten classes + relationships = hundreds of elements; render slows, verifier context grows | Group each box unit (`groupIds`) and keep row counts tight; split large models into multiple diagrams rather than one mega-canvas (FEATURES.md flags "one mega-diagram" as a beginner mistake) | A "draw my whole schema" request producing 20+ entities |
| 3-iteration auto-fix cap exhausted on a structurally hard family | Loop hits iteration 3 and surfaces a still-broken PNG to the user | Front-load correctness via parametric KB recipes (Pitfalls 3/4) so the FIRST render is close; the loop is for polish, not for discovering basic geometry | Sequence/class diagrams where every endpoint is hand-placed |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Canonical example or user diagram references an icon via absolute/`../` `file_path` | Path-traversal info disclosure — the renderer base64-embeds arbitrary host files into the PNG (CONCERNS.md #5) | Examples use only relative `file_path`s into `icons/`; keep CONCERNS.md #5's path-allowlist mitigation in mind (out of scope this milestone but don't add new absolute-path examples) |
| New families pulling in icons that don't exist / duplicate-brand ambiguity | Blank icon slots (fail-open, CONCERNS.md #12) or non-deterministic icon choice (CONCERNS.md #9) in canonical examples | Tech-Architecture family reuses the existing icon strategy; render examples with `--strict` so missing icons fail loudly; don't introduce new duplicate icon variants |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Family→type picker confuses users (which family is "ER"? is "activity" UML or Flow?) | User picks the wrong family, gets the wrong KB/example, diagram is subtly wrong | Family names match real-world mental models (Tech Architecture / Data Modeling / UML / Flow-Process); each family option's description names its member types ("Data Modeling: ER, star, snowflake, data vault"). Activity is explicitly under UML even though it overlaps Flow — document the choice so it's predictable. |
| Two-tier picker feels like extra friction for single-type families | User annoyed by a sub-question when there's only one obvious type | Only show the type sub-pick when the family has many types (UML, DM); Tech-Architecture (one type) skips straight through. |
| Degraded notation (filled triangle for inheritance, textual `1..*` instead of crow's-foot) surprises a UML-literate user | User expects hollow triangle / crow's-foot, sees the house substitution, thinks it's a bug | Document the substitutions as deliberate house conventions IN the diagram-type KB and ideally in a one-line note the agent can surface ("inheritance shown as filled triangle — Excalidraw lacks a hollow head"). |
| Data Vault hub/link/satellite distinguished only by color | Color-blind users or grayscale prints can't tell the three apart | Pair color with a text role label or shape-position convention (STACK.md: semantics live in palette + KB); don't rely on color alone. |

## "Looks Done But Isn't" Checklist

- [ ] **Relationship arrows:** Often missing the cardinality/relationship glyph (renders as plain line) — verify each connector visually encodes one/many/aggregation/inheritance, and that no illegal arrowhead token was used.
- [ ] **Compartmented box:** Often missing full-width dividers or column-aligned rows — verify divider `line` spans the box width, rows share a left x, all coords on the 20-grid.
- [ ] **Sequence diagram:** Often missing return messages and matched activation bars — verify every sync call has a dashed return, activation bars bracket the right messages, message Ys strictly increase.
- [ ] **Canonical example:** Often "rendered once and eyeballed" — verify it actually PASSED the full validator→render→verifier loop and is indexed under the correct family.
- [ ] **diagram-types entry:** Often re-derives geometry instead of referencing primitives — verify it `@`-references the `kb/*.md` files from the FEATURES.md mapping and is added to the index.
- [ ] **Picker wiring:** Often the type sub-pick loads generic assets — verify selecting each specific type loads that type's KB file, its composed primitives, and its example PNG.
- [ ] **No emoji:** Often a key/person/lock emoji slipped into a symbol-dense family — verify the structural pre-check's deny-list covers the emoji these families tempt authors with.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Broken canonical example already indexed (Pitfall 6) | MEDIUM | Re-author the `.excalidraw`, re-run the full verify loop, re-render the PNG; audit any diagrams the agent produced by imitating it |
| Illegal arrowhead token shipped in a KB recipe (Pitfall 1) | LOW | Add the arrowhead-enum validator check (catches it everywhere at once), fix the recipe to a legal token or composed glyph |
| diagram-types KB drifted from kb/ primitives (KB-drift gotcha) | MEDIUM | Replace copied geometry with `@`-references to the primitive files; re-render the affected examples to confirm parity |
| Multi-line text overflow slipping past structural check (Pitfall 2) | LOW-MEDIUM | Harden the width-fit check to split on `\n` and measure the widest row; re-run verify on existing compartmented examples |
| Picker mis-routes a family/type (integration) | LOW | Fix the two-tier wiring; add a per-type smoke check that the right asset set loads |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| 1. Faking crow's-foot/aggregation/inheritance | Class + ER phase | Arrowhead-enum validator check rejects illegal tokens; verifier visual pass confirms relationships are distinguishable |
| 2. Multi-line text breaks width-fit check | Class + ER phase (harden verifier) | Structural check splits `\n` and measures widest row; flag overflow before vision pass |
| 3. Misaligned compartment dividers/columns | First compartmented-box phase (Star / Class) | Structural assertion: divider x-range == box x-range, rows share left x, coords on 20-grid |
| 4. Lifeline/activation/message overlap | Sequence phase | Structural assertion: message Ys monotonic, activation center x == lifeline x, endpoints on lifeline x |
| 5. Emoji/non-monospace glyphs | Cross-cutting (re-validate per symbol-dense family) | Existing emoji deny-list extended; structural pre-check rejects emoji codepoints under fontFamily:3 |
| 6. Canonical examples don't render | Every family/type phase (exit criterion) | Example must PASS the full validator→render→verifier loop before KB indexing |
| KB-layer drift | Every diagram-type authoring phase | diagram-types file `@`-references primitives; "adding a type" procedure followed; indexed once |
| Picker UX / wiring | The "wire it into the loop" phase | Each family/type path reaches the right sub-pick and loads the correct KB + example assets |

## Sources

- `.planning/research/STACK.md` — arrowhead enum (`arrow|bar|dot|triangle|null`), notation→primitive workarounds, multi-element compartment recipe, "What NOT to Use" — **HIGH** (verified against `0.17.3` `.d.ts`)
- `.planning/research/FEATURES.md` — per-type must-have elements, good-vs-beginner mistakes, primitive composition mapping, picker two-tier note — **HIGH/MEDIUM**
- `.planning/PROJECT.md` — Architect's Precision constraints, emoji policy, verifier structural+visual checks, 3-iteration cap, `AskUserQuestion` 4-option cap — **HIGH** (project spec)
- `.claude/agents/excalidraw/examples_excalidraw/star_schema.excalidraw` (inspected: 158 elements, 113 free-floating monospace texts, 0 `groupIds`, 0 `containerId`, arrows `roundness:{type:2}` + unbound, outer rect `roundness:{type:3}`) — **HIGH** (the actual shipped ground truth; reveals it contradicts STACK.md's recommended recipe)
- `.claude/agents/excalidraw/kb/README.md` — grid-of-20, `roughness:0`, `fontFamily:3`, "adding a pattern" procedure, example-index round-trip — **HIGH**
- `.planning/codebase/CONCERNS.md` — CDN render dependency (#2), path-traversal in icon embed (#5), icon duplicates (#9), non-icon PNGs (#10), fail-open on missing icons (#12), two-places-to-update class of bug (#4) — **HIGH**

---
*Pitfalls research for: adding UML + data-modeling diagram families to the constrained Excalidraw authoring subagent*
*Researched: 2026-06-03*
