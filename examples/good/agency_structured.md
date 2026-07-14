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
  "operating_model": "In-house production team",
  "studio_personality": ["Structured", "Collaborative", "Scalable"],
  "creative_dna": ["Corporate"],
  "visual_dna": [],
  "decision_maker": "Head of Production",
  "buyer_personality": ["Process-driven", "Schedule-driven"],
  "most_distinctive_insight": "Full-service agency, no fixed house style",
  "colorkaar_angle": "Reliable finishing across a varied roster",
  "conversation_starter": "How do you keep finishing consistent when the visual style changes brief to brief?",
  "avoid": ["Don't pitch a single signature look", "Don't lead with a founder-to-founder pitch"],
  "why_this_lead": ["Agency-scale volume", "Needs reliable capacity, not a signature look", "Process-driven buyer"],
  "outreach_priority": "Medium",
  "evidence_strength": "Moderate",
  "reasoning": "Fact: mid-size agency, in-house production and post, explicitly no consistent visual signature. Inference: a Head of Production as primary contact signals a process-driven buying pattern, not a founder relationship. Insight: their genuinely distinctive trait is the deliberate absence of a house style, which is worth naming rather than leaving as an empty field."
}
```

(Computed afterward: `outreach_objective` for an agency archetype is
"Become a finishing partner.")

This shows two things at once. First, the honest contrast with the
founder-led example: `operating_model` is "In-house production team," not
"Owner-operated" — a genuinely different structural fact, from the same
closed vocabulary. `decision_maker` is "Head of Production," not a name.
`studio_personality` is "Structured, Collaborative, Scalable" instead of
"Independent, Hands-on" — real work distinguishing how you'd approach this
lead differently. Second, and more important given where the first version
of this system went wrong: `visual_dna` is correctly an empty array (the
evidence explicitly says there's no consistent signature — a genuine dead
end for that specific closed vocabulary), but `most_distinctive_insight` is
NOT left at UNKNOWN just because there's no founder story here. "No fixed
house style" is itself a real, distinctive, evidence-backed trait — the
reasoning ladder found something meaningful even though nothing unique
jumped out.
