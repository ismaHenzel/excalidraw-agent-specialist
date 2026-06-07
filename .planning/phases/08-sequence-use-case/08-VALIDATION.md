---
phase: 8
slug: sequence-use-case
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-07
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Full validate→render→verify loop (excalidraw_specialist + excalidraw_verifier) |
| **Config file** | none — loop is MCP-driven |
| **Quick run command** | Render .excalidraw → inspect PNG + verifier-report.json |
| **Full suite command** | Full validate→render→verify loop on both canonical examples |
| **Estimated runtime** | ~60 seconds per diagram |

---

## Sampling Rate

- **After every task commit:** Check that rendered PNG exists and verifier-report.json has no FAIL entries
- **After every plan wave:** Run full loop on all new .excalidraw files for the wave
- **Before `/gsd-verify-work`:** Both canonical examples must pass verifier with zero FAIL entries
- **Max feedback latency:** ~120 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 8-01-01 | 01 | 1 | UML-01 | — | N/A | manual | render lifeline-activation.md example → verify PNG | ❌ W0 | ⬜ pending |
| 8-01-02 | 01 | 1 | UML-01 | — | N/A | manual | render sequence.md recipe → verify PNG passes loop | ❌ W0 | ⬜ pending |
| 8-02-01 | 02 | 1 | UML-03 | — | N/A | manual | render use-case.md recipe → verify PNG passes loop | ❌ W0 | ⬜ pending |
| 8-03-01 | 03 | 2 | UML-01 | — | N/A | manual | canonical sequence example passes full loop | ❌ W0 | ⬜ pending |
| 8-03-02 | 03 | 2 | UML-03 | — | N/A | manual | canonical use-case example passes full loop | ❌ W0 | ⬜ pending |
| 8-04-01 | 04 | 2 | UML-01, UML-03 | — | N/A | manual | resolver index updated, examples indexed | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] No new test framework needed — validation is loop-based (render + verifier JSON)
- [ ] Canonical .excalidraw examples must exist before verify-work

*Existing infrastructure (excalidraw_specialist + excalidraw_verifier) covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Activation bar center-x aligned to lifeline x | UML-01 | Visual geometry check (no automated assertion today) | Open PNG, confirm each activation bar is horizontally centered on its participant's lifeline column |
| Message Y values increase top-to-bottom | UML-01 | Monotonic Y check not yet in verifier | Open PNG, confirm message arrows appear in sequence order from top to bottom |
| System boundary visually encloses use cases | UML-03 | Visual containment check | Open PNG, confirm group-container box surrounds all use-case ovals |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
