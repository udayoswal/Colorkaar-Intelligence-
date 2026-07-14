#!/usr/bin/env python3
"""Stage 2: deterministic outreach priority. No LLM call, no numeric score.

See prompts/scorer.md for the rubric this implements.

Usage:
    python src/score.py
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Ordered so more-specific keywords are checked before generic ones - e.g.
# "huge production" must be checked before the generic "production compan"
# pattern, or every huge-production row would match the generic bucket
# first. Keep in sync with prompts/scorer.md.
ARCHETYPE_KEYWORDS = [
    (("dp-led", "dp led", "cinematographer-led", "director + dp", "director/dp"), "dp_led"),
    (("founder-led", "founder led", "boutique"), "founder_led_boutique"),
    (("agency",), "agency"),
    (("huge production", "large production"), "huge_production"),
    (("production compan", "production house", "video production", "content production"), "production_company"),
]

# archetype -> {evidence_strength -> outreach_priority}. Mirrors the table
# in prompts/scorer.md exactly; if you change one, change both.
PRIORITY_TABLE = {
    "dp_led": {"Strong": "Immediate", "Moderate": "High", "Weak": "Medium"},
    "founder_led_boutique": {"Strong": "Immediate", "Moderate": "High", "Weak": "Medium"},
    "agency": {"Strong": "High", "Moderate": "Medium", "Weak": "Low"},
    "production_company": {"Strong": "Medium", "Moderate": "Medium", "Weak": "Low"},
    "huge_production": {"Strong": "Medium", "Moderate": "Low", "Weak": "Low"},
    "unknown": {"Strong": "Low", "Moderate": "Low", "Weak": "Low"},
}

# archetype -> outreach_objective. Purely a function of archetype - no
# evidence_strength dimension, no model proposal/disagreement tracking,
# because the mapping is clean enough that a second opinion adds nothing.
OBJECTIVE_TABLE = {
    "dp_led": "Start a creative conversation",
    "founder_led_boutique": "Build the relationship",
    "agency": "Become a finishing partner",
    "production_company": "Open a vendor conversation",
    "huge_production": "Enter the vendor list",
    "unknown": "Research further before outreach",
}


def archetype_bucket(studio_archetype: str) -> str:
    archetype = (studio_archetype or "").lower()
    for keywords, bucket in ARCHETYPE_KEYWORDS:
        if any(kw in archetype for kw in keywords):
            return bucket
    return "unknown"


def priority_for(studio_archetype: str, evidence_strength: str) -> str:
    bucket = archetype_bucket(studio_archetype)
    evidence_strength = evidence_strength if evidence_strength in ("Strong", "Moderate", "Weak") else "Weak"
    return PRIORITY_TABLE[bucket][evidence_strength]


def objective_for(studio_archetype: str) -> str:
    return OBJECTIVE_TABLE[archetype_bucket(studio_archetype)]


def score_record(record: dict) -> dict:
    scored = dict(record)
    scored["llm_outreach_priority"] = record.get("outreach_priority")
    scored["outreach_priority"] = priority_for(record.get("studio_archetype", ""), record.get("evidence_strength", "Weak"))
    scored["outreach_objective"] = objective_for(record.get("studio_archetype", ""))
    return scored


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(ROOT / "output" / "lead_intelligence.raw.jsonl"))
    parser.add_argument("--output", default=str(ROOT / "output" / "lead_intelligence.scored.jsonl"))
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    records = []
    with input_path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    disagreements = 0
    with output_path.open("w") as out:
        for record in records:
            scored = score_record(record)
            if scored["outreach_priority"] != scored["llm_outreach_priority"]:
                disagreements += 1
            out.write(json.dumps(scored) + "\n")

    print(f"Scored {len(records)} leads -> {output_path}")
    print(f"{disagreements} leads where the rubric disagreed with the model's own proposed priority (worth a look during review).")


if __name__ == "__main__":
    main()
