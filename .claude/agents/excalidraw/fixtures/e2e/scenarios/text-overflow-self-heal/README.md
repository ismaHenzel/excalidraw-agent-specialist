# Scenario: text-overflow-self-heal

## Maps to

- **ROADMAP §Phase 3 SC#1** — "Running the specialist on a request that historically produced text-overflow output now delivers a rendered PNG with text fitting its container, achieved within 3 verify-fix iterations."
- **REQUIREMENTS exercised:** LOOP-01 (always-render), LOOP-02 (auto-fix within 3 attempts), LOOP-03 (artefact discipline), VRFY-01 (structural pre-check fires `text_overflow_static`), VRFY-02 (structured report consumed by specialist).

## Expected loop trajectory

1. `verify(1)` fires `text_overflow_static` on element id `t_db` — `passed: false`.
2. Specialist applies the fix from the report's `suggested_fix` field: widens `r_container` from 180 to ≥332, OR shortens the `t_db` label.
3. `verify(2)` returns `passed: true` → specialist delivers via block H ("Diagram rendered and verified at …").

Total attempts: ≤ 2. Mode: `success`.

## Expected check-script invocation

After the specialist run settles and the operator has saved the final assistant message to `working/text-overflow-self-heal.final-message.txt`:

```bash
bash scripts/e2e/e2e_check.sh \
  fixtures/e2e/working/text-overflow-self-heal.excalidraw \
  --mode success \
  --final-message fixtures/e2e/working/text-overflow-self-heal.final-message.txt
```

Expect: all `PASS:` lines, `Summary: 0 fail`, exit 0.

## Fixture-author smoke notes

`python3 scripts/verifier/verifier_structural.py fixtures/e2e/scenarios/text-overflow-self-heal/seed.excalidraw` on commit day returns:

| count | check                  | severity |
|-------|------------------------|----------|
| 1     | `text_overflow_static` | error    |

The seed is a byte-similar copy of `fixtures/verifier/text-overflow/text-overflow.excalidraw` (Phase 1 fixture). Keeping them parallel means a fix to either side's defect detection is detectable from a single re-run.
