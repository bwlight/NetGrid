#!/usr/bin/env python3
"""
Quest Markdown → JSON Generator

Matches the Fixer and Linter exactly:

- Flex-mode Quest Type resolution (filename primary, first matching markdown type wins)
- WARN (not ERROR) when no Quest Type matches filename type
- Canonical header parsing (handles ## **Objectives**, ### *Quest Summary*, etc.)
- Reads canonical quest-system section order
- Preserves unknown sections (ignored for JSON)
- Keeps empty sections
- Produces clean, validated quest JSON files
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# -----------------------------
# Canonical configuration
# -----------------------------

VALID_QUEST_TYPES: set[str] = {
    "Main Story",
    "Dream Story",
    "Bond Quest",
    "Side Quest",
    "Event Quest",
    "Sector Quest",
    "Stabilization Quest",
}

QUEST_HEADERS_ORDER: List[str] = [
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

FILENAME_PREFIX_TO_TYPE: Dict[str, str] = {
    "MAIN": "Main Story",
    "DREAM": "Dream Story",
    "BOND": "Bond Quest",
    "SIDE": "Side Quest",
    "EVENT": "Event Quest",
    "SECTOR": "Sector Quest",
    "STAB": "Stabilization Quest",
    "STABILIZATION": "Stabilization Quest",
}


@dataclass
class Section:
    header: str
    lines: List[str]


# -----------------------------
# Filename inference
# -----------------------------

def infer_quest_code_from_filename(path: Path) -> str:
    stem = path.stem
    return stem.split("_", 1)[0]


def infer_quest_type_from_filename(path: Path) -> Optional[str]:
    stem = path.stem
    prefix = stem.split(".", 1)[0].upper()
    return FILENAME_PREFIX_TO_TYPE.get(prefix)


# -----------------------------
# Header parsing helpers
# -----------------------------

def clean_header_name(raw: str) -> str:
    text = re.sub(r"^#+\s*", "", raw).strip()
    text = re.sub(r"^\*+\s*", "", text)
    text = re.sub(r"\s*\*+$", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    lower = text.lower()
    for canonical in QUEST_HEADERS_ORDER:
        if lower == canonical.lower():
            return canonical

    return text


def is_header_line(line: str) -> bool:
    return line.lstrip().startswith("#")


def parse_sections(lines: List[str]) -> List[Section]:
    sections: List[Section] = []
    current_header: Optional[str] = None
    current_lines: List[str] = []

    for line in lines:
        if is_header_line(line):
            if current_header is not None:
                sections.append(Section(header=current_header, lines=current_lines))
            current_header = clean_header_name(line)
            current_lines = []
        else:
            current_lines.append(line.rstrip("\n"))

    if current_header is not None:
        sections.append(Section(header=current_header, lines=current_lines))

    return sections


# -----------------------------
# Quest Type resolution
# -----------------------------

def extract_all_quest_types_from_sections(sections: List[Section]) -> List[str]:
    types: List[str] = []
    for sec in sections:
        if sec.header.lower() == "quest type":
            for raw in sec.lines:
                stripped = raw.strip()
                if not stripped:
                    continue
                stripped = re.sub(r"^\d+\.\s*", "", stripped)
                stripped = re.sub(r"^[-*]\s*", "", stripped)
                candidate = stripped.title()
                if candidate in VALID_QUEST_TYPES:
                    types.append(candidate)
    return types


def resolve_quest_type(
    sections: List[Section],
    inferred_type: Optional[str],
) -> Tuple[str, bool, List[str]]:
    all_types = extract_all_quest_types_from_sections(sections)
    base = inferred_type or "Unknown"

    if not all_types:
        return base, False, all_types

    for t in all_types:
        if t == base:
            return t, False, all_types

    return base, True, all_types


# -----------------------------
# Section extraction helpers
# -----------------------------

def extract_single_line(sections: List[Section], header: str) -> str:
    sec = next((s for s in sections if s.header.lower() == header.lower()), None)
    if not sec or not sec.lines:
        return ""
    return sec.lines[0].strip()


def extract_multiline_list(sections: List[Section], header: str) -> List[str]:
    sec = next((s for s in sections if s.header.lower() == header.lower()), None)
    if not sec:
        return []

    out: List[str] = []
    for raw in sec.lines:
        stripped = raw.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^\d+\.\s*", "", stripped)
        stripped = re.sub(r"^[-*]\s*", "", stripped)
        stripped = stripped.strip()
        if stripped:
            out.append(stripped)
    return out


# -----------------------------
# JSON builder
# -----------------------------

def build_quest_json(
    path: Path,
    sections: List[Section],
    quest_code: str,
    quest_type: str,
) -> Dict:
    """
    Build the final JSON structure for a quest.
    """
    title = extract_single_line(sections, "Quest Title")
    sector = extract_single_line(sections, "Sector")
    summary = extract_single_line(sections, "Quest Summary")
    steps = extract_multiline_list(sections, "Steps")
    objectives = extract_multiline_list(sections, "Objectives")
    rewards = extract_multiline_list(sections, "Rewards")
    notes = extract_multiline_list(sections, "Notes")

    return {
        "quest_code": quest_code,
        "quest_type": quest_type,
        "title": title,
        "sector": sector,
        "summary": summary,
        "steps": steps,
        "objectives": objectives,
        "rewards": rewards,
        "notes": notes,
        "source_markdown": str(path),
    }


# -----------------------------
# Main generator logic
# -----------------------------

def process_file(path: Path, out_root: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections = parse_sections(lines)

    inferred_code = infer_quest_code_from_filename(path)
    inferred_type = infer_quest_type_from_filename(path)

    quest_type, overridden, all_types = resolve_quest_type(sections, inferred_type)

    if overridden:
        print(
            f"[WARN] {path}: Quest Type {all_types} -> '{quest_type}' "
            f"(overridden from filename)"
        )
    elif not all_types:
        print(
            f"[WARN] {path}: No Quest Type lines found; using '{quest_type}' "
            f"(from filename)"
        )

    quest_json = build_quest_json(
        path=path,
        sections=sections,
        quest_code=inferred_code,
        quest_type=quest_type,
    )

    # Output path
    out_path = out_root / f"{inferred_code}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(quest_json, indent=2), encoding="utf-8")

    print(f"[OK]  {path} -> {out_path}")


def find_markdown_files(root: Path) -> List[Path]:
    return sorted(root.rglob("*.md"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate quest JSON files from markdown."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to scan for .md files (default: current directory)",
    )
    parser.add_argument(
        "--out",
        default="generated_quests",
        help="Output directory for JSON files",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out_root = Path(args.out).resolve()

    md_files = find_markdown_files(root)
    if not md_files:
        print(f"[INFO] No markdown files found under {root}")
        return

    print(f"[INFO] Generating quests from {len(md_files)} markdown files")

    for path in md_files:
        process_file(path, out_root=out_root)

    print("[DONE]")


if __name__ == "__main__":
    main()
