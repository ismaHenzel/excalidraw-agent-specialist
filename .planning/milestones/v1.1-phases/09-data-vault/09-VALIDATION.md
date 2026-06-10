---
phase: 9
slug: data-vault
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-08
---

# Phase 9 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Shell + Python (frozen v1.0 loop — no new test framework) |
| **Config file** | `scripts/validate_and_render.sh` (frozen) |
| **Quick run command** | `bash scripts/validate_and_render.sh <path>.excalidraw` |
| **Full suite command** | `bash scripts/validate_and_render.sh <path>.excalidraw && python scripts/verifier/verifier_structural.py <path>.excalidraw` |
| **Estimated runtime** | ~10–30 seconds per example |

---

## Sampling Rate

- **After every task commit:** Verify file exists at declared path + frontmatter/JSON valid
- **After Wave 1 (recipe authoring):** No automated run — recipe is prose/JSON-template only; verify structure manually
- **After Wave 2 (example authoring):** Run full validate→render→verify loop; verifier_structural.py must exit 0
- **After Wave 3 (resolver + back-refs):** Confirm resolver row present in README, back-refs present in recipe/specialist
- **Before `/gsd-verify-work`:** Full loop on example must be green + EX-03 visual gate passed
- **Max feedback latency:** ~30 seconds (verifier_structural.py pass/fail)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 09-01-01 | 01 | 1 | DM-04 | — | N/A | manual | `test -f .claude/agents/excalidraw/diagram-types/data-vault.md` | ❌ W0 | ⬜ pending |
| 09-01-02 | 01 | 1 | DM-04 | — | N/A | manual | `grep -q "hub\|link\|satellite" .claude/agents/excalidraw/diagram-types/data-vault.md` | ❌ W0 | ⬜ pending |
| 09-01-03 | 01 | 1 | DM-04 | SC-2 | Role label present on every box | manual-checklist | Visual review: hub/link/sat boxes each carry «hub»/«link»/«sat» label | ❌ W0 | ⬜ pending |
| 09-02-01 | 02 | 2 | DM-04/EX-01 | — | N/A | automated | `bash scripts/validate_and_render.sh <example>.excalidraw` | ❌ W0 | ⬜ pending |
| 09-02-02 | 02 | 2 | DM-04/EX-03 | SC-2 | Grayscale-distinguishable | visual-gate | Human visual review of rendered PNG in grayscale (EX-03 gate) | ❌ W0 | ⬜ pending |
| 09-02-03 | 02 | 2 | EX-01 | — | N/A | automated | `python scripts/verifier/verifier_structural.py <example>.excalidraw` exits 0 | ❌ W0 | ⬜ pending |
| 09-03-01 | 03 | 3 | DM-04 | — | N/A | automated | `grep -q "data-vault" .claude/agents/excalidraw/diagram-types/README.md` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

No new test framework needed. The frozen v1.0 loop (`scripts/validate_and_render.sh` + `verifier_structural.py`) is the CI harness. No stubs to create.

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Hub/link/satellite role labels visible on rendered PNG | DM-04 / SC-2 | `verifier_structural.py` has zero color/contrast checks; EX-03 is a visual gate only | Open rendered PNG; confirm each hub, link, and satellite box carries its role label («hub»/«link»/«sat») with no ambiguity |
| Three table classes distinguishable in grayscale | DM-04 / SC-2 | No automated grayscale check in loop | Convert rendered PNG to grayscale (e.g. ImageMagick `convert -colorspace Gray`); confirm hub/link/satellite remain visually distinct |
| In-canvas legend present and legible | DM-04 | No automated legend check | Inspect PNG: a 3-row swatch legend labeling hub/link/satellite must be visible |

---

## Validation Architecture

*(Referenced by plan-phase Nyquist gate.)*

The validate→render→verify loop is the primary automated harness (`scripts/validate_and_render.sh` + `verifier_structural.py`). SC-2 (grayscale safety) is unguarded by automation — the mandatory text role label + in-canvas legend are the load-bearing mechanism, and the EX-03 visual gate is the judge. Wave ordering: recipe prose (W1, manual only) → example round-trip (W2, automated + visual) → resolver wiring (W3, automated grep).

---

## Validation Sign-Off

- [ ] All tasks have automated verify or documented manual gate
- [ ] Wave 2 automated run must pass before resolver row is wired
- [ ] EX-03 visual gate explicitly signed off before `/gsd-verify-work`
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s for automated tasks
- [ ] `nyquist_compliant: true` set in frontmatter after Wave 0 check

**Approval:** pending
