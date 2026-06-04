# Phase 6: Star Schema → Snowflake - Research

**Researched:** 2026-06-04
**Domain:** Excalidraw diagram-type KB authoring — the first compartmented-box (data-modeling table-box) recipe, plus its normalized snowflake variant
**Confidence:** HIGH (this is a closed, self-contained codebase; every claim below is grounded in files read this session, not training data)

## Summary

Phase 6 is **prompt/KB-engineering work, not application code**. It authors two new TYPE-layer recipe files (`diagram-types/star-schema.md`, `diagram-types/snowflake-schema.md`), two canonical example pairs (`.excalidraw` + PNG), and the resolver/back-ref bookkeeping — all built on the **already-existing** Phase 4 `compartmented-box.md` construction. The hard technical problem this phase must *finalize* is the **parametric geometry** that `compartmented-box.md` lines 60–63 explicitly deferred to Phase 6: header height, row pitch, divider-Y formulas, and left-pad — the exact numbers that make dividers span the full box width, rows share a common left x, and the verifier's `text_overflow_static` check pass. Star is authored and passing first; snowflake is literally star + a normalized dimension `tree-hierarchy` (DM-03 building on DM-01).

The single most important — and easily-missed — finding: **no existing example in the repo demonstrates the compartmented-box recipe.** Every current `.excalidraw` (including the "compliant" `architecture_overview`) uses `roundness: {type:3}` (soft), `0` `groupIds`, and `0` `line` elements. The legacy `star_schema.excalidraw` is explicitly **grandfathered and flagged as NOT a safe template** (158 elements, 0 groups, soft corners, unbound arrows). Phase 6 therefore authors the **first** `line` (divider) element and the **first** grouped sharp-cornered box in the whole codebase. There is no template to copy from — the recipe geometry must be derived correctly from scratch and proven against the verifier.

The second critical finding: the verifier's `text_overflow_static` check (`scripts/verifier/verifier_structural.py`) is the precise, deterministic gate for SC-1 and SC-4. It estimates `width = len(text) * 0.6 * fontSize` and flags an `error` if that exceeds the width of the **smallest rectangle/ellipse/diamond whose bbox fully encloses the text**. This dictates exact authoring rules (below). A `line` divider is invisible to this check (it's not a container shape), so divider full-width spanning is a *visual* concern (`layout_collision` / human judgment), not a structural one — the recipe must encode it as deterministic geometry, not rely on the verifier to catch it.

**Primary recommendation:** Finalize one parametric box formula (header 40px, row pitch 20px, left-pad 12px, divider lines spanning exactly `box.x → box.x+width`, all on the 20-grid), write it ONCE into `star-schema.md`, prove it against the real `validate_and_render.sh` + verifier loop, then have `snowflake-schema.md` reference that finalized geometry verbatim and add only the `tree-hierarchy` normalized-dimension extension. Author star fully (recipe + example + passing loop) before touching snowflake.

## Architectural Responsibility Map

This is a single-tier KB/agent system; "tiers" here map to the two-layer KB plus the frozen v1.0 loop.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Star/snowflake *purpose + how-to-draw* prose | TYPE layer (`diagram-types/*.md`) | — | A diagram type is a composition recipe; it lives one layer up from primitives |
| Compartmented-box construction + alignment rules | PRIMITIVE/shared (`diagram-types/compartmented-box.md`) | TYPE layer references it | Already authored in Phase 4; Phase 6 finalizes its deferred parametric offsets, does not re-derive |
| Fan-out / convergence / tree-hierarchy geometry | PRIMITIVE layer (`kb/*.md`) | — | Coordinate math lives only in `kb/`; type files compose by `@`-reference, never re-derive |
| Family→type→recipe dispatch | Resolver table (`diagram-types/README.md`) | `/excalidraw` command + specialist | Single authoritative map; Phase 6 fills in the two planned rows |
| Render correctness (PNG) | v1.0 loop (`scripts/render/`) — FROZEN | — | Additive phase; must not touch validator/renderer |
| Structural + visual pass/fail | v1.0 verifier (`excalidraw_verifier.md` + `verifier_structural.py`) — FROZEN | — | Recipe must satisfy existing checks; do NOT modify the checks |

## User Constraints (from roadmap/STATE — no CONTEXT.md exists yet)

> No `*-CONTEXT.md` exists in the phase directory at research time. These constraints are extracted from ROADMAP.md, REQUIREMENTS.md, and STATE.md and carry locked-decision authority.

### Locked Decisions
- **v1.0 loop, validator, and verifier are FROZEN.** All v1.1 work is additive — new KB files + resolver rows + example pairs only. No edits to `scripts/render/*`, `scripts/verifier/*`, or the verifier prompt. (STATE.md Decisions; REQUIREMENTS.md Out of Scope)
- **`diagram-types/` is a sibling of `kb/`, not nested.** (STATE.md)
- **Single authoritative resolver table** in `diagram-types/README.md` — no duplicated mapping. (STATE.md; DTKB-01/TAX-03)
- **Compartmented-box construction (INT-02) is documented ONCE** in `diagram-types/compartmented-box.md` and REFERENCED by type files — never re-derived. (STATE.md; already exists)
- **Multi-line single `text` blocks are DISALLOWED for compartments.** Each row is its own `text` element. This is a binding rule, the explicit subject of SC-4. (`compartmented-box.md` §"HARD prohibition")
- **The legacy `star_schema.excalidraw` is GRANDFATHERED (EX-02, Option B)** and is **NOT a safe template** for the new recipe. Do not copy its free-floating/unbound/soft-cornered structure. The compliant star example is authored fresh in this phase. (`diagram-types/README.md` §"Legacy example resolution")
- **Star authored first, snowflake second** — snowflake only after star is passing (SC-2 explicit ordering; DM-03 builds on DM-01).
- **Arrowhead set is fixed to `arrow|bar|dot|triangle|null`.** Any other token renders silently as a plain line. (`notation-conventions.md`; DTKB-04) — relevant for the fan-out connectors fact↔dimension.
- **Notation conventions (DTKB-04) are LOCKED** in `notation-conventions.md`; the relationship-glyph pixel geometry is deferred to Phase 7 (ER/Class), NOT this phase. Star/snowflake connectors are plain association arrows, so this phase needs no new glyph work.
- **EX-03 is an exit criterion:** each canonical example must pass the full validate→render→verify loop before the phase is done.

### Claude's Discretion
- Exact parametric offsets (header height, row pitch, left-pad, divider-Y formula) — *must be chosen and finalized this phase*, then locked for all later compartmented types.
- Choice of fact/dimension domain for the canonical examples (e.g., a Sales star). Pick a small, recognizable, real-world schema.
- Which `kb/` primitives the snowflake normalized-dimension tree composes beyond the planned set.

### Deferred Ideas (OUT OF SCOPE)
- ER cardinality glyphs, crow's-foot, PK/FK relationship endpoints — Phase 7.
- Data-vault hub/link/satellite palette — Phase 9.
- Any renderer/validator/verifier change — v2 hardening / out of scope.
- Native crow's-foot/diamond/hollow arrowheads — out of scope (workarounds only).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DM-01 | `diagram-types/star-schema.md` recipe exists; agent authors a star-schema diagram (central fact + dimension entity boxes, fan-out composition) that passes the full loop | Compartmented-box construction (Phase 4) supplies the box; `kb/fan-out.md` supplies the fact→dimension dispatch geometry; `kb/convergence.md`/`evidence-card`/`group-container` are the resolver-named composed set. Parametric box offsets finalized here (see Architecture Patterns). |
| DM-03 | `diagram-types/snowflake-schema.md` recipe exists building on star with a normalized dimension tree-hierarchy; agent authors a snowflake that passes the full loop | Snowflake = star's composed set + `kb/tree-hierarchy.md` (normalized dimension sub-tables) + `kb/linear-pipeline.md` per the resolver table. References star's finalized box geometry verbatim; adds the normalization extension only. |

> SC-3 (canonical example pair indexed for both types) and SC-4 (per-row separate `text` elements) are cross-cutting exit criteria realized through EX-01/EX-03 and the `compartmented-box.md` HARD prohibition respectively.
</phase_requirements>

## Standard Stack

This phase ships **no new software dependencies**. The "stack" is the existing frozen toolchain the recipe must target.

### Core
| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| `@excalidraw/excalidraw` | `0.17.3` (via esm.sh `?bundle`) | Renders `.excalidraw` JSON → SVG → PNG | Pinned in `scripts/render/render_template.html`; the whole notation set (5 arrowheads, `line`/`rectangle`/`text` schema) is fixed to this version [VERIFIED: render_template.html] |
| `validate_and_render.sh` | repo HEAD | Validate JSON + render to sibling PNG | The mandated v1.0 entry point; FROZEN [VERIFIED: scripts/render/validate_and_render.sh] |
| `excalidraw_verifier` + `verifier_structural.py` | repo HEAD | Structural + visual pass/fail report | The gate every example must pass; FROZEN [VERIFIED: read this session] |

### Supporting (existing KB the recipe composes — install nothing, reference these)
| File | Purpose | When to Use |
|------|---------|-------------|
| `diagram-types/compartmented-box.md` | The reusable box construction + alignment rules | Both type files REFERENCE this; Phase 6 finalizes its deferred offsets |
| `kb/fan-out.md` | One source → N destinations (fact → dimensions) | Star's central-fact-to-dimension dispatch |
| `kb/convergence.md` | N sources → one sink (mirror of fan-out) | Resolver-listed for star; optional read-direction variant |
| `kb/tree-hierarchy.md` | Vertical parent→children indent (normalized sub-tables) | Snowflake's normalized dimension hierarchy (DM-03 core) |
| `kb/linear-pipeline.md` | Sequential left-to-right stages | Resolver-listed for snowflake |
| `kb/group-container.md` | Bordered branded scope | Optional outer scope around the schema |
| `kb/evidence-card.md` | Real-data card | Resolver-listed for star (optional evidence strip) |

**Installation:** None. `npm view` / `pip index` are N/A — no packages are added by this phase. The only external artifact is the already-pinned esm.sh Excalidraw bundle, which is not installed locally.

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `line` element for dividers | A thin filled `rectangle` (height ~1px) | Rejected — `compartmented-box.md` mandates `line` dividers; a thin rect would be picked up by `_find_containing_shape` and could perturb `text_overflow_static`. Use `line`. |
| Per-row free-floating `text` | One multi-line `text` | **DISALLOWED** by `compartmented-box.md` HARD prohibition and SC-4 — breaks divider placement and the verifier's per-element width check. |
| Bound title text (`containerId`) | Free-floating title text | Either works; bound text is skipped by `text_overflow_static` (it `continue`s on `containerId`), so binding the title is the *safer* choice for the header. Row texts stay free-floating (they need a `line` between them). |

## Package Legitimacy Audit

> Not applicable. This phase installs **no external packages** — it authors Markdown recipe files and `.excalidraw`/PNG example pairs that target the already-pinned, already-vendored toolchain. slopcheck / registry verification have nothing to check. (Verified: no `package.json` dependency change, no `pip install`, no new runtime in scope.)

## Architecture Patterns

### System Architecture Diagram (authoring + verification flow this phase exercises)

```
  user request ("draw a star schema for Sales")
        │
        ▼
  /excalidraw command ── family pick (Data Modeling) ── type sub-pick (star-schema | snowflake)
        │
        ▼  resolver table (diagram-types/README.md)  →  recipe file + composed kb/*.md + example PNG
        │
        ▼
  excalidraw_specialist  ── reads diagram-types/<type>.md FIRST (INT-01)
        │                   ── composes compartmented-box construction (finalized offsets)
        │                   ── composes fan-out (star) / tree-hierarchy (snowflake)
        ▼
  authored .excalidraw JSON  (grouped sharp box + line dividers + per-row monospace text + elbow arrows)
        │
        ▼
  scripts/render/validate_and_render.sh ──► excalidraw_validator.py (metadata/label check)
        │                                └► render_docker.sh → render_excalidraw.py (esm.sh 0.17.3 exportToSvg) → sibling PNG
        ▼
  excalidraw_verifier ──► verifier_structural.py (text_overflow_static, arrow_endpoint_unanchored, …)
        │              └► visual rubric on the PNG (layout_collision, text_overflow_visual, …)
        ▼
  verifier-report.json  { passed: true/false, issues: [...] }   ◄── EX-03 exit gate
        │
        └─ if passed:false → specialist fixes JSON, re-renders, re-verifies (≤3 iterations, frozen loop)
```

### Recommended file structure (what this phase creates/touches)
```
.claude/agents/excalidraw/
├── diagram-types/
│   ├── star-schema.md            # NEW (DM-01) — references compartmented-box.md + finalizes offsets
│   ├── snowflake-schema.md       # NEW (DM-03) — references star + tree-hierarchy normalization
│   ├── compartmented-box.md      # TOUCH — finalize the deferred §"Scope of this file" offsets
│   └── README.md                 # TOUCH — fill the two planned resolver rows; update example PNG paths
├── examples_excalidraw/
│   ├── star_schema_v2.excalidraw      # NEW canonical source (distinct name; legacy grandfathered)
│   └── snowflake_schema.excalidraw    # NEW canonical source
├── examples/
│   ├── star_schema_v2.png             # NEW rendered ground truth
│   └── snowflake_schema.png           # NEW rendered ground truth
└── kb/
    ├── fan-out.md / convergence.md / tree-hierarchy.md / evidence-card.md / group-container.md / linear-pipeline.md
                                   # TOUCH — add "> Used by types: star-schema" / "snowflake-schema" back-refs (DTKB-03)
```
> **Naming caution:** the legacy `examples/example_star_schema.png` + `examples_excalidraw/star_schema.excalidraw` are grandfathered and referenced by `kb/README.md` and the current resolver row. Author the NEW pair under a *distinct* filename (e.g. `star_schema_v2`) to avoid clobbering grandfathered ground truth, OR explicitly retire the legacy references — decide in planning. [ASSUMED — exact new filename is a planning choice; both options are valid.]

### Pattern 1: The finalized compartmented table-box (the core deliverable)
**What:** One sharp rectangle + N+1 horizontal `line` dividers + one title text + one free `text` per column, all sharing one `groupIds` id.
**When to use:** Every dimension/fact entity box in star and snowflake (and later ER, class, data-vault).
**Recommended finalized offsets** (all multiples of 20 except the 12px left-pad, which is a per-element inset that does not need to be on the 20-grid):

```jsonc
// Box frame — sharp corners, grouped
{
  "type": "rectangle", "id": "fact_sales_box",
  "x": 600, "y": 200, "width": 240, "height": 160,   // width sized to longest row (see width rule)
  "roundness": null,                                  // SHARP — never {type:3} for a formal box
  "roughness": 0, "strokeColor": "#1e3a5f", "backgroundColor": "transparent",
  "groupIds": ["grp_fact_sales"]
}
// Header divider — spans FULL box width: x = box.x, points end at box.width exactly
{
  "type": "line", "id": "div_fact_header",
  "x": 600, "y": 240, "width": 240, "height": 0,
  "points": [[0, 0], [240, 0]],                       // box.x → box.x+width, NO over/undershoot
  "roundness": null, "roughness": 0, "strokeColor": "#1e3a5f",
  "groupIds": ["grp_fact_sales"]
}
// Title text — header compartment (header height = 40 ⇒ divider at box.y+40)
{
  "type": "text", "id": "fact_sales_title",
  "x": 612, "y": 210,                                 // box.x + 12 left-pad
  "width": 100, "height": 20,                         // REQUIRED: explicit width/height
  "text": "fact_sales", "fontSize": 16, "fontFamily": 3,
  "lineHeight": 1.25, "textAlign": "left", "verticalAlign": "top",
  "originalText": "fact_sales", "strokeColor": "#1e1e1e",
  "roundness": null, "groupIds": ["grp_fact_sales"]
}
// Row text — one per column, SHARED left x = box.x + 12, row pitch 20
{
  "type": "text", "id": "fact_sales_row1",
  "x": 612, "y": 250,                                 // first row sits below header divider (box.y+40+10 baseline)
  "width": 180, "height": 20,
  "text": "date_key       FK", "fontSize": 16, "fontFamily": 3,
  "lineHeight": 1.25, "textAlign": "left", "verticalAlign": "top",
  "originalText": "date_key       FK", "strokeColor": "#1e1e1e",
  "roundness": null, "groupIds": ["grp_fact_sales"]
}
```

**The three rules the verifier and SC-1/SC-4 enforce (lock these into the recipe):**
1. **Width rule (passes `text_overflow_static`):** `box.width >= max_over_rows(len(row.text) * 0.6 * row.fontSize)`. At `fontSize:16`, a 24-char row needs `24*0.6*16 = 230.4px`; round box width UP to the next 20-grid value (240). Always size the box to the *longest* row, padded.
2. **Common-left-x rule (SC-1):** every row text `x` is identical = `box.x + 12`. No column drift.
3. **Full-width divider rule (SC-1):** every divider `line` has `x == box.x` and `points[-1][0] == box.width` exactly — divider x-range equals the box x-range. Divider `y` values land on the 20-grid and never bisect a row.

### Pattern 2: Star = central fact box + fan-out to dimension boxes
**What:** One fact box centered, dimension boxes radiating out, connected with elbow arrows via `kb/fan-out.md` geometry.
**Key:** Arrows must satisfy `arrow_endpoint_unanchored` — the **last point must land within 8px of a rectangle/ellipse/diamond border**. So arrows connect the **box rectangle borders**, NOT row texts or `line` dividers (lines are not in the anchorable shape set). Use `elbowed: true`, `roundness: null`, ≥3 points, `endArrowhead: "arrow"` (legal token). Bind via `startBinding`/`endBinding` to the box ids (compliant examples do this with `fixedPoint`/`mode:"orbit"`).

### Pattern 3: Snowflake = star + normalized dimension tree-hierarchy
**What:** Take a star dimension box and normalize it into a sub-hierarchy of smaller boxes (e.g. `dim_product → dim_category → dim_department`), laid out with `kb/tree-hierarchy.md` geometry (children indent +60px x, 40–48px y-step, thin `strokeWidth:1.5` elbow connectors). Author snowflake **only after** star passes (SC-2). Reference star's finalized box offsets verbatim — do not re-derive.

### Anti-Patterns to Avoid
- **Soft corners on a formal box** (`roundness: {type:3}`) — the legacy star's mistake; the recipe mandates `roundness: null`. (`compartmented-box.md`)
- **Multi-line single `text` for compartments** — DISALLOWED; breaks dividers + width check. (SC-4)
- **Anchoring arrows to row texts or dividers** — `arrow_endpoint_unanchored` only counts rectangle/ellipse/diamond borders; an arrow ending on a `line` divider reads as unanchored. Anchor to the box rectangle.
- **Copying `star_schema.excalidraw`** — grandfathered, 0 groups, unbound, soft; explicitly NOT a template.
- **Dividers that stop short of / overrun the border** — a defect per `compartmented-box.md` §Alignment.
- **Forgetting explicit `width`/`height` on text** — triggers `text_missing_dimensions` (error): the text renders in PNG but collapses to invisible in the editor.
- **Illegal arrowhead token** (`crowsfoot`, `diamond`, `hollow`) — renders silently as a plain line; Pitfall 1.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Compartmented box geometry | A fresh box recipe per type file | Reference `diagram-types/compartmented-box.md` (finalize its offsets once) | INT-02 mandates ONE construction; re-deriving per type guarantees drift |
| Fact→dimension connectors | Ad-hoc arrow coordinates | `kb/fan-out.md` shared-rail elbow geometry | Coordinate math lives only in `kb/`; type files compose by `@`-ref |
| Normalized dimension layout | Custom indent math | `kb/tree-hierarchy.md` (+60px x / 40px y / thin elbows) | Already the blessed tree pattern |
| Width-fit / overflow detection | A manual eyeball check | The frozen `text_overflow_static` formula (`len*0.6*fontSize`) | It is the deterministic gate; author TO it, don't reinvent it |
| Pass/fail judgment | A new check script | The frozen `excalidraw_verifier` + `verifier_structural.py` | v1.0 is frozen; additive phase |

**Key insight:** Phase 6's whole value is *composition discipline* — finalize the deferred box geometry exactly once, target the verifier's known formula precisely, and let snowflake inherit star's locked numbers. Any re-derivation is a future drift bug.

## Runtime State Inventory

> This is a KB-authoring phase, not a rename/migration. It does create new files that other files index, so the "what references what" audit below matters.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — no datastore holds schema state. (Verified: this is a prompt/KB repo, no DB.) | None |
| Live service config | None — no external service. | None |
| OS-registered state | None. | None |
| Secrets/env vars | `EXCALIDRAW_ASSETS_DIR` is read by render/verifier for icon resolution, but star/snowflake boxes need no icons (text-only compartments). No new env var introduced. | None |
| Build artifacts | The rendered `examples/*.png` are build artifacts of the `.excalidraw` sources; they must be re-rendered, not hand-edited. Legacy `examples/example_star_schema.png` is grandfathered. | Render new PNGs via `validate_and_render.sh`; do not clobber grandfathered legacy unless explicitly retiring it. |
| Cross-file references (KB) | The new types must be indexed in `diagram-types/README.md` resolver (2 planned rows), and each composed `kb/*.md` needs a `> Used by types:` back-ref (DTKB-03). `kb/README.md` reference-example index also lists the legacy star. | Update resolver rows + add back-refs + reconcile the example index. |

## Common Pitfalls

### Pitfall 1: Illegal arrowhead token renders silently as a plain line
**What goes wrong:** A connector with `endArrowhead: "crowsfoot"` (or any token outside `arrow|bar|dot|triangle|null`) renders as a headless line — the relationship semantics vanish, no error.
**Why it happens:** Excalidraw `0.17.3` silently ignores unknown arrowhead values. (`notation-conventions.md`)
**How to avoid:** Star/snowflake connectors are plain associations — use `endArrowhead: "arrow"`. Never invent a token.
**Warning signs:** Connector looks like a bare line in the PNG; no verifier error (it's not a structural check) — caught only by visual review.

### Pitfall 2: Multi-line text packs rows and silently overflows the box
**What goes wrong:** Authoring all columns as one `text` with `\n`. The verifier's `text_overflow_static` measures one width per element = the widest line; a long row overflows undetected, AND there's no per-row boundary to place a `line` divider.
**Why it happens:** It's the "obvious" way to fill a box; it's exactly what `compartmented-box.md` forbids.
**How to avoid:** One `text` element per row (SC-4). One row string per element.
**Warning signs:** A box with dividers but no clean row boundaries; a row visibly poking past the border in the PNG.

### Pitfall 3: Box width too small → `text_overflow_static` error
**What goes wrong:** Box width < `len(longest_row)*0.6*fontSize` → structural `error`, `passed:false`.
**Why it happens:** Eyeballing width instead of computing it.
**How to avoid:** Compute `max_over_rows(len*0.6*fontSize)`, round UP to a 20-grid width. At `fontSize:16` that's `9.6px/char`; budget ~10px/char plus left-pad.
**Warning signs:** Verifier report `text_overflow_static` with the exact `>=threshold` suggested fix.

### Pitfall 4: Divider `line` doesn't span the full width / arrows anchor to the wrong element
**What goes wrong:** A divider that stops short looks ragged (SC-1 fail). An arrow ending on a row `text` or a `line` divider trips `arrow_endpoint_unanchored` because only rectangle/ellipse/diamond borders count as anchors.
**Why it happens:** `line` is not in the anchorable shape set (`verifier_structural.py` `check_arrow_endpoint_unanchored`); the divider full-width rule is geometric, not verifier-enforced.
**How to avoid:** Divider `x == box.x` and `points[-1][0] == box.width` exactly. Anchor arrows to the **box rectangle** border within 8px; prefer `startBinding`/`endBinding` to the box ids.
**Warning signs:** Ragged dividers in the PNG; `arrow_endpoint_unanchored` error in the report.

### Pitfall 5: Soft corners or ungrouped elements
**What goes wrong:** Using `roundness: {type:3}` (the legacy/default style) on a formal box, or omitting `groupIds`, so dividers desync from the box when moved.
**Why it happens:** Every existing example uses soft corners and 0 groups — copying any of them propagates the wrong style.
**How to avoid:** `roundness: null` on box+dividers; one shared `groupIds` id across frame, dividers, title, and all rows. There is NO compliant template in the repo — author from the recipe, not from an example.
**Warning signs:** Rounded box in the PNG; moving the box leaves dividers behind (won't show in a static render but violates INT-02).

### Pitfall 6: Authoring snowflake before star passes
**What goes wrong:** Snowflake inherits un-finalized box geometry; star and snowflake drift.
**Why it happens:** Skipping the SC-2 ordering gate.
**How to avoid:** Fully land star (recipe + example + green loop) first; lock the offsets; then snowflake references them verbatim.

## Code Examples

See Pattern 1 above for the full annotated box JSON (frame + header divider + title + row), and Patterns 2–3 for fan-out / tree-hierarchy composition. Source field sets verified against `examples_excalidraw/repo_tree_hierarchy.excalidraw` (text element keys) and `examples_excalidraw/data_pipeline_flow.excalidraw` (bound elbow arrow keys) this session.

**Minimum required text-element fields** (omitting any of width/height triggers `text_missing_dimensions`):
`type, x, y, width, height, text, fontSize, fontFamily:3, lineHeight:1.25, textAlign, verticalAlign, originalText, strokeColor, roundness, groupIds`.

## State of the Art

| Old Approach (legacy star) | Current Approach (Phase 6 recipe) | When Changed | Impact |
|----------------------------|-----------------------------------|--------------|--------|
| 113 free-floating manually-positioned texts, 0 groups | Per-row text bound by one `groupIds` group | v1.1 / Phase 4 construction, finalized Phase 6 | Box moves/places as a unit; verifier per-row width check valid |
| `roundness: {type:3}` soft box | `roundness: null` sharp box | v1.1 | Formal-notation convention |
| Unbound arrows (`startBinding:null`, `roundness:{type:2}`) | Bound elbow arrows (`elbowed:true`, `roundness:null`, ≥3 pts) | v1.1 | Passes `arrow_endpoint_unanchored` + avoids `arrow_not_elbow` warning |
| 0 `line` dividers (compartments implied by spacing) | Explicit full-width `line` dividers | Phase 6 (first in repo) | SC-1 dividers visible + placeable |

**Deprecated/outdated:**
- `examples_excalidraw/star_schema.excalidraw` — grandfathered legacy; NOT a template. The new canonical pair supersedes it as the recipe reference.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | New example filenames should be distinct (e.g. `star_schema_v2`) to avoid clobbering grandfathered legacy `example_star_schema.png` | File structure | Low — if planner chooses to retire the legacy refs instead, same outcome; just a naming decision |
| A2 | Recommended offsets (header 40, row pitch 20, left-pad 12, fontSize 16) are *a* valid finalization, not the only one | Pattern 1 | Low — any 20-grid set satisfying the three rules works; these are a concrete, verifier-passing starting point the planner can adopt or adjust |
| A3 | Snowflake's normalized dimensions render cleanly with `tree-hierarchy` thin elbow connectors anchored to sub-box rectangles | Pattern 3 | Medium — must be proven in the render loop; tree connectors anchor to rectangle borders (OK per verifier), but dense snowflakes may need wider rails to avoid `layout_collision` |

## Open Questions

1. **Should the new star example fully replace the grandfathered legacy in `kb/README.md`'s reference-example index, or coexist?**
   - What we know: legacy is referenced in `kb/README.md` (row: `example_star_schema.png`) and the resolver row currently points at the legacy PNG.
   - What's unclear: whether to retire the legacy reference now or leave it as a historical artifact.
   - Recommendation: point the resolver row at the NEW compliant PNG (it's the type's canonical ground truth); leave the legacy file on disk but stop indexing it as the star reference. Decide explicitly in planning.

2. **Title text: bind via `containerId` or leave free-floating?**
   - What we know: `text_overflow_static` skips text with a `containerId` (it `continue`s). Binding the title makes the header immune to the width check.
   - Recommendation: bind the title to the box (safer header), keep row texts free-floating (they need `line` dividers between them and must be width-checked).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `validate_and_render.sh` + Docker render path | EX-03 loop (rendering examples) | Assumed ✓ (used through Phases 1–5) | repo HEAD | none — required to produce ground-truth PNGs |
| esm.sh `@excalidraw/excalidraw@0.17.3` (network at render) | render_template.html | ✓ at render time | 0.17.3 | none (HARD-01 to vendor it is a deferred v2 item) |
| `python3` (validator + verifier helper) | validate + structural check | ✓ (used throughout) | system | none |

**Missing dependencies with no fallback:** None known — the same toolchain shipped Phases 1–5. The Docker render path's availability should be confirmed at execution time (it is the only way to generate the EX-03 ground-truth PNGs).

## Validation Architecture

> `nyquist_validation` is enabled (config.json `workflow.nyquist_validation: true`). This project's "tests" are the validate→render→verify loop, not a unit-test framework.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | The frozen v1.0 loop (no pytest/jest) — `validate_and_render.sh` + `excalidraw_verifier` |
| Config file | none (script-driven) |
| Quick run command | `bash .claude/agents/excalidraw/scripts/render/validate_and_render.sh <file>.excalidraw` |
| Full suite command | render the example, then invoke `excalidraw_verifier` on the `.excalidraw` and assert `verifier-report.json` `passed:true` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DM-01 / SC-1 | star example renders; dividers full-width; rows share left x; no overflow | loop | `validate_and_render.sh star_schema_v2.excalidraw` → verifier `passed:true`, no `text_overflow_static`/`text_missing_dimensions` | ❌ Wave 0 (example not yet authored) |
| DM-03 / SC-2 | snowflake example renders; passes loop; authored after star | loop | same command on `snowflake_schema.excalidraw` → `passed:true` | ❌ Wave 0 |
| SC-3 | both pairs indexed in resolver | structural | grep `diagram-types/README.md` resolver for both rows pointing at the new PNGs | ❌ Wave 0 |
| SC-4 | per-row separate `text` (no multi-line) | structural | assert each box's row count == number of `text` elements in its group; no row `text` contains `\n` | ❌ Wave 0 (assertion script optional) |

### Sampling Rate
- **Per task commit:** run `validate_and_render.sh` on the example being authored; eyeball the PNG.
- **Per wave merge:** full verifier pass (`passed:true`) on every authored example.
- **Phase gate:** both star and snowflake examples green (EX-03) before `/gsd-verify-work`.

### Wave 0 Gaps
- [ ] `examples_excalidraw/star_schema_v2.excalidraw` — the compliant star source (DM-01)
- [ ] `examples/star_schema_v2.png` — rendered ground truth
- [ ] `examples_excalidraw/snowflake_schema.excalidraw` + `examples/snowflake_schema.png` (DM-03)
- [ ] Finalized offsets written into `compartmented-box.md` §"Scope of this file"
- [ ] (Optional) a tiny SC-4 assertion (one `text` per row, no `\n` in row texts) — can be a manual check or a throwaway grep; the existing verifier does NOT check this, so it's the one gap the frozen loop won't catch automatically.

> **Note:** The frozen verifier covers overflow, missing dimensions, arrow anchoring, arrowhead legality, monospace, roughness. It does NOT enforce SC-4's "no multi-line text" or SC-1's "divider spans full width" — those are geometric/authoring rules. Plan a manual or scripted spot-check for them.

## Security Domain

> `security_enforcement` is not present in config.json (treated as enabled by default), but this phase has **no attack surface**: it authors static Markdown + `.excalidraw` JSON consumed only by the local render/verify toolchain. No auth, no network input handling, no user-supplied code execution introduced.

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | marginal | The verifier already treats `.excalidraw` text as DATA, never instructions (prompt-injection-resistant by design — see `excalidraw_verifier.md` `<role>`). Phase 6 introduces no new untrusted input path. |
| V2/V3/V4/V6 | no | No auth, session, access-control, or cryptography surface in a KB-authoring phase. |

### Known Threat Patterns for this stack
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Diagram-text prompt injection (e.g., a label saying "ignore instructions") | Tampering | Already mitigated: verifier `<role>` mandates treating file content as data only — do not regress this when authoring example text. |

## Sources

### Primary (HIGH confidence — read in full this session)
- `.claude/agents/excalidraw/diagram-types/compartmented-box.md` — the deferred-offsets construction + alignment rules + HARD prohibition
- `.claude/agents/excalidraw/diagram-types/README.md` — resolver table, two planned rows, legacy grandfathering
- `.claude/agents/excalidraw/diagram-types/notation-conventions.md` — legal arrowhead set, silent-failure rule
- `.claude/agents/excalidraw/diagram-types/tech-architecture.md` — the exemplar TYPE-file structure to mirror
- `.claude/agents/excalidraw/excalidraw_verifier.md` + `scripts/verifier/verifier_structural.py` — exact check formulas (`text_overflow_static`, `arrow_endpoint_unanchored`, `text_missing_dimensions`, etc.)
- `.claude/agents/excalidraw/scripts/render/{validate_and_render.sh,excalidraw_validator.py,render_excalidraw.py,render_template.html}` — render pipeline + pinned 0.17.3
- `kb/{fan-out,convergence,tree-hierarchy,linear-pipeline,group-container,evidence-card,README}.md` — composed primitives + back-ref convention
- `examples_excalidraw/{star_schema,architecture_overview,repo_tree_hierarchy,data_pipeline_flow}.excalidraw` — element-schema + non-compliance analysis (Python introspection this session)
- `.planning/{ROADMAP,REQUIREMENTS,STATE}.md` — phase scope, success criteria, locked decisions

### Secondary / Tertiary
- None needed. This is a closed codebase; no external/web sources were required, and none would supersede the in-repo frozen toolchain.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — every component read directly; no packages added.
- Architecture / recipe geometry: HIGH on the *rules* (verifier formulas are source-of-truth), MEDIUM on the *exact offset numbers* (A2 — a valid finalization, to be confirmed by a render pass).
- Pitfalls: HIGH — derived from the actual verifier checks and the documented construction prohibitions, not training data.

**Research date:** 2026-06-04
**Valid until:** stable indefinitely while the v1.0 loop stays frozen (no external/fast-moving deps). Re-check only if `verifier_structural.py` or the Excalidraw pin changes.
