# Bad example — the failure modes this system exists to prevent

## Input evidence given to the model

Same input as `examples/good/founder_led_boutique.md` — Northlight Films.

## What a bad output looks like

```json
{
  "company": "Northlight Films",
  "studio_archetype": "creative studio",
  "operating_model": "Founder-led boutique, small passionate team",
  "studio_personality": ["Award-winning", "Innovative", "Craft-focused"],
  "creative_dna": ["Apparel"],
  "visual_dna": ["Beautiful cinematography with stunning, high-quality visuals throughout"],
  "decision_maker": "The creative team",
  "buyer_personality": ["Values quality and creativity"],
  "most_distinctive_insight": "Award-winning, passionate, visual storytellers",
  "colorkaar_angle": "Colorkaar can help elevate their already amazing work with our world-class grading services",
  "conversation_starter": "Loved your work on the outdoor apparel campaigns!",
  "avoid": [],
  "why_this_lead": ["They make great content"],
  "outreach_priority": "Immediate",
  "evidence_strength": "Strong",
  "reasoning": "This is clearly a top-tier creative studio."
}
```

## Every rule this violates

- `operating_model` restates `studio_archetype` ("Founder-led boutique")
  instead of naming a distinct structural fact, and phrases it as a
  sentence with filler ("small passionate team") instead of picking one
  value from the closed vocabulary (Owner-operated, Creative partnership,
  Director-led collective, Agency-owned production arm, In-house production
  team, Independent production company, Multi-founder studio). Like
  `studio_personality`, the real schema would reject this outright now that
  `operating_model` is enum-constrained.
- `decision_maker` is "The creative team" — vague and not a role at all.
  It should be something specific like "Founder/Director," and should never
  contain the contact's actual name either way (the lead database already
  has it).
- `studio_personality` uses "Award-winning" and "Craft-focused" — neither
  is in the closed vocabulary (`Independent, Boutique, Hands-on,
  Relationship-driven, Structured, Collaborative, Scalable, Experimental,
  Image-first`). The real API schema would reject this outright; this
  example shows what it looks like when a prompt doesn't enforce the list.
- `creative_dna` is `["Apparel"]` — not in the closed vocabulary either, and
  even if it were, "Apparel" restates the client's product, not a creative
  specialty. It should be something like `["Outdoor"]` per the good example
  — Outdoor-as-creative-passion, not Apparel-as-client-industry.
- `visual_dna` is a full sentence with filler ("beautiful... stunning,
  high-quality") instead of 1-3 tags from the closed vocabulary. The
  compression rule and the controlled vocabulary both exist specifically to
  prevent this.
- `most_distinctive_insight` is a list of three banned adjectives, not one
  concrete observation. This is the single most important rule in the whole
  system and this example breaks it directly.
- `colorkaar_angle` is a full sentence with a compliment and "world-class" —
  the target is 3-8 words, e.g. "A long-term partner, not a vendor."
- `conversation_starter` is "Loved your work" — the exact banned phrase
  named in `prompts/system.md`.
- `why_this_lead` ("They make great content") isn't a synthesis of
  anything above it — it doesn't reference founder-led, image-first, or any
  other concrete fact. It reads like a rating, not a case.
- `avoid` is empty with no attempt to actually think about what would
  misread the room for this company.
- `evidence_strength: "Strong"` is unjustified — nothing here is actually
  more directly stated than in the good example, it's just written more
  confidently. Evidence strength should track what's actually in the
  evidence, not how enthusiastically the field is phrased.
- `reasoning` doesn't explain anything — "clearly a top-tier creative
  studio" is not a reason, it's a restatement of the inflated priority.

If an analyzer run ever produces something that reads like this, the fix is
in `prompts/system.md` or `schemas/intelligence.schema.json`, not in
hand-editing the row.
