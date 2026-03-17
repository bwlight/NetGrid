# tools/reference/reference_folder.py

from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
REF = BASE / "docs" / "reference"


def run():
    """
    Ensures the reference output directory exists.
    This tool has no other responsibilities.
    """
    REF.mkdir(parents=True, exist_ok=True)
