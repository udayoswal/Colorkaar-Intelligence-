# Bad example — the failure mode this system exists to prevent

## Input evidence given to the model

Same input as `examples/good/founder_led_boutique.md` — Northlight Films.

## What a bad output looks like

```json
{
  "company": "Northlight Films",
  "studio_archetype": "creative studio",
  "operating_model": "A passionate, innovative team of visual storytellers",
  "creative_dna": ["Award-winning", "High quality", "Creative"],
  "visual_dna": ["Beautiful cinematography", "Stunning visuals"],
  "decision_maker": "The creative team",
  "buyer_personality": "Values quality and creativity",
  "human_angle": "Award-winning, passionate, visual storytellers",
  "colorkaar_angle": "Colorkaar can help elevate their already amazing work",
  "conversation_starter": "Loved your work on the outdoor apparel campaigns!",
  "avoid": [],
  "priority": "A+",
  "relationship_score": 99,
  "confidence": 95,
  "reasoning": "This is clearly a top-tier creative studio."
}
```

## Every rule this violates

- `studio_archetype`, `operating_model`, `creative_dna`, `visual_dna` are all
  generic filler ("passionate," "innovative," "visual storytellers," "award-
  winning," "stunning") — none of it is specific to Northlight Films. It
  could describe any studio in the input file.
- `human_angle` is a list of three banned adjectives, not one concrete
  observation. This is the single most important rule in the whole system
  and this example breaks it directly.
- `colorkaar_angle` is a compliment ("already amazing work"), not a mapping
  from who they are to why Colorkaar matters.
- `conversation_starter` is "Loved your work" — the exact banned phrase
  named in `prompts/system.md`.
- `avoid` is empty with no attempt to actually think about what would
  misread the room for this company.
- `confidence: 95` is unjustified — nothing here is actually more certain
  than the good example, it's just written more confidently. Confidence
  should track evidence, not enthusiasm.
- `reasoning` doesn't explain anything — "clearly a top-tier creative
  studio" is not a reason, it's a restatement of the inflated score.

If an analyzer run ever produces something that reads like this, the fix is
in `prompts/system.md`, not in hand-editing the row.
