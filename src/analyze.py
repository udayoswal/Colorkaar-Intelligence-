#!/usr/bin/env python3
"""Stage 1: understand each company. One Claude call per lead, structured JSON output.

Usage:
    python src/analyze.py --input examples/sample_leads.csv --limit 25
"""

import argparse
import csv
import json
import sys
from pathlib import Path

from client import get_client, structured_call
from prompts import load_prompt, render_template

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "intelligence.schema.json"
EXAMPLES_GOOD = ROOT / "examples" / "good"
EXAMPLES_BAD = ROOT / "examples" / "bad"

LEAD_FIELDS = [
    "company",
    "description",
    "website_summary",
    "contact_name",
    "contact_title",
    "visual_style_notes",
    "projects",
]


def load_few_shot_examples() -> str:
    """Feeds examples/good and examples/bad back into the system prompt.

    Keeping these as reviewable files (rather than hardcoding them into
    prompts/system.md) is what makes "add an example when you find a bad
    output" a real workflow instead of a suggestion.
    """
    sections = []
    for label, directory in (("Good examples", EXAMPLES_GOOD), ("Bad examples — do not do this", EXAMPLES_BAD)):
        if not directory.exists():
            continue
        files = sorted(directory.glob("*.md"))
        if not files:
            continue
        body = "\n\n".join(f.read_text() for f in files)
        sections.append(f"## {label}\n\n{body}")
    return "\n\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "input" / "enriched_leads.csv"))
    parser.add_argument("--output", default=str(ROOT / "output" / "lead_intelligence.raw.jsonl"))
    parser.add_argument("--limit", type=int, default=25, help="Max leads to process. Default 25 on purpose — see CLAUDE.md.")
    parser.add_argument("--start", type=int, default=0, help="Skip this many rows first (for resuming a batch).")
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text())
    base_system, user_template = load_prompt("system")
    _, analyzer_template = load_prompt("analyzer")
    few_shot = load_few_shot_examples()
    system = base_system if not few_shot else f"{base_system}\n\n{few_shot}"

    input_path = Path(args.input)
    output_path = Path(args.output)
    errors_path = output_path.with_suffix(".errors.jsonl")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    rows = rows[args.start : args.start + args.limit]
    if not rows:
        print(f"No rows to process (start={args.start}, limit={args.limit}, total in file={args.start}).", file=sys.stderr)
        return

    client = get_client()
    processed = 0
    with output_path.open("a") as out, errors_path.open("a") as errs:
        for i, row in enumerate(rows, start=1):
            values = {field: (row.get(field) or "").strip() for field in LEAD_FIELDS}
            user = render_template(analyzer_template, values)

            try:
                result, usage = structured_call(
                    client,
                    system=system,
                    user=user,
                    json_schema=schema,
                    model=args.model,
                    max_tokens=2048,
                )
            except Exception as e:  # noqa: BLE001 - continue the batch on any single-lead failure
                print(f"[{i}/{len(rows)}] {values['company']!r} FAILED: {e}", file=sys.stderr)
                errs.write(json.dumps({"lead_id": row.get("lead_id"), "company": values["company"], "error": str(e)}) + "\n")
                errs.flush()
                continue

            result["lead_id"] = row.get("lead_id")
            for key in ("relationship_score", "confidence"):
                result[key] = max(0, min(100, int(result.get(key, 0))))

            out.write(json.dumps(result) + "\n")
            out.flush()
            processed += 1
            print(
                f"[{i}/{len(rows)}] {result['company']} -> {result['studio_archetype']} "
                f"| llm priority {result['priority']} (confidence {result['confidence']})"
            )

    print(f"\nDone. {processed}/{len(rows)} leads analyzed -> {output_path}")
    if processed < len(rows):
        print(f"{len(rows) - processed} failed -> {errors_path}")


if __name__ == "__main__":
    main()
