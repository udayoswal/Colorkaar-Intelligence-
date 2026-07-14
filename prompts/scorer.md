# Relationship score & priority rubric

This is not sent to the model. It's the deterministic rubric `src/score.py`
implements — documented here so it's a single source of truth you can tune
without touching code, and code that keeps `score.py` honest to what's
written here.

## The question the score answers

Not "how much revenue could this lead generate." The question is:

> Would Uday genuinely enjoy working with them?

## Base score by studio archetype

| `studio_archetype` (matched loosely, case-insensitive) | `relationship_score` |
|---|---|
| DP-led (director/cinematographer partnership) | 98 |
| Founder-led boutique | 95 |
| Agency | 82 |
| Huge production company | 71 |
| Unknown / insufficient evidence | 30 |

`src/score.py` matches on keywords in `studio_archetype`, so the model can
phrase it naturally ("founder-led boutique studio", "DP-led shop") and still
hit the right bucket. Anything that doesn't match a known archetype falls
back to "unknown" (30) rather than guessing.

## Priority tiers

| Priority | Meaning | Score threshold |
|---|---|---|
| A+ | Immediate outreach | ≥ 95 |
| A | Very high quality | ≥ 85 |
| B | Worth contacting | ≥ 65 |
| C | Generic | ≥ 40 |
| D | Skip | < 40 |

## The confidence gate

A high score built on thin evidence is worse than no score. If `confidence`
(as reported by the analyzer) is below 40, priority is capped:

- score ≥ 60 → capped at C ("worth a second look once we know more, not an
  immediate send")
- score < 60 → D

This is the mechanical version of "confidence matters more than coverage" —
a studio that *looks* DP-led from a two-line description doesn't get an A+
just because the archetype match was lucky.

## Why this isn't the model's job

The model's own `relationship_score`/`priority` proposal is kept on the
record as `llm_relationship_score` / `llm_priority` — useful for spotting
where the model's instinct disagrees with the rubric, which is exactly the
kind of thing you want to notice during the "review the first 25" step. But
the exported number always comes from this table, because a fixed rubric is
auditable and can be re-tuned in one place, instead of re-prompting 1,469
leads every time the definition of "A+" changes.
