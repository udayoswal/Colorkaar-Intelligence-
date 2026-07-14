#!/usr/bin/env python3
"""Map a raw CRM/ICP-tool export into the schema analyze.py expects.

Written for the columns produced by the prior ICP-screening pass (id,
company, companyDescription, contentTypes, clientIndustries, visualStyle,
namedProjects, companySize, yearsEstablished, location, icpContactName/
icpContactTitle, contactName, email, website, disqualified, stage, ...).

Deliberately does NOT carry forward that tool's own conclusions
(outreachAngle, emailSubjectIdea, icpReason, awards, namedClients) - those
are a different process's judgment, not raw evidence, and letting them leak
into the analyzer's input would contaminate a fresh read. Company size,
years established, and location are kept - they're structural facts, not
opinions.

Usage:
    python src/import_leads.py --input /path/to/raw_export.csv
    (writes to input/enriched_leads.csv by default - gitignored)
"""

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OUTPUT_COLUMNS = [
    "lead_id",
    "company",
    "description",
    "content_types",
    "client_industries",
    "visual_style_notes",
    "projects",
    "company_size",
    "years_established",
    "location",
    "contact_name",
    "contact_title",
    "email",
    "website_url",
    "stage",
]


def map_row(row: dict) -> dict:
    # icpContactName/icpContactTitle are the curated pick when present;
    # contactName is the fallback (raw, uncurated) contact.
    contact_name = (row.get("icpContactName") or row.get("contactName") or "").strip()
    contact_title = (row.get("icpContactTitle") or "").strip()

    return {
        "lead_id": row.get("id", "").strip(),
        "company": row.get("company", "").strip(),
        "description": row.get("companyDescription", "").strip(),
        "content_types": row.get("contentTypes", "").strip(),
        "client_industries": row.get("clientIndustries", "").strip(),
        "visual_style_notes": row.get("visualStyle", "").strip(),
        "projects": row.get("namedProjects", "").strip(),
        "company_size": row.get("companySize", "").strip(),
        "years_established": row.get("yearsEstablished", "").strip(),
        "location": row.get("location", "").strip(),
        "contact_name": contact_name,
        "contact_title": contact_title,
        "email": row.get("email", "").strip(),
        "website_url": row.get("website", "").strip(),
        "stage": row.get("stage", "").strip(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the raw CRM/ICP-tool export CSV")
    parser.add_argument("--output", default=str(ROOT / "input" / "enriched_leads.csv"))
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    kept, skipped_disqualified, skipped_no_company = [], 0, 0
    for row in rows:
        if (row.get("disqualified") or "0").strip() == "1":
            skipped_disqualified += 1
            continue
        if not row.get("company", "").strip():
            skipped_no_company += 1
            continue
        kept.append(map_row(row))

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(kept)

    print(f"{len(rows)} rows read")
    print(f"{skipped_disqualified} skipped (disqualified)")
    print(f"{skipped_no_company} skipped (no company name)")
    print(f"{len(kept)} rows written -> {output_path}")


if __name__ == "__main__":
    main()
