---
type: seed
status: open
created: 2026-06-07
source: /gsd-explore — review of github.com/coleam00/excalidraw-diagram-skill
related_milestone: v1.1 (or later)
---

# Seed: Borrow the few genuinely-useful bits from coleam00/excalidraw-diagram-skill

## Context

Reviewed `github.com/coleam00/excalidraw-diagram-skill` (a single-file SKILL.md +
references/) to find anything worth complementing our multi-agent excalidraw system with.

**Headline:** ~95% is the same philosophy we already implement, and OUR version is more
mature (closed render→verify→fix loop with an independent verifier vs. their manual
self-review checklist; richer 10-semantic + brand palette; per-pattern kb/ layer they
lack; Docker renderer + separate validator + structural checks). Their docs are a
condensed restatement of what we already have — not a source of new methodology.

## The few things worth borrowing (priority order)

### 1. Concept→Pattern selector table (HIGHEST value — confirmed missing from our kb)
They have a "If the concept... use this pattern" lookup that routes a concept to a visual
pattern BEFORE you open any pattern file. Our `kb/README.md` has NO such selector — we jump
straight to pattern implementations. Grep confirmed: no concept→pattern routing exists.

Proposed: add a routing table to `kb/README.md` (or specialist `<drawing_methodology>`):

| If the concept...          | Use pattern        | kb file              |
|----------------------------|--------------------|----------------------|
| Spawns multiple outputs    | Fan-out            | fan-out.md           |
| Combines inputs into one   | Convergence        | convergence.md       |
| Sequence of steps          | Linear pipeline / timeline | linear-pipeline.md / timeline.md |
| Loops / improves           | Feedback loop      | feedback-loop.md     |
| Has hierarchy / nesting    | Tree               | tree-hierarchy.md    |
| Decision / condition       | Decision branch/marker | decision-*.md    |
| Compares two things        | Side-by-side       | (NEW — see #2)       |
| Abstract state / context   | Cloud              | (NEW — see #3)       |

### 2. side-by-side.md (NEW pattern — confirmed missing)
Comparison pattern: two parallel structures with visual contrast (before/after, options,
trade-offs). We have no comparison primitive. Cheap to author following the existing kb
file shape (purpose / coordinate math / JSON skeleton / "See in examples").

### 3. cloud.md (NEW pattern — confirmed missing)
Abstract-state pattern: overlapping ellipses for context/memory/fuzzy state. We have no
abstract-state primitive. Lower priority than side-by-side (less common in technical
architecture diagrams, which are our core families).

### 4. Explicit "Simple vs Comprehensive" depth gate (nice-to-have)
A pre-flight decision: does this diagram need abstract shapes (mental model) or concrete
evidence artifacts (real system)? Their §"Depth Assessment" makes this an explicit Step 0.
Our specialist jumps more directly to drawing; an explicit gate could improve when it pulls
in evidence-card.md vs. stays lean. Could live in `<drawing_methodology>`.

## Explicitly NOT worth taking

- Their philosophy / palette / element-templates / json-schema / renderer — we have
  superior versions of all of these.
- Their manual render-view-fix self-review loop — our independent verifier is strictly
  better (avoids the confirmation bias their single-agent loop is exposed to).
- Their "don't write a Python generator / don't use a coding agent" warnings — anti-patterns
  specific to their single-file approach; irrelevant to our architecture.

## Open questions before promoting

- Bundle items #1–#4 into one small "kb-vocabulary-expansion" phase, or fold #2/#3 into the
  next diagram-type phase that needs them?
- Author side-by-side/cloud only when a real diagram demands them (demand-driven), or
  proactively for completeness?

## Related
- See `replace-example-pngs-with-composition-specs.md` (sibling seed from same session).
