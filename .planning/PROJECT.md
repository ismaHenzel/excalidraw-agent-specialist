# Excalidraw Specialist — Self-Verifying Diagram Authoring

## What This Is

A Claude Code subagent plugin that authors professional Excalidraw diagrams in the
"Architect's Precision" style. This milestone evolves the plugin from "generate `.excalidraw`
JSON and hope it renders correctly" to a **closed-loop self-verifying authoring agent**:
every diagram is always rendered to PNG via the existing validate-and-render pipeline,
then visually + structurally inspected by a dedicated verifier subagent before it is
delivered. When defects are found (text overflow, broken arrow anchors, missing icons,
emojis rendering as boxes), the main agent fixes the JSON and re-renders — up to 3
iterations.

## Core Value

**Every diagram the agent delivers has been rendered, inspected, and confirmed visually
correct.** No more silent broken diagrams. If verification fails after 3 attempts, the
user sees the failed PNG, the structured issue list, and the source JSON — never a
"done" message hiding broken output.

## Current Milestone: v1.1 Diagram Families & UML Expansion

**Goal:** Reorganize the plugin around recognizable real-world diagram families and add a
diagram-type knowledge layer so the agent draws UML, data models, and tech architectures
correctly — without disturbing the self-verifying loop shipped in v1.0.

**Target features:**
- **Family-based taxonomy** — replace the vague Q1 kinds with four recognizable families:
  Tech Architecture, Data Modeling, UML / SW Engineering, and Flow / Process. The
  `/excalidraw` Q1 picks a family; a follow-up sub-pick selects the specific type when the
  family has many (UML → sequence/class/use-case/activity; Data Modeling →
  star/snowflake/data-vault/ER).
- **New `diagram-types` KB layer** — a second KB directory, one file per diagram *type*, each
  explaining purpose (what it's for), how to draw it, and which existing layout sub-patterns
  it composes. The existing `kb/` layout-pattern files remain the primitive layer this new
  layer references.
- **UML core 4** — diagram-type entries + drawing conventions for sequence, class, use-case,
  and activity diagrams (sourced from the Creately reference). Remaining UML types deferred.
- **Data Modeling types** — diagram-type entries for star schema, snowflake, data vault, and
  ER, building on the existing `example_star_schema.png`.
- **Tech Architecture family** — reframe the existing architecture/overview material as the
  Tech Architecture family entry (technologies, services, clouds + their relationships).
- **Reference examples** — one canonical `.excalidraw` + rendered PNG per new family/type as
  visual ground truth, added to `examples/` and indexed in the KB.
- **Wire it into the loop** — update `excalidraw_specialist` and `/excalidraw` so
  family/type selection drives which KB files and example PNGs get consulted. The render →
  verify → fix loop itself is untouched.

**Key context:**
- Brownfield on top of v1.0 (self-verifying loop, 100% shipped).
- The existing KB sub-patterns (fan-out, decision-branch, group-container, etc.) become
  composable sub-patterns *inside* the new diagram-type families, not top-level choices.
- `AskUserQuestion` caps at 4 options, so the family/type picker is two-tier (family, then
  type) rather than one flat list.

## Requirements

### Validated

<!-- Inferred from .planning/codebase/ARCHITECTURE.md and STACK.md — already shipping. -->

- ✓ Subagent definition with inlined visual standards (`excalidraw_specialist.md`) — existing
- ✓ Pattern KB across Macro/Flow/Decision/Structure categories (`kb/*.md`, 13 patterns) — existing
- ✓ Brand-icon library (`icons/`, 73 PNGs) discoverable via `Glob` — existing
- ✓ Canonical reference PNGs (`examples/*.png`) used as visual ground truth — existing
- ✓ Excalidraw MCP integration (`mcp__excalidraw__*`, 5 tools) — existing
- ✓ Offline render pipeline: validator + Docker + Playwright + Chromium + `esm.sh` Excalidraw bundle — existing
- ✓ Static JSON validator with rules: metadata, no `label` field on shapes, text/contrast warnings — existing

### Active

<!-- This milestone — building toward these. Hypotheses until shipped. -->

- [ ] **Mandatory render-and-verify loop:** Every diagram generation MUST end by invoking
  `scripts/validate_and_render.sh` to produce a sibling PNG, then handing off to the
  verifier subagent. No "JSON-only" delivery path.
- [ ] **Verifier subagent (`excalidraw_verifier`)** living at
  `.claude/agents/excalidraw/excalidraw_verifier.md`. Performs:
    - **Structural pre-check** of the `.excalidraw` JSON (cheap, no vision tokens):
      arrow endpoints land on element borders; text width fits container width given
      monospace metrics; image `file_path` resolves; no raw emoji in `text` elements
      that use `fontFamily: 3`.
    - **Visual review** of the rendered PNG via multimodal Read: text overflow at render
      time, arrows visibly connecting, icons present and not blank, no missing-glyph
      boxes, overall layout coherence vs. the matching `examples/*.png`.
- [ ] **Structured verifier output:** verifier returns a pass/fail report — e.g.
  `{ passed: false, issues: [ { check: "text_overflow", element_id: "...", severity: "error", detail: "...", suggested_fix: "..." } ] }` —
  that the main agent can parse and act on programmatically.
- [ ] **Auto-fix loop with 3-iteration cap:** generate → render → verify → fix → render → verify → fix → render → verify.
  On the 3rd failure, surface the issues + last PNG + source JSON to the user.
- [ ] **Emoji policy:** raw Unicode emoji codepoints in `text` elements are forbidden
  (they render as boxes under `fontFamily: 3`). When the user requests an emoji, the
  agent maps it to a PNG from `icons/` and uses an `image` element. Pre-check enforces
  the ban; visual check catches anything that slipped through.
- [ ] **Iteration artefact discipline:** the latest PNG and verifier report sit as
  siblings of the `.excalidraw` file and are overwritten each iteration. No versioned
  history clutter; the source `.excalidraw` is the only versioned artefact.

### Out of Scope

- **Vendoring the `@excalidraw/excalidraw@0.17.3` JS bundle into the Docker image** —
  CDN dependency is a real risk ([[CONCERNS.md#2]]) but separate concern; defer to a
  hardening milestone.
- **Icon-library cleanup** (8 Databricks variants, non-icon PNGs mixed in) — separate
  hardening concern ([[CONCERNS.md#9-10]]); affects visual quality only marginally.
- **Sandboxing the path resolver** in `render_excalidraw.py` — security hardening
  ([[CONCERNS.md#5]]); orthogonal to verification.
- **Multi-tool diagram support (Mermaid, draw.io, etc.)** — this plugin stays
  Excalidraw-specific. The verifier subagent is named `excalidraw_verifier`, not a
  generic `diagram_verifier`.
- **Pixel-diff visual regression against `examples/*.png`** — the verifier judges
  per-diagram correctness, not stylistic similarity to canonical references. The
  examples remain visual ground truth for the *generator*, not a test oracle for the
  verifier.
- **CI/automated harness running the verifier on every change to the plugin** — no
  test infrastructure to build on (no git history of diagrams, no fixture suite); revisit
  after the verifier is shipped.
- **Replacing the existing static `excalidraw_validator.py`** — the new structural
  pre-check augments it; both can coexist.

## Context

- **Plugin state:** brownfield. A complete Excalidraw subagent already exists at
  `.claude/agents/excalidraw/` with agent definition, pattern KB, icons, examples, and
  the validate+render scripts. See `.planning/codebase/` for the full map.
- **Where the gap is:** the agent's operational mandate #7 says "use
  `mcp__excalidraw__create_view` to verify the visual result and fix overlaps or layout
  issues before finalizing" — but that's MCP-canvas verification, not the Docker-rendered
  PNG that users actually receive. Today an agent can declare "done" and the PNG can
  still be broken (text overflow, blank icons, emoji boxes). This milestone closes that gap.
- **Render path already exists:** `scripts/validate_and_render.sh` runs
  validator → Docker render → instructional "now look at the PNG" line. The new loop
  treats Phase 3 (visual analysis) as a real verifier subagent, not a print statement.
- **Multimodal capability:** the verifier subagent will `Read` the rendered PNG; Claude
  Code's `Read` tool natively supplies image content to the multimodal model, so no
  separate vision pipeline is needed.
- **Subagent discovery:** multiple agent files can co-exist under
  `.claude/agents/excalidraw/`; agent identity is established by the `name:` field in
  YAML frontmatter, not by directory layout. The verifier ships as a peer of
  `excalidraw_specialist.md`.

## Constraints

- **Tech stack:** Claude Code subagent runtime (Markdown + YAML frontmatter; tools:
  Read, Bash, Grep, Glob, MCP). Render pipeline is Python 3.11 + uv + Playwright +
  Chromium inside Docker.
- **Performance:** auto-fix loop is hard-capped at 3 iterations. Each iteration cost
  is one Docker render (~10–20s wall-clock) + verifier subagent turn (~vision tokens
  for the PNG). Budget the verifier prompt + PNG to stay under a typical Sonnet/Opus
  context.
- **Compatibility:** must not break existing `excalidraw_specialist.md` behaviour for
  callers who invoke it directly. The mandatory render-and-verify is enforced inside
  the agent's operational flow, not by external orchestration.
- **No new external dependencies on host:** continues to require Docker, bash, and the
  Excalidraw MCP server (`excalidraw/excalidraw-mcp`). No npm, no Python on host beyond
  what `scripts/validate_and_render.sh` already uses.
- **No assumption of git history:** repo was just initialized; verifier cannot rely on
  diff-against-prior-version for any check.
- **Self-contained plugin:** the verifier subagent lives inside
  `.claude/agents/excalidraw/`, ships with the rest of the plugin, and discovers assets
  via the same relative-path convention used by `excalidraw_specialist.md`.

## Key Decisions

<!-- Decisions made during questioning that constrain future work. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Separate verifier subagent (not self-review by main agent) | Fresh eyes reduce confirmation bias on visual inspection; cleaner concerns; verifier prompt can specialize | — Pending |
| Both structural + visual checks (not vision-only, not structural-only) | Structural catches cheap defects (raw emoji, unresolved icon paths) without burning vision tokens; visual catches what JSON parse can't see (actual render overflow, glyph boxes) | — Pending |
| 3-iteration auto-fix cap | Balances "let the agent self-heal" with cost ceiling; surfaces stubborn diagrams to the human instead of looping forever | — Pending |
| Always-render policy (no opt-out) | The verifier is only meaningful if a PNG always exists; removing the opt-out closes the "I forgot to render" failure mode | — Pending |
| Replace emojis with `icons/` PNGs (not switch fonts) | Switching `fontFamily` mid-diagram breaks the Architect's Precision monospace standard; icon mapping is consistent with the existing brand-icon strategy | — Pending |
| Overwrite artefacts each iteration (no versioning) | Keeps the user's directory clean; only the source `.excalidraw` and final PNG persist; the agent has the iteration history in its context | — Pending |
| Verifier subagent lives at `.claude/agents/excalidraw/excalidraw_verifier.md` | Self-contained plugin; ships alongside the specialist; same relative-asset-path convention | — Pending |
| Structured pass/fail JSON-ish report from the verifier | Main agent parses and acts programmatically; less re-interpretation drift than a markdown narrative | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-03 — started milestone v1.1 (Diagram Families & UML Expansion)*
