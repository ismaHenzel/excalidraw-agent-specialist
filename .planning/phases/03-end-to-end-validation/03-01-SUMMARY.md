# Plan 03-01 — Summary

**Status:** Complete (artefact-side). Operator-driven specialist-loop runs deferred by design — see "Deferred to interactive runs" below.

## Files Created (11 of 11)

| Path | Status |
|------|--------|
| `fixtures/e2e/.gitignore` | ✓ one line, `working/` |
| `fixtures/e2e/README.md` | ✓ 7-step operator protocol + EVIDENCE.md template + troubleshooting |
| `fixtures/e2e/scenarios/text-overflow-self-heal/seed.excalidraw` | ✓ byte-similar to `fixtures/verifier/text-overflow/text-overflow.excalidraw` (per D3-14) |
| `fixtures/e2e/scenarios/text-overflow-self-heal/REQUEST.md` | ✓ pastes verbatim into a session, single `<ABSOLUTE_PATH_TO_WORKING_COPY>` placeholder |
| `fixtures/e2e/scenarios/text-overflow-self-heal/README.md` | ✓ maps to ROADMAP §SC#1, mode `success`, ≤2 attempts |
| `fixtures/e2e/scenarios/emoji-as-icon/REQUEST.md` | ✓ no seed; specialist authors from scratch |
| `fixtures/e2e/scenarios/emoji-as-icon/README.md` | ✓ maps to ROADMAP §SC#2 + CONT-01, mode `success`, 1 attempt |
| `fixtures/e2e/scenarios/under-specified-honest-failure/seed.excalidraw` | ✓ 5 rectangles + 5 elbow arrows, all endpoints 60+ px from any border |
| `fixtures/e2e/scenarios/under-specified-honest-failure/REQUEST.md` | ✓ includes the "do not move or resize" constraint |
| `fixtures/e2e/scenarios/under-specified-honest-failure/README.md` | ✓ maps to ROADMAP §SC#3, mode `honest-failure`, 3 attempts |
| `scripts/e2e_check.sh` | ✓ executable, ≤8 KB; success + honest-failure modes; staleness soft-assert; word-bounded forbidden-token grep |

## Seed Verification (fixture-author time)

| Seed | Helper invocation | Result |
|------|-------------------|--------|
| `text-overflow-self-heal/seed.excalidraw` | `python3 scripts/verifier_structural.py …/seed.excalidraw` | 1 issue, `check == text_overflow_static`, `severity == error`, `element_id == t_db` |
| `under-specified-honest-failure/seed.excalidraw` | `python3 scripts/verifier_structural.py …/seed.excalidraw` | 5 issues, all `check == arrow_endpoint_unanchored`, all `severity == error`, ids `arrow_endpoint_unanchored_seed_a1`..`a5` |
| Both seeds | `python3 scripts/excalidraw_validator.py …/seed.excalidraw` | Static validator returns 0 (warnings only — low-contrast text on overflow seed, no-text-elements on under-specified seed); render pipeline accepts |

## ROADMAP §Phase 3 Success-Criteria Trace

| # | Success criterion | Where validated |
|---|-------------------|-----------------|
| 1 | Text-overflow request → fits within 3 iterations | `scenarios/text-overflow-self-heal/` (seed reuses Phase 1's defect; specialist runs in mode `success`) — operator-confirmed via `e2e_check.sh --mode success` |
| 2 | Emoji request → `icons/*.png` image element, not missing-glyph box | `scenarios/emoji-as-icon/` (no seed; specialist authors fresh; `<content_policy>` maps ✅ → `success_icon.png`) — operator-confirmed via `e2e_check.sh --mode success` |
| 3 | Under-specified request → honest-failure with PNG path + structured issues + source path; no "done" | `scenarios/under-specified-honest-failure/` (5 unanchored arrows + constraint that forbids moving rectangles) — operator-confirmed via `e2e_check.sh --mode honest-failure --final-message …` |
| 4 | Output dir contains only `.excalidraw` + 1 `.png` (+ verifier report); no `.v1`, `.v2`, iteration artefacts | All three scenarios via `e2e_check.sh`'s S4/H4 artefact-discipline glob check (`.v[0-9]*.excalidraw`, `_iter*.{excalidraw,png}`, `.bak*`, `.report-[0-9]*.json`) |

## Check-Script Smoke Test Results (fixture-author time)

| Case | Expected exit | Actual exit |
|------|---------------|-------------|
| `bash scripts/e2e_check.sh` (no args) | 2 | 2 ✓ |
| `bash scripts/e2e_check.sh /tmp/foo.excalidraw --mode BOGUS` | 2 | 2 ✓ |
| `bash scripts/e2e_check.sh /tmp/foo.excalidraw` (no `--mode`) | 2 | 2 ✓ |
| `bash scripts/e2e_check.sh --mode success` (no source) | 2 | 2 ✓ |
| `bash scripts/e2e_check.sh /tmp/foo.txt --mode success` (wrong extension) | 2 | 2 ✓ |
| `bash scripts/e2e_check.sh /tmp/foo.excalidraw --mode` (no value) | 2 | 2 ✓ |
| `bash scripts/e2e_check.sh /tmp/foo.excalidraw --mode success --final-message` (no value) | 2 | 2 ✓ |
| `bash scripts/e2e_check.sh /nonexistent.excalidraw --mode success` | 1 + `FAIL: source not found` | 1 ✓ |
| Synthetic `success` happy-path (all sibling files present, `passed: true`) | 0 + all `PASS:` | 0 ✓ |
| Synthetic `success` with `<base>.v1.excalidraw` suffixed sibling | 1 + `FAIL: suffixed siblings present` | 1 ✓ |
| Synthetic `honest-failure` with valid final-message | 0 + all `PASS:` | 0 ✓ |
| Synthetic `honest-failure` with `All done!` in final-message | 1 + `FAIL: forbidden success token(s)` | 1 ✓ |

12/12 smoke cases pass. All ROADMAP §Phase 3 success-criteria asserts are mechanically verifiable.

## Deferred to Interactive Runs

The actual specialist-loop runs require an interactive Claude Code session (Phase 3 ships the harness, not the harness driver — per PROJECT.md "CI harness running verifier on every plugin change — Out of Scope"). The operator workflow is documented step-by-step in `fixtures/e2e/README.md` and yields a per-scenario `Summary: 0 fail` from `e2e_check.sh` on a green run.

Operator-driven evidence lands in the git-ignored `fixtures/e2e/working/EVIDENCE.md` (template in the README). Successful operator runs are sufficient to declare the v1 milestone shippable — no SUMMARY edit is required for additional re-runs.

## Deviations

- **Smoke-positive happy-path test uses synthetic artefacts**, not a real specialist run, because the real run requires Docker + an interactive Claude Code session. Synthetic artefacts validate the script's logic; the real check happens at operator time. This is acknowledged in 03-CONTEXT.md `<specifics>` ("smoke-tested fixture-author-time; real specialist-loop runs deferred to operator-driven runs").
- **The script's `WARN: --final-message not provided` path is intentional**: a check without `--final-message` still validates the artefact-side invariants (S1–S5 / H1–H4) and tells the operator to inspect the message manually. Exit 0 in that path is correct — the LOOP-02 grep is an OPTIONAL strengthening, not a precondition. Operator workflow documented in the README always supplies `--final-message`, so this path is mainly a safety net for quick re-checks of just the on-disk artefacts.
- **The under-specified seed produces 5 unanchored arrows, not the "≥2" minimum from the plan's must-haves.** Five gives the specialist meaningful work to attempt on each iteration (so the failure isn't trivial), and the abundance makes accidental convergence less likely — which is the whole point of the scenario.
