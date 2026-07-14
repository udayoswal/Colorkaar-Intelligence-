#!/usr/bin/env python3
"""Stage 3: write one email per lead, only after intelligence exists.

Usage:
    python src/generate_email.py --priority A+ A
"""

import argparse
import csv
import json
from pathlib import Path

from client import get_client, structured_call
from prompts import load_prompt, render_template

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schemas" / "email.schema.json"

TEMPLATE_FIELDS = [
    "company",
    "studio_archetype",
    "operating_model",
    "decision_maker",
    "buyer_personality",
    "human_angle",
    "colorkaar_angle",
    "conversation_starter",
    "priority",
    "contact_name",
    "contact_title",
]
LIST_FIELDS = ["creative_dna", "visual_dna", "avoid"]


def load_contacts(leads_csv: Path) -> dict[str, dict]:
    if not leads_csv.exists():
        return {}
    with leads_csv.open(newline="") as f:
        return {row["lead_id"]: row for row in csv.DictReader(f)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "output" / "lead_intelligence.scored.jsonl"))
    parser.add_argument("--output", default=str(ROOT / "output" / "emails.raw.jsonl"))
    parser.add_argument("--leads-csv", default=str(ROOT / "input" / "enriched_leads.csv"), help="Used to fill in contact_name/contact_title if not carried on the intelligence record.")
    parser.add_argument("--priority", nargs="*", default=None, help="Only email leads with these priorities, e.g. --priority A+ A")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text())
    system, user_template = load_prompt("email")
    contacts = load_contacts(Path(args.leads_csv))

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    with input_path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if args.priority:
        records = [r for r in records if r.get("priority") in args.priority]
    if args.limit:
        records = records[: args.limit]

    if not records:
        print("No leads match the given filters.")
        return

    client = get_client()
    with output_path.open("a") as out:
        for i, record in enumerate(records, start=1):
            values = {}
            for field in TEMPLATE_FIELDS:
                values[field] = str(record.get(field, "UNKNOWN"))
            for field in LIST_FIELDS:
                values[field] = ", ".join(record.get(field) or []) or "none"
            values["relationship_score"] = str(record.get("relationship_score", ""))
            values["confidence"] = str(record.get("confidence", ""))

            contact = contacts.get(str(record.get("lead_id")), {})
            values["contact_name"] = contact.get("contact_name") or values.get("contact_name", "UNKNOWN")
            values["contact_title"] = contact.get("contact_title") or values.get("contact_title", "UNKNOWN")

            user = render_template(user_template, values)

            try:
                result, usage = structured_call(
                    client,
                    system=system,
                    user=user,
                    json_schema=schema,
                    model=args.model,
                    max_tokens=1024,
                )
            except Exception as e:  # noqa: BLE001 - continue the batch on any single-lead failure
                print(f"[{i}/{len(records)}] {record.get('company')!r} FAILED: {e}")
                continue

            result["lead_id"] = record.get("lead_id")
            result["priority"] = record.get("priority")
            out.write(json.dumps(result) + "\n")
            out.flush()
            print(f"[{i}/{len(records)}] {result['company']} -> \"{result['subject']}\"")

    print(f"\nDone -> {output_path}")


if __name__ == "__main__":
    main()
