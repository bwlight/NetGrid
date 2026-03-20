#!/usr/bin/env python3
"""
Quest Markdown Linter

- Flex-mode Quest Type resolution (filename primary, first matching markdown type wins)
- WARN (not ERROR) when no Quest Type matches filename type
- Canonical header parsing (handles ## **Objectives**, ### *Quest Summary*, etc.)
- Validates canonical quest-system section order
- Validates Quest Code and Quest Type
- Validates required sections exist (but does NOT insert them)
- Supports --diff mode to preview what the Fixer would rewrite
- Color-coded output for readability
"""

from __future__ import annotations

import argparse
import difflib
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

# ANSI colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


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
# Linting logic
# -----------------------------

def lint_file(path: Path, show_diff: bool = False) -> Tuple[int, int]:
    """
    Returns (num_errors, num_warnings)
    """
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections = parse_sections(lines)

    errors = []
    warnings = []

    # Quest Code
    inferred_code = infer_quest_code_from_filename(path)
    code_section = next((s for s in sections if s.header.lower() == "quest code"), None)
    if not code_section:
        errors.append(f"Missing Quest Code section")
    else:
        if not code_section.lines:
            warnings.append("Quest Code section is empty")
        else:
            md_code = code_section.lines[0].strip()
            if md_code != inferred_code:
                warnings.append(
                    f"Quest Code '{md_code}' does not match filename '{inferred_code}'"
                )

    # Quest Type
    inferred_type = infer_quest_type_from_filename(path)
    quest_type, overridden, all_types = resolve_quest_type(sections, inferred_type)

    if not all_types:
        warnings.append("Missing Quest Type lines")
    else:
        if inferred_type and inferred_type not in all_types:
            warnings.append(
                f"Quest Type(s) {all_types} do not include filename type '{inferred_type}'"
            )

    # Required sections
    present_headers = {s.header for s in sections}
    for header in QUEST_HEADERS_ORDER:
        if header not in present_headers:
            warnings.append(f"Missing section: {header}")

    # Diff mode (show what Fixer would rewrite)
    if show_diff:
        from tempfile import TemporaryDirectory
        from quest_markdown_fixer import process_file as fixer_process  # type: ignore

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp) / path.name
            tmp_path.write_text(text, encoding="utf-8")
            fixer_process(tmp_path, dry_run=False)
            fixed_text = tmp_path.read_text(encoding="utf-8")

        diff = difflib.unified_diff(
            text.splitlines(),
            fixed_text.splitlines(),
            fromfile=str(path),
            tofile=str(path) + " (fixed)",
            lineterm="",
        )
        for line in diff:
            print(line)

    # Print results
    if errors:
        print(f"{RED}[ERROR]{RESET} {path}")
        for e in errors:
            print(f"  {RED}- {e}{RESET}")
    if warnings:
        print(f"{YELLOW}[WARN]{RESET}  {path}")
        for w in warnings:
            print(f"  {YELLOW}- {w}{RESET}")
    if not errors and not warnings:
        print(f"{GREEN}[OK]{RESET}    {path}")

    return len(errors), len(warnings)


# -----------------------------
# Main
# -----------------------------

def find_markdown_files(root: Path) -> List[Path]:
    return sorted(root.rglob("*.md"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint quest markdown files.")
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Show diff of what the Fixer would change",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    md_files = find_markdown_files(root)

    total_errors = 0
    total_warnings = 0

    for path in md_files:
        e, w = lint_file(path, show_diff=args.diff)
        total_errors += e
        total_warnings += w

    print()
    print("=== Lint Summary ===")
    print(f"Errors:   {total_errors}")
    print(f"Warnings: {total_warnings}")


if __name__ == "__main__":
    main()
