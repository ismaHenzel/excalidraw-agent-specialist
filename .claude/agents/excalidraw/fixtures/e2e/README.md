# End-to-End Closed-Loop Validation Harness

This directory exercises the Excalidraw closed-loop specialist (`excalidraw_specialist`) end-to-end against representative defect cases. It is the **acceptance gate** for the v1 milestone — see `.planning/ROADMAP.md` §Phase 3 for the four success criteria validated here.

## Layout

```
fixtures/e2e/
├── README.md                       # this file — operator protocol + EVIDENCE.md template
├── .gitignore                       # excludes working/
├── working/                         # OPERATOR-SIDE; git-ignored; created on first run
│   ├── <scenario>.excalidraw         # working copy the specialist mutates
│   ├── <scenario>.png                # latest render
│   ├── <scenario>.verifier-report.json
│   ├── <scenario>.final-message.txt  # operator copy-pastes the specialist's last message
│   └── EVIDENCE.md                   # operator records of each scenario run
└── scenarios/                       # COMMITTED; the seed corpus
    ├── text-overflow-self-heal/
    │   ├── REQUEST.md                # user-facing prompt to paste verbatim
    │   ├── README.md                 # success criteria + check-script invocation
    │   └── seed.excalidraw           # defective starting file
    ├── emoji-as-icon/
    │   ├── REQUEST.md                # specialist authors from scratch — no seed
    │   └── README.md
    └── under-specified-honest-failure/
        ├── REQUEST.md
        ├── README.md
        └── seed.excalidraw
```

The check script lives at `scripts/e2e/e2e_check.sh`, not inside this directory. Its sibling helpers — the render pipeline at `scripts/render/` and the verifier helper + self-test at `scripts/verifier/` — are grouped the same way.

## Operator protocol

Run each scenario inside an **interactive Claude Code session** rooted at the project working directory. The specialist subagent cannot be spawned from a shell script (no SDK harness in v1 — see PROJECT.md §Out of Scope).

1. **Copy the seed.** If the scenario directory contains a `seed.excalidraw`, copy it into `working/`:

   ```bash
   mkdir -p fixtures/e2e/working
   cp fixtures/e2e/scenarios/<scenario>/seed.excalidraw \
      fixtures/e2e/working/<scenario>.excalidraw
   ```

   For `emoji-as-icon` (no seed), skip this step — the specialist will author the file from scratch.

2. **Open a Claude Code session** at the project root. Ensure the `excalidraw_specialist` and `excalidraw_verifier` subagents are discoverable (check `claude doctor` if unsure).

3. **Paste the request.** Open `fixtures/e2e/scenarios/<scenario>/REQUEST.md`, copy everything below the horizontal rule, and paste it into the session. Substitute `<ABSOLUTE_PATH_TO_WORKING_COPY>` with the absolute path to the working file (the path printed by `realpath fixtures/e2e/working/<scenario>.excalidraw`).

4. **Wait for the loop to settle.** The specialist will run its render → verify → fix cycle. The session ends when the specialist either:
   - delivers a success message citing the rendered PNG (mode `success`), OR
   - emits the LOOP-02 honest-failure template starting with `Verifier failed after 3 attempts.` (mode `honest-failure`).

5. **Save the final assistant message.** Copy the specialist's last message into a text file:

   ```bash
   # paste the message body into this file
   ${EDITOR:-vi} fixtures/e2e/working/<scenario>.final-message.txt
   ```

6. **Run the check script.** Use the exact invocation documented in the scenario's README:

   ```bash
   bash scripts/e2e/e2e_check.sh \
     fixtures/e2e/working/<scenario>.excalidraw \
     --mode <success|honest-failure> \
     --final-message fixtures/e2e/working/<scenario>.final-message.txt
   ```

   Expect: all `PASS:` lines and `Summary: 0 fail`. Any `FAIL:` line indicates the loop's output diverged from the scenario's expectations.

7. **Record the result.** Append a row to `fixtures/e2e/working/EVIDENCE.md` (create the file on first run using the template below):

   ```markdown
   | Date       | Scenario                          | Mode             | Check exit | Notes |
   |------------|-----------------------------------|------------------|------------|-------|
   | 2026-MM-DD | text-overflow-self-heal           | success          | 0          |       |
   | 2026-MM-DD | emoji-as-icon                     | success          | 0          |       |
   | 2026-MM-DD | under-specified-honest-failure    | honest-failure   | 0          |       |
   ```

   The file is git-ignored — it's an operator-side log, not committed history.

## Troubleshooting

- **`STALE: report checked_at is older than source mtime`** — the verifier report on disk is from a previous run. Clear `working/<scenario>.*` and re-run the scenario from step 1.
- **Exit-code legend:** `0` = all asserts hold; `1` = at least one assert failed (script prints which); `2` = bad invocation (missing args, wrong `--mode`, path without `.excalidraw` extension).
- **`final-message contains forbidden success token(s)`** — the specialist's honest-failure path leaked a `done`/`completed`/`successfully`/`ready` token. This is a specialist-prompt bug; file a Phase 2.x insertion to tighten `<verification_loop>` block G's token ban.
- **Specialist accidentally converged on `under-specified-honest-failure`** — the seed wasn't stubborn enough OR the specialist relaxed the user's constraint. Re-check the seed with `python3 scripts/verifier/verifier_structural.py fixtures/e2e/scenarios/under-specified-honest-failure/seed.excalidraw` — it should still report 5 `arrow_endpoint_unanchored` errors. If the seed is correct, the prompt regressed.
- **Adding a new scenario** — create `scenarios/<new-name>/{REQUEST.md,README.md,[seed.excalidraw]}` following the existing pattern. No changes to the check script are needed; it is scenario-agnostic.
