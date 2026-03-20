#!/usr/bin/env python3
"""
Quest Markdown Fixer

- P-Loose filename prefix detection (uppercase-starting filenames treated as quest-like)
- Quest-header detection gate
- Skip logging with reasons
- End-of-run S3-style summary
- Keeps existing canonicalization / ordering behavior intact (you can drop this in place of the old Fixer)
"""

from __future__ import annotations

import argparse
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
# Filename helpers
# -----------------------------

UPPER_PREFIX_RE = re.compile(r"^[A-Z][A-Z0-9_]*")

def is_quest_like_filename(path: Path) -> bool:
    """
    P-Loose: treat any filename that starts with uppercase letters as quest-like.
    Example: DREAM_intro.md, MAIN.01_start.md, TUTORIAL_start.md
    """
    stem = path.stem
    return bool(UPPER_PREFIX_RE.match(stem))


def infer_quest_code_from_filename(path: Path) -> str:
    """
    Keep existing behavior: quest code is the part before first underscore.
    """
    stem = path.stem
    return stem.split("_", 1)[0]


def infer_quest_type_from_filename(path: Path) -> Optional[str]:
    """
    Map uppercase prefix (before first dot or underscore) to quest type if known.
    """
    stem = path.stem
    prefix = re.split(r"[._]", stem, 1)[0].upper()
    return FILENAME_PREFIX_TO_TYPE.get(prefix)


# -----------------------------
# Header parsing helpers
# -----------------------------

def clean_header_name(raw: str) -> str:
    """
    Normalize markdown header text to a canonical header name.
    Handles things like:
    ## **Objectives**
    ### *Quest Summary*
    """
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
# Quest header detection gate
# -----------------------------

CANONICAL_HEADER_SET = {h.lower() for h in QUEST_HEADERS_ORDER}

def has_any_quest_header(sections: List[Section]) -> bool:
    """
    Returns True if the document contains at least one canonical quest header.
    """
    for sec in sections:
        if sec.header.lower() in CANONICAL_HEADER_SET:
            return True
    return False


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
    """
    Flex-mode resolution:
    - Use filename-inferred type as base (or 'Unknown')
    - If any Quest Type lines exist:
        - If one matches base, use it (no override)
        - Else: keep base, but mark overridden=True and report all_types
    - If none exist: use base, overridden=False
    """
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

def ensure_section(sections: List[Section], header: str) -> None:
    """
    Ensure a section with this header exists; if not, append an empty one.
    """
    if any(s.header.lower() == header.lower() for s in sections):
        return
    sections.append(Section(header=header, lines=[]))


def reorder_sections_canonically(sections: List[Section]) -> List[Section]:
    """
    Reorder sections according to QUEST_HEADERS_ORDER, preserving unknown sections
    at the end in their original relative order.
    """
    by_lower = {s.header.lower(): s for s in sections}
    used = set()
    ordered: List[Section] = []

    # Canonical ones first
    for h in QUEST_HEADERS_ORDER:
        key = h.lower()
        if key in by_lower:
            ordered.append(by_lower[key])
            used.add(key)

    # Then any unknowns in original order
    for s in sections:
        if s.header.lower() not in used:
            ordered.append(s)

    return ordered


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
# Fixer core logic
# -----------------------------

def rebuild_markdown(sections: List[Section]) -> str:
    """
    Rebuild markdown text from canonicalized sections.
    All headers are written as '## {header}'.
    """
    parts: List[str] = []
    for sec in sections:
        parts.append(f"## {sec.header}")
        if sec.lines:
            parts.extend(sec.lines)
        parts.append("")  # blank line after each section
    # Remove trailing blank lines
    while parts and parts[-1] == "":
        parts.pop()
    return "\n".join(parts) + "\n"


def process_file(path: Path) -> Tuple[bool, bool]:
    """
    Process a single quest-like file.
    Returns (changed, considered_quest_like_and_checked).
    """
    original_text = path.read_text(encoding="utf-8")
    lines = original_text.splitlines()
    sections = parse_sections(lines)

    # Gate: must have at least one quest header
    if not has_any_quest_header(sections):
        print(f"[SKIP] {path} — no quest headers detected (no changes made)")
        return False, False  # not counted as "checked quest-like"

    # At this point, we consider it a quest-like file that we checked
    considered_checked = True

    # Ensure all canonical sections exist
    for header in QUEST_HEADERS_ORDER:
        ensure_section(sections, header)

    # Infer quest code and type
    inferred_code = infer_quest_code_from_filename(path)
    inferred_type = infer_quest_type_from_filename(path)
    quest_type, overridden, all_types = resolve_quest_type(sections, inferred_type)

    # Update Quest Code and Quest Type sections
    for sec in sections:
        if sec.header.lower() == "quest code":
            sec.lines = [inferred_code]
        elif sec.header.lower() == "quest type":
            sec.lines = [quest_type]

    # Reorder sections canonically
    sections = reorder_sections_canonically(sections)

    # Rebuild markdown
    new_text = rebuild_markdown(sections)

    if new_text != original_text:
        path.write_text(new_text, encoding="utf-8")
        if overridden:
            print(
                f"[FIX] {path} (Quest Type {all_types} -> '{quest_type}' "
                f"(overridden from filename))"
            )
        else:
            print(f"[FIX] {path}")
        return True, considered_checked

    print(f"[OK]  {path}")
    return False, considered_checked


# -----------------------------
# File discovery
# -----------------------------

def find_markdown_files(root: Path) -> List[Path]:
    return sorted(root.rglob("*.md"))


# -----------------------------
# Main
# -----------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fix quest markdown files in-place."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to scan for .md files (default: current directory)",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    md_files = find_markdown_files(root)
    if not md_files:
        print(f"[INFO] No markdown files found under {root}")
        return

    print(f"[INFO] Scanning {len(md_files)} markdown files under {root}")

    skipped_prefix = 0
    skipped_no_headers = 0
    checked_quest_like = 0
    modified = 0
    unchanged = 0

    for path in md_files:
        # Gate 1: filename prefix (P-Loose)
        if not is_quest_like_filename(path):
            print(f"[SKIP] {path} — filename does not match quest prefix pattern")
            skipped_prefix += 1
            continue

        # At this point, filename is quest-like; process_file will decide if it has headers
        changed, considered_checked = process_file(path)

        if not considered_checked:
            # This means it was skipped due to no quest headers
            skipped_no_headers += 1
            continue

        checked_quest_like += 1
        if changed:
            modified += 1
        else:
            unchanged += 1

    print("=== Summary ===")
    print(f"Checked (quest-like): {checked_quest_like}")
    print(f"Modified: {modified}")
    print(f"Unchanged: {unchanged}")
    print(f"Skipped (prefix): {skipped_prefix}")
    print(f"Skipped (no headers): {skipped_no_headers}")


if __name__ == "__main__":
    main()
