from __future__ import annotations

from typing import Optional, Dict, Any
from .battle_entity import BattleEntity


class StatusEffect:
    """
    Represents a single status effect instance on a BattleEntity.
    Supports:
    - DOT / HOT
    - immobilize / stun
    - buffs / debuffs
    - custom metadata
    """

    def __init__(
        self,
        status_id: str,
        duration: int,
        effect_type: str,
        value: float = 0,
        stat_modifiers: Optional[Dict[str, float]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.id = status_id
        self.duration = duration
        self.effect_type = effect_type  # "dot", "hot", "immobilize", "buff", "debuff", etc.
        self.value = value
        self.stat_modifiers = stat_modifiers or {}
        self.metadata = metadata or {}

        # Internal flags
        self.applied_once = False  # for buffs/debuffs

    # ---------------------------------------------------------
    # Per-turn effect logic
    # ---------------------------------------------------------

    def tick(self, entity: BattleEntity) -> Optional[str]:
        """
        Called once per turn by StatusEngine.
        Applies DOT/HOT, immobilize flags, or stat modifiers.
        Returns a log message or None.
        """

        # DOT
        if self.effect_type == "dot":
            entity.apply_damage(self.value)
            return f"{entity.id} took {self.value} DOT damage from {self.id}"

        # HOT
        if self.effect_type == "hot":
            entity.heal(self.value)
            return f"{entity.id} recovered {self.value} HP from {self.id}"

        # Immobilize
        if self.effect_type == "immobilize":
            entity.metadata["immobilized"] = True
            return f"{entity.id} is immobilized by {self.id}"

        # Buff / Debuff (apply once)
        if self.effect_type in ("buff", "debuff"):
            if not self.applied_once:
                for stat, multiplier in self.stat_modifiers.items():
                    entity.apply_stat_modifier(stat, multiplier)
                self.applied_once = True
                return f"{entity.id}'s {self.id} applied"

        return None

    # ---------------------------------------------------------
    # Cleanup logic
    # ---------------------------------------------------------

    def on_expire(self, entity: BattleEntity) -> None:
        """
        Called when the status expires.
        Used to revert buffs/debuffs or cleanup flags.
        """

        # Revert stat modifiers
        if self.effect_type in ("buff", "debuff"):
            for stat, multiplier in self.stat_modifiers.items():
                if stat in entity.stats:
                    entity.stats[stat] /= multiplier

        # Remove immobilize flag
        if self.effect_type == "immobilize":
            if "immobilized" in entity.metadata:
                del entity.metadata["immobilized"]
