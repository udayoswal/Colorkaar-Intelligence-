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
  "operating_model": "Small team, founder-directed, founder shoots personally",
  "creative_dna": ["Outdoor/apparel specialist", "Location-first production"],
  "visual_dna": ["Cool, desaturated, high-contrast look", "Minimal visible grading"],
  "decision_maker": "Founder (Mara) — creative and business decisions likely sit with one person",
  "buyer_personality": "Likely values a direct relationship over a sales process; small team means fast decisions",
  "human_angle": "Founder still shoots",
  "colorkaar_angle": "Founder to founder — a long-term grading partner who understands the look rather than a vendor",
  "conversation_starter": "Developing a consistent look across location-shot work",
  "avoid": ["High-volume commercial throughput pitch — this is a boutique, not a volume shop"],
  "priority": "A",
  "relationship_score": 93,
  "confidence": 78,
  "reasoning": "Two-person structure and founder-as-director are both directly stated, so human_angle is high-confidence. Visual DNA is inferred from the described look, not from seeing actual footage, so confidence is not higher than 78."
}
```

This is good because: `human_angle` is exactly one concrete thing ("Founder
still shoots"), not a list of adjectives. `colorkaar_angle` maps founder to
founder — specific to this company's structure, not a generic pitch.
`conversation_starter` is a real topic, not a compliment. Nothing here
mentions awards, named clients, or "storytelling."
