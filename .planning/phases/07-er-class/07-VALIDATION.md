---
phase: 7
slug: er-class
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-07
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python (excalidraw validator + verifier structural scripts) + shell loop |
| **Config file** | none — validation via existing `excalidraw_validator.py` and `verifier_structural.py` |
| **Quick run command** | `python .claude/agents/excalidraw/excalidraw_validator.py <file.excalidraw>` |
| **Full suite command** | render + verify loop via `mcp__excalidraw__create_view` then verifier agent |
| **Estimated runtime** | ~30 seconds per diagram |

---

## Sampling Rate

- **After every task commit:** Run quick validator on authored `.excalidraw` file
- **After every plan wave:** Run full render→verify loop on each produced diagram
- **Before `/gsd-verify-work`:** Full suite must be green (all examples pass full loop)
- **Max feedback latency:** ~30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 7-01-01 | 01 | 1 | DM-02, UML-02 | — | No illegal arrowhead token in authored JSON | structural | `python .claude/agents/excalidraw/excalidraw_validator.py kb/relationship-endpoint.md` | ❌ W0 | ⬜ pending |
| 7-01-02 | 01 | 1 | DM-02 | — | Crow's-foot/bar/dot glyphs visually distinguishable | manual + visual | render + verifier loop | ❌ W0 | ⬜ pending |
| 7-02-01 | 02 | 2 | DM-02 | — | er.md renders to passing PNG | render loop | `mcp__excalidraw__create_view` + verifier | ❌ W0 | ⬜ pending |
| 7-03-01 | 03 | 2 | UML-02 | — | class.md renders to passing PNG | render loop | `mcp__excalidraw__create_view` + verifier | ❌ W0 | ⬜ pending |
| 7-04-01 | 04 | 3 | DM-02, UML-02 | — | Example pairs indexed and pass full loop | integration | render + verify + index check | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Validate existing `excalidraw_validator.py` covers arrowhead token checking (or note gap for SC-1)
- [ ] Confirm verifier structural script is available and up-to-date
- [ ] Confirm render loop (`mcp__excalidraw__create_view`) is functional in current session

*Existing infrastructure (validator + verifier) covers most phase requirements; Wave 0 is lightweight.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Crow's-foot vs. plain association visually distinguishable | DM-02 SC-2 | Visual distinction cannot be auto-asserted | Render example ER diagram; inspect PNG — verify cardinality glyphs differ from plain line |
| Generalization triangle visually present | UML-02 SC-3 | Visual glyph shape requires human judgment | Render example class diagram; inspect PNG — verify triangle arrowhead on generalization line |
| «stereotype» guillemet rendering safe | UML-02 | Empirical render safety for non-ASCII | Author class with stereotype compartment text; verify no verifier `text_overflow_static` error |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
