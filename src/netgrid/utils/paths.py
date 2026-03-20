from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"
TOOLS = ROOT / "tools"

def list_json(folder: Path):
    return sorted(folder.glob("*.json"))

def ensure_exists(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    return path
