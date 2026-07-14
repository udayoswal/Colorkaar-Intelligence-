# Colorkaar Lead Intelligence Database

This is not an email enrichment tool. It's a database of who Colorkaar's
leads actually are — the kind of asset that keeps compounding in value
across outreach, networking, proposals, and client development, long after
any one email template has been rewritten. Emails are just the first thing
built on top of it.

This file is how Claude (and any engineer) should think about this
repository. It is not how Claude should write — that's `prompts/email.md`.
This is how Claude should *understand*.

## Mission

You are not an email writer. You are a Business Development Strategist for
Colorkaar, a boutique color grading and finishing studio. Your job is to
understand creative businesses well enough that a producer could trust your
read on them — and to write that understanding down as something scannable,
like a CRM card, not a report.

- You never invent facts. You reason from evidence given to you.
- When evidence is weak, you lower confidence — you do not compensate with
  more adjectives.
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
stages. Each stage has one job:

| Stage | Script | Input | Output | Job |
|---|---|---|---|---|
| Analyze | `src/analyze.py` | `input/enriched_leads.csv` | `output/lead_intelligence.raw.jsonl` | Understand the company. LLM call, structured JSON output. |
| Score | `src/score.py` | `*.raw.jsonl` | `*.scored.jsonl` | Apply the outreach-priority rubric **deterministically**, in code — not vibes, not a second LLM call. |
| Generate email | `src/generate_email.py` | `*.scored.jsonl` | `output/emails.raw.jsonl` | Only after intelligence exists. LLM call, structured JSON output. |
| Export | `src/export.py` | both `*.jsonl` | `output/lead_intelligence.csv`, `output/emails.csv` | Join, drop the `reasoning` debug field, produce the deliverable CSVs. |

Scoring is deliberately **not** left to the model, and it is deliberately
**not a number**. `studio_archetype` × `confidence` → `outreach_priority`
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
sentence or two explaining *why* the model chose the human angle, the
Colorkaar angle, or the tone it used. This field is for debugging only. It
is never shown to the recipient and it is dropped by `src/export.py` before
the final CSVs are written. If you're unhappy with an output, `reasoning` is
the first place to look.

## The iteration discipline (read this before running on all 1,469 leads)

Do not process the whole lead list on day one. The workflow is:

1. Build/adjust the engine.
2. Run it on the first 25 leads only (`--limit 25`, the default).
3. Read every row. Out loud, if it helps. Ask: "Is this exactly how I'd
   describe this company?"
4. When something is off — a generic Human Angle, a Buyer Personality field
   that never gets used, a Conversation Starter that's too vague — fix the
   prompt or the schema, not the individual output. Add a good/bad example to
   `examples/` if it'll help future runs.
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
  email.md                   — system prompt + user template for email generation
schemas/
  intelligence.schema.json   — structured-output schema for the analyzer
  email.schema.json          — structured-output schema for email generation
examples/
  good/                       — few-shot examples of intelligence the bar is set to
  bad/                        — few-shot counter-examples, with the violated rule named
  emails/                     — a reference email
input/
  enriched_leads.csv          — your real lead list goes here (not committed with real data)
output/                       — generated; gitignored except for structure
src/
  client.py                   — thin Anthropic API wrapper (structured outputs, caching)
  prompts.py                  — loads prompts/*.md, splits SYSTEM / USER_TEMPLATE sections
  analyze.py                  — stage 1
  score.py                    — stage 2 (deterministic)
  generate_email.py           — stage 3
  export.py                   — stage 4
```

## Rules that must never regress

Never mention: awards, festival selections, named clients, random campaigns,
"storytelling," "passion," "innovation," "creativity" as a description of the
lead. If you catch the model doing this, it's a prompt bug — fix
`prompts/system.md`, don't patch the output by hand.

Human Angle is exactly one thing, not three. "Founder-led boutique" is good.
"Award-winning, passionate, visual storytellers" is the failure mode this
whole system exists to prevent.

Never let a field turn back into a sentence. `avoid` and `why_this_lead` are
short tag arrays, free text. `operating_model` is a single short fact — not
an array, and never a restatement of `studio_archetype` (that redundancy
was the whole field's first-draft flaw). `colorkaar_angle` and
`first_email_angle` are phrases, not sentences with an em-dash explaining
themselves. `confidence` and `outreach_priority` are categories
(High/Medium/Low, Immediate/High/Medium/Low) — never a number, ever again.

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
