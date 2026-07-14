# Colorkaar Lead Intelligence Database

The best lead intelligence engine for a boutique creative studio. Not an
email enrichment tool, and not a prompt — a small pipeline that builds a
database of who your leads actually are: understand the company, score it
deterministically, write one email, export. The database is the asset; the
emails are just the first thing built on top of it.

Read `CLAUDE.md` first — it explains the philosophy and the iteration
discipline this repo is built around. This file is just setup and commands.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Auth — either works:
export ANTHROPIC_API_KEY=sk-ant-...
# or: ant auth login
```

Optional: `export CLAUDE_MODEL=claude-opus-4-8` (this is already the default).

## Input format

`input/enriched_leads.csv` needs these columns (extra columns are ignored,
missing ones are treated as unknown):

| Column | Meaning |
|---|---|
| `lead_id` | Any stable identifier — used to join intelligence to emails later |
| `company` | Company name |
| `description` | Whatever blurb you have on them |
| `website_summary` | A summary of their website / portfolio |
| `contact_name` | The person you'd email |
| `contact_title` | Their title — this is how the model infers who makes creative decisions |
| `visual_style_notes` | Anything about their visual style / look |
| `projects` | Notable project types (not names to drop in the email — context only) |
| `website_url` | For your own reference |

A synthetic (fake) example file is at `examples/sample_leads.csv` — use it to
smoke-test the pipeline before pointing it at real data.

## Run it — on 25 leads first

```bash
python src/analyze.py --input examples/sample_leads.csv --limit 25
python src/score.py
python src/generate_email.py
python src/export.py
```

Then open `output/lead_intelligence.csv` and `output/emails.csv` and read
every row. See `CLAUDE.md` → "The iteration discipline" — this is the step
that actually determines quality. Don't skip it, and don't run the full
1,469-lead list until these 25 feel right.

Once you're happy:

```bash
python src/analyze.py --input input/enriched_leads.csv --limit 1469
python src/score.py
python src/generate_email.py --priority Immediate High Medium
python src/export.py
```

## Stages, individually

- **`src/analyze.py`** — one Claude call per lead, structured JSON output
  matching `schemas/intelligence.schema.json`. Flags: `--input`, `--output`,
  `--limit` (default 25), `--start` (resume partway through a file), `--model`.
- **`src/score.py`** — no LLM call. Applies the deterministic rubric in
  `prompts/scorer.md` to compute `outreach_priority` (Immediate / High /
  Medium / Low — no numeric score) from `studio_archetype` and `confidence`.
  Reads `*.raw.jsonl`, writes `*.scored.jsonl`.
- **`src/generate_email.py`** — one Claude call per lead, only for leads that
  already have intelligence. Flags: `--priority Immediate High` to only
  email your best leads, `--limit`.
- **`src/export.py`** — joins everything, drops the debug `reasoning` field,
  writes the two CSVs BD actually reads.

## Debugging a bad output

Every intermediate `.jsonl` record has a `reasoning` field — a sentence or
two on why the model chose what it chose. It's dropped before the final
CSVs. If a Human Angle or Colorkaar Angle looks wrong, read `reasoning`
first; it usually tells you whether the input data was thin or the prompt
needs adjusting.

## Adding examples

`examples/good/` and `examples/bad/` are fed back into the analyzer prompt as
few-shot examples (see `src/analyze.py::load_few_shot_examples`). When you
find an output that's exactly right, or exactly wrong, add it there — that's
how the engine gets better without hand-editing `prompts/system.md` every
time.
