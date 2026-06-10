# Deferred Items — Phase 09 (data-vault)

Out-of-scope discoveries logged during execution. Not fixed in this phase (SCOPE BOUNDARY:
only issues directly caused by the current task's changes are auto-fixed).

## DEF-09-01: use_case_checkout.excalidraw emits 18 elbow-routing warnings

- **Discovered during:** 09-03 Task 3 (end-to-end structural regression)
- **File:** `.claude/agents/excalidraw/examples_excalidraw/use_case_checkout.excalidraw`
- **Finding:** `verifier_structural.py` returns 18 `warning`-severity issues (9 ×
  `arrow_points_too_few`, 9 × `arrow_not_elbow`) on the use-case association arrows
  (`assoc_*`, `rel_include_*`, `rel_extend_*`). The arrows are straight 2-point connectors
  lacking `elbowed: true` and the ≥3-point form.
- **Severity:** all 18 are `warning` (NOT `error`); the verifier process exits 0. Use-case
  actor→oval associations are conventionally straight lines, so the elbow warning is
  arguably a false positive for this diagram type — but the plan's stricter acceptance
  criterion is `issues == []`, which this example does not meet.
- **Pre-existing:** confirmed present at the Phase 9 wave-3 base commit `5ff640e` (18 issues
  before any wave-3 work). NOT introduced by 09-03 — this plan only edited markdown
  (resolver table + kb back-refs), no `.excalidraw` source.
- **Why deferred:** out of 09-03's scope. Fixing it would mutate a Phase-8 canonical
  example and require fresh EX-03 visual re-approval (the example is wired ground truth the
  specialist imitates). That is a separate remediation, not a markdown-wiring plan's job.
- **Recommended resolution:** either (a) add a verifier exemption so straight actor→oval
  use-case associations are not flagged for elbow routing, or (b) re-author the
  associations with the 3-point elbow form and re-clear EX-03. Track as a Phase-8
  follow-up / hardening item.
