# Bad example — over-conservative UNKNOWN (the bug this version fixes)

Same input as `examples/good/thin_evidence_still_useful.md` — Lakeview
Reel Co, where the only evidence is the company name and a contact name
with no title.

## What the over-conservative output looked like

```json
{
  "company": "Lakeview Reel Co",
  "studio_archetype": "unknown",
  "operating_model": "UNKNOWN",
  "studio_personality": [],
  "creative_dna": [],
  "visual_dna": [],
  "decision_maker": "UNKNOWN",
  "buyer_personality": [],
  "most_distinctive_insight": "UNKNOWN",
  "colorkaar_angle": "UNKNOWN",
  "conversation_starter": "UNKNOWN",
  "avoid": [],
  "why_this_lead": [],
  "outreach_priority": "Low",
  "evidence_strength": "Low",
  "reasoning": "Insufficient evidence."
}
```

## Why this is wrong

Every field defaulted to UNKNOWN/empty except `outreach_priority` and
`evidence_strength` (which was still called "Low" — the old, three-value
confidence scale, not the current evidence-strength framing). But there
*was* something to work with: the company name is "Lakeview Reel Co" — the
word "Reel" is real, if faint, evidence that this is a video/production
business. That single signal is enough to clear step 2 of the reasoning
ladder for `studio_archetype`, `most_distinctive_insight`, and
`why_this_lead`. Treating "the description field is empty" as equivalent
to "there is no evidence anywhere, including in the company's own name"
was the exact bug: it confused *caution about hallucinating specific
facts* with *refusal to draw any inference at all*. Nine of the first 25
real leads run through this version came back looking almost exactly like
this — not because the leads were all equally hopeless, but because the
model stopped reasoning the moment the description field was blank.

`reasoning: "Insufficient evidence."` is itself a symptom — it doesn't
even attempt a Fact → Inference → Insight trace, because there was no
inference step being performed at all.

If an analyzer run ever produces a wall of UNKNOWNs like this on rows that
have *any* signal — a company name, a job title — the fix is in
`prompts/system.md` → "The reasoning ladder," not in hand-editing the row.
