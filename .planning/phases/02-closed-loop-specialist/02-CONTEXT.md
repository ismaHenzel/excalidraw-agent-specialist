# Phase 2: Closed-Loop Specialist Integration - Context

**Gathered:** 2026-05-24
**Status:** Ready for planning
**Depends on:** Phase 1 (verifier subagent + structural helper shipped)

<domain>
## Phase Boundary

Revise the **existing** `excalidraw_specialist.md` subagent so that **every** diagram delivery flows through a mandatory render → verify → fix loop that closes on a verifier-approved PNG (or honestly surfaces failure after 3 attempts). The deliverable is a single edited file plus a small accompanying delivery checklist; no new scripts, no new fixtures.

Concretely, after this phase the specialist's prompt:

1. Forbids any path that delivers a `.excalidraw` without a sibling `.png` produced by `scripts/validate_and_render.sh`.
2. Forbids raw Unicode emoji codepoints in `text` elements at generation time — the agent maps emoji requests to `image` elements pointing at `icons/*.png`.
3. After rendering, mandatorily spawns the `excalidraw_verifier` subagent on the source `.excalidraw` (single absolute-path arg, per Phase 1's D-13 contract).
4. Reads the canonical sibling `<basename>.verifier-report.json` (Phase 1's D-01), parses it as JSON, and branches on `passed`.
5. On `passed: false`, mutates the source JSON using the issues' `suggested_fix` hints, re-runs `validate_and_render.sh`, and re-spawns the verifier — capped at **3 total verify attempts** (the initial verify + up to 2 fix-and-reverify cycles).
6. On a 3rd-attempt failure, emits a final user message that contains (a) the failed PNG absolute path, (b) the full structured issue list copied from the report, (c) the source `.excalidraw` absolute path — and explicitly does NOT claim success.
7. Maintains "sibling-only, overwrite-each-iteration" artefact discipline: after any iteration only `<basename>.excalidraw`, `<basename>.png`, and `<basename>.verifier-report.json` exist next to each other; no `.v1`, `.v2`, `_iter1`, or numbered-fix artefacts ever land on disk.

Out of this phase: building the verifier (Phase 1, shipped), end-to-end validation across representative defect fixtures (Phase 3), MCP-canvas tooling reform, vendoring the Excalidraw bundle (HARD-01, deferred to v2).

</domain>

<decisions>
## Implementation Decisions

### Edit Surface
- **D2-01:** The phase modifies exactly ONE existing file: `.claude/agents/excalidraw/excalidraw_specialist.md`. No other source-code changes. The verifier subagent file, the structural helper, the render scripts, and the KB are read but not edited.
- **D2-02:** YAML frontmatter (`name`, `description`, `tools`) is NOT touched. The specialist's existing `tools:` list (`Read, Bash, Grep, Glob, mcp__excalidraw__*`) already covers everything the loop needs: `Bash` runs `validate_and_render.sh`, `Read` opens the verifier report, MCP tools stay for canvas-side discretion. The `Task` tool is intentionally NOT added — subagent delegation in Claude Code happens via the natural-language delegation mechanism described in the subagent docs, not via an explicit tool. The specialist's prompt instructs it to delegate to `excalidraw_verifier` by name; Claude's delegation router handles the spawn.
- **D2-03:** Section ordering inside the agent body remains the existing seven XML-tagged sections (`<role>` → `<capabilities>` → `<asset_paths>` → `<visual_standards>` → `<drawing_methodology>` → `<style_principles>` → `<operational_mandates>`), PLUS two NEW sections inserted between `<style_principles>` and `<operational_mandates>`:
  - `<content_policy>` — the emoji-as-icon rule and other generation-time content constraints.
  - `<verification_loop>` — the mandatory render-verify-fix loop, the 3-iteration cap, the artefact-discipline rules, and the structured 3rd-failure delivery format.
  Operational mandates remain last because they are the imperatives the agent reads on every turn; the new sections supply the policy that the revised mandates reference.

### The 3-Iteration Cap — Exact Semantics
- **D2-04:** "3 iterations" means **3 total verifier invocations**, equivalently the initial verify plus up to 2 fix-and-reverify cycles. Concretely the sequence is:

  ```
  generate.v0  → render → verify(1)  ── passed:true ──► DELIVER
                                     ── passed:false ─┐
                                                      ▼
  fix → render → verify(2)  ── passed:true ──► DELIVER
                            ── passed:false ─┐
                                             ▼
  fix → render → verify(3)  ── passed:true ──► DELIVER
                            ── passed:false ──► HONEST-FAILURE message
  ```

  The "3rd attempt" criterion in ROADMAP success criterion #3 is satisfied by the third call to the verifier. The counter advances on each verify call, not on each fix application.
- **D2-05:** The specialist tracks the attempt counter mentally (it's a finite small integer in its context). No persistent counter file. If the agent ever loses track of the count it MUST default to honest-failure delivery on the next failed verify rather than looping further — over-counting is the safe direction.
- **D2-06:** A *fix* is a mutation to the source `.excalidraw` JSON only. The specialist re-emits the entire file via `Read` → mental-edit → `Bash` overwrite (e.g., `python3 -c "import json; …"` or `cat <<EOF > path` — whichever the specialist chooses). It does NOT need to keep `.bak` files or use a special tool — the previous PNG/report siblings will be overwritten on the next render+verify, satisfying D2-09.

### Verifier Spawning & Report Consumption
- **D2-07:** The specialist delegates to the verifier by naming the subagent in its instructions (e.g., "Delegate to the excalidraw_verifier subagent with the absolute path `…`"). The verifier's spawn contract per Phase 1 D-13 is a single absolute path to the `.excalidraw` file. The specialist MUST NOT pass the PNG path separately — the verifier derives it.
- **D2-08:** The specialist parses the **sibling `<basename>.verifier-report.json` file** (Phase 1's Channel A), not the verifier's in-message fenced ```json block. Channel A is the canonical machine-readable artefact (Phase 1 D-01). Reading the on-disk JSON is more reliable than re-parsing the verifier's message text, and it survives if the verifier's message is truncated. Concretely the specialist runs `Read` on `<basename>.verifier-report.json`, then mentally parses the JSON, then branches on `passed`. If the report file is missing after the verifier returns, treat it as a verifier internal failure: emit honest-failure to the user citing "verifier did not produce a sibling report".

### Artefact Discipline (LOOP-03)
- **D2-09:** After **any** iteration, the only files that exist next to the `.excalidraw` source are:
  - `<basename>.excalidraw` — the source (latest revision; overwritten in place during fixes).
  - `<basename>.png` — the most recent render (overwritten by the next render).
  - `<basename>.verifier-report.json` — the most recent verifier report (overwritten by the next verify).
  No `<basename>.v1.excalidraw`, no `<basename>_iter1.png`, no `<basename>.report-1.json`, no `.bak` files. The render and verify pipelines already overwrite siblings by default; the agent simply MUST NOT introduce new suffixed siblings during its fix step.
- **D2-10:** If the specialist needs to inspect the previous iteration's diff during a fix, it does so from its own conversation context (it has the previous JSON in its turns) — NOT by reading a `.bak` file from disk. This is consistent with the project's "no test infrastructure / no history clutter" stance (PROJECT.md Out of Scope).

### Emoji Policy at Generation Time (CONT-01 generation half)
- **D2-11:** When the user requests an emoji glyph in a diagram (e.g., "add a check next to the success node", "use a warning emoji here"), the specialist:
  1. `Glob`s `.claude/agents/excalidraw/icons/*.png` to discover available functional icons.
  2. Maps common requests via the table below (the specialist's prompt lists this table verbatim — it is the authoritative generation-side mirror of the verifier's `EMOJI_TO_ICON` dict from Phase 1).
  3. Emits an `image` element pointing at the matching `icons/*.png`, NOT a `text` element with the raw codepoint.
  4. If no matching icon exists, the specialist asks the user which icon they prefer rather than silently inserting a raw codepoint.

  **Generation-side emoji-to-icon table** (must appear verbatim in the specialist prompt):

  | User request    | Codepoint | Icon file                       |
  |-----------------|-----------|---------------------------------|
  | check / success | U+2705 ✅ | `icons/success_icon.png`        |
  | x / fail / no   | U+274C ❌ | `icons/failure_icon.png`        |
  | warning         | U+26A0 ⚠  | `icons/failure_icon.png` (closest available; no dedicated warning icon — see Phase 1 deviation note) |

  Other emojis: the specialist asks the user for an icon choice from `Glob` results rather than guessing.

- **D2-12:** The structural pre-check (`raw_emoji_in_text`, Phase 1) catches anything that slips through. The specialist's prompt explicitly acknowledges this as the safety net but does not lean on it — the policy at generation time is the primary defense.

### Always-Render Mandate (LOOP-01)
- **D2-13:** Every diagram-delivery turn ends with `bash scripts/validate_and_render.sh <path>`. There is NO code path in the revised specialist prompt that says "if the user only asks for JSON, skip rendering". The render is mandatory because the verifier is meaningful only with a PNG, and the verifier is mandatory because LOOP-02 + LOOP-03 require it.
- **D2-14:** The render command is the existing `scripts/validate_and_render.sh` — Phase 2 does NOT modify this script. The existing 3-phase output (validate → render → "now use read_file on the .png") is consumed by the specialist; Phase 3's instructional `echo` line becomes informational only because the verifier subagent supersedes the human-prompted "now read the PNG" step.

### Honest-Failure Delivery Format (LOOP-02 part b)
- **D2-15:** On the 3rd consecutive `passed: false`, the specialist's final user-facing message MUST contain (in this exact order, with these exact labels — caller tooling may grep for them):

  ```
  Verifier failed after 3 attempts. No "done" claim.

  Failed PNG: <absolute path to the latest .png>
  Source:     <absolute path to the .excalidraw>
  Report:     <absolute path to the latest .verifier-report.json>

  Outstanding issues:
  - [<severity>] <check>: <detail>
    suggested_fix: <suggested_fix>
  - [<severity>] <check>: <detail>
    suggested_fix: <suggested_fix>
  ...
  ```

  The bulleted issue list is verbatim from the report's `issues` array. The specialist MUST NOT paraphrase, summarize, or omit issues. It MUST NOT use phrases like "done", "completed", "successfully", or "ready" anywhere in this message — the prompt explicitly bans those tokens in the failure-delivery context.
- **D2-16:** The success-delivery message (`passed: true` within 3 attempts) is the agent's free choice but MUST cite the rendered PNG absolute path so the user can open it. Example: "Diagram rendered and verified at `<path>.png`." This is the only path on which the specialist may use words like "done" or "complete".

### Claude's Discretion
- The exact wording of the new `<content_policy>` and `<verification_loop>` section bodies, as long as every D2-* invariant above is captured and verifiable against the prompt text.
- The precise update to `<operational_mandates>` items #5 ("Local Creation") and #7 ("Iterative Quality via mcp__excalidraw__create_view"). #5 must add the always-render-and-verify clause; #7 must be replaced (or augmented) so the verifier subagent — not the MCP canvas viewer — is the verification authority. The MCP `create_view` tool may stay as a *during-drafting* discretion (helpful for arrow geometry preview), but it is no longer the verification gate.
- Whether to fold the artefact-discipline rule into `<verification_loop>` as a sub-paragraph or to give it its own H2 inside that section. Either is acceptable as long as the rule is discoverable by the agent during a fix.
- The exact prompt phrasing for the JSON-mutation step (e.g., "use `Bash` with `python3 -c …` to mutate the JSON in place" vs. "use `Bash` with `cat` heredoc"). Either approach is consistent with the existing toolset.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents (planner + executor) MUST read these before touching the specialist file.**

### Phase Scope & Requirements
- `.planning/PROJECT.md` — core value (no silent broken diagrams), the eight locked Key Decisions
- `.planning/REQUIREMENTS.md` §v1 — LOOP-01, LOOP-02, LOOP-03, CONT-01 (generation-side half)
- `.planning/ROADMAP.md` §Phase 2 — goal + 5 success criteria (NB: criterion #5 says "only one PNG and at most one verifier-report sibling exist" — match this exactly in D2-09)

### Phase 1 Outputs (the contract the loop consumes)
- `excalidraw_verifier.md` — the verifier subagent (Phase 1 deliverable). Read its `<inputs>` and `<output_contract>` sections to confirm the spawn arg shape and the report schema.
- `scripts/verifier_structural.py` — the structural helper. Read its `EMOJI_TO_ICON` dict to keep the specialist's generation-side mapping in sync with Phase 1's structural enforcement.
- `fixtures/verifier/{good,raw-emoji,text-overflow}/expected-report.json` — concrete examples of the report schema the specialist will parse.
- `scripts/verifier_self_test.sh` — for understanding the diff-ignore convention (`checked_at`, `source`, `png`). Not used at runtime by the specialist.

### Existing Specialist Surface
- `excalidraw_specialist.md` — the file being edited. Read the full file before drafting the edit.
- `.planning/codebase/CONVENTIONS.md` §"Agent definition" — section-ordering doctrine + YAML frontmatter rules. The edit MUST preserve the XML-tag section convention.

### Existing Render Pipeline (read but DO NOT modify)
- `scripts/validate_and_render.sh` — the orchestrator the specialist invokes via `Bash`. Reading it confirms phase output format and exit-code semantics.
- `scripts/render_docker.sh` + `scripts/render_excalidraw.py` — referenced indirectly; the specialist treats them as a black box behind `validate_and_render.sh`.

### Brand-Icon Library (informs the emoji-policy table)
- `icons/*.png` — confirm `success_icon.png` and `failure_icon.png` exist (Phase 1 already verified; re-verify with `ls icons/ | grep -E '(success|failure)_icon'` before publishing the prompt table).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/validate_and_render.sh` — already does the render. The specialist already has `Bash`; invocation is `bash scripts/validate_and_render.sh "<absolute path>"`.
- `excalidraw_verifier.md` — already exists. Spawning is "delegate to the excalidraw_verifier subagent with arg `<path>`"; the specialist's existing `tools:` list does not include `Task` because Claude Code's subagent delegation does not require it (delegation is a runtime affordance, not a tool).
- `<basename>.verifier-report.json` — Phase 1's canonical Channel A. The specialist parses this via `Read`; no new helper is needed to extract the report.
- `excalidraw_specialist.md`'s existing `<operational_mandates>` #5 ("Local Creation") and #7 ("Iterative Quality" via MCP canvas) are the surfaces being revised. Their existing numbering and imperative style is the model for the additions.

### Established Patterns
- **XML-tagged body sections in a fixed order.** Adding two new sections is consistent with the doctrine — they slot between `<style_principles>` and `<operational_mandates>` so policy precedes imperatives (see D2-03).
- **Inlined imperatives in the operational mandates.** The new sections supply the *rules*; the mandates are the *do-this-on-every-turn list*. After the edit, mandate #5 references `<verification_loop>` and mandate #7 references `<verification_loop>` + `<content_policy>`.
- **Relative paths from project working directory.** `<asset_paths>` already establishes that paths are relative to the project CWD (`.claude/agents/excalidraw/...`). The new sections reuse this convention — never hard-code repo-checkout paths.
- **Emoji-glyph rendering reality** (from existing visual_standards): `fontFamily: 3` is the monospace standard but does NOT render colour emoji. The new content policy makes this explicit and points to the icons directory.

### Integration Points
- **The verifier subagent is a peer, not a child.** The specialist delegates to it by name. The specialist's prompt MUST use the verifier's exact YAML `name:` value (`excalidraw_verifier`) so Claude Code's delegation router finds it.
- **The verifier report path is deterministic.** Given source `/abs/foo.excalidraw`, the report is always `/abs/foo.verifier-report.json`. The specialist can construct this path locally and `Read` it directly — no need to scrape the verifier's message for the path.
- **The render output path is deterministic.** Given source `/abs/foo.excalidraw`, the PNG is always `/abs/foo.png` (per `validate_and_render.sh` line 27: `PNG_FILE="${EXCALIDRAW_FILE%.excalidraw}.png"`). The specialist can construct this path locally.
- **The verifier may write a `verifier_internal_error` report.** Per Phase 1's `<failure_modes>`, the verifier always emits a report — even on its own internal failure. The specialist treats `verifier_internal_error` issues the same as other errors for cap-counting purposes: each is a `passed: false` and consumes one of the 3 attempts.

</code_context>

<specifics>
## Specific Ideas

- **Counter mechanics:** the prompt should explicitly tell the agent to track "attempt N of 3" in its own narrative — e.g., after each verify call the agent says (to itself / to the user) "Verifier attempt 1 of 3: passed=true|false". This is a self-anchoring trick that prevents the agent from losing count in long fix-iterations. Caller tooling can grep for the line if it wants telemetry.

- **Fix-application phrasing:** the prompt should NOT specify an exact JSON-mutation mechanism. The agent has `Bash` and can choose between (a) `python3 -c "import json; ..."` for surgical key updates, (b) writing a heredoc to overwrite the whole file, or (c) any other in-process technique. Telling the agent *what* to fix (the issues in the report) is in-scope; telling it *how* to mutate JSON is overreach — leave to discretion.

- **No "go fix it yourself" delegation back to the verifier.** The verifier subagent is read-only by Phase 1 contract (`<role>`: "You REPORT. You never mutate."). The specialist's prompt must make this asymmetry explicit so the specialist never tries to ask the verifier to do the fix.

- **The honest-failure template (D2-15) is grep-friendly.** Match the exact label tokens (`Failed PNG:`, `Source:`, `Report:`, `Outstanding issues:`) so a caller can detect a failure delivery by pattern. The prompt should call out that the labels are stable contract, not free phrasing.

- **MCP canvas tools stay for drafting, not verification.** The specialist's existing `mcp__excalidraw__create_view` is useful during initial layout (the agent can preview a draft on the live canvas before writing the file). Phase 2 does NOT ban this — it just demotes it from "the verification step" to "an optional drafting aid". The new operational mandate #7 should call out this distinction explicitly to prevent the agent from treating canvas-view as a substitute for the render-verify loop.

- **Verifier's own internal errors count toward the 3-attempt cap.** Per D2-08, a missing report file or a `verifier_internal_error` issue is treated as a `passed: false` for cap purposes. The prompt phrases this as: "Any non-`passed:true` outcome — including a missing report or a verifier_internal_error — counts as one attempt." This prevents the specialist from looping infinitely on verifier malfunctions.

</specifics>

<deferred>
## Deferred Ideas

- **Persisting a per-iteration log of `suggested_fix` strings** so the specialist can detect when it's applying the same fix twice. Useful telemetry but out-of-scope for v1 — the 3-attempt cap is the hard ceiling and is sufficient signal that the specialist is stuck. Revisit if Phase 3's E2E validation surfaces oscillation behaviour.

- **Configurable iteration cap.** v1 hard-codes 3. Configurability would mean a settings file or a prompt argument — neither aligns with the "self-contained subagent" architecture. Out of scope.

- **Re-running the static `excalidraw_validator.py` separately during fixes.** The existing pre-render validator already runs as Phase 1 of `validate_and_render.sh` on every iteration; double-invoking it from the specialist would be redundant. Deferred — re-evaluate if validator + verifier ever diverge on rule coverage.

- **Failure-mode taxonomy for the verifier-side outage cases.** Phase 1 ships a single `verifier_internal_error` check; v2 could split into `verifier_helper_crash`, `verifier_read_failed`, `verifier_write_denied`, etc. for richer telemetry. v1 treats them all the same — counted attempt + surfaced as-is.

- **`mcp__excalidraw__export_to_excalidraw` integration as a fix mechanism.** The specialist could export from the live canvas to a file as one of its fix moves. Deferred — adds complexity vs. plain Bash+Python mutation, and the live canvas's state-vs-file divergence is itself a foot-gun.

- **CI harness running the full closed loop on representative defect diagrams** (this is Phase 3, by design — listed here only to flag that Phase 2 does NOT include test-infrastructure work).

</deferred>

---

*Phase: 02-Closed-Loop Specialist Integration*
*Context gathered: 2026-05-24*
