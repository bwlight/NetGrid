# ability.py V4

from typing import Optional, Dict, Any


class Ability:
    """
    Immutable runtime wrapper for an ability loaded from JSON.
    This class provides:
    - clean attribute access
    - schema-aligned fields
    - safe defaults
    - helper methods for engine logic
    """

    def __init__(self, data: Dict[str, Any]):
        # Raw JSON data (kept immutable)
        self._data = data

        # Required fields
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: str = data["type"]              # "attack" or "support"
        self.element: str = data["element"]        # "fire", "pulse", "void", etc.
        self.accuracy: float = data.get("accuracy", 1.0)
        self.cooldown: int = data.get("cooldown", 0)

        # Optional fields
        self.power: Optional[int] = data.get("power")  # None for support abilities
        self.target: str = data.get("target", "enemy") # "enemy", "ally", "self", "area"

        # Multi-hit structure: { "min": int, "max": int }
        self.multi_hit: Optional[Dict[str, int]] = data.get("multi_hit")

        # Stat modifiers: { "atk": +0.2, "def": -0.1, ... }
        self.stat_modifiers: Optional[Dict[str, float]] = data.get("stat_modifiers")

        # Status application
        self.status_inflict: Optional[str] = data.get("status_inflict")
        self.status_chance: Optional[float] = data.get("status_chance")

        # Optional tags for AI or synergy
        self.tags = data.get("tags", [])

    # -------------------------------------------------------------------------
    # Accessors
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Returns the raw JSON dictionary."""
        return self._data

    def is_attack(self) -> bool:
        return self.type == "attack" and self.power is not None

    def is_support(self) -> bool:
        return self.type == "support" or self.power is None

    def has_multi_hit(self) -> bool:
        return self.multi_hit is not None

    def has_status(self) -> bool:
        return self.status_inflict is not None

    def __repr__(self):
        return f"<Ability {self.id}: {self.name}>"
