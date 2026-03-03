# cyberkin.py V4

from typing import List, Dict, Any, Optional
from netgrid.core.systems.battle.ability import Ability

class Cyberkin:
    """
    Immutable species/form data for a Cyberkin.
    This is NOT the runtime battle entity.
    """

    def __init__(
        self,
        id: str,
        name: str,
        family: str,
        stage: int,
        stats: Dict[str, Any],
        abilities: List[Ability],
        ai: Dict[str, Any],
        team: str = "A",
        evolves_to: Optional[str] = None,
        evolution_level: Optional[int] = None,
        tags: Optional[List[str]] = None,
        raw_data: Optional[Dict[str, Any]] = None,
    ):
        # Identity
        self.id = id
        self.name = name
        self.family = family
        self.stage = stage

        # Stats (immutable base stats)
        self.stats = stats

        # Ability objects (immutable)
        self.abilities = abilities

        # AI metadata
        self.ai = ai or {}

        # Team assignment (A/B/etc.)
        self.team = team

        # Evolution metadata
        self.evolves_to = evolves_to
        self.evolution_level = evolution_level

        # Optional synergy/lore tags
        self.tags = tags or []

        # Raw JSON for debugging or export
        self.raw_data = raw_data or {}

    # -------------------------------------------------------------------------
    # Convenience Accessors
    # -------------------------------------------------------------------------

    def get_stat(self, key: str):
        """Returns a base stat value."""
        return self.stats.get(key)

    def get_ability_ids(self) -> List[str]:
        """Returns the list of ability IDs from the raw JSON."""
        return self.raw_data.get("abilities", [])

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Returns the original JSON data."""
        return self.raw_data

    def __repr__(self):
        return f"<Cyberkin {self.id}: {self.name} (Stage {self.stage})>"
