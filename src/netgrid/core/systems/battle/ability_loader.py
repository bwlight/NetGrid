# ability_loader.py V4

import json
import os
from typing import List, Dict, Union
from .ability import Ability


class AbilityLoader:
    """
    Loads ability JSON files from disk and converts them into Ability objects.
    Works with AbilityManager to register abilities into the game.
    """

    def __init__(self, base_path: str):
        """
        base_path: directory where ability JSON files are stored.
        Example: "data/abilities/"
        """
        self.base_path = base_path

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def load_all(self) -> List[Ability]:
        """
        Loads all .json files in the base_path directory.
        Returns a list of Ability objects.
        """
        abilities: List[Ability] = []

        for filename in os.listdir(self.base_path):
            if not filename.endswith(".json"):
                continue

            full_path = os.path.join(self.base_path, filename)
            loaded = self._load_file(full_path)

            # Single ability file
            if isinstance(loaded, dict):
                abilities.append(Ability(loaded))

            # Multi-ability file
            elif isinstance(loaded, list):
                for ability_data in loaded:
                    abilities.append(Ability(ability_data))

        return abilities

    def load_file(self, filename: str) -> List[Ability]:
        """
        Loads a single JSON file by name (relative to base_path).
        Returns a list of Ability objects.
        """
        full_path = os.path.join(self.base_path, filename)
        loaded = self._load_file(full_path)

        if isinstance(loaded, dict):
            return [Ability(loaded)]
        return [Ability(a) for a in loaded]

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _load_file(self, path: str) -> Union[dict, List[dict]]:
        """
        Loads a JSON file and returns the parsed data.
        """
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
