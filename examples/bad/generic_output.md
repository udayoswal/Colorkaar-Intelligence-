# Bad example — the failure modes this system exists to prevent

## Input evidence given to the model

Same input as `examples/good/founder_led_boutique.md` — Northlight Films.

## What a bad output looks like

```json
{
  "company": "Northlight Films",
  "studio_archetype": "creative studio",
  "operating_model": ["A passionate, innovative team of visual storytellers who bring creativity to every project"],
  "studio_personality": ["Award-winning", "Innovative"],
  "creative_dna": ["Outdoor", "Apparel"],
  "visual_dna": ["Beautiful cinematography with stunning, high-quality visuals throughout"],
  "decision_maker": "The creative team",
  "buyer_personality": ["Values quality and creativity"],
  "human_angle": "Award-winning, passionate, visual storytellers",
  "colorkaar_angle": "Colorkaar can help elevate their already amazing work with our world-class grading services",
  "conversation_starter": "Loved your work on the outdoor apparel campaigns!",
  "avoid": [],
  "why_this_lead": ["They make great content"],
  "outreach_priority": "Immediate",
  "confidence": "High",
  "reasoning": "This is clearly a top-tier creative studio."
}
```

## Every rule this violates

- `creative_dna` is `["Outdoor", "Apparel"]` — that's market, not aesthetic.
  It describes what their clients sell, not how the studio sees. It should
  be something like `["Naturalistic", "Restrained"]`.
- `operating_model` and `visual_dna` are full sentences with filler
  ("passionate, innovative team," "beautiful cinematography... stunning,
  high-quality") instead of 2-4 short tags. The compression rule exists
  specifically to prevent this.
- `studio_personality` is two banned adjectives ("Award-winning,"
  "Innovative"), not a description of how you'd actually work with them.
- `human_angle` is a list of three banned adjectives, not one concrete
  observation. This is the single most important rule in the whole system
  and this example breaks it directly.
- `colorkaar_angle` is a full sentence with a compliment and "world-class" —
  the target is 3-8 words, e.g. "A long-term partner, not a vendor."
- `conversation_starter` is "Loved your work" — the exact banned phrase
  named in `prompts/system.md`.
- `why_this_lead` ("They make great content") isn't a synthesis of
  anything above it — it doesn't reference founder-led, image-first, or any
  other concrete fact. It reads like a rating, not a case.
- `avoid` is empty with no attempt to actually think about what would
  misread the room for this company.
- `confidence: "High"` is unjustified — nothing here is actually more
  certain than the good example, it's just written more confidently.
  Confidence should track evidence, not enthusiasm — and a categorical
  confidence value doesn't get a pass on this just because it isn't a raw
  number anymore.
- `reasoning` doesn't explain anything — "clearly a top-tier creative
  studio" is not a reason, it's a restatement of the inflated priority.

If an analyzer run ever produces something that reads like this, the fix is
in `prompts/system.md`, not in hand-editing the row.
