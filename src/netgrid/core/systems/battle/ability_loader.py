# src/netgrid/core/systems/battle/ability_loader.py

import os
import json
from typing import Dict, Any

from .ability import Ability
from .status_effect import StatusEffect


class AbilityLoader:
    """
    Loads all ability JSON files from data/abilities/, supports schema-wrapped
    JSON ({"ability": {...}}) and flat JSON, validates required fields, and
    constructs Ability objects.
    """

    def __init__(self, base_path: str = "data/abilities"):
        self.base_path = base_path
        self.abilities: Dict[str, Ability] = {}
        self._load_all()

    # ----------------------------------------------------------------------
    # Load all ability files
    # ----------------------------------------------------------------------
    def _load_all(self):
        if not os.path.isdir(self.base_path):
            raise FileNotFoundError(f"Ability directory not found: {self.base_path}")

        for filename in os.listdir(self.base_path):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(self.base_path, filename)

            with open(filepath, "r") as fp:
                raw = json.load(fp)

            # Unwrap schema-wrapped abilities
            data = raw.get("ability", raw)

            ability = self._parse_ability(data)
            self.abilities[ability.id] = ability

    # ----------------------------------------------------------------------
    # Parse a single ability JSON block
    # ----------------------------------------------------------------------
    def _parse_ability(self, data: Dict[str, Any]) -> Ability:
        required = ["id", "name", "type", "target"]

        for field in required:
            if field not in data:
                raise ValueError(f"Ability JSON missing required field: '{field}'")

        # Parse status effects if present
        effects = data.get("effects", {})
        status_effects = []

        if "status" in effects:
            for status_block in effects["status"]:
                status_effects.append(StatusEffect.from_json(status_block))

        # Construct Ability object
        return Ability(
            id=data["id"],
            name=data["name"],
            type=data.get("type", "attack"),
            element=data.get("element"),
            power=data.get("power", 0),
            cost=data.get("cost", 0),
            cooldown=data.get("cooldown", 0),
            accuracy=data.get("accuracy", 1.0),
            target=data["target"],
            effects=effects,
            status_effects=status_effects,
            description=data.get("description", "")
        )

    # ----------------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------------
    def get(self, ability_id: str) -> Ability:
        if ability_id not in self.abilities:
            raise KeyError(f"Ability not found: {ability_id}")
        return self.abilities[ability_id]
