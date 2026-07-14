# Good example — thin evidence, but the ladder still finds something

This is the case the reasoning ladder exists for. An earlier version of
this system saw evidence this thin and returned UNKNOWN across almost
every field. That was wrong — not because the profile should pretend to
know more than it does, but because it stopped one step too early.

## Input evidence given to the model

Company: Lakeview Reel Co (fictional, sample data)
Description: (none given)
Website summary: (none given)
Contact name: Priya Nathan
Contact title: (none given)
Visual style notes: (none given)
Projects: (none given)

That's genuinely all there is: a company name and a contact name. No
description, no title, no visual notes, no size, no location.

## Why this output is good

```json
{
  "company": "Lakeview Reel Co",
  "studio_archetype": "production company",
  "operating_model": "UNKNOWN",
  "studio_personality": [],
  "creative_dna": [],
  "visual_dna": [],
  "decision_maker": "UNKNOWN",
  "buyer_personality": [],
  "most_distinctive_insight": "Small, likely emerging production company",
  "colorkaar_angle": "UNKNOWN",
  "conversation_starter": "UNKNOWN",
  "avoid": [],
  "why_this_lead": ["Company name signals video/production work", "No other evidence yet - needs research before outreach"],
  "outreach_priority": "Low",
  "evidence_strength": "Weak",
  "reasoning": "Fact: the only evidence is the company name, 'Lakeview Reel Co,' and a contact name with no title. Inference: 'Reel Co' is a real, if faint, typological signal - a company doesn't call itself that unless it's in video/production. There's no signal at all for structure or decision-maker role, so those stay UNKNOWN rather than guessed. Insight: still a production company, just an unconfirmed and probably small one - stated plainly rather than left blank."
}
```

(Computed afterward: `outreach_objective` for "production company" is "Open
a vendor conversation," and `outreach_priority` recomputes to "Low" given
Weak evidence.)

This is the difference the ladder makes. `studio_archetype`,
`most_distinctive_insight`, and `why_this_lead` all have real content
instead of UNKNOWN, because "Reel Co" in a self-chosen company name is
real signal — step 2 of the ladder (a meaningful inference from what *is*
there). But `operating_model`, `decision_maker`, `studio_personality`, and
`buyer_personality` are correctly UNKNOWN/empty, because there is
genuinely nothing — not even a job title — to run the ladder on for those.
`conversation_starter` and `colorkaar_angle` also correctly stay UNKNOWN:
there's nothing specific enough here for a real question or a real angle,
and a generic one would be filler, not insight — different from the
classification fields, which have a legitimate generic-but-true fallback.
`evidence_strength: "Weak"` carries the honesty; it is not achieved by
leaving fields blank.
