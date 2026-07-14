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
  "operating_model": ["Founder-led boutique", "Owner-operated"],
  "studio_personality": ["Independent", "Hands-on", "Relationship-driven"],
  "creative_dna": ["Naturalistic", "Restrained"],
  "visual_dna": ["Desaturated", "High-contrast", "Clean"],
  "decision_maker": "Founder (Mara)",
  "buyer_personality": ["Relationship-driven", "Fast decisions"],
  "human_angle": "Founder still shoots",
  "colorkaar_angle": "A long-term partner, not a vendor",
  "conversation_starter": "Developing a consistent look on location",
  "avoid": ["Volume framing", "Sales process"],
  "why_this_lead": ["Founder-led", "Image-first", "No visible in-house grading", "Relationship-driven"],
  "outreach_priority": "High",
  "confidence": "Medium",
  "reasoning": "Two-person structure and founder-as-director are both directly stated, so human_angle is high-confidence. Visual DNA is inferred from a described look, not seen footage, so overall confidence is Medium rather than High."
}
```

This is good because: `human_angle` is exactly one concrete thing, not a
list of adjectives. `colorkaar_angle` is four words, not a sentence that
explains itself. `creative_dna` is aesthetic ("Naturalistic," "Restrained")
rather than market ("outdoor," "apparel") — the market context lives in the
raw evidence, not in this field. Every array field is short tags, not
clauses. `confidence` and `outreach_priority` are categories, not numbers.
Nothing here mentions awards, named clients, or "storytelling."
