from __future__ import annotations

from typing import List, Dict, Any
from .battle_entity import BattleEntity
from .status_effect import StatusEffect


class StatusEngine:
    """
    Applies and updates status effects on BattleEntity objects.
    Handles:
    - DOT / HOT
    - immobilize / stun
    - buffs / debuffs
    - duration ticking
    """

    def apply_status(self, entity: BattleEntity, status: StatusEffect) -> None:
        """
        Adds a new status effect instance to the entity.
        """
        entity.status_effects.append(status)

    def remove_status(self, entity: BattleEntity, status_name: str) -> None:
        """
        Removes a status effect by ID/name.
        """
        entity.status_effects = [
            s for s in entity.status_effects if s.id != status_name
        ]

    def update_statuses(self, entity: BattleEntity) -> List[str]:
        """
        Called each turn to:
        - apply DOT/HOT
        - apply immobilize flags
        - decrement durations
        - remove expired statuses

        Returns a list of log messages for the turn.
        """
        logs: List[str] = []
        remaining: List[StatusEffect] = []

        for status in entity.status_effects:
            # Apply per-turn effect (DOT/HOT)
            tick_log = status.tick(entity)
            if tick_log:
                logs.append(tick_log)

            # Decrement duration
            status.duration -= 1

            # Keep if still active
            if status.duration > 0:
                remaining.append(status)
            else:
                logs.append(f"{entity.id}'s {status.id} expired")

        entity.status_effects = remaining
        return logs