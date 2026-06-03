---
phase: 01
slug: verifier-subagent
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-21
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Derived from `01-RESEARCH.md` § Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | None — Bash + `jq` fixture diff (no test framework introduced) |
| **Config file** | None — see Wave 0 |
| **Quick run command** | `python3 scripts/verifier_structural.py fixtures/verifier/good/good.excalidraw \| jq 'length == 0'` (expects `true`) |
| **Full suite command** | `bash scripts/verifier_self_test.sh` (loops over all 3 fixtures) — or 3 manual one-liners |
| **Estimated runtime** | < 3 seconds total |

---

## Sampling Rate

- **After every task commit:** Run the helper directly against the relevant fixture (`python3 scripts/verifier_structural.py <fixture-path> | jq .`). < 1 sec each.
- **After every plan wave:** Run helper against all 3 fixtures; confirm severity counts match expected.
- **Before `/gsd:verify-work`:** Spawn the full `excalidraw_verifier` subagent on each fixture; diff generated report against `expected-report.json` ignoring `checked_at`, `source`, `png`.
- **Max feedback latency:** < 3 seconds for helper-level checks; manual for subagent-level (requires Claude Code session).

---

## Per-Task Verification Map

*Populated by planner. Each PLAN.md task should declare its `<automated>` verify command; this table aggregates them. Task IDs follow the convention `01-<plan>-<task>`.*

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| *TBD by planner* | — | — | — | — | — | — | — | — | ⬜ pending |

---

## Wave 0 Requirements

- [ ] `scripts/verifier_structural.py` — implements 4 error + 4 warning checks; JSON-array stdout; exit 0 always
- [ ] `excalidraw_verifier.md` — subagent definition with YAML frontmatter + 7-step operational sequence + output contract
- [ ] `fixtures/verifier/good/good.excalidraw` + `good.png` + `expected-report.json`
- [ ] `fixtures/verifier/raw-emoji/raw-emoji.excalidraw` + `raw-emoji.png` + `expected-report.json`
- [ ] `fixtures/verifier/text-overflow/text-overflow.excalidraw` + `text-overflow.png` + `expected-report.json`
- [ ] **Optional polish:** `scripts/verifier_self_test.sh` — loops the helper across all 3 fixtures + emits pass/fail summary. Per CONTEXT.md `<deferred>`, may be a manual recipe in PLAN.md instead.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Subagent end-to-end on each fixture | VRFY-02 | Requires multimodal `Read` on the rendered PNG inside an interactive Claude Code session | 1) `/agents` shows `excalidraw_verifier` 2) Invoke it with each fixture's `.excalidraw` path 3) `diff <(jq 'del(.checked_at,.source,.png)' expected-report.json) <(jq 'del(.checked_at,.source,.png)' <fixture>.verifier-report.json)` → exits 0 |
| Visual checks (`text_overflow_visual`, `arrow_disconnected_visual`, `icon_blank`, `missing_glyph_box`, `layout_collision`) | VRFY-02 | LLM judgment on rendered PNG — no deterministic per-pixel rule | Compare visual issues against the fixture's `expected-report.json` visual-issue subset |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 3s for helper-level; manual for subagent-level
- [ ] `nyquist_compliant: true` set in frontmatter (set when planner has populated Per-Task table)

**Approval:** pending

---

## Coverage Rationale

Three fixtures cover both severity classes plus the good-case baseline:
- `good` exercises the empty-issues happy path. **False-positive detection:** if `good` ever produces issues, the helper has a logic bug.
- `raw-emoji` exercises the error-severity branch (`raw_emoji_in_text`) AND the file/icons cross-reference for `suggested_fix`.
- `text-overflow` exercises the geometric containing-shape lookup AND the suggested-fix string generation.

Adding a 4th fixture (e.g., for `image_path_unresolvable`) is acceptable polish but not required by CONTEXT.md D-15.

**Signal-to-noise pattern:** Fixture-diff is a single-source-of-truth test. `expected-report.json` is stable in the repo; the diff rule (ignore `checked_at`, `source`, `png`) is deterministic. No flaky LLM-side assertions — the LLM faithfully echoes helper output and applies the deterministic visual rubric.
