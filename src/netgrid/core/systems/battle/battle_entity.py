# battle_entity.py V4

from typing import Dict, Optional, Iterator, Tuple
import uuid


class BattleEntity:
    """
    Runtime wrapper for a Cyberkin during battle.
    Keeps battle state isolated from the core Cyberkin object.
    """

    def __init__(self, cyberkin):
        # Immutable reference to the base Cyberkin data
        self.cyberkin = cyberkin

        # Unique runtime ID for tie-breaking and logs
        self.entity_id = uuid.uuid4().hex[:8]

        # Core stats (copied from Cyberkin so battle can modify them)
        self.base_stats = {
            "atk": cyberkin.stats.get("atk", 0),
            "def": cyberkin.stats.get("def", 0),
            "spd": cyberkin.stats.get("spd", 0),
            "res": cyberkin.stats.get("res", 0),
            "int": cyberkin.stats.get("int", 0),
            "acc": cyberkin.stats.get("acc", 1.0),
            "eva": cyberkin.stats.get("eva", 0.0),
            "crt": cyberkin.stats.get("crt", 0.0),
        }

        # Current HP
        self.max_hp = cyberkin.stats.get("hp", 1)
        self.current_hp = self.max_hp

        # Cooldowns: ability_id -> turns remaining
        self.cooldowns: Dict[str, int] = {}

        # Active statuses: status_id -> status_instance
        self.statuses: Dict[str, dict] = {}

        # Temporary flags (locks, skip turn, etc.)
        self.skip_turn_flag = False

        # AI metadata
        self.role = cyberkin.ai.get("role")
        self.personality = cyberkin.ai.get("personality")
        self.threat_table: Dict[str, float] = {}

        # For deterministic speed ties
        self.initiative_tiebreaker = cyberkin.ai.get("initiative", 0)

        # Debug name for logs
        self.debug_name = cyberkin.name

    # -------------------------------------------------------------------------
    # Basic state
    # -------------------------------------------------------------------------

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def apply_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int) -> None:
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    # -------------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------------

    def get_effective_stat(self, stat: str) -> float:
        """
        Returns the stat after applying all active status modifiers.
        """
        base = self.base_stats.get(stat, 0)
        total_mod = 0.0

        for status_id, instance in self.statuses.items():
            mods = instance.get("stat_modifiers") or {}
            if stat in mods:
                total_mod += mods[stat]

        return base * (1 + total_mod)

    def modify_stat(self, stat: str, delta: float) -> None:
        """
        Applies an instant stat change (from abilities, not statuses).
        """
        if stat in self.base_stats:
            self.base_stats[stat] *= (1 + delta)

    # -------------------------------------------------------------------------
    # Status management
    # -------------------------------------------------------------------------

    def add_status_instance(self, status_id: str, instance: dict) -> None:
        self.statuses[status_id] = instance

    def has_status(self, status_id: str) -> bool:
        return status_id in self.statuses

    def get_status(self, status_id: str) -> Optional[dict]:
        return self.statuses.get(status_id)

    def remove_status(self, status_id: str) -> None:
        if status_id in self.statuses:
            del self.statuses[status_id]

    def refresh_status_duration(self, status_id: str, duration: int) -> None:
        if status_id in self.statuses:
            self.statuses[status_id]["duration"] = duration

    def iter_statuses(self) -> Iterator[Tuple[str, dict]]:
        for status_id, instance in self.statuses.items():
            yield status_id, instance

    # -------------------------------------------------------------------------
    # Turn flags
    # -------------------------------------------------------------------------

    def set_skip_turn(self, value: bool) -> None:
        self.skip_turn_flag = value

    def should_skip_turn(self) -> bool:
        return self.skip_turn_flag

    def clear_turn_flags(self) -> None:
        self.skip_turn_flag = False

    # -------------------------------------------------------------------------
    # Ability access
    # -------------------------------------------------------------------------

    @property
    def abilities(self):
        return self.cyberkin.abilities

    def is_ability_available(self, ability_id: str) -> bool:
        return ability_id not in self.cooldowns

    # -------------------------------------------------------------------------
    # Threat system
    # -------------------------------------------------------------------------

    def add_threat(self, source_id: str, amount: float) -> None:
        self.threat_table[source_id] = self.threat_table.get(source_id, 0) + amount

    def get_threat(self, source_id: str) -> float:
        return self.threat_table.get(source_id, 0.0)
