from __future__ import annotations
from typing import Dict, Any, Optional, List


class EvolutionEngine:
    """
    Handles Cyberkin evolution logic.
    Evolutions can be triggered by:
    - level
    - friendship
    - items
    - story events
    - relationship modifiers
    """

    def __init__(self, evolution_data: Dict[str, Any]):
        self.evolution_data = evolution_data

    def can_evolve(self, cyberkin) -> bool:
        evo = self.evolution_data.get(cyberkin.species_id)
        if not evo:
            return False

        # Level requirement
        if "level" in evo and cyberkin.level < evo["level"]:
            return False

        # Friendship requirement
        if "friendship" in evo and cyberkin.friendship < evo["friendship"]:
            return False

        # Item requirement
        if "item" in evo and evo["item"] not in cyberkin.inventory:
            return False

        return True

    def evolve(self, cyberkin):
        """
        Evolves the Cyberkin if requirements are met.
        Returns evolution result or None.
        """
        if not self.can_evolve(cyberkin):
            return None

        evo = self.evolution_data[cyberkin.species_id]
        new_species = evo["into"]

        cyberkin.species_id = new_species
        cyberkin.level = max(cyberkin.level, evo.get("min_level", cyberkin.level))

        return new_species
