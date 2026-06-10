# Excalidraw Specialist — Self-Verifying Diagram Authoring

## What This Is

A Claude Code subagent plugin that authors professional Excalidraw diagrams in the
"Architect's Precision" style. The plugin operates as a closed-loop self-verifying
authoring agent organized around four real-world diagram families (Tech Architecture,
Data Modeling, UML / SW-Engineering, Flow / Process): every diagram is rendered to PNG,
inspected by a dedicated `excalidraw_verifier` subagent, and auto-fixed up to 3
iterations before delivery. A `diagram-types/` knowledge layer guides the agent to draw
each family correctly — using the right primitives, conventions, and canonical examples
— without touching the v1.0 verify loop.

## Core Value

**Every diagram the agent delivers has been rendered, inspected, and confirmed visually
correct using the right drawing conventions for its type.** No more silent broken
diagrams. If verification fails after 3 attempts, the user sees the failed PNG, the
structured issue list, and the source JSON — never a "done" message hiding broken output.

## Current State: v1.1 Shipped (2026-06-09)

**Shipped in v1.1:**
- `/excalidraw` two-tier family/type picker (4 families → type sub-pick)
- `diagram-types/` KB layer with 10 type recipe files + authoritative resolver table
- Data modeling: star schema, snowflake, ER, data vault (+ canonical examples)
- UML core 4: sequence, class, use-case, activity (+ canonical examples)
- Shared primitives: notation-conventions, compartmented-box, relationship-endpoint, lifeline-activation

**Codebase state:**
- Agent files: `.claude/agents/excalidraw/` (specialist, verifier, icon fetcher, 10 diagram-type recipes, 15+ kb primitives)
- Canonical examples: 10 type pairs in `examples/` + `examples_excalidraw/` (all loop-verified)
- Icon library: 73+ PNGs in `icons/`
- Render pipeline: Python + Docker + Playwright + Chromium; `validate_and_render.sh`

## Requirements

### Validated

- ✓ Subagent definition with inlined visual standards (`excalidraw_specialist.md`) — existing pre-v1.0
- ✓ Pattern KB across Macro/Flow/Decision/Structure categories (`kb/*.md`, 15+ patterns) — v1.0 + v1.1
- ✓ Brand-icon library (`icons/`, 73+ PNGs) discoverable via `Glob` — existing pre-v1.0
- ✓ Canonical reference PNGs (`examples/*.png`) used as visual ground truth — v1.1
- ✓ Excalidraw MCP integration (`mcp__excalidraw__*`, 5 tools) — existing pre-v1.0
- ✓ Offline render pipeline: validator + Docker + Playwright + Chromium + `esm.sh` Excalidraw bundle — existing pre-v1.0
- ✓ Static JSON validator with rules: metadata, no `label` field on shapes, text/contrast warnings — existing pre-v1.0
- ✓ Mandatory render-and-verify loop — v1.0
- ✓ Verifier subagent (`excalidraw_verifier`) with structural pre-check + visual PNG review — v1.0
- ✓ Structured verifier pass/fail report (5-key issue objects) — v1.0
- ✓ Auto-fix loop with 3-iteration cap — v1.0
- ✓ Emoji policy: raw Unicode → `icons/` PNG mapping — v1.0
- ✓ Iteration artefact discipline (overwrite, not accumulate) — v1.0
- ✓ Two-tier family/type picker in `/excalidraw` — v1.1
- ✓ `diagram-types/` KB layer with authoritative resolver table — v1.1
- ✓ Notation workaround conventions (compartmented-box, relationship-endpoint glyphs) — v1.1
- ✓ 10 diagram types with canonical example pairs passing the full loop — v1.1

### Active

<!-- Next milestone — hypotheses until shipped. -->

- [ ] **UMLX-01**: Remaining UML types beyond the core 4 (state machine, component, deployment, object, package, communication, timing, composite-structure, profile, interaction-overview)
- [ ] **HARD-01**: Vendor the `@excalidraw/excalidraw@0.17.3` JS bundle into the Docker image (remove CDN dependency on `esm.sh`)
- [ ] **HARD-02**: Clean up `icons/` (collapse 8 Databricks variants; remove non-icon PNGs)
- [ ] **HARD-03**: Sandbox path resolver in `render_excalidraw.py`
- [ ] **HARD-04**: SDK-driven E2E harness that spawns the specialist subagent and validates the loop without an operator

### Out of Scope

| Feature | Reason |
|---------|--------|
| Native crow's-foot / hollow-triangle / diamond arrowheads | Not in the `0.17.3` arrowhead enum; composed-glyph/textual workarounds used instead |
| Multi-tool diagram support (Mermaid, draw.io, PlantUML) | Plugin stays Excalidraw-specific |
| Pixel-diff visual regression against `examples/*.png` | Verifier judges per-diagram correctness, not stylistic similarity |
| Auto-generating diagrams from source code / schemas | This plugin is about drawing conventions + KB, not reverse-engineering inputs |
| Changing the render→verify→fix loop, validator, or verifier internals | v1.0 loop is frozen; additions must be additive |

## Context

- **Plugin state:** brownfield. Two shipped milestones. v1.0 closed the render-verify gap; v1.1 added diagram families and type-aware drawing conventions.
- **Tech stack:** Claude Code subagent runtime (Markdown + YAML frontmatter; tools: Read, Bash, Grep, Glob, MCP). Render pipeline: Python 3.11 + uv + Playwright + Chromium inside Docker.
- **Known tech debt:** `star_schema.excalidraw` legacy file alongside compliant `star_schema_v2.*`; CDN dependency on `esm.sh` for the Excalidraw bundle; `icons/` has 8 Databricks variants + non-icon PNGs.
- **Outstanding operator work:** interactive smoke test for Phase 4 Plan 03 (structural verification passed; human run awaiting); 06/09-VERIFICATION.md human-needed sign-offs deferred.

## Constraints

- **Tech stack:** Claude Code subagent runtime. Render pipeline: Python + Docker. No new external host dependencies.
- **Performance:** auto-fix loop hard-capped at 3 iterations. Budget verifier prompt + PNG to stay under typical Sonnet/Opus context.
- **Compatibility:** must not break `excalidraw_specialist.md` behavior for direct callers.
- **No assumption of git history:** verifier cannot rely on diff-against-prior-version.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Separate verifier subagent (not self-review) | Fresh eyes reduce confirmation bias; cleaner concerns | ✓ Good — v1.0 shipped |
| Both structural + visual checks | Structural catches cheap defects without vision tokens | ✓ Good — v1.0 shipped |
| 3-iteration auto-fix cap | Balances self-heal with cost ceiling | ✓ Good — v1.0 shipped |
| Always-render policy (no opt-out) | Closes the "forgot to render" failure mode | ✓ Good — v1.0 shipped |
| Replace emojis with `icons/` PNGs | Consistent with existing brand-icon strategy; avoids font switch | ✓ Good — v1.0 shipped |
| Overwrite artefacts each iteration | Keeps directory clean; agent has iteration history in context | ✓ Good — v1.0 shipped |
| `diagram-types/` as sibling of `kb/` | Clear two-layer separation: type files compose primitives | ✓ Good — v1.1 shipped |
| One authoritative resolver table | No duplicated mapping that could drift | ✓ Good — v1.1 shipped |
| EX-02 Option B (grandfather star_schema.excalidraw) | Avoid breaking existing references; document reason; ship compliant v2 | ✓ Good — star_schema_v2 shipped, legacy preserved |
| Compartmented-box: per-row text elements | Dividers stay placeable; verifier width-fit check stays valid | ✓ Good — v1.1 shipped |
| Lifeline pixel geometry: ASSUMED from RESEARCH A1 | No authoritative spec; best-effort values; monotonic-Y deferred | ⚠️ Revisit — pixel values may need calibration against real renders |
| center-x verifier check added | Catches off-center activation bars early | ✓ Good — no false-positives in regression |
| Data vault role labels: guillemet form | Small superscript `«hub»/«link»/«sat»` avoids title overlap; grayscale-safe | ✓ Good — SC-2 confirmed |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-06-09 after v1.1 milestone*
