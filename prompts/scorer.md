# Outreach priority rubric

This is not sent to the model. It's the deterministic rubric `src/score.py`
implements — documented here so it's a single source of truth you can tune
without touching code, and code that keeps `score.py` honest to what's
written here.

## The question the score answers

Not "how much revenue could this lead generate." The question is:

> Would Uday genuinely enjoy working with them?

There is deliberately no numeric score anywhere in this system.
`relationship_score` (0-100) was tried and removed — it read as precise but
was really an opinion, and a number invites treating "93" and "95" as
meaningfully different when they aren't. `outreach_priority` is a category,
not a score.

## Outreach priority = f(studio archetype, evidence strength)

| `studio_archetype` (matched loosely, case-insensitive) | Strong evidence | Moderate evidence | Weak evidence |
|---|---|---|---|
| DP-led (director/cinematographer partnership) | Immediate | High | Medium |
| Founder-led boutique | Immediate | High | Medium |
| Agency | High | Medium | Low |
| Production company (generic, size/structure unconfirmed) | Medium | Medium | Low |
| Huge production company | Medium | Low | Low |
| Unknown / no archetype match | Low | Low | Low |

`src/score.py` matches on keywords in `studio_archetype`, so the model can
phrase it naturally ("founder-led boutique studio," "DP-led shop") and
still hit the right row. The "production company" row exists specifically
so a plain, evidence-backed "this is a production company, but I don't know
if it's a boutique or a huge shop" doesn't collapse into "unknown" priority
— it's real signal, just not enough to place it at the top or bottom of the
table. Anything that doesn't match a known archetype falls back to the
"Unknown" row rather than guessing.

This is the mechanical version of "confidence matters more than coverage" —
a studio that *looks* DP-led from a two-line description doesn't get
Immediate priority just because the archetype match was lucky; Weak
evidence pulls every archetype down by at least one tier. Note this table
is deliberately **less punishing on Weak evidence than the old version
was** — `evidence_strength: Weak` no longer means the model was allowed to
leave fields blank, so a Weak-evidence row is a real, if generic,
characterization rather than an empty one, and its priority reflects that.

## Why this isn't the model's job

The model's own `outreach_priority` proposal is kept on the record as
`llm_outreach_priority` — useful for spotting where the model's instinct
disagrees with the rubric, which is exactly the kind of thing you want to
notice during the "review the first 25" step. But the exported priority
always comes from this table, because a fixed rubric is auditable and can
be re-tuned in one place, instead of re-prompting 1,469 leads every time the
definition of "Immediate" changes.

`llm_outreach_priority` lives in `output/lead_intelligence.scored.jsonl` for
that audit purpose only — `src/export.py` deliberately drops it from the
final CSV. The exported deliverable has one column for priority, not two.
