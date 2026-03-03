# status_effect.py V3

from typing import Dict, Any, Optional


class StatusEffect:
    """
    Immutable runtime wrapper for a status effect loaded from JSON.
    This class mirrors the canonical status schema and provides
    clean attribute access for the StatusEngine and BattleEntity.
    """

    def __init__(self, data: Dict[str, Any]):
        self._data = data

        self.id: str = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]

        # Mechanical role (buff, debuff, dot, special, etc.)
        self.type: str = data.get("type", data.get("category"))

        # Elemental family (archive, cloud, core, corrupt, etc.)
        self.element: str = data["element"]

        self.duration: int = data["duration"]
        self.stacking: str = data.get("stacking", "none")

        # Effects list or single effect
        self.effects = data.get("effects", [])
        self.effect = data.get("effect")


        # Optional fields
        self.tick_damage: Optional[int] = data.get("tick_damage")
        self.stat_modifiers: Optional[Dict[str, float]] = data.get("stat_modifiers")
        self.shield_value: Optional[int] = data.get("shield_value")
        self.shield_decay: Optional[int] = data.get("shield_decay")
        self.unique: bool = data.get("unique", False)

        # Optional tags for AI or synergy
        self.tags = data.get("tags", [])

    # -------------------------------------------------------------------------
    # Accessors
    # -------------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Returns the raw JSON dictionary."""
        return self._data

    def is_dot(self) -> bool:
        return self.type == "dot"

    def is_buff(self) -> bool:
        return self.type == "buff"

    def is_debuff(self) -> bool:
        return self.type == "debuff"

    def is_shield(self) -> bool:
        return self.type == "shield"

    def is_lock(self) -> bool:
        return self.type == "lock"

    def is_special(self) -> bool:
        return self.type == "special"

    def has_stat_modifiers(self) -> bool:
        return self.stat_modifiers is not None

    def has_tick_damage(self) -> bool:
        return self.tick_damage is not None

    def __repr__(self):
        return f"<StatusEffect {self.id}: {self.name}>"
