#!/usr/bin/env python3
"""Stage 2: deterministic scoring. No LLM call. See prompts/scorer.md for the rubric.

Usage:
    python src/score.py
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Ordered so more-specific keywords (e.g. "dp-led") are checked before
# generic ones — keep this in sync with prompts/scorer.md.
ARCHETYPE_RULES = [
    (("dp-led", "dp led", "cinematographer-led", "director + dp", "director/dp"), "DP-led", 98),
    (("founder-led", "founder led", "boutique"), "founder-led boutique", 95),
    (("agency",), "agency", 82),
    (("huge production", "large production", "production company"), "huge production company", 71),
]
UNKNOWN_SCORE = 30

PRIORITY_THRESHOLDS = [
    (95, "A+"),
    (85, "A"),
    (65, "B"),
    (40, "C"),
]
LOW_CONFIDENCE_THRESHOLD = 40


def base_score(studio_archetype: str) -> int:
    archetype = (studio_archetype or "").lower()
    for keywords, _label, score in ARCHETYPE_RULES:
        if any(kw in archetype for kw in keywords):
            return score
    return UNKNOWN_SCORE


def priority_for(score: int, confidence: int) -> str:
    if confidence < LOW_CONFIDENCE_THRESHOLD:
        # Thin evidence should never produce an "immediate outreach" tier,
        # even if the archetype match happened to land on a high base score.
        return "C" if score >= 60 else "D"
    for threshold, label in PRIORITY_THRESHOLDS:
        if score >= threshold:
            return label
    return "D"


def score_record(record: dict) -> dict:
    scored = dict(record)
    scored["llm_relationship_score"] = record.get("relationship_score")
    scored["llm_priority"] = record.get("priority")
    scored["relationship_score"] = base_score(record.get("studio_archetype", ""))
    scored["priority"] = priority_for(scored["relationship_score"], int(record.get("confidence", 0)))
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
            if scored["priority"] != scored["llm_priority"]:
                disagreements += 1
            out.write(json.dumps(scored) + "\n")

    print(f"Scored {len(records)} leads -> {output_path}")
    print(f"{disagreements} leads where the rubric disagreed with the model's own proposed priority (worth a look during review).")


if __name__ == "__main__":
    main()
