#!/usr/bin/env python3
"""Stage 4: join intelligence + emails, drop the debug `reasoning` field, write CSVs.

Usage:
    python src/export.py
"""

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INTELLIGENCE_COLUMNS = [
    "lead_id",
    "company",
    "contact_name",
    "contact_title",
    "email",
    "stage",
    "outreach_priority",
    "confidence",
    "studio_archetype",
    "operating_model",
    "studio_personality",
    "creative_dna",
    "visual_dna",
    "decision_maker",
    "buyer_personality",
    "human_angle",
    "colorkaar_angle",
    "conversation_starter",
    "avoid",
    "why_this_lead",
    "website_url",
]

EMAIL_COLUMNS = [
    "lead_id",
    "company",
    "outreach_priority",
    "subject",
    "first_email_angle",
    "body",
    "human_angle_used",
    "conversation_starter_used",
    "confidence",
]

# llm_outreach_priority is intentionally excluded here (kept in the .jsonl
# for audit, per CLAUDE.md) - the exported CSV has one source of truth.
LIST_FIELDS = {"studio_personality", "creative_dna", "visual_dna", "buyer_personality", "avoid", "why_this_lead"}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_csv(path: Path, columns: list[str], records: list[dict]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            row = dict(record)
            for field in LIST_FIELDS:
                if field in row and isinstance(row[field], list):
                    row[field] = "; ".join(row[field])
            row.pop("reasoning", None)
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intelligence", default=str(ROOT / "output" / "lead_intelligence.scored.jsonl"))
    parser.add_argument("--emails", default=str(ROOT / "output" / "emails.raw.jsonl"))
    parser.add_argument("--intelligence-out", default=str(ROOT / "output" / "lead_intelligence.csv"))
    parser.add_argument("--emails-out", default=str(ROOT / "output" / "emails.csv"))
    args = parser.parse_args()

    intelligence = load_jsonl(Path(args.intelligence))
    write_csv(Path(args.intelligence_out), INTELLIGENCE_COLUMNS, intelligence)
    print(f"{len(intelligence)} rows -> {args.intelligence_out}")

    # Emails are optional and not part of the core pipeline (see CLAUDE.md) -
    # only export them if src/generate_email.py was actually run.
    emails_path = Path(args.emails)
    if emails_path.exists():
        emails = load_jsonl(emails_path)
        write_csv(Path(args.emails_out), EMAIL_COLUMNS, emails)
        print(f"{len(emails)} rows -> {args.emails_out}")


if __name__ == "__main__":
    main()
