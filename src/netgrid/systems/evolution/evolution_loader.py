import json
import jsonschema
from pathlib import Path
from typing import Dict, Any


class EvolutionLoader:
    """
    Loads and validates all evolution JSON files inside the families/ folder.
    Merges them into a single evolution dictionary.
    """

    def __init__(self, base_folder: str, schema_path: str):
        self.base_folder = Path(base_folder)
        self.families_folder = self.base_folder / "families"
        self.schema_path = Path(schema_path)

    def _load_schema(self) -> Dict[str, Any]:
        with open(self.schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_file(self, file_path: Path, schema: Dict[str, Any]) -> Dict[str, Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        jsonschema.validate(instance=data, schema=schema)
        return data

    def load_all(self) -> Dict[str, Any]:
        """
        Loads all evolution_*.json files inside families/.
        Returns a merged evolution dictionary.
        """
        schema = self._load_schema()
        merged: Dict[str, Any] = {}

        if not self.families_folder.exists():
            raise FileNotFoundError(f"Missing folder: {self.families_folder}")

        for file in sorted(self.families_folder.glob("evolution_*.json")):
            family_data = self._load_file(file, schema)

            for species_id, evo_data in family_data.items():
                if species_id in merged:
                    raise ValueError(f"Duplicate evolution entry detected: {species_id}")
                merged[species_id] = evo_data

        return merged
