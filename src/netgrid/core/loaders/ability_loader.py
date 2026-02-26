from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any, List

from jsonschema import validate, ValidationError


class Ability:
    """
    Represents a single ability loaded from JSON.
    """

    def __init__(
        self,
        ability_id: str,
        name: str,
        ability_type: str,
        element: str,
        power: float,
        cost: float,
        cooldown: float,
        accuracy: float,
        target: str,
        effects: Dict[str, Any],
        description: str,
    ):
        self.id = ability_id
        self.name = name
        self.type = ability_type
        self.element = element
        self.power = power
        self.cost = cost
        self.cooldown = cooldown
        self.accuracy = accuracy
        self.target = target
        self.effects = effects
        self.description = description

    def __repr__(self) -> str:
        return f"<Ability {self.id}: {self.name}>"


class AbilityLoader:
    """
    Loads and validates all abilities from the abilities data folder.
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.data_dir = base_path / "data" / "abilities"
        self.schema_path = Path("schemas/abilities.schema.json")

        if not self.data_dir.exists():
            raise FileNotFoundError(f"Abilities directory not found: {self.data_dir}")

        if not self.schema_path.exists():
            raise FileNotFoundError(f"Ability schema not found: {self.schema_path}")

        with self.schema_path.open("r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def load_all(self) -> Dict[str, Ability]:
        """
        Loads all ability JSON files and returns a dictionary of Ability objects.
        """
        abilities: Dict[str, Ability] = {}

        for file in self.data_dir.glob("*.json"):
            ability = self._load_single(file)
            abilities[ability.id] = ability

        return abilities

    def _load_single(self, file_path: Path) -> Ability:
        """
        Loads and validates a single ability JSON file.
        """
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Validate JSON against schema
        try:
            validate(instance=data, schema=self.schema)
        except ValidationError as e:
            raise ValueError(
                f"Ability validation failed for {file_path.name}:\n"
                f"  → {e.message}\n"
                f"  → Path: {'/'.join(map(str, e.path))}"
            )

        ability_data = data["ability"]

        return Ability(
            ability_id=ability_data["id"],
            name=ability_data["name"],
            ability_type=ability_data["type"],
            element=ability_data.get("element", "none"),
            power=ability_data.get("power", 0),
            cost=ability_data.get("cost", 0),
            cooldown=ability_data.get("cooldown", 0),
            accuracy=ability_data.get("accuracy", 1.0),
            target=ability_data.get("target", "single"),
            effects=ability_data.get("effects", {}),
            description=ability_data["description"],
        )
