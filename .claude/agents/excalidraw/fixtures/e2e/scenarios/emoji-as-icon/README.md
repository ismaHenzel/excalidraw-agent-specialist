# Scenario: emoji-as-icon

## Maps to

- **ROADMAP §Phase 3 SC#2** — "Running the specialist on a request that asks for an emoji glyph … delivers a rendered PNG where the glyph is a brand/functional icon from `icons/`, not a missing-glyph box."
- **REQUIREMENTS exercised:** CONT-01 (generation-side emoji-to-icon mapping), VRFY-01 (structural `raw_emoji_in_text` check confirms compliance), LOOP-01 (always-render), LOOP-03 (artefact discipline).

## Expected loop trajectory

1. Specialist consults `<content_policy>` mapping table: "checkmark" → `icons/success_icon.png`.
2. Specialist authors the source `.excalidraw` with an `image` element pointing at `success_icon.png` (NOT a `text` element containing `✅`).
3. `validate_and_render.sh` produces a sibling PNG.
4. `verify(1)` runs — structural `raw_emoji_in_text` is silent (no raw codepoint); visual `missing_glyph_box` is silent (the checkmark is a rendered PNG, not a tofu box) → `passed: true`.

Total attempts: 1. Mode: `success`.

This scenario is the happy-path validator for the closed loop: the specialist's content policy works at generation time, the verifier confirms it, no fix iteration is needed.

## Expected check-script invocation

After the specialist run settles and the operator has saved the final assistant message to `working/emoji-as-icon.final-message.txt`:

```bash
bash scripts/e2e/e2e_check.sh \
  fixtures/e2e/working/emoji-as-icon.excalidraw \
  --mode success \
  --final-message fixtures/e2e/working/emoji-as-icon.final-message.txt
```

Expect: all `PASS:` lines, `Summary: 0 fail`, exit 0.

## Fixture-author smoke notes

No seed file — the specialist starts from scratch. No `verifier_structural.py` invocation possible at fixture-author time.

Operator-side sanity check (post-run): grep the produced `.excalidraw` for raw emoji codepoints and the `image` element. If raw codepoint present → the specialist's `<content_policy>` regressed → file a Phase 2.x insertion.

```bash
# Should return zero matches:
grep -P '[\x{2700}-\x{27BF}\x{1F300}-\x{1FAFF}]' fixtures/e2e/working/emoji-as-icon.excalidraw

# Should return at least one match:
grep -F 'success_icon.png' fixtures/e2e/working/emoji-as-icon.excalidraw
```
