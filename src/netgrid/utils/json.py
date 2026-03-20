import json
from .errors import DataLoadError

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise DataLoadError(f"Failed to load {path}: {e}")

def write_json(path, data, indent=4):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    except Exception as e:
        raise DataLoadError(f"Failed to write {path}: {e}")
