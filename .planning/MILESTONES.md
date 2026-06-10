# Milestones

## v1.0 — Self-Verifying Loop

**Shipped:** 2026-05-24
**Phases:** 1–3 | **Plans:** 5

Delivered the closed-loop self-verifying authoring agent: every diagram is rendered to PNG, inspected by a dedicated `excalidraw_verifier` subagent, and auto-fixed up to 3 iterations before delivery. Broken diagrams surface the issues + failed PNG + source JSON — never a silent "done".

**Key accomplishments:**
- Standalone `excalidraw_verifier` subagent with structural pre-check + visual PNG review
- Mandatory render→verify→fix loop in specialist (always-render policy, 3-iteration cap)
- Emoji → `icons/` PNG policy; artefact overwrite discipline
- End-to-end validation on representative defect cases (self-heal + honest-failure confirmed)

**Archive:** `.planning/milestones/v1.0-ROADMAP.md` *(not separately archived — v1.0 phases retained inline in ROADMAP.md before v1.1 archival)*

---

## v1.1 — Diagram Families & UML Expansion

**Shipped:** 2026-06-09
**Phases:** 4–9 | **Plans:** 19 | **Duration:** 7 days (2026-06-03 → 2026-06-09)

Reorganized the plugin around four real-world diagram families (Tech Architecture, Data Modeling, UML / SW-Engineering, Flow / Process) and a new `diagram-types/` KB layer. All 10 diagram types ship with canonical examples passing the full validate→render→verify loop. The v1.0 loop is untouched.

**Key accomplishments:**
1. Two-tier family/type picker in `/excalidraw` — single authoritative resolver table (no drift)
2. `diagram-types/` KB layer with 10 type recipes composing existing `kb/` primitives with bidirectional back-refs
3. Data modeling: star schema, snowflake, ER, data vault — all loop-verified canonical examples
4. UML core 4: sequence, class, use-case, activity — all loop-verified canonical examples
5. Shared primitives built once: notation-conventions, compartmented-box, relationship-endpoint, lifeline-activation
6. End-to-end regression: 7/8 wired examples `issues == []`; use_case_checkout exit 0 (pre-existing warnings)

**Known deferred items at close:** 3 (see STATE.md Deferred Items — UAT gap + 2 human-needed verification gaps, all acknowledged)

**Archive:** `.planning/milestones/v1.1-ROADMAP.md`, `.planning/milestones/v1.1-REQUIREMENTS.md`
