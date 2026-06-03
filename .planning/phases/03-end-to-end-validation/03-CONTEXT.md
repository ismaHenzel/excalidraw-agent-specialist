# Phase 3: End-to-End Closed-Loop Validation - Context

**Gathered:** 2026-05-24
**Status:** Ready for planning
**Depends on:** Phase 1 (verifier shipped) + Phase 2 (specialist prompt closed the loop)

<domain>
## Phase Boundary

Validate the full closed loop — author → render → verify → fix → re-render → re-verify → deliver/honest-failure — on representative defect cases. Phase 3 is an **acceptance gate** for the v1 milestone: it introduces NO new requirements; it proves the six v1 requirements (VRFY-01, VRFY-02, LOOP-01, LOOP-02, LOOP-03, CONT-01) hold together when the specialist + verifier are exercised end-to-end.

Concretely, after this phase the repo contains:

1. A small **scenario corpus** under `fixtures/e2e/scenarios/`, one directory per ROADMAP §Phase 3 success criterion (text-overflow self-heal, emoji-as-icon mapping, under-specified honest-failure). Each scenario directory holds:
   - `REQUEST.md` — the user-facing prompt an operator pastes into an interactive Claude Code session.
   - (For scenarios that need a pre-existing seed) `seed.excalidraw` — a deliberately defective starting file the specialist will mutate during fix iterations.
   - `README.md` — what success looks like for that scenario, including the exact check-script invocation.
2. A runnable **check script** (`scripts/e2e_check.sh`) that, given the path to a scenario's working `.excalidraw`, validates the loop's *artefact-side* invariants — artefact discipline (LOOP-03), success-vs-honest-failure shape (LOOP-02 + LOOP-03), and the presence/structure of the sibling verifier report (LOOP-02). The script does NOT itself spawn the specialist subagent — that requires an interactive Claude Code session.
3. A **run protocol** (`fixtures/e2e/README.md`) explaining the operator workflow: copy seed → paste request → wait for the specialist's loop to settle → run `e2e_check.sh` → record evidence in `EVIDENCE.md`.

Out of this phase:
- Automated harness that spawns the specialist subagent itself (no test-infrastructure mandate per PROJECT.md Out of Scope).
- Pixel-diff regression vs `examples/*.png` (explicitly excluded by PROJECT.md).
- New requirements, new check rules, or new verifier-side logic — Phase 3 is a gate, not a feature.
- Editing `excalidraw_specialist.md` or `excalidraw_verifier.md` — both are frozen by the time Phase 3 runs.

</domain>

<decisions>
## Implementation Decisions

### Phase Shape — Why a Single Plan (03-01)
- **D3-01:** Phase 3 ships as ONE plan: scenario corpus + check script + run protocol + summary. There is no research/patterns/validation pre-plan triad (as Phase 1 had) because no new code paths or contracts are introduced — every contract was locked in Phases 1 & 2. The deliverable surface is small (≤6 new files, no edits to existing source) and the success criteria are mechanically checkable by the check script + a short operator walkthrough.
- **D3-02:** Phase 3 does NOT modify any of `excalidraw_specialist.md`, `excalidraw_verifier.md`, `scripts/verifier_structural.py`, `scripts/validate_and_render.sh`, or any KB/icon file. If a scenario surfaces a real specialist-prompt bug during execution, that bug becomes a Phase 2.x insertion (per ROADMAP's "decimal phases for urgent insertions" convention) — Phase 3 still ships its scenario corpus + check script regardless.

### Scenario Corpus Shape
- **D3-03:** Exactly THREE scenarios, one per ROADMAP §Phase 3 success criterion #1–#3 (criterion #4 — artefact discipline — is observable across all three, so it does not need a dedicated scenario):
  1. **`text-overflow-self-heal/`** — operator hands the specialist a defective `seed.excalidraw` (text label visibly overflows its container, same shape as `fixtures/verifier/text-overflow/text-overflow.excalidraw`) and asks for "fix this so the label fits". The verifier flags `text_overflow_static` (and likely `text_overflow_visual`); the specialist mutates the container width or shortens the label; the loop converges to `passed: true` within the 3-attempt cap. Validates LOOP-02 self-heal half + LOOP-03 artefact discipline.
  2. **`emoji-as-icon/`** — operator asks the specialist to "create a small diagram with a green checkmark next to a node labelled 'deploy-success'". The specialist's `<content_policy>` must map the ✅ request to `icons/success_icon.png` and emit an `image` element. The verifier's structural pre-check (`raw_emoji_in_text`) confirms no raw codepoint in any `text` element; the visual check confirms no `missing_glyph_box`. The loop should converge on the FIRST verifier call (no fix iterations needed). Validates CONT-01 generation half + VRFY-01 structural half.
  3. **`under-specified-honest-failure/`** — operator hands the specialist a `seed.excalidraw` that the specialist will keep failing to fix in 3 attempts. Concretely: a diagram with multiple unanchored elbow arrows whose target shapes are intentionally far away in a topology the specialist won't easily re-route, AND a request that constrains the specialist not to move or recolor the existing shapes. The verifier emits `arrow_endpoint_unanchored` errors; the specialist's best fixes still leave some arrows unanchored after 3 attempts; the specialist MUST emit the LOOP-02 honest-failure template (with the `Failed PNG:`, `Source:`, `Report:`, `Outstanding issues:` tokens, no "done"). Validates LOOP-02 honest-failure half.
- **D3-04:** Each scenario directory holds at most three files:
  - `REQUEST.md` — verbatim text an operator pastes into a Claude Code session. The text references `seed.excalidraw` by relative path when relevant.
  - `seed.excalidraw` — present only for `text-overflow-self-heal/` and `under-specified-honest-failure/`. The emoji scenario starts from scratch (the specialist authors a brand-new file).
  - `README.md` — one-pager describing the scenario's mapping to ROADMAP success criteria, expected loop trajectory (1 attempt? 3 attempts?), and the `e2e_check.sh` invocation that confirms the artefact-side invariants.
- **D3-05:** Scenario seeds are STATIC — they are committed once and never overwritten. The specialist works on a COPY (the operator copies seed.excalidraw → working/<scenario>.excalidraw before pasting the request) so the seed remains a clean re-runnable starting point. The check script takes the working copy's path, not the seed.

### Check Script (`scripts/e2e_check.sh`)
- **D3-06:** Single-purpose script: given a `<basename>.excalidraw` path AND a `--mode {success|honest-failure}` flag, validate the artefact-side invariants the operator can observe without re-running the specialist. The script does NOT spawn the specialist or the verifier — it only reads files on disk and an optional pasted final message.
- **D3-07:** `success` mode asserts (exits 0 iff all hold):
  1. The `<basename>.excalidraw` file exists and is valid JSON.
  2. The sibling `<basename>.png` exists and is non-empty.
  3. The sibling `<basename>.verifier-report.json` exists, is valid JSON, has the 5 top-level keys (`passed`, `checked_at`, `source`, `png`, `issues`), and `passed == true`.
  4. The basename's parent directory contains NO suffixed siblings matching `<basename>.v[0-9]*.excalidraw`, `<basename>_iter*.{excalidraw,png}`, `<basename>.bak*`, or `<basename>.report-[0-9]*.json`. The only `<basename>.*` files allowed are `.excalidraw`, `.png`, and `.verifier-report.json`.
- **D3-08:** `honest-failure` mode asserts (exits 0 iff all hold):
  1. The `<basename>.excalidraw` file exists and is valid JSON.
  2. The sibling `<basename>.png` exists and is non-empty (failure mode still has a rendered PNG — the last failed render).
  3. The sibling `<basename>.verifier-report.json` exists, is valid JSON, and `passed == false` with `issues` non-empty.
  4. Same artefact-discipline assertion as success mode (no suffixed siblings).
  5. An optional final-message file (`--final-message <path>`) is provided; if so, the script `grep`s for the LOOP-02 honest-failure tokens (`Failed PNG:`, `Source:`, `Report:`, `Outstanding issues:`) AND asserts the message does NOT contain the forbidden tokens (`done`, `completed`, `successfully`, `ready`). If no `--final-message` is supplied, the script prints a "checkpoint:human-verify" reminder for the operator and exits 0 on the artefact-side asserts alone.
- **D3-09:** Exit codes: `0` = all asserts hold; `1` = at least one assert failed (script prints which); `2` = bad invocation (missing args, unknown mode). The script never modifies files — it only reads.
- **D3-10:** The script lives at `scripts/e2e_check.sh` (peer of `verifier_self_test.sh`, NOT inside `fixtures/`). This mirrors Phase 1's helper-vs-fixtures placement: scripts under `scripts/`, fixtures under `fixtures/`.

### Run Protocol (`fixtures/e2e/README.md`)
- **D3-11:** The operator protocol is a numbered checklist:
  1. Copy `fixtures/e2e/scenarios/<name>/seed.excalidraw` (if present) → `fixtures/e2e/working/<name>.excalidraw`. Create `fixtures/e2e/working/` on first run; it is git-ignored (Phase 3 commits the seeds, not the working copies).
  2. Spawn an interactive Claude Code session in the project root.
  3. Paste the `REQUEST.md` body verbatim. If the request references a seed, the operator includes the absolute path to the working copy in the prompt.
  4. Wait for the specialist's loop to settle (success message OR honest-failure template).
  5. Save the specialist's final assistant message to `fixtures/e2e/working/<name>.final-message.txt` (operator copy-paste).
  6. Run `bash scripts/e2e_check.sh fixtures/e2e/working/<name>.excalidraw --mode <success|honest-failure> --final-message fixtures/e2e/working/<name>.final-message.txt`.
  7. Record the result in `fixtures/e2e/working/EVIDENCE.md` (one line per scenario: `[YYYY-MM-DD] <name>: <mode> → <exit-code> <notes>`).
- **D3-12:** `fixtures/e2e/working/` and `fixtures/e2e/working/EVIDENCE.md` are NOT committed — they are operator-side artefacts that re-fill on each Phase-3 re-run. A short `.gitignore` entry under `fixtures/e2e/` excludes them. The committed surface is the scenario corpus + the protocol README + the check script.
- **D3-13:** The protocol is operator-driven by design — automating the specialist subagent spawn from a shell script would require a Claude Code SDK harness, which is out of scope per PROJECT.md ("CI harness running verifier on every plugin change — Out of Scope"). The operator-driven protocol is the v1 stance.

### Seed Design Discipline
- **D3-14:** `text-overflow-self-heal/seed.excalidraw` is byte-for-byte similar to `fixtures/verifier/text-overflow/text-overflow.excalidraw` (same defect, same dimensions). Reusing the verifier fixture's defect ensures Phase 1 + Phase 3 share a known-flagged defect. The Phase 3 seed lives at its own path so the verifier fixture remains a Phase 1 oracle (operator must not work on the Phase 1 fixture directly — it is read-only test data).
- **D3-15:** `under-specified-honest-failure/seed.excalidraw` is hand-authored to trip the `arrow_endpoint_unanchored` check on multiple arrows simultaneously, with shape coordinates spaced so straightforward "snap to nearest border" fixes still leave at least one arrow unanchored. The seed must produce `passed: false` on a verifier dry-run before Phase 3 ships — the check script's `honest-failure` mode is meaningless if the loop accidentally converges. The seed is verified by running `python3 scripts/verifier_structural.py <seed>` at fixture-author time and recording the issue count in the scenario's `README.md`.

### What "Validates" Means at Phase 3 Granularity
- **D3-16:** Phase 3 "validation" is *artefact validation*, not *behavioural simulation*. The check script confirms the loop's outputs look right; the operator confirms the loop's narrative looks right (attempt counters, verifier delegations, fix mutations). The combined evidence — green check-script run + a short operator note in `EVIDENCE.md` — is sufficient signal to mark the v1 milestone shippable. A future v2 hardening phase could automate this with a Claude Code SDK harness if needed (see HARD-NN in Deferred Items).
- **D3-17:** The 03-01-SUMMARY documents which scenarios were exercised manually before commit (a single Phase-3 fixture-author run, recorded inline). Subsequent re-runs by other operators land in `fixtures/e2e/working/EVIDENCE.md` (git-ignored), not in the SUMMARY.

### Claude's Discretion
- The exact wording of each `REQUEST.md` (must include the working-copy path placeholder and the user-intent prose; otherwise free).
- The exact element ids and coordinates inside `under-specified-honest-failure/seed.excalidraw`, as long as the structural verifier flags ≥2 `arrow_endpoint_unanchored` errors on the seed.
- The check script's internal organization (one bash function per assert vs. inline asserts vs. case statement) — what matters is the contract in D3-07 + D3-08 + D3-09.
- Whether to include a fourth "happy-path-only" scenario (e.g., a known-good request that converges on verify-call #1). The three above already cover the four ROADMAP success criteria; a fourth is allowed but not required.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (planner + executor) MUST read these before authoring scenarios or the check script.**

### Phase Scope & Requirements
- `.planning/PROJECT.md` — core value (no silent broken diagrams); Out of Scope explicitly excludes CI harnesses (this is why D3-13 keeps the protocol operator-driven).
- `.planning/REQUIREMENTS.md` §v1 — VRFY-01, VRFY-02, LOOP-01, LOOP-02, LOOP-03, CONT-01 (Phase 3 validates ALL six end-to-end).
- `.planning/ROADMAP.md` §Phase 3 — the 4 success criteria. Criterion #1 maps to `text-overflow-self-heal`, #2 to `emoji-as-icon`, #3 to `under-specified-honest-failure`, #4 to all three via `e2e_check.sh`'s artefact-discipline assertions.

### Phase 1 + Phase 2 Outputs (the surface Phase 3 exercises)
- `excalidraw_specialist.md` — frozen contract; do NOT edit. The honest-failure template in `<verification_loop>` block G defines the grep tokens for D3-08.
- `excalidraw_verifier.md` — frozen contract; do NOT edit. Its `<output_contract>` defines the report schema for D3-07/D3-08.
- `scripts/verifier_structural.py` — used during fixture authoring to confirm seeds trigger the expected structural checks.
- `scripts/validate_and_render.sh` — invoked by the specialist (not by Phase 3 directly). Phase 3 assumes Docker is available, per existing PROJECT.md Constraints.
- `fixtures/verifier/text-overflow/text-overflow.excalidraw` — pattern source for the Phase 3 text-overflow seed (per D3-14).

### Existing Conventions
- `scripts/verifier_self_test.sh` — the bash-script style + structure the new `scripts/e2e_check.sh` follows (header comment, argparse pattern, `PASS:`/`FAIL:` per-assert line, final `Summary:` line, exit on fail count).
- `fixtures/verifier/` directory layout — the parallel pattern for `fixtures/e2e/scenarios/`.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/verifier_self_test.sh` (Phase 1) — bash structure template for `scripts/e2e_check.sh`. Same header, same `SCRIPT_DIR`/`AGENT_DIR` derivation, same `PASS:`/`FAIL:` reporting style. Diff: e2e_check.sh takes a single working file + mode flag (not a fixture name).
- `fixtures/verifier/text-overflow/text-overflow.excalidraw` (Phase 1) — copy this verbatim into `fixtures/e2e/scenarios/text-overflow-self-heal/seed.excalidraw` (per D3-14). The defect (label width 312px > container 180px) is exactly what the Phase 3 self-heal scenario needs.
- The verifier's report schema is documented in `excalidraw_verifier.md` `<output_contract>` — the check script's JSON-schema asserts inline this schema; no need to re-derive.
- The specialist's honest-failure template is documented verbatim in `excalidraw_specialist.md` `<verification_loop>` block G — the check script's `grep`s use those exact label tokens.
- `icons/success_icon.png`, `icons/failure_icon.png` exist (verified inline) — the emoji scenario maps to `success_icon.png`.

### Established Patterns
- **Fixtures under `fixtures/<phase-feature>/`, helpers under `scripts/`.** Phase 1 followed this; Phase 3 mirrors it (`fixtures/e2e/`, `scripts/e2e_check.sh`).
- **Bash scripts use `SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"` + `AGENT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"` for portability.** Phase 3's check script reuses this idiom.
- **Operator-driven manual checkpoints are an accepted deliverable.** Phase 1 explicitly deferred Task 4 ("manual end-to-end checkpoint") as operator-driven; Phase 3 makes the operator-driven protocol the *primary* deliverable, not a deferred one, because Phase 3's nature is end-to-end exercise.

### Integration Points
- **The specialist invokes the verifier by NAME.** Operator copies of the working file MUST live at an absolute path the specialist can pass through (`fixtures/e2e/working/<name>.excalidraw` resolves to absolute via the project CWD). The check script accepts either relative or absolute paths and normalizes via `realpath`.
- **The verifier writes `<basename>.verifier-report.json` next to the source.** The check script reads this file directly — no need to grep the specialist's final message for the report contents.
- **The 3-attempt cap is enforced inside the specialist's prompt, not by Phase 3 tooling.** The check script only observes the END state (success or honest-failure) — it does NOT count attempts. The operator confirms attempt counters in the narrative.

</code_context>

<specifics>
## Specific Ideas

- **Check-script anti-false-positive: empty `<basename>.png`.** A render failure could leave a 0-byte `<basename>.png` on disk (theoretical — `validate_and_render.sh` exits on render failure, so this is unlikely). The check script's PNG-existence assert MUST also check the file size is > 0 to catch this edge case.

- **Check-script anti-false-positive: stale verifier report.** If the operator re-runs a scenario without first clearing `fixtures/e2e/working/<name>.*`, an OLD report could satisfy the asserts. The check script's `checked_at` field in the report is parsed and compared against the `<basename>.excalidraw` mtime — the report MUST be at least as new as the source. This catches stale reports without forcing the operator to nuke `working/` between runs.

- **Forbidden-token grep is case-insensitive but word-bounded.** `grep -iE '\b(done|completed|successfully|ready)\b'` — case-insensitive (catches `Done`, `READY`, etc.) AND word-bounded (the substring `ready` in a quoted JSON like `"already"` does NOT trigger). The check script documents this in a comment so a future maintainer doesn't "fix" the regex.

- **`under-specified-honest-failure/seed.excalidraw` design.** Make it 5 small rectangles in a star pattern with 5 elbow arrows whose endpoint coordinates land in empty space ~50 px from any shape. The user request says "connect these but DON'T move or resize any rectangle". The specialist's fix space is bounded — it can only move arrow endpoints, but the constraint that 2+ arrows must share a target shape forces overlapping or wrong-side endpoint moves. After 3 attempts the verifier should still flag ≥1 `arrow_endpoint_unanchored`. Verify this by running the helper on the seed before committing — record the expected issue count in the scenario README.

- **The `EVIDENCE.md` template** lives in `fixtures/e2e/README.md` as a code fence — operators copy it on first run rather than committing an empty file. Format:
  ```
  | Date       | Scenario                          | Mode             | Check exit | Notes |
  |------------|-----------------------------------|------------------|------------|-------|
  | 2026-MM-DD | text-overflow-self-heal           | success          | 0          |       |
  | 2026-MM-DD | emoji-as-icon                     | success          | 0          |       |
  | 2026-MM-DD | under-specified-honest-failure    | honest-failure   | 0          |       |
  ```

- **First-run smoke check (fixture-author time).** Before committing the Phase 3 deliverables, the author runs each scenario's check script against a HYPOTHETICAL working directory populated with placeholder artefacts (a minimal valid `.excalidraw` + a 1-pixel `.png` + a hand-authored report) to confirm the check script's asserts fire correctly (false positive on missing-PNG; true negative on stale report). This is documented in the SUMMARY as "smoke-tested fixture-author-time; real specialist-loop runs deferred to operator-driven runs".

</specifics>

<deferred>
## Deferred Ideas

- **SDK-driven harness that spawns the specialist subagent and waits for the loop to settle.** This would let Phase 3 ship as a green CI badge. Out of scope for v1 per PROJECT.md ("CI harness running verifier on every plugin change — Out of Scope"). Revisit as a v2 hardening item (HARD-04?) if the operator-driven protocol proves too slow.

- **Telemetry: a fourth scenario that intentionally oscillates** (specialist applies the same fix twice). Useful signal that the specialist's fix mechanics need a "previous fix log" mechanism. Deferred — the 3-attempt cap is a sufficient ceiling for v1; oscillation is a quality concern, not a correctness one.

- **Cross-scenario assertion: aggregate check script** that runs all three scenarios' `e2e_check.sh` invocations and produces a single PASS/FAIL summary like `verifier_self_test.sh`. Worth ~30 lines of bash, but requires the working copies to be present — which means the operator has already run all three scenarios manually. Defer until operator feedback says aggregation would be valuable.

- **Recording the specialist's narrative trace (attempt counters, fix descriptions) to `fixtures/e2e/working/<name>.transcript.md`** for richer post-hoc analysis. Operator-side niceity; orthogonal to Phase 3's correctness gate. Defer.

- **Editing the specialist's prompt based on Phase-3 discoveries.** If the loop never reaches honest-failure on the under-specified scenario (e.g., the specialist learns to refuse the user request instead of looping), that surfaces a real specialist-prompt bug — but the fix lives in a NEW Phase 2.x insertion, not in Phase 3. Phase 3 ships its scenarios + check script regardless of any prompt drift discovered during execution.

</deferred>

---

*Phase: 03-End-to-End Closed-Loop Validation*
*Context gathered: 2026-05-24*
