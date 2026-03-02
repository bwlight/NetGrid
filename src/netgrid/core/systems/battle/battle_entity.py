from __future__ import annotations
from typing import Dict, List, Any

class BattleEntity:
    """
    Runtime wrapper for a Cyberkin during battle.
    Keeps battle state separate from the core Cyberkin object.
    """

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
        self.max_hp = self.stats.get("hp", 1)  # REQUIRED for AIController
        self.hp = self.current_hp  # alias for compatibility

        self.energy = 0
        self.status_effects = []

        # Cooldowns must be a manager, not a dict
        # If you already have CooldownManager, use it here:
        # self.cooldowns = CooldownManager()
        self.cooldowns = DummyCooldownManager()  # temporary fallback

        # AI metadata
        self.role = getattr(cyberkin, "role", "aggressive")
        self.personality = getattr(cyberkin, "personality", "neutral")
        self.threat = {}

        # Speed passthrough (needed for control-role targeting)
        self.speed = self.stats.get("speed", 1)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def apply_damage(self, amount: float) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: float) -> None:
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def apply_stat_modifier(self, stat: str, multiplier: float) -> None:
        if stat in self.stats:
            self.stats[stat] *= multiplier


# ---------------------------------------------------------
# TEMPORARY COOLDOWN MANAGER (until your real one is wired in)
# ---------------------------------------------------------

class DummyCooldownManager:
    def __init__(self):
        self.cooldowns = {}

    def is_on_cooldown(self, ability_id: str) -> bool:
        return self.cooldowns.get(ability_id, 0) > 0

    def tick(self):
        for k in list(self.cooldowns.keys()):
            self.cooldowns[k] = max(0, self.cooldowns[k] - 1)

    def set_cooldown(self, ability_id: str, turns: int):
        self.cooldowns[ability_id] = turns
