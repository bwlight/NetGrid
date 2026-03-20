#!/usr/bin/env python3
"""
Quest Markdown Fixer — Idempotent Version with TO-DO placeholders
and exactly one blank line between sections.

Features:
- Exact-name directory exclusion
- P-Loose uppercase prefix detection
- Quest-header detection
- Empty sections auto-filled with "TO-DO"
- Deterministic formatting (idempotent)
- Exactly one blank line between sections
- Continue-on-skip behavior
- Only logs FIX and OK
- S3 summary
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Optional

# -----------------------------
# Directory Exclusions
# -----------------------------
EXCLUDED_DIRS = {
    ".venv",
    ".pytest_cache",
    ".git",
    "site-packages",
    "__pycache__",
    "dist",
    "build",
    "lore",
    "design",
    "familes",
    "tools",
    "reference",
    "bestiary"
    # Add more here
}

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
# Filename helpers
# -----------------------------
UPPER_PREFIX_RE = re.compile(r"^[A-Z][A-Z0-9_]*")

def is_quest_like_filename(path: Path) -> bool:
    return bool(UPPER_PREFIX_RE.match(path.stem))

def infer_quest_code_from_filename(path: Path) -> str:
    return path.stem.split("_", 1)[0]

def infer_quest_type_from_filename(path: Path) -> Optional[str]:
    prefix = re.split(r"[._]", path.stem, maxsplit=1)[0].upper()
    return FILENAME_PREFIX_TO_TYPE.get(prefix)

# -----------------------------
# Header parsing
# -----------------------------
def clean_header_name(raw: str) -> str:
    text = re.sub(r"^#+\s*", "", raw).strip()
    text = re.sub(r"^\*+|\*+$", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    lower = text.lower()
    for canonical in QUEST_HEADERS_ORDER:
        if lower == canonical.lower():
            return canonical
    return text

def is_header_line(line: str) -> bool:
    return line.lstrip().startswith("#")

def parse_sections(lines: List[str]) -> List[Section]:
    sections = []
    current_header = None
    current_lines = []

    for line in lines:
        if is_header_line(line):
            if current_header is not None:
                sections.append(Section(current_header, current_lines))
            current_header = clean_header_name(line)
            current_lines = []
        else:
            current_lines.append(line.rstrip("\n"))

    if current_header is not None:
        sections.append(Section(current_header, current_lines))

    return sections

# -----------------------------
# Quest header detection
# -----------------------------
CANONICAL_HEADER_SET = {h.lower() for h in QUEST_HEADERS_ORDER}

def has_any_quest_header(sections: List[Section]) -> bool:
    return any(sec.header.lower() in CANONICAL_HEADER_SET for sec in sections)

# -----------------------------
# Quest Type resolution
# -----------------------------
def extract_all_quest_types_from_sections(sections: List[Section]) -> List[str]:
    types = []
    for sec in sections:
        if sec.header.lower() == "quest type":
            for raw in sec.lines:
                stripped = re.sub(r"^\d+\.?\s*|^[-*]\s*", "", raw.strip())
                candidate = stripped.title()
                if candidate in VALID_QUEST_TYPES:
                    types.append(candidate)
    return types

def resolve_quest_type(sections, inferred_type):
    all_types = extract_all_quest_types_from_sections(sections)
    base = inferred_type or "Unknown"

    if not all_types:
        return base, False, all_types

    for t in all_types:
        if t == base:
            return t, False, all_types

    return base, True, all_types

# -----------------------------
# Section helpers
# -----------------------------
def ensure_section(sections, header):
    if not any(s.header.lower() == header.lower() for s in sections):
        sections.append(Section(header, []))

def reorder_sections_canonically(sections):
    by_lower = {s.header.lower(): s for s in sections}
    used = set()
    ordered = []

    for h in QUEST_HEADERS_ORDER:
        key = h.lower()
        if key in by_lower:
            ordered.append(by_lower[key])
            used.add(key)

    for s in sections:
        if s.header.lower() not in used:
            ordered.append(s)

    return ordered

# -----------------------------
# Deterministic Markdown Builder
# -----------------------------
def rebuild_markdown(sections):
    parts = []

    for sec in sections:
        # Header
        parts.append(f"## {sec.header}")

        # Normalize lines
        cleaned = [line.rstrip() for line in sec.lines]

        # If empty → TO-DO
        if not any(line.strip() for line in cleaned):
            parts.append("TO-DO")
        else:
            # Use exactly one line of content
            parts.append(cleaned[0])

        # EXACTLY ONE blank line after each section
        parts.append("")

    # Remove trailing blanks
    while parts and parts[-1] == "":
        parts.pop()

    return "\n".join(parts) + "\n"

# -----------------------------
# Core processing
# -----------------------------
def process_file(path: Path):
    original_text = path.read_text(encoding="utf-8")
    lines = original_text.splitlines()
    sections = parse_sections(lines)

    if not has_any_quest_header(sections):
        return False, False

    considered_checked = True

    for header in QUEST_HEADERS_ORDER:
        ensure_section(sections, header)

    inferred_code = infer_quest_code_from_filename(path)
    inferred_type = infer_quest_type_from_filename(path)
    quest_type, overridden, all_types = resolve_quest_type(sections, inferred_type)

    for sec in sections:
        if sec.header.lower() == "quest code":
            sec.lines = [inferred_code]
        elif sec.header.lower() == "quest type":
            sec.lines = [quest_type]

    sections = reorder_sections_canonically(sections)
    new_text = rebuild_markdown(sections)

    if new_text != original_text:
        path.write_text(new_text, encoding="utf-8")
        print(f"[FIX] {path}")
        return True, considered_checked

    print(f"[OK]  {path}")
    return False, considered_checked

# -----------------------------
# File discovery
# -----------------------------
def is_in_excluded_dir(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)

def find_markdown_files(root: Path):
    return sorted(root.rglob("*.md"))

# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    md_files = find_markdown_files(root)

    print(f"[INFO] Scanning {len(md_files)} markdown files under {root}")

    skipped_prefix = 0
    skipped_no_headers = 0
    skipped_excluded = 0
    checked = 0
    modified = 0
    unchanged = 0

    for path in md_files:
        if is_in_excluded_dir(path):
            skipped_excluded += 1
            continue

        if not is_quest_like_filename(path):
            skipped_prefix += 1
            continue

        changed, considered_checked = process_file(path)

        if not considered_checked:
            skipped_no_headers += 1
            continue

        checked += 1
        if changed:
            modified += 1
        else:
            unchanged += 1

    print("=== Summary ===")
    print(f"Checked (quest-like): {checked}")
    print(f"Modified: {modified}")
    print(f"Unchanged: {unchanged}")
    print(f"Skipped (prefix): {skipped_prefix}")
    print(f"Skipped (no headers): {skipped_no_headers}")
    print(f"Skipped (excluded dirs): {skipped_excluded}")

if __name__ == "__main__":
    main()
