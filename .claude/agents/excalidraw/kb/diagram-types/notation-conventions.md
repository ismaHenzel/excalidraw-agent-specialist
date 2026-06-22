# Notation Conventions — Arrowhead-Workaround House Rules (DTKB-04)

This file LOCKS, once, the single convention the agent must use for every notation that
the fixed Excalidraw arrowhead set cannot express natively. Every relationship-bearing
diagram type (UML class, ER, sequence, use-case, activity) MUST embed or reference this
table so the same ambiguous notation is encoded identically across all diagrams. These
are deliberate house conventions, not approximations chosen ad hoc per diagram.

## Legal arrowhead tokens (the only renderable set)

Excalidraw `0.17.3` exposes exactly five arrowhead values:

    arrow | bar | dot | triangle | null

`null` means "no head". **Any other token (e.g. `crowsfoot`, `diamond`, `hollow`,
`open`) renders SILENTLY as a plain line — no error, no warning** — and the entire
relationship semantics of the diagram vanish (Pitfall 1). Treat any arrowhead value
outside the five legal tokens above as a hard authoring bug. When a relationship needs a
decoration that is not in this set, it MUST be expressed by one of the committed
workarounds below (a composed glyph element or a textual label), never by inventing a
token.

## Committed notation → legal-encoding table

Each row below is the ONE binding convention. Where a choice existed, the
research-recommended default was adopted and the alternative is explicitly NOT used so
diagrams stay mutually consistent.

| Notation | Committed legal encoding |
|---|---|
| Association / message direction | `endArrowhead: "arrow"`, solid stroke. |
| Dependency / return message | `endArrowhead: "arrow"` + `strokeStyle: "dashed"`. |
| Generalization (inheritance) | `endArrowhead: "triangle"` — **FILLED** (house convention; NOT hollow, because no hollow-triangle token exists). |
| Realization | `endArrowhead: "triangle"` + `strokeStyle: "dashed"`. |
| Aggregation | A small (~14px) composed `diamond` element grouped at the OWNER end — **white fill**. |
| Composition | A small (~14px) composed `diamond` element grouped at the owner end — **solid fill**. |
| ER "one" | `endArrowhead: "bar"`. |
| ER "zero / optional" | `endArrowhead: "dot"`, or a small composed `ellipse` glyph at the endpoint. |
| ER "many" (crow's-foot) | **COMMITTED DEFAULT: textual multiplicity label** (`0..*` / `1..*`) placed at the endpoint. The grouped 3-line crow's-foot glyph is the alternative and is **NOT used** — pick the textual form everywhere so cardinality reads consistently and never collapses to a plain line. |
| Actor | **COMMITTED DEFAULT: a labelled box** (rectangle + text label, e.g. `«actor» Customer`). The stick-figure composed glyph is **NOT used**. |
| Multiplicity (general) | Textual labels — `1`, `0..*`, `1..*` — wherever a dedicated glyph is not committed above. |

## Why these are committed, not suggested

- A filled triangle for generalization is a deliberate substitution for the standard
  hollow triangle; surface it to the user as a house convention when relevant
  ("inheritance shown as a filled triangle — Excalidraw lacks a hollow head").
- Mixing crow's-foot glyphs and textual multiplicity across diagrams looks like a bug;
  the textual default is chosen once and used everywhere.
- The labelled-box actor avoids fragile stick-figure geometry and stays legible under
  the monospace-only `fontFamily: 3` constraint.

## Scope of this file

This file fixes the CONVENTION CHOICE only. Exact glyph PIXEL GEOMETRY — crow's-foot
stroke sizing/rotation (should the default ever change), diamond exact dimensions and
placement offset, ellipse glyph size — is DEFERRED to the phase that first ships the
ER / Class types (Phase 7). Each affected later type file must embed or reference this
table verbatim rather than re-deriving its own encoding, so the conventions cannot
silently drift between diagram types.
