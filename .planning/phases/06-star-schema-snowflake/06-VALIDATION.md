---
phase: 6
slug: star-schema-snowflake
status: ready
nyquist_compliant: true
wave_0_complete: false
created: 2026-06-05
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Frozen v1.0 loop — `validate_and_render.sh` + `excalidraw_verifier` subagent (no pytest/jest) |
| **Config file** | none — script-driven |
| **Quick run command** | `bash .claude/agents/excalidraw/scripts/render/validate_and_render.sh <file>.excalidraw` |
| **Full suite command** | Run quick command → invoke `excalidraw_verifier` on the `.excalidraw` → assert `verifier-report.json` `passed: true` |
| **Estimated runtime** | ~30–60 seconds per example (Docker render + verifier) |

---

## Sampling Rate

- **After every authoring task:** Run the quick render command on the authored `.excalidraw`
- **After every plan wave:** Full loop (render + verifier `passed: true`) on all authored examples
- **Before `/gsd-verify-work`:** Full suite must be green for both star and snowflake examples
- **Max feedback latency:** ~60 seconds (Docker render is the bottleneck)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-T1 | 01 | 1 | DM-01 | T-06-01 | Recipe references compartmented-box for offsets; no raw numbers re-derived | structural | `grep -q "row pitch" .claude/agents/excalidraw/diagram-types/compartmented-box.md && grep -q "star-schema" .claude/agents/excalidraw/diagram-types/star-schema.md && echo PASS` | ❌ W0 | ⬜ pending |
| 06-01-T2 | 01 | 1 | DM-01 / SC-1,3,4 | T-06-01 | Example renders; dividers present; no multi-line text; resolver wired | loop + structural | `test -f .claude/agents/excalidraw/examples/star_schema_v2.png && python3 -c "..."` (see plan) | ❌ W0 | ⬜ pending |
| 06-02-T1 | 02 | 2 | DM-03 | T-06-03 | Recipe builds on star by @-reference; no re-derived geometry | structural | `test -f .claude/agents/excalidraw/diagram-types/snowflake-schema.md && grep -q "star-schema" .claude/agents/excalidraw/diagram-types/snowflake-schema.md && grep -q "tree-hierarchy" .claude/agents/excalidraw/diagram-types/snowflake-schema.md && echo PASS` | ❌ W0 | ⬜ pending |
| 06-02-T2 | 02 | 2 | DM-03 / SC-2,3,4 | T-06-03 | Example renders after star passes; SC-2 ordering gate enforced; no multi-line text | loop + structural | `test -f .claude/agents/excalidraw/examples/snowflake_schema.png && python3 -c "..."` (see plan) | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

The test artifacts (`.excalidraw` sources and rendered PNGs) are **created** by the phase plans — they do not pre-exist. Wave 0 is complete when:

- [ ] `validate_and_render.sh` is confirmed executable (used in Phases 1–5; re-confirm Docker is available)
- [ ] `excalidraw_verifier` subagent is available for post-render structural checks

*No new test framework installs required — the frozen v1.0 loop is already in place.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Compartment dividers span full box width; rows share common left x | SC-1 | `text_overflow_static` does not enforce geometric alignment — only overflow | Open rendered PNG; visually confirm dividers reach both side walls; all row texts align to same x |
| No multi-line row text in rendered PNG | SC-4 | Automated python3 check catches `\n` in JSON but not visual wrapping | Confirm row texts are single-line in the PNG; no truncation or wrapping visible |
| Snowflake normalization layout is correct | SC-2 | Structural verifier checks anchoring, not semantic layout | Confirm at least one dimension is split into a child sub-table chain connected by thin elbow arrows |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify (Task 3 in each plan is checkpoint:human-verify)
- [x] Wave 0 covers all MISSING references (files created by plans themselves — confirmed in RESEARCH Validation Architecture)
- [x] No watch-mode flags
- [x] Feedback latency < 60s (Docker render bound)
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
