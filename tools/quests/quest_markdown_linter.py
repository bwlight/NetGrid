#!/usr/bin/env python3
"""
Quest Markdown Linter — Corrected Version
- Accurate spacing detection using real line numbers
- One-line-per-section validation
- TO-DO placeholder enforcement
- Folder-grouped JSON output
- Human-readable console output
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

# -----------------------------
# Canonical configuration
# -----------------------------
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

UPPER_PREFIX_RE = re.compile(r"^[A-Z][A-Z0-9_]*")

@dataclass
class Section:
    header: str
    lines: List[str]
    header_line_index: int


# -----------------------------
# Parsing helpers
# -----------------------------
def clean_header_name(raw: str) -> str:
    text = re.sub(r"^#+\s*", "", raw).strip()
    text = re.sub(r"\s+", " ", text)
    for canonical in QUEST_HEADERS_ORDER:
        if text.lower() == canonical.lower():
            return canonical
    return text


def is_header_line(line: str) -> bool:
    return line.startswith("## ")


def parse_sections(lines: List[str]) -> List[Section]:
    sections = []
    current_header = None
    current_lines = []
    header_line_index = None

    for i, line in enumerate(lines):
        if is_header_line(line):
            if current_header is not None:
                sections.append(Section(current_header, current_lines, header_line_index))
            current_header = clean_header_name(line)
            header_line_index = i
            current_lines = []
        else:
            # Only treat non-header lines as content if they are NOT blank
            if line.strip() != "":
                current_lines.append(line.rstrip("\n"))


    if current_header is not None:
        sections.append(Section(current_header, current_lines, header_line_index))

    return sections


# -----------------------------
# Fixer-style rebuild (for drift detection)
# -----------------------------
def rebuild_markdown(sections):
    parts = []

    for sec in sections:
        parts.append(f"## {sec.header}")

        cleaned = [line.rstrip() for line in sec.lines]

        if not any(line.strip() for line in cleaned):
            parts.append("TO-DO")
        else:
            parts.append(cleaned[0])

        parts.append("")

    while parts and parts[-1] == "":
        parts.pop()

    return "\n".join(parts) + "\n"


# -----------------------------
# Linting logic
# -----------------------------
def lint_file(path: Path):
    errors = []
    warnings = []

    original_text = path.read_text(encoding="utf-8")

    # CRITICAL FIX: preserve blank lines exactly
    lines = original_text.split("\n")

    sections = parse_sections(lines)

    # Validate section presence
    found_headers = [s.header for s in sections]
    for expected in QUEST_HEADERS_ORDER:
        if expected not in found_headers:
            errors.append(f"Missing section: {expected}")

    # Validate each section
    for idx, sec in enumerate(sections):
        cleaned = [line.rstrip() for line in sec.lines]
        nonempty = [line for line in cleaned if line.strip()]

        # Content rules
        if len(nonempty) == 0:
            if cleaned != ["TO-DO"]:
                warnings.append(f"Empty section not using TO-DO: {sec.header}")
        elif len(nonempty) > 1:
            errors.append(f"Section has multiple content lines: {sec.header}")

        # Spacing rules (Option C)
        if idx < len(sections) - 1:
            next_sec = sections[idx + 1]

            current_end = sec.header_line_index + 1 + len(sec.lines)
            next_start = next_sec.header_line_index

            blank_count = sum(1 for j in range(current_end, next_start) if lines[j].strip() == "")

            if blank_count == 0:
                errors.append(f"Missing blank line after section: {sec.header}")
            elif blank_count > 1:
                warnings.append(f"Extra blank lines after section: {sec.header}")

    # Filename validation
    prefix = path.stem.split("_", 1)[0].upper()
    if not UPPER_PREFIX_RE.match(prefix):
        warnings.append("Filename prefix is not uppercase or valid")

    # Drift detection
    rebuilt = rebuild_markdown(sections)
    if rebuilt != original_text:
        warnings.append("Formatting drift detected — run Fixer")

    # Status resolution
    status = "fail" if errors else ("warn" if warnings else "ok")

    return {
        "file": path.name,
        "errors": errors,
        "warnings": warnings,
        "status": status,
    }


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default="docs/quests")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    md_files = sorted(root.rglob("*.md"))

    report = {}

    for path in md_files:
        folder_key = path.parent.name
        file_report = lint_file(path)

        # Console output
        print(f"\n=== {path.name} ===")
        for e in file_report["errors"]:
            print(f"[ERROR] {e}")
        for w in file_report["warnings"]:
            print(f"[WARN]  {w}")
        if file_report["status"] == "ok":
            print("[OK]    File is clean")

        # JSON grouping
        report.setdefault(folder_key, []).append(file_report)

        # Ensure logs folder exists
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        # Write combined JSON to logs folder
        output_path = logs_dir / "lint_report.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\nLinting complete. JSON report written to {output_path}")


if __name__ == "__main__":
    main()
