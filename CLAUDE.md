# Colorkaar Lead Intelligence Database

This is not an email enrichment tool. It's a database of who Colorkaar's
leads actually are — the kind of asset that keeps compounding in value
across outreach, networking, proposals, and client development, long after
any one email template has been rewritten. The core pipeline builds and
scores that database and stops there; it does not generate emails. Optimize
for one question: could a new employee at Colorkaar open a row and
immediately understand how to approach this company?

This file is how Claude (and any engineer) should think about this
repository. It is not how Claude should write — that's `prompts/email.md`.
This is how Claude should *understand*.

## Mission

You are not an email writer. You are a Business Development Strategist for
Colorkaar, a boutique color grading and finishing studio. Your job is to
understand creative businesses well enough that a producer could trust your
read on them — and to write that understanding down as something scannable,
like a CRM card, not a report.

- You never invent a *specific* fact — a named client, an award, a number,
  a size claim — that isn't in the evidence. You do not shy away from a
  *reasonable, clearly-labeled inference* from real signal, even thin
  signal (a company name, a job title). Refusing to infer is not the same
  virtue as refusing to hallucinate — see `prompts/system.md` → "Facts,
  inference, and hallucination."
- When evidence is weak, you say so via `evidence_strength` — you do not
  leave the field blank. UNKNOWN is a last resort after the reasoning
  ladder is exhausted, not a default.
- You never compliment unless there is a genuine, specific reason.
- You never mention awards, named clients, or campaigns unless doing so
  materially strengthens the relationship (rare — almost never).
- You always optimize for long-term relationships over short-term replies.
- Think like a producer. Write like a filmmaker.
- **The shorter a field is, the more useful it is.** If a field reads like
  a sentence explaining itself, it's wrong. See `prompts/system.md` →
  "The compression rule."

The single most important sentence in this whole repo:

> **Personalization comes from WHO THEY ARE, not WHAT THEY MAKE.**

Everything else — the schema, the scoring rubric, the email rules — exists to
protect that sentence from drifting into generic AI-written outreach.

## This is a product, not a prompt

The engine is split into discrete, inspectable, independently-improvable
stages. The core pipeline is three stages — understand, score, export — and
that's the whole deliverable:

| Stage | Script | Input | Output | Job |
|---|---|---|---|---|
| Analyze | `src/analyze.py` | `input/enriched_leads.csv` | `output/lead_intelligence.raw.jsonl` | Understand the company. LLM call, structured JSON output. |
| Score | `src/score.py` | `*.raw.jsonl` | `*.scored.jsonl` | Apply the outreach-priority rubric **deterministically**, in code — not vibes, not a second LLM call. |
| Export | `src/export.py` | `*.scored.jsonl` | `output/lead_intelligence.csv` | Drop the `reasoning` debug field, produce the deliverable CSV. |

`src/generate_email.py` still exists and still works, but it is **not part
of the core workflow** — the database is not organized around producing
emails, and the default run (see README) stops after `export.py`. Run it
by hand later, per lead or per batch, when you actually need a specific
email — treat it as a consumer of the database, not a pipeline stage.

Scoring is deliberately **not** left to the model, and it is deliberately
**not a number**. `studio_archetype` × `evidence_strength` → `outreach_priority`
(Immediate / High / Medium / Low) is a fixed lookup table in `src/score.py`
(mirrored in `prompts/scorer.md`). There is no `relationship_score` field —
an earlier version had one (0-100) and it was cut on purpose: a number
implies a precision that doesn't exist and invites treating "93" and "95"
as meaningfully different when they aren't. The model still proposes a
priority as part of its analysis (useful signal, kept in the record as
`llm_outreach_priority`), but the exported priority always comes from the
rubric. This is what makes the scoring auditable and tunable without
re-prompting 1,469 leads every time you want to change what "Immediate"
means.

## The `reasoning` field

Every analyzer and email record carries a `reasoning` field — a short
Fact → Inference → Insight trace explaining *why* the model chose the most
distinctive insight, the Colorkaar angle, or the tone it used. This field
is for debugging only. It
is never shown to the recipient and it is dropped by `src/export.py` before
the final CSVs are written. If you're unhappy with an output, `reasoning` is
the first place to look.

## The iteration discipline (read this before running on all 1,469 leads)

Do not process the whole lead list on day one. The workflow is:

1. Build/adjust the engine.
2. Run it on the first 25 leads only (`--limit 25`, the default).
3. Read every row. Out loud, if it helps. Ask: "Is this exactly how I'd
   describe this company?"
4. When something is off — a generic Most Distinctive Insight, a wall of
   UNKNOWNs on rows that actually had some signal, a Conversation Starter
   that's too vague — fix the prompt or the schema, not the individual
   output. Add a good/bad example to `examples/` if it'll help future runs.
   The first real pass at this system erred toward too many UNKNOWNs by
   treating "not explicitly stated" the same as "no evidence at all" — see
   `prompts/system.md` → "The reasoning ladder" for the fix. If UNKNOWN
   starts creeping back in on rows that have a company name, a job title,
   or a one-line description to work with, that's the same bug recurring.
5. Only once 25/25 feel right, increase `--limit` and keep going in batches.

That loop — not the first draft of the prompt — is where the quality comes
from.

## Project structure

```
CLAUDE.md                  — this file
README.md                  — setup + how to run
prompts/
  system.md                — the durable system prompt for the analyzer (cached, stable)
  analyzer.md               — per-lead user-message template for the analyzer
  scorer.md                  — the outreach-priority rubric (mirrors src/score.py)
  email.md                   — [optional, not core] system prompt + user template for email generation
schemas/
  intelligence.schema.json   — structured-output schema for the analyzer
  email.schema.json          — [optional, not core] structured-output schema for email generation
examples/
  good/                       — few-shot examples of intelligence the bar is set to
  bad/                        — few-shot counter-examples, with the violated rule named
  emails/                     — [optional, not core] a reference email
input/
  enriched_leads.csv          — your real lead list goes here (not committed with real data)
output/                       — generated; gitignored except for structure
src/
  client.py                   — thin Anthropic API wrapper (structured outputs, caching)
  prompts.py                  — loads prompts/*.md, splits SYSTEM / USER_TEMPLATE sections
  analyze.py                  — stage 1
  score.py                    — stage 2 (deterministic)
  export.py                   — stage 3 (the pipeline ends here)
  generate_email.py           — [optional, not core] run by hand per lead/batch when you need an email
```

## Rules that must never regress

Never mention: awards, festival selections, named clients, random campaigns,
"storytelling," "passion," "innovation," "creativity" as a description of the
lead. If you catch the model doing this, it's a prompt bug — fix
`prompts/system.md`, don't patch the output by hand.

`most_distinctive_insight` (formerly "Human Angle") is exactly one thing,
not three. "Founder-led boutique" is good. "Award-winning, passionate,
visual storytellers" is the failure mode this whole system exists to
prevent. But "distinctive" does not mean "rare" or "explicitly stated" —
it means the strongest insight the reasoning ladder can reach. UNKNOWN for
this field should be rare, not the default outcome for any row without a
paragraph of description.

UNKNOWN is a last resort, not a hedge. Two failure modes bracket this
field, and both are real: inventing a specific fact with no evidence
behind it, and refusing to infer anything from evidence that's merely
thin rather than absent. The first version of this system over-corrected
into the second failure mode — nine of the first 25 real rows came back
UNKNOWN across the board, several of them for companies whose own name
("1 Lab Productions," "72 Films") was sitting right there as evidence.
`prompts/system.md` → "The reasoning ladder" is the fix; if UNKNOWN rates
climb again, that's the regression to check for first.

Never let a field turn back into a sentence. `avoid` and `why_this_lead` are
short tag arrays, free text. `operating_model` is a single short fact — not
an array, and never a restatement of `studio_archetype` (that redundancy
was the whole field's first-draft flaw). `colorkaar_angle` and
`first_email_angle` are phrases, not sentences with an em-dash explaining
themselves. `evidence_strength` and `outreach_priority` are categories
(Strong/Moderate/Weak, Immediate/High/Medium/Low) — never a number, ever
again. `evidence_strength` (formerly "confidence") describes how much of
a profile is fact vs. inference — it is explicitly not permission to leave
fields blank; a Weak-evidence row should still have real values almost
everywhere, just clearly inference-based ones.

`studio_personality`, `creative_dna`, `visual_dna`, and `buyer_personality`
are **closed vocabularies**, enforced as JSON Schema `enum`s in
`schemas/intelligence.schema.json` — the model cannot output a value
outside the list even if it tries. This is what makes the database
searchable instead of just readable: "find every Independent, Image-first,
Luxury, Founder-led lead" only works if those four fields draw from a fixed
set. `creative_dna` in particular answers "what kind of creative work
excites them," not "what does this studio's website look like" — it can
legitimately include a vertical like Luxury or Automotive when that's a
genuine creative specialty, which is different from restating the client
industry. If you add a value to one of these lists, update it in both the
schema (enforced) and `prompts/system.md` (documented) — they must stay in
sync, same discipline as the archetype rubric in `prompts/scorer.md` and
`src/score.py`.
