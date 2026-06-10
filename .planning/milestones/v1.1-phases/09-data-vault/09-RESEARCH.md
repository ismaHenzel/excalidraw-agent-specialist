# Phase 9: Data Vault - Research

**Researched:** 2026-06-08
**Domain:** Excalidraw `.excalidraw` JSON authoring — the Data Vault data-modeling type (hub / link / satellite), layering a documented, accessibility-safe 3-role semantic palette + text role label onto the already-proven compartmented-box + fan-out + tree-hierarchy recipes
**Confidence:** HIGH (closed, pinned codebase; every structural claim grounded in files read this session. The one genuinely new design surface — the 3-role palette — is MEDIUM until proven through a render+visual-review pass.)

## Summary

Phase 9 is the **last** v1.1 type and, like Phases 6–8, it is **prompt/KB-engineering work, not application code**. It authors one new TYPE-layer recipe (`diagram-types/data-vault.md`), one canonical example pair (`.excalidraw` + PNG), and the resolver/back-ref bookkeeping. Almost everything it needs is **already built and locked**: the compartmented-box construction with finalized offsets (`compartmented-box.md`, Phase 4/6), fan-out geometry (`kb/fan-out.md`), tree-hierarchy indent geometry (`kb/tree-hierarchy.md`), convergence (`kb/convergence.md`), and the legal-arrowhead house rules (`notation-conventions.md`). The data-vault entity boxes (hub, link, satellite) are **literally the same compartmented box** that star/snowflake/ER/class already use — sharp rectangle + full-width `line` dividers + bound title + per-row monospace texts + one `groupIds` per box. No new box geometry is derived.

The **one genuinely new design surface** — and the entire distinctive value of this phase — is the **3-role semantic palette** that distinguishes hub / link / satellite, paired with a **text role label** so the three classes stay distinguishable **in grayscale** (SC-2: "no color-only distinction"). This is the first time the project ships a recipe whose semantics are carried by *fill color*: every prior compliant example (star_v2, snowflake, ER, class) is essentially monochrome — `strokeColor` is `#1e3a5f`/`#1e1e1e` and `backgroundColor` is `transparent` across the board [VERIFIED: introspected all four example sources this session]. So there is no in-repo precedent for a color-semantic data-model box to copy; the palette must be chosen and documented from scratch, then proven.

The single most important verified finding for de-risking SC-2: **nothing in the loop checks color.** I read `verifier_structural.py` (10 checks: emoji, overflow, missing-dims, unanchored-arrow, image-path, roughness, fontfamily, points-too-few, not-elbow, sequence-center-x) — **zero color/contrast/palette checks** — and the validator (`excalidraw_validator.py`) checks metadata + labels only. The verifier's visual rubric (`excalidraw_verifier.md`) mentions color only incidentally. **Therefore SC-2 (grayscale-distinguishable, never color-alone) has NO automated guard.** The mandatory **text role label** on every box (`«hub»` / `«link»` / `«sat»`) is not a nicety — it is the *only* mechanism that survives the grayscale test, and it is the thing the planner must make a hard authoring rule + manual/visual checklist item, exactly as Phase 7 handled the unguarded arrowhead-legality gap.

**Primary recommendation:** Author `data-vault.md` to compose the locked compartmented-box verbatim for all three table classes; assign each class a distinct **fill from the existing Semantic Color Palette chosen for well-separated WCAG luminance** (recommended below: hub `#dbeafe` light-blue, link `#fef3c7` light-amber, satellite `#a7f3d0` light-green — luminance 0.81 / 0.89 / 0.77 are NOT separated enough alone, so the text role label is mandatory; alternatively pick a darker hub fill for stronger grayscale spread — see the palette section); pair EVERY box with a mandatory `«hub»`/`«link»`/`«sat»` stereotype text label and a small in-canvas **legend** (3 swatch rows) so the role is readable with color stripped. Use fan-out for hub→link spine connectors and tree-hierarchy thin elbows for satellite attachments. Plain `endArrowhead:"arrow"` connectors anchored to box RECTANGLE borders (legal-token set only). Author the example, pass the full validate→render→verify loop including the EX-03 visual gate (the real SC-2 judge), THEN wire the resolver row.

## Architectural Responsibility Map

Single-tier KB/agent system; "tiers" map to the two-layer KB plus the frozen v1.0 loop (same framing as Phases 6–8).

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Data-vault *purpose + how-to-draw* prose | TYPE layer (`diagram-types/data-vault.md`) | — | A diagram type is a composition recipe; lives one layer above primitives |
| Hub/link/satellite box geometry | `diagram-types/compartmented-box.md` (LOCKED) | TYPE file references it | INT-02 finalized offsets; reused verbatim — never re-derived |
| Hub→link spine connectors (fan-out) | `kb/fan-out.md` (LOCKED) | TYPE file references | Coordinate math lives only in `kb/` |
| Satellite attachments (indented) | `kb/tree-hierarchy.md` (LOCKED) | `kb/convergence.md` | Thin elbow indent geometry already proven on snowflake |
| 3-role semantic palette + role label | **NEW — documented in `data-vault.md`** | specialist Semantic Color Palette table | The genuinely new design surface; no in-repo color-semantic precedent |
| Legal-arrowhead encoding | `diagram-types/notation-conventions.md` (LOCKED) | — | DTKB-04; data-vault connectors are plain associations |
| Family→type→recipe dispatch | Resolver table (`diagram-types/README.md`) | `/excalidraw` + specialist | Single authoritative map; Phase 9 fills the one reserved row |
| Render correctness (PNG) | v1.0 loop (`scripts/render/`) — FROZEN | — | Additive phase; must not touch validator/renderer |
| Structural + visual pass/fail | v1.0 verifier (`excalidraw_verifier.md` + `verifier_structural.py`) — FROZEN | — | Recipe must satisfy existing checks; SC-2 color distinction is NOT checked — visual gate is the judge |

## User Constraints

**No `*-CONTEXT.md` exists for this phase yet** (`.planning/phases/09-data-vault/` is empty at research time — no `/gsd-discuss-phase` decisions to honor). The binding constraints below are extracted from ROADMAP.md, REQUIREMENTS.md, STATE.md, and the committed in-repo KB, and carry locked-decision authority. There is no CLAUDE.md and no `.claude/skills/` directory in this project, so no project-skill rules apply.

### Locked Decisions (from committed KB + ROADMAP/STATE/REQUIREMENTS)
- **v1.0 loop, validator, and verifier are FROZEN.** All v1.1 work is additive — new KB file + resolver row + example pair only. No edits to `scripts/render/*`, `scripts/verifier/*`, or the verifier prompt. (STATE.md Decisions; REQUIREMENTS.md Out of Scope)
- **Hub/link/satellite distinction uses a documented 3-role palette PAIRED WITH a text role label — never color alone** (SC-2). The three classes MUST remain distinguishable in grayscale. This is the central, non-negotiable requirement of DM-04.
- **Compartmented-box offsets are FINALIZED** (`compartmented-box.md`): header 40px, row pitch 20px, left-pad 12px, fontSize 16, monospace `fontFamily: 3`, box-width rule `len*0.6*16` rounded up to the 20-grid. Reused VERBATIM by hub/link/satellite boxes — not re-derived.
- **Multi-line single `text` blocks are DISALLOWED for compartments.** Each row is its own `text` element. Binding rule from `compartmented-box.md` HARD prohibition.
- **Arrowhead set is fixed to `arrow|bar|dot|triangle|null`.** Any other token renders silently as a plain line. Data-vault connectors are plain associations → `endArrowhead: "arrow"`. (`notation-conventions.md`; DTKB-04)
- **Legacy `star_schema.excalidraw` is grandfathered and NOT a safe template** (0 groupIds, unbound arrows, soft roundness). Do not imitate it. (`README.md` Legacy resolution)
- **EX-01/EX-03 are per-type EXIT CRITERIA**: the canonical example must pass the full validate→render→verify loop (structural automated + EX-03 visual human approval) BEFORE the resolver row is wired. (REQUIREMENTS.md; every prior shipped type followed this.)
- **Data Vault is the LONG POLE, sequenced last (Phase 9)** per explicit user decision; depends on Phase 6 (table-box) and Phase 7 (relationships), both COMPLETE. (STATE.md; ROADMAP.md)
- **Resolver row already RESERVED** in `diagram-types/README.md`: `data-vault | data-vault.md (planned — Phase 9) | group-container, fan-out, tree-hierarchy, convergence, evidence-card | (planned)`. The composed-primitive list is pre-declared; the recipe must honor it (or the row is updated if the composition is refined).

### Claude's Discretion
- **The exact 3-role palette** (which fills/strokes for hub/link/satellite). Recommendation below; the requirement only mandates "documented, accessibility-safe, grayscale-distinguishable + text label." The chosen colors should come from (or extend) the existing specialist Semantic Color Palette and be proven through the visual gate.
- **The exact form of the role label** (`«hub»` guillemet stereotype vs. `[HUB]` bracket vs. a header-band convention). Guillemets are confirmed safe under `fontFamily: 3` (Phase 7 A1).
- **Whether to include an in-canvas legend** (3 swatch+label rows). STRONGLY recommended as the most robust grayscale-safety guarantee — but the form is discretionary.
- **Example subject matter** (which business domain the canonical hub/link/satellite model depicts — e.g. a Sales/Customer vault). Pick a small, recognizable, real-world raw-vault slice.
- **Whether satellite layout uses `tree-hierarchy` (indented) or `fan-out` (radial)** for attaching satellites to hubs/links — both are in the reserved composition list; pick per readability.

### Deferred Ideas (OUT OF SCOPE)
- Any renderer/validator/verifier change — v2 hardening / frozen. (Note: unlike Phase 7's arrowhead-enum check, there is no recommended validator addition here — a color/contrast check would be a frozen-component change and is NOT recommended; rely on the role label + visual gate.)
- Native crow's-foot/diamond/hollow arrowheads — out of scope (workarounds only).
- Business Vault / PIT / Bridge tables and other advanced Data Vault 2.0 constructs beyond hub/link/satellite — out of scope (DM-04 scopes exactly hub/link/satellite).
- Remaining ~10 UML types (v2); pixel-diff visual regression (out of scope); auto-generating diagrams from schemas (out of scope).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DM-04 | A `diagram-types/data-vault.md` recipe exists (hub / link / satellite, distinguished by the semantic palette) and the agent can author a data-vault diagram that passes the full validate→render→verify loop | Hub/link/satellite boxes = the locked `compartmented-box.md` construction (Phase 4/6), reused verbatim. Hub→link spine = `kb/fan-out.md`; satellite attachment = `kb/tree-hierarchy.md` (indented) or `kb/convergence.md`. 3-role palette = NEW, chosen from the specialist Semantic Color Palette with separated luminance + mandatory text role label (SC-2). Connectors = plain `endArrowhead:"arrow"`, legal-token set (`notation-conventions.md`). Canonical example pair authored + passed loop + resolver row wired (EX-01/EX-03). |

> SC-1 (recipe exists + example passes the full loop), SC-2 (grayscale-safe 3-role palette + text label), and SC-3 (canonical example pair indexed) are the three success criteria; SC-2 is the distinctive one and has NO automated guard (visual gate + role-label discipline only).
</phase_requirements>

## Standard Stack

This phase ships **no new software dependencies**. The "stack" is the existing frozen toolchain the recipe must target — identical to Phases 6–8.

### Core (frozen toolchain the recipe targets)
| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| `@excalidraw/excalidraw` | `0.17.3` (via esm.sh `?bundle`) | Renders `.excalidraw` JSON → SVG → PNG | Pinned in `scripts/render/render_template.html`; fixes the 5-arrowhead set + element schema [VERIFIED: in-repo, Phases 6–8 research] |
| `validate_and_render.sh` | repo HEAD | Validate JSON + render to sibling PNG | Mandated v1.0 entry point; FROZEN |
| `excalidraw_verifier` + `verifier_structural.py` | repo HEAD | Structural + visual pass/fail report | The gate the example must pass; FROZEN. **10 checks, none color-related** [VERIFIED: read this session] |

### Supporting (existing KB the recipe composes — install nothing, reference these)
| File | Purpose | When to Use |
|------|---------|-------------|
| `diagram-types/compartmented-box.md` | Locked box construction + finalized offsets | EVERY hub/link/satellite box references this verbatim |
| `diagram-types/notation-conventions.md` | Legal arrowhead set + house rules | Connectors = plain `arrow`; legal-token discipline |
| `kb/fan-out.md` | One source → N destinations | Hub → its links / a hub radiating to satellites |
| `kb/tree-hierarchy.md` | Vertical parent→child indent, thin elbows | Satellites attached/indented off a hub or link |
| `kb/convergence.md` | N sources → one sink | Multiple hubs converging into a link (link references ≥2 hubs) |
| `kb/group-container.md` | Bordered named scope | Optional outer "Raw Vault" scope; the in-canvas legend box |
| `kb/evidence-card.md` | Real-data card | Optional sample-row strip (reserved in resolver list) |

**Installation:** None. `npm view` / `pip index` / `cargo search` are N/A — no packages are added by this phase. The only external artifact is the already-pinned esm.sh Excalidraw bundle (not installed locally; HARD-01 to vendor it is a deferred v2 item).

**Version verification:** No registry install this phase, so there is nothing to version-verify against npm/PyPI/crates. `0.17.3` is the pinned render version confirmed across Phases 1–8 [VERIFIED: render_template.html per prior research].

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Distinct fill per role + text label | Distinct fill ONLY (color-alone) | **DISALLOWED by SC-2** — fails the grayscale test. The text role label is mandatory. |
| Text role label as a `«hub»` guillemet stereotype | `[HUB]` ASCII bracket prefix in the title row | Both work; guillemets match the class-diagram stereotype convention and are safe under `fontFamily:3` (Phase 7 A1). ASCII brackets are the zero-risk fallback if guillemets ever tofu. |
| Three fills from the existing palette | A bespoke colorblind-optimized triad (e.g. Okabe–Ito) | Bespoke triads have better raw color-separation, but extend beyond the documented Semantic Color Palette and still wouldn't satisfy SC-2 without a label. Prefer reusing the documented palette + label; surface as a house decision. |
| `tree-hierarchy` indented satellites | `fan-out` radial satellites | Both reserved in the resolver list; indent reads as "belongs to", radial reads as "attached spokes". Pick per example density. |

## Package Legitimacy Audit

> **Not applicable.** This phase installs **no external packages** — it authors one Markdown recipe file and one `.excalidraw`/PNG example pair that target the already-pinned, already-vendored toolchain. slopcheck / registry verification have nothing to check. (Verified: no `package.json` dependency change, no `pip install`, no new runtime in scope — identical posture to Phases 6–8.)

## Architecture Patterns

### System Architecture Diagram (the authoring + verify flow this phase exercises)

```
User request ("draw a Data Vault model for Sales")
        │
        ▼
/excalidraw ── family pick (Data Modeling) ── type sub-pick (… | data-vault)
        │
        ▼  resolver table (diagram-types/README.md) → recipe + composed kb/*.md + example PNG
        │
        ▼
excalidraw_specialist ── reads diagram-types/data-vault.md FIRST (INT-01)
        │   ├─► @compartmented-box.md      (locked box offsets — hub/link/satellite boxes)
        │   ├─► @kb/fan-out.md             (hub → link spine)
        │   ├─► @kb/tree-hierarchy.md      (satellite attachments, thin elbows)
        │   ├─► @kb/convergence.md         (≥2 hubs → one link)
        │   ├─► @notation-conventions.md   (legal arrowhead set; plain association arrows)
        │   └─► NEW: 3-role palette + mandatory «hub»/«link»/«sat» label + legend
        ▼
authored data-vault.excalidraw JSON
   (3 box classes, distinct fills + role labels, legend, plain-arrow spine + sat elbows)
        │
        ▼
scripts/render/validate_and_render.sh
   ├─ Phase 1: excalidraw_validator.py   ◄── checks metadata+labels only; NO color check
   ├─ Phase 2: render_docker.sh → PNG
   └─ Phase 3: instruction to read PNG
        │
        ▼
excalidraw_verifier (structural: verifier_structural.py 10 checks + multimodal visual review)
   ├─ structural: emoji, overflow, missing-dims, unanchored-arrow, roughness, fontfamily, elbow…
   │     ◄── NO color/contrast/palette check anywhere
   └─ visual (EX-03 gate): "are the three roles distinguishable — including in grayscale?"
        │     ◄── THE ONLY judge of SC-2
        ▼
   passed:false → specialist fixes JSON, re-render, re-verify (≤3 iterations, frozen loop)
   passed:true  → EX-03 visual human approval → wire the resolver row
```

### Recommended File Structure (additive)

```
.claude/agents/excalidraw/
├── diagram-types/
│   ├── data-vault.md                    # NEW type recipe (DM-04) — composes locked primitives + NEW palette section
│   └── README.md                        # EDIT: wire the reserved data-vault resolver row (AFTER loop + EX-03 pass)
├── examples_excalidraw/
│   └── data_vault_<subject>.excalidraw  # NEW canonical source
├── examples/
│   └── data_vault_<subject>.png         # NEW rendered ground truth (sibling, passes loop)
└── kb/
    ├── fan-out.md / tree-hierarchy.md / convergence.md / group-container.md / evidence-card.md
                                         # EDIT: append ", data-vault" to each "> Used by types:" back-ref (DTKB-03)
```

> **Naming caution:** follow the established convention `data_vault_<subject>` (mirrors `star_schema_v2`, `er_retail_orders`, `class_order_domain`, `use_case_checkout`). The PNG and `.excalidraw` share the base name and live in sibling dirs `examples/` and `examples_excalidraw/`.

### Pattern 1: Hub / Link / Satellite as the locked compartmented box (reused verbatim)
**What:** Each of the three table classes is the SAME compartmented box star/snowflake/ER/class already use — sharp rectangle (`roundness: null`, `roughness: 0`), full-width `line` header divider (`x == box.x`, `points = [[0,0],[width,0]]`), one title text bound via `containerId`, N free-floating per-row monospace texts (`fontFamily: 3`, `fontSize: 16`), all under one `groupIds`.
**When to use:** Every hub, link, and satellite box.
**The only difference between the three classes is `backgroundColor` (the role fill) + the role label text — NOT the geometry.** Box offsets are inherited verbatim from `compartmented-box.md`; do not re-derive.
**Typical Data Vault columns (informs example row content):**
- **Hub** — business-key table: `HUB_<biz>_HK` (hash key, PK), the natural business key column(s), `LOAD_DTS`, `RECORD_SRC`.
- **Link** — relationship table: `LINK_<rel>_HK` (PK), two-or-more `HUB_*_HK` foreign hash keys, `LOAD_DTS`, `RECORD_SRC`.
- **Satellite** — descriptive-attribute / history table: parent `HUB_*_HK` or `LINK_*_HK` (FK), `LOAD_DTS` (part of PK — history), `HASH_DIFF`, descriptive attribute columns, `RECORD_SRC`.

### Pattern 2: The 3-role palette + mandatory text role label (the NEW work, SC-2)
**What:** Assign a distinct documented fill per role, AND put a role label on every box, AND add a small legend. The label is what survives grayscale.
- **Fill (role color):** pick three fills from the existing specialist Semantic Color Palette with the WIDEST luminance separation you can get while staying in the documented palette. See the palette table below.
- **Text role label (MANDATORY):** a `«hub»` / `«link»` / `«sat»` stereotype text in/above each box's header (guillemets safe under `fontFamily:3`; ASCII `[HUB]`/`[LINK]`/`[SAT]` is the zero-risk fallback). This is the SC-2-critical element — color is decorative, the label is load-bearing.
- **Legend:** a small `group-container` box (or a 3-row swatch+label strip) naming each role↔color mapping, so a grayscale reader can still decode roles.
**When to use:** Always, for data-vault. Color-alone is forbidden.
**Why:** SC-2 has no automated guard; the label + legend are the deterministic guarantee that the diagram does not collapse to ambiguity when color is removed.

### Pattern 3: Hub spine + satellite attachments via existing flow primitives
**What:** The hub/link "spine" connectors use `kb/fan-out.md` (a hub fanning to its links) and `kb/convergence.md` (≥2 hubs converging into a link). Satellites attach to their parent hub/link via `kb/tree-hierarchy.md` thin (`strokeWidth: 1.5`) elbow connectors (indented), or `kb/fan-out.md` radial spokes.
**Connector rules (LOCKED, same as snowflake/ER):** `endArrowhead: "arrow"` only (plain association — Data Vault relationships are not cardinality-decorated in this scope); `elbowed: true`, `roundness: null`, `roughness: 0`, ≥3 orthogonal points; bind via `startBinding`/`endBinding` to the box **RECTANGLE** ids (never to row texts or `line` dividers — those are not in the anchorable shape set). Endpoint must land within 8px of a rectangle/ellipse/diamond border (`arrow_endpoint_unanchored`).

### Anti-Patterns to Avoid
- **Color-only role distinction** — DISALLOWED (SC-2). Every box needs the text role label; add a legend.
- **Picking three fills with near-identical luminance and no label** — they merge in grayscale. (Most of the existing pale palette fills sit at luminance 0.68–0.89 — close together — which is *exactly* why the label is mandatory, not optional.)
- **Re-deriving box offsets** — use `compartmented-box.md` verbatim.
- **Multi-line single `text` for compartments** — DISALLOWED; breaks dividers + width check.
- **Anchoring connectors to row texts or `line` dividers** — trips `arrow_endpoint_unanchored`; anchor to the box rectangle.
- **Illegal arrowhead token** (`crowsfoot`, `diamond`, `hollow`) — renders silently as a plain line; no error.
- **Copying `star_schema.excalidraw`** — grandfathered, 0 groups, unbound, soft; NOT a template.
- **Soft corners on a formal box** (`roundness: {type:3}`) — boxes are sharp (`roundness: null`); the only intentional rounded rectangle in the family is the use-case system boundary, which does not apply here (an optional outer "Raw Vault" `group-container` MAY be rounded if you choose to scope the vault).
- **Wiring the resolver row before EX-03 passes** — imitating broken ground truth forever (Phase 7/8 Pitfall).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Hub/link/satellite box geometry | A fresh box recipe in `data-vault.md` | `@compartmented-box.md` finalized offsets verbatim | INT-02 mandates ONE construction; re-deriving guarantees drift |
| Hub→link spine connectors | Ad-hoc arrow coordinates | `@kb/fan-out.md` / `@kb/convergence.md` shared-rail elbow geometry | Coordinate math lives only in `kb/` |
| Satellite attachment layout | Custom indent math | `@kb/tree-hierarchy.md` (+60px x / 40px y / thin elbows) | Already the blessed indent pattern (proven on snowflake) |
| Notation encoding | Ad-hoc arrowhead choices | `@notation-conventions.md` legal-token table | DTKB-04; connectors are plain associations |
| Width-fit / overflow detection | Manual eyeball | The frozen `text_overflow_static` formula (`len*0.6*fontSize`) | The deterministic gate; author TO it |
| Pass/fail judgment | A new check script | The frozen `excalidraw_verifier` + visual gate | v1.0 frozen; additive phase |
| Color/contrast enforcement | A new validator color-check | The mandatory text role label + legend + EX-03 visual gate | A color check would touch a frozen component; the label is the robust, additive guarantee |

**Key insight:** Phase 9's whole value is *one new design decision* — a documented, grayscale-safe 3-role palette + label convention — layered onto a fully-proven composition stack. Everything structural is already locked; resist re-opening it. The genuinely novel risk is purely visual (SC-2), and the loop cannot catch it automatically — so the label + legend + the human EX-03 gate ARE the test.

## 3-Role Palette — Recommendation (the distinctive Phase-9 decision)

> This is the one section with real design latitude. SC-2 demands "documented, accessibility-safe, grayscale-distinguishable, NEVER color-alone." The text role label is what makes it grayscale-safe; the fill is decorative reinforcement.

**WCAG relative-luminance of candidate fills from the existing Semantic Color Palette** [VERIFIED: computed this session]:

| Fill | Palette role | Luminance |
|------|--------------|-----------|
| `#3b82f6` | Primary | 0.235 |
| `#60a5fa` | Secondary | 0.363 |
| `#93c5fd` | Tertiary | 0.532 |
| `#fecaca` | Error | 0.676 |
| `#ddd6fe` | AI/LLM | 0.706 |
| `#fed7aa` | Start/Trigger | 0.726 |
| `#a7f3d0` | End/Success | 0.769 |
| `#fee2e2` | Warning | 0.810 |
| `#dbeafe` | Inactive | 0.811 |
| `#fef3c7` | Decision | 0.893 |

**Recommended triad (maximize grayscale spread within the documented palette):**

| Role | Fill | Stroke | Luminance | Role label |
|------|------|--------|-----------|------------|
| **Hub** | `#93c5fd` (Tertiary blue) | `#1e3a5f` | 0.53 (darkest) | `«hub»` |
| **Link** | `#fed7aa` (Start/Trigger amber) | `#c2410c` | 0.73 (mid) | `«link»` |
| **Satellite** | `#fef3c7` (Decision pale-yellow) | `#b45309` | 0.89 (lightest) | `«sat»` |

This triad uses **hue + a ~0.36 luminance spread** (0.53 → 0.73 → 0.89), which is far better grayscale separation than three pale fills clustered at 0.7–0.9. **Even so, the text role label remains mandatory** — luminance ordering helps but is not a guarantee under PNG compression, and SC-2 explicitly forbids color-alone. [ASSUMED — this specific triad is *a* defensible choice from the documented palette; the planner/discuss-phase may pick a different documented triad. The hard requirement is "documented + label + legend + passes the visual grayscale check," not these exact hexes.]

**Mandatory companions to the palette (these satisfy SC-2, not the color):**
1. **Role label on every box** — `«hub»`/`«link»`/`«sat»` (or `[HUB]`/`[LINK]`/`[SAT]` ASCII fallback).
2. **In-canvas legend** — a 3-row swatch+label strip (a `group-container` is ideal) decoding role↔color so a grayscale reader still recovers the mapping.
3. **EX-03 visual gate must explicitly confirm grayscale-distinguishability** — make it a checklist line in the plan's visual-review step.

## Common Pitfalls

### Pitfall 1: SC-2 fails silently — color-only distinction with no role label
**What goes wrong:** Three nicely-colored box classes that, in grayscale (or to a colorblind viewer, or under PNG compression), become indistinguishable — the entire hub/link/satellite semantics collapse. NOTHING in the loop catches this.
**Why it happens:** Color is the "obvious" way to distinguish roles; the label feels redundant when colors look clear on screen.
**How to avoid:** Mandatory `«hub»`/`«link»`/`«sat»` text role label on EVERY box + an in-canvas legend. Treat the label, not the color, as the carrier of role identity. Make grayscale-distinguishability an explicit EX-03 checklist item.
**Warning signs:** A reviewer asks "which one is the hub?"; converting the PNG to grayscale makes two roles look identical; no legend present.

### Pitfall 2: Box width too small → `text_overflow_static` error
**What goes wrong:** Data Vault column names are LONG (`HUB_CUSTOMER_HK`, `LOAD_DTS`, `HASH_DIFF`, `RECORD_SRC`). Box width < `len(longest_row)*0.6*16` → structural `error`, `passed:false`.
**Why it happens:** Eyeballing width; DV hash-key names are longer than typical star/ER columns.
**How to avoid:** Compute `box.width >= max_over_rows(len*0.6*16)`, round UP to the 20-grid (~9.6px/char). `HUB_CUSTOMER_HK  PK` ≈ 19 chars → ≥ 184 → box ≥ 200.
**Warning signs:** `text_overflow_static` with the exact `>=threshold` suggested fix.

### Pitfall 3: Connector anchored to a row text or `line` divider → `arrow_endpoint_unanchored`
**What goes wrong:** A spine or satellite arrow ends on a row `text` or the header `line` divider instead of the box rectangle border → the last point isn't within 8px of a rectangle/ellipse/diamond border → structural `error`.
**Why it happens:** It feels natural to point at the specific FK row; lines/texts are not in the anchorable set.
**How to avoid:** Bind via `startBinding`/`endBinding` to the box **rectangle** id (gap 4), as snowflake/ER do.
**Warning signs:** `arrow_endpoint_unanchored` error; arrow floating off the box at render.

### Pitfall 4: Illegal arrowhead token renders silently as a plain line
**What goes wrong:** `endArrowhead:"crowsfoot"`/`"diamond"` → headless line, no error. (DV connectors should be plain `arrow` anyway, so this is mostly a guard against over-decoration.)
**Why it happens:** Reflex to decorate data-model relationships.
**How to avoid:** `endArrowhead: "arrow"` (or `null`) only. Never invent a token. (No automated check — verified Phase 7.)
**Warning signs:** Connector reads as a bare line in the PNG.

### Pitfall 5: Multi-line text packs rows and silently overflows
**What goes wrong:** Authoring all columns as one `\n`-joined `text`; the widest line overflows undetected and there's no per-row boundary for a divider.
**How to avoid:** One `text` element per row (HARD prohibition). One row string per element.
**Warning signs:** A box with no clean row boundaries; a row poking past the border.

### Pitfall 6: Soft corners / ungrouped boxes
**What goes wrong:** `roundness:{type:3}` on a formal DV box, or omitting `groupIds`, so dividers/label desync.
**How to avoid:** `roundness: null` on box+dividers; one shared `groupIds` per box (frame + dividers + title + role label + every row text). There is no compliant color-semantic template in the repo — author from the recipe + the existing monochrome compliant examples for *structure*, then add the fills.
**Warning signs:** Rounded DV box; moving the box leaves elements behind.

### Pitfall 7: Resolver row wired before EX-03 passes
**What goes wrong:** The `data-vault` row is wired while the example still fails the visual grayscale gate → the agent imitates a broken ground truth forever.
**How to avoid:** EX-01/EX-03 are exit criteria — example passes full validate→render→verify (structural green + EX-03 visual human approval, explicitly including the grayscale check) BEFORE wiring the resolver row. Every prior type followed this.
**Warning signs:** Resolver row marked wired with no verifier pass / no grayscale confirmation on record.

## Code Examples

> Derived from in-repo locked conventions (`compartmented-box.md`, `notation-conventions.md`) and the verified snowflake/ER example structure. Coordinates illustrate the locked formulas; the authoring agent computes exact values.

### Hub box — compartmented box + role fill + mandatory role label
```jsonc
// Box frame — SHARP, grouped, ROLE FILL (hub = #93c5fd). Width sized to longest row.
{ "type":"rectangle","id":"hub_customer_box",
  "x":600,"y":200,"width":260,"height":160,
  "roundness":null,"roughness":0,
  "strokeColor":"#1e3a5f","backgroundColor":"#93c5fd",   // hub role fill
  "groupIds":["grp_hub_customer"] }
// Header divider — full width (x==box.x, points end at box.width)
{ "type":"line","id":"div_hub_customer",
  "x":600,"y":240,"width":260,"height":0,"points":[[0,0],[260,0]],
  "roundness":null,"roughness":0,"strokeColor":"#1e3a5f",
  "groupIds":["grp_hub_customer"] }
// Role label «hub» (MANDATORY — SC-2 carrier). Place in/above header.
{ "type":"text","id":"hub_customer_role","x":612,"y":206,
  "width":60,"height":18,"text":"«hub»","originalText":"«hub»",
  "fontSize":14,"fontFamily":3,"lineHeight":1.25,
  "textAlign":"left","verticalAlign":"top","strokeColor":"#1e3a5f",
  "roundness":null,"groupIds":["grp_hub_customer"] }
// Title (bound via containerId is safest — skipped by text_overflow_static)
{ "type":"text","id":"hub_customer_title","x":612,"y":222,
  "width":160,"height":20,"text":"HUB_CUSTOMER","originalText":"HUB_CUSTOMER",
  "fontSize":16,"fontFamily":3,"lineHeight":1.25,
  "textAlign":"left","verticalAlign":"top","strokeColor":"#1e1e1e",
  "roundness":null,"groupIds":["grp_hub_customer"] }
// Rows — one text per column, shared left x = box.x+12, pitch 20
{ "type":"text","id":"hub_customer_r1","x":612,"y":250,
  "width":220,"height":20,"text":"CUSTOMER_HK     PK","originalText":"CUSTOMER_HK     PK",
  "fontSize":16,"fontFamily":3,"lineHeight":1.25,
  "textAlign":"left","verticalAlign":"top","strokeColor":"#1e1e1e",
  "roundness":null,"groupIds":["grp_hub_customer"] }
// …CUSTOMER_BK, LOAD_DTS, RECORD_SRC as further rows at y += 20 each.
// Width rule: "CUSTOMER_HK     PK" ~18 chars -> 18*9.6=172.8 -> width >= 180; 260 is safe.
```
Link box = identical structure with `backgroundColor:"#fed7aa"`, `«link»` label, rows = `LINK_*_HK PK` + the referenced `HUB_*_HK` FKs + `LOAD_DTS` + `RECORD_SRC`.
Satellite box = `backgroundColor:"#fef3c7"`, `«sat»` label, rows = parent `*_HK FK` + `LOAD_DTS PK` + `HASH_DIFF` + descriptive attrs + `RECORD_SRC`.

### Spine + satellite connectors (plain association, anchored to rectangles)
```jsonc
// Hub -> Link spine (fan-out / convergence geometry), plain arrow, bound to RECTANGLES:
{ "type":"arrow","id":"sp_cust_link","elbowed":true,"roundness":null,"roughness":0,
  "points":[[0,0],[80,0],[80,40]],"strokeColor":"#1e3a5f","strokeWidth":2,
  "endArrowhead":"arrow","startArrowhead":null,
  "startBinding":{"elementId":"hub_customer_box","focus":0,"gap":4},
  "endBinding":{"elementId":"link_order_box","focus":0,"gap":4} }
// Satellite attachment (tree-hierarchy indent), THIN elbow, bound to RECTANGLES:
{ "type":"arrow","id":"sat_cust_attach","elbowed":true,"roundness":null,"roughness":0,
  "points":[[0,0],[0,32],[48,32]],"strokeColor":"#1e3a5f","strokeWidth":1.5,
  "endArrowhead":"arrow","startArrowhead":null,
  "startBinding":{"elementId":"hub_customer_box","focus":0,"gap":4},
  "endBinding":{"elementId":"sat_customer_box","focus":0,"gap":4} }
```

### Legend (grayscale-safety guarantee — a small group-container with 3 swatch rows)
```jsonc
// Outer legend box (group-container; a swatch rectangle + label per role).
{ "type":"rectangle","id":"legend_box","x":100,"y":600,"width":220,"height":120,
  "roundness":{"type":3},"roughness":0,"strokeColor":"#1e3a5f",
  "backgroundColor":"transparent","strokeWidth":2 }
{ "type":"rectangle","id":"sw_hub","x":120,"y":620,"width":24,"height":24,
  "roundness":null,"roughness":0,"strokeColor":"#1e3a5f","backgroundColor":"#93c5fd" }
{ "type":"text","id":"lbl_hub","x":156,"y":622,"width":140,"height":20,
  "text":"Hub","originalText":"Hub","fontSize":16,"fontFamily":3,
  "lineHeight":1.25,"textAlign":"left","verticalAlign":"top","strokeColor":"#1e1e1e" }
// repeat swatch+label for Link (#fed7aa) and Satellite (#fef3c7) at y += 32.
```

**Minimum required text-element fields** (omitting width/height triggers `text_missing_dimensions`):
`type, x, y, width, height, text, originalText, fontSize, fontFamily:3, lineHeight:1.25, textAlign, verticalAlign, strokeColor, roundness, groupIds`.

## State of the Art

Not a moving ecosystem — a closed, pinned authoring environment. The only relevant "state" change is internal to the project:

| Old Approach | Current Approach (Phase 9) | When Changed | Impact |
|--------------|----------------------------|--------------|--------|
| Compliant data-model boxes are monochrome (transparent fill, dark stroke) | Data-vault boxes carry a *semantic fill* per role + mandatory text label | Phase 9 (first color-semantic data-model type) | First time fill color encodes meaning in a data-model recipe; SC-2 governs it |
| Color distinction "would just be color" | Color + mandatory text role label + legend (grayscale-safe) | Phase 9 | SC-2 satisfied without a (forbidden) renderer/verifier change |
| Glyph/notation gaps caught only by visual review | Same — plus the new SC-2 grayscale check is also visual-only | Phase 9 | No automated color guard; visual gate is load-bearing (as with arrowhead legality, Phase 7) |

**Deprecated/outdated:**
- `examples_excalidraw/star_schema.excalidraw` — grandfathered legacy; NOT a template (carried from Phase 4/6).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The recommended hub/link/satellite triad (`#93c5fd`/`#fed7aa`/`#fef3c7`) is *a* defensible documented-palette choice; the exact hexes are discretionary | 3-Role Palette | LOW — any documented triad + mandatory label + legend that passes the grayscale visual gate satisfies SC-2; these are a concrete, luminance-separated starting point |
| A2 | `«hub»`/`«link»`/`«sat»` guillemet stereotypes render correctly under `fontFamily:3` (Cascadia) | Patterns / Code | LOW — confirmed for class-diagram `«interface»` in Phase 7 (A1); ASCII `[HUB]`/`[SAT]` is the zero-risk fallback if they ever tofu |
| A3 | A `«…»` role label + an in-canvas legend is sufficient to pass the EX-03 grayscale-distinguishability judgement | Pattern 2 / SC-2 | MEDIUM — this is the SC-2 crux and is judged by the visual gate, not automated; must be confirmed empirically in the render+review pass. If a reviewer still can't distinguish roles in grayscale, strengthen labels (e.g. a header role band) |
| A4 | The reserved resolver composition list (group-container, fan-out, tree-hierarchy, convergence, evidence-card) is the right set; the recipe honors it | File Structure / resolver | LOW — if the example uses a subset (e.g. fan-out + tree-hierarchy only), update the resolver row's composition list to match what is actually composed |
| A5 | Standard Data Vault column conventions (HK/BK/LOAD_DTS/RECORD_SRC/HASH_DIFF) are the right row content for a recognizable example | Pattern 1 | LOW — these are the canonical Data Vault 2.0 raw-vault columns; example fidelity is about being recognizable, and the loop only checks width/structure, not DV correctness |

## Open Questions (RESOLVED)

1. **Exact 3-role palette — adopt the recommended triad or pick another documented triad?**
   - RESOLVED: hub `#93c5fd` / link `#fed7aa` / satellite `#fef3c7` — encoded as HARD RULE in 09-01-PLAN.md Task 2 action (e). Grayscale-sufficiency confirmed at EX-03 visual gate.

2. **Role label form — guillemet stereotype `«hub»` vs. ASCII `[HUB]` vs. header role band?**
   - RESOLVED: `«hub»`/`«link»`/`«sat»` guillemet form (consistent with class-diagram stereotype convention; safe under `fontFamily:3`). ASCII fallback if tofu appears. Encoded in 09-01-PLAN.md Task 2 action (e).

3. **Satellite attachment layout — `tree-hierarchy` (indented) or `fan-out` (radial)?**
   - RESOLVED: `tree-hierarchy` thin elbows for satellite attachments (reads as "belongs to the hub"). Encoded in 09-01-PLAN.md Task 2 action (d), step 5.

## Environment Availability

This phase is authoring (JSON + Markdown) plus running the existing frozen loop — the same toolchain that shipped Phases 5–8.

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `python3` (validator + structural verifier) | validate + structural checks | Assumed ✓ (used through Phases 1–8) | system | none needed |
| Docker / `render_docker.sh` | Phase-2 PNG render | Assumed ✓ (use-case rendered 2026-06-08) | — | `render_excalidraw.py` direct path exists |
| `@excalidraw/excalidraw@0.17.3` via esm.sh CDN | render engine | Assumed ✓ (frozen render path) | 0.17.3 | none (HARD-01 vendoring deferred to v2) |

**Missing dependencies with no fallback:** None identified — the render+verify toolchain is the same one that shipped every prior v1.1 type. The render path depends on the esm.sh CDN (HARD-01 deferred); if the CDN is unreachable at execution time, rendering blocks — the same risk all prior phases carried. Confirm Docker render availability at execution time (only way to produce the EX-03 ground-truth PNG).

## Validation Architecture

> `nyquist_validation: true` in `.planning/config.json` — section included. This project's "tests" are the validate→render→verify loop, not a unit-test framework.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | The frozen v1.0 loop (no pytest/jest) — `validate_and_render.sh` + `excalidraw_verifier` (`verifier_structural.py` + multimodal visual review) |
| Config file | none (script-driven) |
| Quick run command | `python3 .claude/agents/excalidraw/scripts/verifier/verifier_structural.py <file.excalidraw>` (structural only, sub-second, no render) |
| Full suite command | `bash .claude/agents/excalidraw/scripts/render/validate_and_render.sh <file.excalidraw>` then read the PNG + invoke `excalidraw_verifier` and assert `passed:true` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | Check Exists? |
|--------|----------|-----------|-------------------|---------------|
| DM-04 / SC-1 | data-vault example renders; boxes fit; connectors anchored/elbow; legal arrowheads | structural + visual | `validate_and_render.sh data_vault_<subject>.excalidraw` + verifier `passed:true` | ✅ structural (overflow, missing-dims, unanchored-arrow, not-elbow, fontfamily) |
| DM-04 / SC-2 | hub/link/satellite distinguishable IN GRAYSCALE; never color-alone; role label + legend present | **visual only** | EX-03 visual gate: review PNG, AND review a grayscale conversion, confirm 3 roles still readable | ❌ Wave 0 — NO automated check (color is unguarded); manual/visual gate is the test |
| SC-2 (label) | every box carries a `«hub»`/`«link»`/`«sat»` role label | structural-ish | grep each box group for a role-label text; assert 3 distinct labels present | ❌ Wave 0 — optional throwaway grep; verifier does not check this |
| SC-3 / EX-01 | canonical pair indexed in resolver, pointing at the new PNG | structural | grep `diagram-types/README.md` resolver for the wired data-vault row + back-refs on composed kb files | ❌ Wave 0 (after example passes) |

### Sampling Rate
- **Per task commit:** `verifier_structural.py <file>` (sub-second structural gate) + eyeball the PNG.
- **Per example completion:** full `validate_and_render.sh` + visual verifier pass, **including a grayscale-distinguishability review** (the SC-2 judge).
- **Phase gate:** the canonical example passes the full loop (structural green + EX-03 visual human approval *with explicit grayscale confirmation*) BEFORE the resolver row is wired.

### Wave 0 Gaps
- [ ] `examples_excalidraw/data_vault_<subject>.excalidraw` — the canonical source (DM-04). Must not exist before authoring.
- [ ] `examples/data_vault_<subject>.png` — rendered ground truth.
- [ ] **Grayscale-distinguishability review step** — there is NO automated color check; add an explicit manual/visual checklist line ("convert PNG to grayscale; confirm hub/link/satellite still readable via label + luminance"). This is the one SC-2 gap the frozen loop cannot catch.
- [ ] (Optional) a throwaway grep asserting each box group contains exactly one role-label text from `{«hub»,«link»,«sat»}` — the verifier does not check this.
- [ ] No framework install needed — the loop is the existing frozen toolchain.

> **Note:** The frozen verifier covers overflow, missing dimensions, arrow anchoring, elbow-ness, monospace, roughness, emoji. It does NOT enforce SC-2's color/grayscale distinction, the role-label presence, the "no multi-line text" prohibition, or divider full-width spanning — those are geometric/semantic authoring rules judged by visual review + discipline.

## Security Domain

> `security_enforcement` is absent from `.planning/config.json` (treated as enabled by default), but this phase has **no attack surface**: it authors static Markdown + `.excalidraw` JSON consumed only by the local render/verify toolchain. No auth, no network input handling, no user-supplied code execution introduced — identical posture to Phases 6–8.

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V5 Input Validation | marginal | The verifier already treats `.excalidraw` text as DATA, never instructions (prompt-injection-resistant by design — `excalidraw_verifier.md` `<role>`). Phase 9 introduces no new untrusted input path. |
| V2/V3/V4/V6 | no | No auth, session, access-control, or cryptography surface in a KB-authoring phase. |

### Known Threat Patterns for this stack
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Diagram-text prompt injection (e.g., a label saying "ignore instructions") | Tampering | Already mitigated: verifier `<role>` mandates treating file content as data only — do not regress this when authoring example text. |

## Sources

### Primary (HIGH confidence — read in full / introspected this session)
- `.claude/agents/excalidraw/diagram-types/compartmented-box.md` — finalized parametric offsets + HARD prohibition + alignment rules
- `.claude/agents/excalidraw/diagram-types/notation-conventions.md` — legal arrowhead set, silent-failure rule, committed encodings
- `.claude/agents/excalidraw/diagram-types/README.md` — resolver table (reserved data-vault row + composition list), two-layer rule, add-a-type procedure, legacy grandfathering
- `.claude/agents/excalidraw/diagram-types/snowflake-schema.md` + `use-case.md` — most recent TYPE-file structures to mirror (compose-by-reference, ground-truth section)
- `.claude/agents/excalidraw/excalidraw_specialist.md` — Semantic Color Palette + Text Hierarchy + Brand Stroke Colors (the documented palette to draw the 3-role fills from); Rule 7 text-dimension requirement
- `.claude/agents/excalidraw/scripts/verifier/verifier_structural.py` — verified: 10 checks, **none color/contrast/palette related**
- `.claude/agents/excalidraw/kb/{fan-out,tree-hierarchy,convergence,group-container,evidence-card}.md` — composed primitives + back-ref convention (`> Used by types:`)
- `examples_excalidraw/{star_schema_v2,snowflake_schema,er_retail_orders,class_order_domain}.excalidraw` — color introspection (all monochrome: transparent fills, `#1e3a5f`/`#1e1e1e` strokes) confirming no color-semantic precedent
- `.planning/{ROADMAP,REQUIREMENTS,STATE}.md` + `.planning/config.json` — Phase 9 scope, DM-04, SC-1/2/3, locked decisions, nyquist/security flags
- Phase 6 (`06-RESEARCH.md`) and Phase 7 (`07-RESEARCH.md`) — table-box recipe + relationship/connector precedent and pitfall corpus (reused verbatim where applicable)

### Secondary (MEDIUM confidence)
- WCAG relative-luminance computation of palette fills — computed this session to ground the grayscale-separation recommendation (standard WCAG formula; the *application* to SC-2 is the design judgement, confirmed only by the visual gate).

### Tertiary (LOW confidence)
- None. No external web sources were needed or would supersede the in-repo frozen toolchain. Data Vault 2.0 column conventions (HK/BK/HASH_DIFF/LOAD_DTS/RECORD_SRC) are standard domain knowledge used only to make the example recognizable; the loop does not validate DV semantics. [ASSUMED — A5]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — every component read directly; no packages added; identical toolchain to Phases 6–8.
- Architecture / box+connector composition: HIGH — reuses locked, already-shipped primitives verbatim; mirrors the snowflake/ER recipe exactly.
- 3-role palette (the new surface): MEDIUM — the *requirement* and the *mechanism* (fill + mandatory label + legend) are HIGH-confidence; the *exact triad* and its grayscale-sufficiency are a design choice judged by the EX-03 visual gate, not automation (A1/A3).
- Pitfalls: HIGH — derived from the actual verifier checks (read this session) + the documented prohibitions + the verified absence of any color guard.

**Research date:** 2026-06-08
**Valid until:** Stable indefinitely while the v1.0 loop stays frozen (no external/fast-moving deps). Re-check only if `verifier_structural.py`, the specialist Semantic Color Palette, or the Excalidraw `0.17.3` pin changes.
