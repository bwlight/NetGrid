import json
import os
from typing import Dict, Any

from src.netgrid.core.systems.battle.status_effect import StatusEffect


class StatusLoader:
    def __init__(self, base_path: str):
        self.base_path = base_path.rstrip("/")

    def load_all(self) -> Dict[str, StatusEffect]:
        index_path = os.path.join(self.base_path, "status_index.json")

        with open(index_path, "r") as f:
            index_data = json.load(f)

        status_effects = {}

        for entry in index_data.get("status_effects", []):
            status_id = entry["id"]
            rel_path = entry["path"]

            print(f"Loading status: {status_id} from {rel_path}")  # <--- ADD THIS

            full_path = os.path.join("data", rel_path)


            full_path = os.path.join("data", rel_path)

            with open(full_path, "r") as f:
                status_json = json.load(f)

            effect = StatusEffect(status_json)
            status_effects[status_id] = effect

        return status_effects
