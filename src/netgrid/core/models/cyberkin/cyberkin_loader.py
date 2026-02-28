import os
import json
from typing import Dict, Any, List

from .cyberkin import Cyberkin


class CyberkinLoader:
    """
    Loads Cyberkin using the master index file (cyberkin_index.json).
    Ensures ordering, evolution integrity, and clean data loading.
    """

    def __init__(self, ability_loader, index_path="data/cyberkin_index.json"):
        self.ability_loader = ability_loader
        self.index_path = index_path
        self.cyberkin: Dict[str, Cyberkin] = {}

        self.index = self._load_index()
        self._load_all()

    # --------------------------------------------------------------
    # Load the master index
    # --------------------------------------------------------------
    def _load_index(self) -> List[Dict[str, Any]]:
        if not os.path.isfile(self.index_path):
            raise FileNotFoundError(f"Cyberkin index not found: {self.index_path}")

        with open(self.index_path, "r") as fp:
            raw = json.load(fp)

        if "cyberkin_index" not in raw:
            raise ValueError("Invalid index format: missing 'cyberkin_index'")

        return raw["cyberkin_index"]

    # --------------------------------------------------------------
    # Load all Cyberkin listed in the index
    # --------------------------------------------------------------
    def _load_all(self):
        for entry in self.index:
            path = os.path.join("data", entry["path"])

            if not os.path.isfile(path):
                raise FileNotFoundError(f"Cyberkin file missing: {path}")

            with open(path, "r") as fp:
                raw = json.load(fp)

            if "cyberkin" not in raw:
                raise ValueError(f"Invalid Cyberkin file (missing 'cyberkin'): {path}")

            data = raw["cyberkin"]

            ck = self._parse_cyberkin(data)
            self.cyberkin[ck.id] = ck

    # --------------------------------------------------------------
    # Parse a single Cyberkin JSON block
    # --------------------------------------------------------------
    def _parse_cyberkin(self, data: Dict[str, Any]) -> Cyberkin:
        required = ["id", "name", "family", "stage", "stats"]

        for field in required:
            if field not in data:
                raise ValueError(f"Cyberkin JSON missing required field: '{field}'")

        return Cyberkin(
            id=data["id"],
            name=data["name"],
            family=data["family"],
            stage=data["stage"],
            stats=data["stats"],
            abilities=data.get("abilities", []),
            evolution=data.get("evolution", {}),
            personality=data.get("personality", {}),
            role=data.get("role"),
            description=data.get("description", ""),
        )

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------
    def get(self, cyberkin_id: str) -> Cyberkin:
        if cyberkin_id not in self.cyberkin:
            raise KeyError(f"Cyberkin not found: {cyberkin_id}")
        return self.cyberkin[cyberkin_id]

    def all(self) -> List[Cyberkin]:
        return list(self.cyberkin.values())
