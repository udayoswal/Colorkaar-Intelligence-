# Colorkaar Lead Intelligence Database

The best lead intelligence engine for a boutique creative studio. Not an
email enrichment tool, and not a prompt — a small pipeline that builds a
database of who your leads actually are: understand the company, score it
deterministically, export. That's the whole core workflow. The database is
the asset; email generation is a separate, optional tool you run by hand
later when you actually need to write to someone (see "Optional" below) —
it is not part of the default run.

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
| `lead_id` | Any stable identifier — used to join related rows later |
| `company` | Company name |
| `description` | Whatever blurb you have on them |
| `content_types` | What kinds of content/video they make |
| `client_industries` | Markets they serve — raw context, not `creative_dna` |
| `visual_style_notes` | Anything about their visual style / look |
| `projects` | Notable project types (context only, not names to drop in an email) |
| `company_size` | e.g. "boutique," headcount, whatever you have |
| `years_established` | Founder-longevity signal |
| `location` | For context |
| `contact_name` | The person you'd email |
| `contact_title` | Their title — this is how the model infers who makes creative decisions |
| `email` | Passed through untouched to the final CSV, never shown to the model |
| `website_url` | For your own reference |

### Importing from another CRM/ICP-screening export

If your source data has a different shape — e.g. a prior enrichment tool's
export with columns like `companyDescription`, `contentTypes`,
`icpContactName` — write a small mapper like `src/import_leads.py`
(already set up for exactly that shape) rather than reshaping 1,469 rows by
hand. It also filters out disqualified leads and intentionally does **not**
carry forward another tool's own conclusions (an `outreachAngle` or
`icpReason` column, say) as if they were evidence — see the file's
docstring for why.

```bash
python src/import_leads.py --input /path/to/raw_export.csv
```

A synthetic (fake) example file is at `examples/sample_leads.csv` — use it to
smoke-test the pipeline before pointing it at real data. `input/enriched_leads.example.csv`
documents the header only. Your real file goes at `input/enriched_leads.csv`
— that exact path is gitignored, so it can never end up in a commit.

## Run it — on 25 leads first

```bash
python src/analyze.py --input examples/sample_leads.csv --limit 25
python src/score.py
python src/export.py
```

Then open `output/lead_intelligence.csv` and read every row. See
`CLAUDE.md` → "The iteration discipline" — this is the step that actually
determines quality. Don't skip it, and don't run the full 1,469-lead list
until these 25 feel right.

Once you're happy:

```bash
python src/analyze.py --input input/enriched_leads.csv --limit 1469
python src/score.py
python src/export.py
```

## Stages, individually

- **`src/analyze.py`** — one Claude call per lead, structured JSON output
  matching `schemas/intelligence.schema.json`. Flags: `--input`, `--output`,
  `--limit` (default 25), `--start` (resume partway through a file), `--model`.
- **`src/score.py`** — no LLM call. Applies the deterministic rubric in
  `prompts/scorer.md` to compute `outreach_priority` (Immediate / High /
  Medium / Low — no numeric score) from `studio_archetype` and `evidence_strength`.
  Reads `*.raw.jsonl`, writes `*.scored.jsonl`.
- **`src/export.py`** — drops the debug `reasoning` field, writes
  `output/lead_intelligence.csv`, the deliverable. The pipeline ends here.

## Optional: generating an email

`src/generate_email.py` still exists and still works, but it's not part of
the core workflow above — the database isn't organized around producing
emails. Run it by hand, per lead or per batch, only when you're actually
about to write to someone:

```bash
python src/generate_email.py --priority Immediate High
python src/export.py   # re-run to also produce output/emails.csv
```

## Debugging a bad output

Every intermediate `.jsonl` record has a `reasoning` field — a sentence or
two on why the model chose what it chose. It's dropped before the final
CSVs. If a Most Distinctive Insight or Colorkaar Angle looks wrong, read `reasoning`
first; it usually tells you whether the input data was thin or the prompt
needs adjusting.

## Adding examples

`examples/good/` and `examples/bad/` are fed back into the analyzer prompt as
few-shot examples (see `src/analyze.py::load_few_shot_examples`). When you
find an output that's exactly right, or exactly wrong, add it there — that's
how the engine gets better without hand-editing `prompts/system.md` every
time.
