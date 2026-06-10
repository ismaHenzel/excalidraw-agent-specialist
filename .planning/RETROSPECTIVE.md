# Retrospective

## Milestone: v1.0 — Self-Verifying Loop

**Shipped:** 2026-05-24
**Phases:** 3 | **Plans:** 5

### What Was Built

- Standalone `excalidraw_verifier` subagent (structural pre-check + visual PNG review)
- Mandatory render→verify→fix loop in specialist (3-iteration cap, always-render policy)
- Emoji → `icons/` PNG mapping; artefact overwrite discipline
- End-to-end validation on representative defect cases

### What Worked

- Separation of concerns: verifier as a separate subagent avoids confirmation bias on self-review
- Both structural + visual: structural catches cheap defects without vision tokens; visual catches render-time surprises
- Overwrite discipline: clean output directory without versioned clutter

### Key Lessons

- Always-render policy closes failure modes that opt-out paths create
- 3-iteration cap is the right balance — stubborn diagrams surface to the human rather than loop forever

---

## Milestone: v1.1 — Diagram Families & UML Expansion

**Shipped:** 2026-06-09
**Phases:** 6 (Phases 4–9) | **Plans:** 19

### What Was Built

- Two-tier family/type picker in `/excalidraw` (4 families → type sub-pick; single authoritative resolver table)
- `diagram-types/` KB layer with 10 type recipe files; bidirectional back-refs between type files and `kb/` primitives
- Data modeling: star schema, snowflake, ER, data vault — all canonical examples loop-verified
- UML core 4: sequence, class, use-case, activity — all canonical examples loop-verified
- Shared primitives built once: notation-conventions.md, compartmented-box.md, relationship-endpoint.md, lifeline-activation.md
- End-to-end regression: 7/8 wired examples `issues == []`; use_case_checkout exit 0 (pre-existing warnings)

### What Worked

- Scaffolding-first (Phase 4): proving the family→type→bundle→specialist flow against an existing type before authoring new notation avoided rework in later phases
- EX-03 gate discipline: wiring resolver rows only after canonical examples pass the full loop prevented broken references
- Co-locating ER + Class in Phase 7: shared relationship-endpoint primitive was built once, saving duplication
- Compartmented-box built once in Phase 4: reused cleanly by star, snowflake, ER, class, data vault with no re-derivation
- Phase sequencing by shared primitive: each primitive was built exactly once (the right phase), then reused

### What Was Inefficient

- Phase 8 ROADMAP.md status not updated at completion — milestone close had to fix Phase 8 from "In Progress" to "Complete" retroactively
- REQUIREMENTS.md traceability table not updated during execution — 13 checkboxes were shipped but unchecked, requiring bulk update at milestone close
- Phase 4 Plan 03 smoke test: Tasks 1–2 verified structurally but Task 3 (interactive operator run) never completed — the integration was correct but the gate was left open

### Patterns Established

- Resolver wiring discipline: EX-03 visual gate must be approved before wiring a resolver row; Pitfall 6 enforced throughout Phases 5–9
- Bidirectional KB link: type file @-references primitive; primitive carries `> Used by types:` back-ref — kept the two-layer relationship discoverable
- Evidence-based sub-pattern columns: resolver table columns were corrected to match actual @-references in recipe files, not placeholder guesses
- Deferred items: acknowledged at close with explicit STATE.md Deferred Items table; clear audit trail for future milestones

### Key Lessons

- Update ROADMAP.md and REQUIREMENTS.md checkboxes immediately after each plan completes — don't let tracking lag execution
- Smoke tests that require interactive operator sessions should have an explicit "deadline by when" or be downgraded to deferred
- The resolver table is the single source of truth — any drift between it and recipe files breaks the whole intent pick flow; enforce at every wiring step
- Lifeline pixel geometry ASSUMED from RESEARCH A1 — pixel values may need calibration against real renders in a future spike

### Cost Observations

- Timeline: 7 days (2026-06-03 → 2026-06-09) for 6 phases and 19 plans
- Sessions: multiple (phases 5–9 each spanned 1–2 sessions)
- Notable: data vault (Phase 9) was the most complex type and required 3 plans + a grayscale confirmation gate; it delivered on schedule as the last phase

---

## Cross-Milestone Trends

| Milestone | Phases | Plans | Duration | Deferred Items |
|-----------|--------|-------|----------|----------------|
| v1.0 | 3 | 5 | ~1 week | 0 |
| v1.1 | 6 | 19 | 7 days | 3 (acknowledged) |

**Recurring pattern:** Milestones close with deferred operator-driven verification steps (human-needed gates). Consider building interactive operator checkpoints into the phase plan rather than leaving them to milestone close.
