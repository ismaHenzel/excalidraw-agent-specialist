# Roadmap: Excalidraw Specialist — Self-Verifying Diagram Authoring

## Milestones

- ✅ **v1.0 MVP** — Phases 1–3 (shipped 2026-05-24)
- ✅ **v1.1 Diagram Families & UML Expansion** — Phases 4–9 (shipped 2026-06-09)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1–3) — SHIPPED 2026-05-24</summary>

Closed the render-and-verify gap: a standalone verifier subagent, a mandatory render→verify→fix loop in the specialist, and end-to-end validation of self-healing and honest-failure behavior.

- [x] Phase 1: Verifier Subagent (3/3 plans) — completed 2026-05-23
- [x] Phase 2: Closed-Loop Specialist Integration (1/1 plan) — completed 2026-05-24
- [x] Phase 3: End-to-End Closed-Loop Validation (1/1 plan) — completed 2026-05-24

Archive: `.planning/milestones/v1.0-ROADMAP.md` *(v1.0 phases retained inline; see commit history)*

</details>

<details>
<summary>✅ v1.1 Diagram Families & UML Expansion (Phases 4–9) — SHIPPED 2026-06-09</summary>

Reorganized the plugin around four real-world diagram families and a `diagram-types/` knowledge layer. All 10 diagram types shipped with canonical examples passing the full loop.

- [x] Phase 4: Taxonomy Spine & Star Resolution (3/3 plans) — completed 2026-06-03
- [x] Phase 5: Tech Architecture + Activity (3/3 plans) — completed 2026-06-05
- [x] Phase 6: Star Schema → Snowflake (2/2 plans) — completed 2026-06-07
- [x] Phase 7: ER + Class (4/4 plans) — completed 2026-06-08
- [x] Phase 8: Sequence + Use-Case (4/4 plans) — completed 2026-06-08
- [x] Phase 9: Data Vault (3/3 plans) — completed 2026-06-09

Archive: `.planning/milestones/v1.1-ROADMAP.md`, `.planning/milestones/v1.1-REQUIREMENTS.md`

</details>

### Next Milestone (Planned)

Start with `/gsd-new-milestone` to define v2 scope. Candidates from Active requirements:

- [ ] UMLX-01: Additional UML types (state, component, deployment, …)
- [ ] HARD-01: Vendor Excalidraw bundle (remove CDN dependency)
- [ ] HARD-02: Clean up icons/ directory
- [ ] HARD-03: Sandbox path resolver
- [ ] HARD-04: SDK-driven E2E harness

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Verifier Subagent | v1.0 | 3/3 | Complete | 2026-05-23 |
| 2. Closed-Loop Specialist Integration | v1.0 | 1/1 | Complete | 2026-05-24 |
| 3. End-to-End Closed-Loop Validation | v1.0 | 1/1 | Complete | 2026-05-24 |
| 4. Taxonomy Spine & Star Resolution | v1.1 | 3/3 | Complete | 2026-06-03 |
| 5. Tech Architecture + Activity | v1.1 | 3/3 | Complete | 2026-06-05 |
| 6. Star Schema → Snowflake | v1.1 | 2/2 | Complete | 2026-06-07 |
| 7. ER + Class | v1.1 | 4/4 | Complete | 2026-06-08 |
| 8. Sequence + Use-Case | v1.1 | 4/4 | Complete | 2026-06-08 |
| 9. Data Vault | v1.1 | 3/3 | Complete | 2026-06-09 |
