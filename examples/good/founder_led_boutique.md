# Good example — founder-led boutique

## Input evidence given to the model

Company: Northlight Films (fictional, sample data)
Description: Two-person commercial studio. Founder shoots most projects
personally.
Website summary: Portfolio is mostly outdoor apparel and gear brands, shot
on location. Consistent muted, desaturated look across projects.
Contact name: Mara Lindqvist
Contact title: Founder / Director
Visual style notes: Cool color temperature, high contrast, minimal color
grading visible — looks close to camera-native.
Projects: Outdoor apparel campaigns, a handful of documentary shorts.

## Why this output is good

```json
{
  "company": "Northlight Films",
  "studio_archetype": "founder-led boutique",
  "operating_model": "Owner-operated",
  "studio_personality": ["Independent", "Hands-on", "Relationship-driven"],
  "creative_dna": ["Outdoor"],
  "visual_dna": ["Naturalistic", "Raw"],
  "decision_maker": "Founder (Mara)",
  "buyer_personality": ["Relationship-driven", "Founder-led"],
  "most_distinctive_insight": "Founder still shoots",
  "colorkaar_angle": "A long-term partner, not a vendor",
  "conversation_starter": "Developing a consistent look on location",
  "avoid": ["Volume framing", "Sales process"],
  "why_this_lead": ["Founder-led", "Image-first", "No visible in-house grading", "Relationship-driven"],
  "outreach_priority": "High",
  "evidence_strength": "Moderate",
  "reasoning": "Fact: two-person structure, founder shoots personally, on-location apparel/gear work. Inference: consistent desaturated look implies a deliberate, maintained visual identity rather than one-off styling. Insight: founder still shoots, which is the strongest and most specific thing about them."
}
```

This is good because: `most_distinctive_insight` is exactly one concrete
thing, not a list of adjectives. `colorkaar_angle` is four words, not a
sentence that explains itself. `operating_model` is "Owner-operated," not a
restatement of `studio_archetype` — the founder-led-boutique fact is
already carried by `studio_archetype`, so this field earns its place with
something new. `creative_dna`, `visual_dna`, `studio_personality`, and
`buyer_personality` are each drawn from the closed vocabulary in
`prompts/system.md` — nothing invented, nothing outside the list.
`evidence_strength` and `outreach_priority` are categories, not numbers.
Nothing here mentions awards, named clients, or "storytelling."
