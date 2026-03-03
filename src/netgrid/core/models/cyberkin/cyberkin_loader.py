# cyberkin_loader.py V4

import json
import os
from typing import List, Dict, Union

from netgrid.core.systems.battle.ability import Ability


class Cyberkin:
    """
    Immutable data model for a Cyberkin species/form.
    This is NOT the BattleEntity — this is the base data.
    """

    def __init__(self, data: dict, resolved_abilities: List[Ability]):
        self._data = data

        # Core identity
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.family: str = data.get("family")
        self.stage: int = data.get("stage", 1)

        # Stats
        self.stats: Dict[str, Union[int, float]] = data["stats"]

        # Abilities (resolved Ability objects)
        self.abilities: List[Ability] = resolved_abilities

        # AI metadata
        self.ai: Dict[str, Union[str, int]] = data.get("ai", {})

        # Team assignment (A/B/etc.)
        self.team: str = data.get("team", "A")

        # Evolution metadata
        self.evolves_to: Union[str, None] = data.get("evolves_to")
        self.evolution_level: Union[int, None] = data.get("evolution_level")

        # Optional tags for synergy, lore, etc.
        self.tags = data.get("tags", [])

    def to_dict(self):
        return self._data

    def __repr__(self):
        return f"<Cyberkin {self.id}: {self.name}>"


class CyberkinLoader:
    """
    Loads Cyberkin JSON files and resolves their ability IDs into Ability objects.
    """

    def __init__(self, base_path: str, ability_manager):
        """
        base_path: directory containing Cyberkin JSON files.
        ability_manager: used to resolve ability IDs into Ability objects.
        """
        self.base_path = base_path
        self.ability_manager = ability_manager

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def load_all(self) -> Dict[str, Cyberkin]:
        """
        Recursively loads all Cyberkin JSON files in the directory.
        Returns dict: cyberkin_id -> Cyberkin object.
     """
        library: Dict[str, Cyberkin] = {}

        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if not file.endswith(".json"):
                    continue

                full_path = os.path.join(root, file)
                print(f"Loading Cyberkin file: {full_path}")

                loaded = self._load_file(full_path)

                # Single Cyberkin file
                if isinstance(loaded, dict):
                    ck = self._build_cyberkin(loaded)
                    library[ck.id] = ck

                # Multi-Cyberkin file
                elif isinstance(loaded, list):
                    for ck_data in loaded:
                        ck = self._build_cyberkin(ck_data)
                        library[ck.id] = ck

        return library


    def load_file(self, filename: str) -> List[Cyberkin]:
        """
        Loads a single Cyberkin JSON file.
        Returns a list of Cyberkin objects.
        """
        full_path = os.path.join(self.base_path, filename)
        loaded = self._load_file(full_path)

        if isinstance(loaded, dict):
            return [self._build_cyberkin(loaded)]
        return [self._build_cyberkin(c) for c in loaded]

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _load_file(self, path: str) -> Union[dict, List[dict]]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_cyberkin(self, data: dict) -> Cyberkin:
        """
        Converts raw JSON into a Cyberkin object with resolved abilities.
        """
        ability_ids = data.get("abilities", [])
        resolved = []

        for ability_id in ability_ids:
            ability_dict = self.ability_manager.get(ability_id)
            if ability_dict:
                resolved.append(Ability(ability_dict))
            # If missing, silently skip — or log externally

        return Cyberkin(data, resolved)
