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

# Ordered so more-specific keywords (e.g. "dp-led") are checked before
# generic ones — keep this in sync with prompts/scorer.md.
ARCHETYPE_KEYWORDS = [
    (("dp-led", "dp led", "cinematographer-led", "director + dp", "director/dp"), "dp_led"),
    (("founder-led", "founder led", "boutique"), "founder_led_boutique"),
    (("agency",), "agency"),
    (("huge production", "large production", "production company"), "huge_production"),
]

# archetype -> {confidence -> outreach_priority}. Mirrors the table in
# prompts/scorer.md exactly; if you change one, change both.
PRIORITY_TABLE = {
    "dp_led": {"High": "Immediate", "Medium": "High", "Low": "Medium"},
    "founder_led_boutique": {"High": "Immediate", "Medium": "High", "Low": "Medium"},
    "agency": {"High": "High", "Medium": "Medium", "Low": "Low"},
    "huge_production": {"High": "Medium", "Medium": "Low", "Low": "Low"},
    "unknown": {"High": "Low", "Medium": "Low", "Low": "Low"},
}


def archetype_bucket(studio_archetype: str) -> str:
    archetype = (studio_archetype or "").lower()
    for keywords, bucket in ARCHETYPE_KEYWORDS:
        if any(kw in archetype for kw in keywords):
            return bucket
    return "unknown"


def priority_for(studio_archetype: str, confidence: str) -> str:
    bucket = archetype_bucket(studio_archetype)
    confidence = confidence if confidence in ("High", "Medium", "Low") else "Low"
    return PRIORITY_TABLE[bucket][confidence]


def score_record(record: dict) -> dict:
    scored = dict(record)
    scored["llm_outreach_priority"] = record.get("outreach_priority")
    scored["outreach_priority"] = priority_for(record.get("studio_archetype", ""), record.get("confidence", "Low"))
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
