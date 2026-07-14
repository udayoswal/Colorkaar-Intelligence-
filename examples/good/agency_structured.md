# Good example — structured agency (contrast case for studio_personality)

## Input evidence given to the model

Company: Bright Field Collective (fictional, sample data)
Description: Mid-size creative agency offering production and post
in-house.
Website summary: Broad range of commercial clients, generalist look, varies
by project.
Contact name: Priya Anand
Contact title: Head of Production
Visual style notes: No consistent visual signature across projects; varies
by client brief.
Projects: Retail and tech brand campaigns.

## Why this output is good

```json
{
  "company": "Bright Field Collective",
  "studio_archetype": "agency",
  "operating_model": "In-house production and post",
  "studio_personality": ["Structured", "Collaborative", "Scalable"],
  "creative_dna": ["Corporate"],
  "visual_dna": [],
  "decision_maker": "Head of Production (Priya)",
  "buyer_personality": ["Process-driven", "Schedule-driven"],
  "human_angle": "UNKNOWN",
  "colorkaar_angle": "Reliable finishing across a varied roster",
  "conversation_starter": "Finishing capacity for varied campaign work",
  "avoid": ["Single-look framing", "Founder-to-founder pitch"],
  "why_this_lead": ["Agency-scale volume", "Needs reliable capacity, not a signature look", "Process-driven buyer"],
  "outreach_priority": "Medium",
  "confidence": "Medium",
  "reasoning": "Operating model and decision-maker are directly stated. No visual signature is stated, so visual_dna is correctly left empty rather than invented, and human_angle is UNKNOWN rather than a forced compliment. creative_dna landed on Corporate as the closest closed-vocabulary fit for a generalist retail/tech client roster, not because either client industry is itself a creative specialty."
}
```

This is good because it shows the honest alternative to the founder-led
example: `studio_personality` is "Structured, Collaborative, Scalable"
instead of "Independent, Hands-on" — the field is doing real work
distinguishing how you'd approach this lead differently. `visual_dna` is an
empty array, not filler, because the evidence explicitly says there's no
consistent signature. `human_angle` is UNKNOWN rather than invented. This
lead is still worth contacting (`outreach_priority: Medium`) — it's just a
different kind of relationship than a boutique.
