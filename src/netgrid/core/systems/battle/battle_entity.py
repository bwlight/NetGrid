from __future__ import annotations

from typing import Dict, List, Any


class BattleEntity:
    """
    Runtime wrapper for a Cyberkin during battle.
    Keeps battle state separate from the core Cyberkin object.
    """

class BattleEntity:
    def __init__(self, cyberkin):
        self.cyberkin = cyberkin
        self.id = cyberkin.id

        # Passthroughs for convenience
        self.name = cyberkin.name
        self.family = cyberkin.family
        self.stage = cyberkin.stage
        self.abilities = cyberkin.abilities

        # Stats copied from Cyberkin
        self.stats = cyberkin.stats.copy()

        # Runtime battle state
        self.current_hp = self.stats.get("hp", 1)
        self.hp = self.current_hp  # alias for test compatibility

        self.energy = 0
        self.status_effects = []
        self.cooldowns = {}

        # AI metadata
        self.role = getattr(cyberkin, "role", "aggressive")
        self.personality = getattr(cyberkin, "personality", "neutral")
        self.threat = {}

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def apply_damage(self, amount: float) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: float) -> None:
        max_hp = self.stats.get("hp", self.current_hp)
        self.current_hp = min(max_hp, self.current_hp + amount)

    def apply_stat_modifier(self, stat: str, multiplier: float) -> None:
        if stat in self.stats:
            self.stats[stat] *= multiplier
    