---
phase: 5
slug: tech-architecture-activity
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-04
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | bash / Python (existing validate + render + verify scripts) |
| **Config file** | none — existing scripts used directly |
| **Quick run command** | `bash .claude/agents/excalidraw/scripts/validate_excalidraw.sh <file>` |
| **Full suite command** | `python .claude/agents/excalidraw/scripts/excalidraw_validator.py <file> && python .claude/agents/excalidraw/verifier_structural.py <file>` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run quick validate on any produced `.excalidraw` file
- **After every plan wave:** Run full validate→render→verify loop on canonical examples
- **Before `/gsd-verify-work`:** Full suite must be green for all canonical examples
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | ARCH-01 | — | N/A | file-existence | `test -f diagram-types/tech-architecture.md` | ✅ | ⬜ pending |
| 05-01-02 | 01 | 1 | ARCH-01 | — | N/A | file-content | `grep -q "Used by types" .claude/agents/excalidraw/kb/*.md` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 1 | UML-04 | — | N/A | file-existence | `test -f diagram-types/activity.md` | ❌ W0 | ⬜ pending |
| 05-02-02 | 02 | 2 | UML-04 | — | N/A | render-loop | `python .claude/agents/excalidraw/scripts/excalidraw_validator.py <activity.excalidraw> && python .claude/agents/excalidraw/verifier_structural.py <activity.excalidraw>` | ❌ W0 | ⬜ pending |
| 05-02-03 | 02 | 2 | UML-04 | — | N/A | file-existence | `grep -q "activity" diagram-types/README.md` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `diagram-types/activity.md` — recipe file for Activity diagram type
- [ ] `diagram-types/tech-architecture.md` — verify back-refs + resolver row
- [ ] Canonical Activity example `.excalidraw` + rendered PNG
- [ ] `diagram-types/README.md` updated with both type entries

*Existing validate/render/verify infrastructure covers all automated checks.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Activity diagram with swimlanes renders correctly | UML-04 | Visual layout verification | Author an activity diagram with 2 swimlanes, render to PNG, inspect lanes are distinct and flow arrows stay within lane boundaries |
| Tech-architecture back-refs are discoverable | ARCH-01 | Prose/link audit | Open each referenced `kb/*.md` primitive, confirm "Used by types: tech-architecture" appears |

---

## Validation Architecture

The validation loop for diagram-type files is:
1. **Markdown lint** — verify the `.md` file has required sections (Header, When to use, Composition, Excalidraw recipe, Example)
2. **Resolver table** — confirm the type slug appears in the resolver/dispatch table
3. **Excalidraw validator** — `excalidraw_validator.py` passes on the canonical `.excalidraw`
4. **Render** — PNG produced by render script
5. **Verifier** — `verifier_structural.py` passes (no `arrow_endpoint_unanchored`, no `text_missing_dimensions`, no `layout_collision`)
6. **README index** — `diagram-types/README.md` contains entry for the type

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
