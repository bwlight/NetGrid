#!/usr/bin/env python3
"""
Quest Generator — Converts canonical markdown quests into structured JSON.

Pipeline:
1. Parse Fixer-formatted markdown
2. Extract canonical sections
3. Convert to structured JSON (Mode C: TO-DO → null/[])
4. Build structured steps (Option C)
5. Tokenize rewards + follow-ups
6. Validate (Mode B: warn but generate)
7. Mirror folder structure into data/quests/
8. Ask once before overwriting existing JSON files
9. Rebuild global + per-folder indexes
10. Write generator log to logs/quest_generator_report.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------
# Canonical configuration
# ---------------------------------------------------------

QUEST_HEADERS_ORDER = [
    "Quest Code",
    "Quest Type",
    "Quest Title",
    "Sector",
    "Quest Summary",
    "Steps",
    "Objectives",
    "Rewards",
    "Notes",
]

LIST_SECTIONS = {"Steps", "Objectives", "Rewards"}

VALID_QUEST_TYPES = {
    "Main Story",
    "Dream Story",
    "Bond Quest",
    "Side Quest",
    "Event Quest",
    "Sector Quest",
    "Stabilization Quest",
}

FILENAME_PREFIX_TO_TYPE = {
    "MAIN": "Main Story",
    "DREAM": "Dream Story",
    "BOND": "Bond Quest",
    "SIDE": "Side Quest",
    "EVENT": "Event Quest",
    "SECTOR": "Sector Quest",
    "STAB": "Stabilization Quest",
    "STABILIZATION": "Stabilization Quest",
}

# ---------------------------------------------------------
# Markdown parsing helpers
# ---------------------------------------------------------

def clean_header_name(raw: str) -> str:
    text = re.sub(r"^#+\s*", "", raw).strip()
    text = re.sub(r"\s+", " ", text)
    for canonical in QUEST_HEADERS_ORDER:
        if text.lower() == canonical.lower():
            return canonical
    return text


def parse_markdown_sections(path: Path):
    """Parse Fixer-formatted markdown into {header: content}."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    sections = {}
    current_header = None
    current_content = None

    for line in lines:
        if line.startswith("## "):
            if current_header is not None:
                sections[current_header] = current_content
            current_header = clean_header_name(line)
            current_content = None
        else:
            if current_header is not None and current_content is None:
                current_content = line.strip()

    if current_header is not None:
        sections[current_header] = current_content

    return sections


# ---------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------

def convert_text_field(value: str):
    """Mode C: TO-DO → null, else string."""
    if value is None or value.strip().upper() == "TO-DO":
        return None
    return value


def convert_list_field(value: str):
    """Mode C: TO-DO → [], else parse bullet list."""
    if value is None or value.strip().upper() == "TO-DO":
        return []
    items = []
    for line in value.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items


def convert_steps(raw_list):
    """Option C: Fully structured steps."""
    steps = []
    for i, text in enumerate(raw_list, start=1):
        steps.append({
            "id": f"step_{i}",
            "text": text,
            "conditions": [],
            "triggers": [],
            "optional": False,
        })
    return steps


def convert_rewards(raw_list):
    """Convert reward names → reward tokens."""
    tokens = []
    for item in raw_list:
        slug = item.lower().replace(" ", "_")
        tokens.append(f"reward:{slug}")
    return tokens


def convert_followups(raw_list):
    """Convert follow-up quest codes → unlock tokens."""
    tokens = []
    for item in raw_list:
        tokens.append(f"unlock:{item}")
    return tokens


# ---------------------------------------------------------
# Quest JSON builder
# ---------------------------------------------------------

def build_quest_json(sections, folder_name, filename, warnings):
    """Convert parsed sections into structured JSON."""
    code = sections.get("Quest Code")
    qtype = sections.get("Quest Type")
    title = sections.get("Quest Title")
    sector = sections.get("Sector")

    summary = convert_text_field(sections.get("Quest Summary"))
    if summary is None:
        warnings.append("Quest Summary is TO-DO")

    # Steps
    raw_steps = convert_list_field(sections.get("Steps"))
    if not raw_steps:
        warnings.append("Steps are TO-DO")
    steps = convert_steps(raw_steps)

    # Objectives
    raw_obj = convert_list_field(sections.get("Objectives"))
    if not raw_obj:
        warnings.append("Objectives are TO-DO")

    # Rewards
    raw_rewards = convert_list_field(sections.get("Rewards"))
    rewards = convert_rewards(raw_rewards)

    # Notes
    notes = convert_text_field(sections.get("Notes"))

    # Build JSON
    quest = {
        "code": code,
        "type": qtype,
        "title": title,
        "sector": sector,
        "summary": summary,
        "steps": steps,
        "objectives": raw_obj,
        "rewards": rewards,
        "notes": notes,
    }

    return quest


# ---------------------------------------------------------
# Index building
# ---------------------------------------------------------

def build_indexes(data_root: Path):
    """Rebuild global + per-folder indexes."""
    all_entries = []

    for folder in sorted(data_root.iterdir()):
        if not folder.is_dir():
            continue

        entries = []
        for json_file in sorted(folder.glob("*.json")):
            data = json.loads(json_file.read_text(encoding="utf-8"))
            entries.append({
                "code": data["code"],
                "type": data["type"],
                "title": data["title"],
                "path": str(json_file),
            })

        # Write per-folder index
        with open(folder / "index.json", "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)

        all_entries.extend(entries)

    # Write global index
    with open(data_root / "index.json", "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2)


# ---------------------------------------------------------
# Main generator
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default="docs/quests")
    args = parser.parse_args()

    docs_root = Path(args.root).resolve()
    data_root = Path("data/quests").resolve()
    logs_root = Path("logs").resolve()

    logs_root.mkdir(exist_ok=True)
    data_root.mkdir(parents=True, exist_ok=True)

    md_files = sorted(docs_root.rglob("*.md"))
    existing_json = list(data_root.rglob("*.json"))

    overwrite = True
    if existing_json:
        ans = input("Overwrite existing quest JSON files? (y/n): ").strip().lower()
        if ans != "y":
            overwrite = False

    report = {
        "timestamp": datetime.now().isoformat(),
        "overwrite": overwrite,
        "files": [],
        "summary": {},
    }

    for md_path in md_files:
        rel_folder = md_path.parent.relative_to(docs_root)
        out_folder = data_root / rel_folder
        out_folder.mkdir(parents=True, exist_ok=True)

        sections = parse_markdown_sections(md_path)
        warnings = []

        # Build JSON
        quest_json = build_quest_json(
            sections,
            rel_folder,
            md_path.name,
            warnings
        )

        out_path = out_folder / f"{quest_json['code']}.json"

        if overwrite:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(quest_json, f, indent=2)

        report["files"].append({
            "file": str(md_path),
            "output": str(out_path),
            "warnings": warnings,
            "status": "warn" if warnings else "ok",
        })

    # Build indexes if overwriting
    if overwrite:
        build_indexes(data_root)

    # Write generator log
    log_path = logs_root / "quest_generator_report.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\nQuest generation complete. Report written to {log_path}")


if __name__ == "__main__":
    main()
